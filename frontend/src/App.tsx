import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import MainLayout from './layouts/MainLayout'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import Onboarding from './pages/Onboarding'
import Jobs from './pages/Jobs'
import JobDetail from './pages/JobDetail'
import Editor from './pages/Editor'
import Submissions from './pages/Submissions'

function App() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/" element={<Login />} />

        {/* Protected routes with sidebar */}
        <Route element={<MainLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/jobs/:id" element={<JobDetail />} />
          <Route path="/editor/:id" element={<Editor />} />
          <Route path="/submissions" element={<Submissions />} />
        </Route>
      </Routes>
      <Toaster />
    </Router>
  )
}

export default App
