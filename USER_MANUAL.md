# CareerPilot — User Manual

A job-application assistant for students. Upload your resume once, browse matched
jobs, let the AI agent draft a tailored resume + cover note for each job, approve
before anything is sent, track applications, and practice interviews that remember
your weak areas.

---

## 1. Starting the app (one-time setup)

1. Open two terminals in the project folder.

2. **Terminal 1 — backend:**
   ```
   cd backend
   ..\.venv\Scripts\python -m uvicorn backend.main:app --reload --port 8000
   ```

3. **Terminal 2 — frontend:**
   ```
   cd frontend
   npm run dev
   ```

4. Open **http://localhost:5173** in your browser.

> If you see a yellow "database" banner at the top, the backend is not running —
> check Terminal 1 for errors.

The app comes pre-loaded with **500 mock job listings** and a **demo profile**
("Ananya Sharma", labelled *Sample data*) so you can explore everything before
uploading your own resume.

---

## 2. Profile — "who am I?"

**Sidebar → Profile**

1. Click **Upload Resume** and select a PDF resume.
   - The AI reads it and fills in: name, email, education, skills, projects,
     experience, and preferred roles/locations.
   - No PDF handy? Use the **sample resume** link to test the flow first.
2. Review the extracted fields and **edit anything that looks wrong** —
   the agent is only allowed to use skills, projects and employers that exist
   in your profile, so this data drives everything else.
3. Click **Save**.

You can re-upload a new resume at any time; the profile is re-parsed.

---

## 3. Jobs — finding openings

**Sidebar → Jobs**

- Use the search box and filters (role keyword, location, job type,
  closing soon) to narrow the 500 listings. Results are paginated, 25 per page.
- Click a job to open its detail card, which shows:
  - **Fit rating** (Strong / Good / Weak) and a match ratio vs. required skills
  - **"Why it fits" bullets** — 3 AI-generated reasons tied to *your* profile
  - **Missing skills** — what you'd need to strengthen
- Click **Save** on a job to bookmark it without generating anything yet.

---

## 4. Prepare — the agent drafts your application

**Sidebar → Prepare** (or click "Prepare application" on any job)

1. Pick the job you want (or paste a job ID).
2. Click **Run agent**. In a few seconds it:
   - Recalls your interview weak areas (so bullets can address them)
   - Rewrites/tailors your resume for this job → **PDF**
   - Drafts a **cover note**
   - Creates the application in **awaiting approval** status
   - Generates a **calendar reminder (.ics)** for the deadline
   - Logs every step to the action log
3. Review the tailored PDF (click to open it) and the cover note.
4. Choose one:
   - **Approve & mark applied** — the *only* way an application becomes "applied".
     Nothing is ever auto-sent; you always press this button.
   - **Edit cover note** — tweak the text, save.
   - **Discard** — delete the draft.

The agent cannot invent skills, projects or employers — anything not in your
profile is automatically dropped and logged.

---

## 5. Applications — tracking your pipeline

**Sidebar → Applications**

- View every application grouped by status:
  `saved → awaiting_approval → applied → interview → offer`.
- From each card you can:
  - **Update status** as you progress (got an interview? set it).
  - **Re-generate the reminder** (.ics downloads — import it into Google
    Calendar/Outlook; no Google login needed).
  - Open the **tailored resume PDF** for that application.
- Below the list, the **Action Log** shows everything the agent did, step by
  step (also exportable as a file from the top bar).

---

## 6. Practice — mock interviews with memory

**Sidebar → Practice**

1. Enter a role (e.g. "Python Backend Developer") and click **Start interview**.
   The AI asks a realistic question for that role.
2. Type your answer and submit. You get:
   - A **score (1–5)** with feedback on what to improve
   - A **follow-up question** targeting the same skill
3. Over multiple sessions the app builds a **Weak Areas** list (e.g.
   "Database Indexing — last score 1") so both you and the agent know what to
   drill next. Prepare also uses this memory.

---

## 7. Today — your daily dashboard

**Sidebar → Today**

A one-glance summary: items needing attention, upcoming deadlines,
what you applied to this week, and weak areas worth practicing. Start here
each day.

---

## How reliable is the AI part?

The app talks to AI providers with an automatic fallback chain (Groq models →
OpenRouter → deterministic logic). If a provider is rate-limited or down, the
app keeps working — resume parsing, fit bullets and interviews switch to
rule-based versions and are still useful. No key or outage ever blocks the core
tracking features.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Yellow database banner | Backend not running — restart Terminal 1 |
| "Agent tailoring failed" | Click again; if it persists, check the backend terminal output |
| Slow first answer | First AI call can take a few seconds; retries happen automatically |
| Wrong resume details | Edit them on the Profile page — the agent only trusts profile data |
| Want a clean slate | `python -m backend.data.reset` (drops all data, reseeds demo content) |

> **Note:** All jobs and companies in the app are fictional mock data.
> Never commit your `.env` file or share your API keys.
