"""Creates a keep-alive monitor for the Render deployment on UptimeRobot or
cron-job.org, so the free-tier service never sleeps for 15+ minutes.

Usage (run from the repo root, with the venv python):
    ..\\.venv\\Scripts\\python scripts\\keep_alive_setup.py uptimerobot <api_key> <render_url>
    ..\\.venv\\Scripts\\python scripts\\keep_alive_setup.py cronjob <api_key> <render_url>

- UptimeRobot key: https://uptimerobot.com -> Settings -> API -> Main API key
- cron-job.org key: https://cron-job.org -> Settings -> REST API key

Both are free accounts. The script is idempotent: UptimeRobot monitors are
matched by name, cron-job.org jobs by title, so re-running won't duplicate.
"""

import json
import sys
import urllib.request

MONITOR_NAME = "CareerPilot keep-alive"


def _post(url: str, payload: dict, headers: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def _get(url: str, headers: dict) -> dict:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def setup_uptimerobot(api_key: str, render_url: str) -> None:
    base = "https://api.uptimerobot.com/v2"
    headers = {"Cache-Control": "no-cache"}  # auth goes in the payload

    # List existing monitors to stay idempotent
    existing = _post(f"{base}/getMonitors", {"api_key": api_key, "format": "json", "limit": 50}, headers)
    for m in existing.get("monitors", []):
        if m.get("friendly_name") == MONITOR_NAME:
            print(f"Monitor '{MONITOR_NAME}' already exists (id={m['id']}) — nothing to do.")
            return

    result = _post(
        f"{base}/newMonitor",
        {
            "api_key": api_key,
            "format": "json",
            "type": 1,  # HTTP(s)
            "url": f"{render_url}/api/health",
            "friendly_name": MONITOR_NAME,
            "interval": 300,  # every 5 min (free-tier minimum)
        },
        headers,
    )
    if result.get("stat") == "ok":
        print(f"UptimeRobot monitor created (id={result['monitor']['id']}) — pings every 5 min.")
    else:
        raise SystemExit(f"UptimeRobot error: {result}")


def setup_cronjob(api_key: str, render_url: str) -> None:
    base = "https://api.cron-job.org"
    headers = {"Authorization": f"Bearer {api_key}"}

    existing = _get(f"{base}/jobs", headers)
    for j in existing.get("jobs", []):
        if j.get("title") == MONITOR_NAME:
            print(f"Job '{MONITOR_NAME}' already exists (id={j['jobId']}) — nothing to do.")
            return

    result = _post(
        f"{base}/jobs",
        {
            "job": {
                "title": MONITOR_NAME,
                "url": f"{render_url}/api/health",
                "enabled": True,
                "saveResponses": False,
                "requestMethod": 0,  # GET
                "schedule": {
                    "timezone": "UTC",
                    "days": list(range(31)),   # every day
                    "hours": list(range(24)),  # every hour
                    "minutes": [0, 10, 20, 30, 40, 50],  # every 10 min
                },
                "notification": {"onFailure": True, "onSuccess": False},
            }
        },
        headers,
    )
    if result.get("jobId"):
        print(f"cron-job.org job created (id={result['jobId']}) — pings every 10 min.")
    else:
        raise SystemExit(f"cron-job.org error: {result}")


def main() -> None:
    if len(sys.argv) != 4:
        print(__doc__)
        raise SystemExit(1)
    provider, api_key, render_url = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("/")
    if provider == "uptimerobot":
        setup_uptimerobot(api_key, render_url)
    elif provider == "cronjob":
        setup_cronjob(api_key, render_url)
    else:
        print(__doc__)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
