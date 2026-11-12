import React, { useCallback, useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { Sidebar } from './components/Sidebar'
import { DbStatusBanner } from './components/DbStatusBanner'
import { TodayPage } from './pages/Today'
import { JobsPage } from './pages/Jobs'
import { PreparePage } from './pages/Prepare'
import { ApplicationsPage } from './pages/Applications'
import { PracticePage } from './pages/Practice'
import { ProfilePage } from './pages/Profile'

const Shell: React.FC = () => {
  const location = useLocation()
  const [studentName, setStudentName] = useState('Ananya Sharma')
  const [studentCollege, setStudentCollege] = useState("B.Tech CSE '26")

  const loadProfile = useCallback(() => {
    fetch('/api/profile')
      .then((res) => (res.ok ? res.json() : null))
      .then((p) => {
        if (p && p.name) {
          setStudentName(p.name)
          setStudentCollege(p.education || "B.Tech CSE '26")
        }
      })
      .catch(() => {})
  }, [])

  useEffect(() => {
    loadProfile()
  }, [loadProfile, location.pathname])

  useEffect(() => {
    window.addEventListener('profile:updated', loadProfile)
    return () => window.removeEventListener('profile:updated', loadProfile)
  }, [loadProfile])

  return (
    <div className="min-h-screen bg-canvas text-ink flex">
      {/* Left Sidebar */}
      <Sidebar studentName={studentName} studentCollege={studentCollege} />

      {/* Main Content Area */}
      <main className="ml-52 flex-1 min-h-screen flex flex-col">
        <div className="max-w-[1120px] w-full mx-auto p-8">
          <DbStatusBanner />
          <Routes>
            <Route path="/" element={<TodayPage />} />
            <Route path="/jobs" element={<JobsPage />} />
            <Route path="/prepare" element={<PreparePage />} />
            <Route path="/prepare/:jobId" element={<PreparePage />} />
            <Route path="/applications" element={<ApplicationsPage />} />
            <Route path="/practice" element={<PracticePage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  )
}

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Shell />
    </BrowserRouter>
  )
}

export default App
