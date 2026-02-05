import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { RecruiterAuthProvider, useRecruiterAuth } from './contexts/RecruiterAuthContext'
import Header from './components/Header'
import CompanyList from './pages/CompanyList'
import CompanyBrowse from './pages/CompanyBrowse'
import Register from './components/Register'
import Login from './components/Login'
import DashboardNew from './pages/DashboardNew'
import JobPreferences from './pages/JobPreferences'
import ProfileEdit from './pages/ProfileEdit'
import ResumeUpload from './pages/ResumeUpload'
import RecruiterRegister from './pages/RecruiterRegister'
import RecruiterLogin from './pages/RecruiterLogin'
import RecruiterDashboard from './pages/RecruiterDashboard'
import DashboardOverview from './pages/DashboardOverview'
import RecruiterProfile from './pages/RecruiterProfile'
import JobOpenings from './pages/JobOpenings'
import JobOpeningForm from './pages/JobOpeningForm'
import RecruiterAnalytics from './pages/RecruiterAnalytics'
import CandidateSearch from './pages/CandidateSearch'
import JobApplications from './pages/JobApplications'
import './App.css'

// Protected Route Component for Users
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  return isAuthenticated ? children : <Navigate to="/login" />;
};

// Protected Route Component for Recruiters
const RecruiterProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useRecruiterAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  return isAuthenticated ? children : <Navigate to="/recruiter/login" />;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <RecruiterAuthProvider>
          <div className="app">
            <Header />
            <Routes>
            {/* Auth routes without main-content wrapper */}
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            
            {/* Regular routes with main-content wrapper */}
            <Route path="/" element={
              <main className="main-content">
                <CompanyList />
              </main>
            } />
            <Route path="/companies" element={
              <main className="main-content">
                <CompanyBrowse />
              </main>
            } />
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <DashboardNew />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/dashboard/profile" 
                element={
                  <ProtectedRoute>
                    <ProfileEdit />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/dashboard/preferences" 
                element={
                  <ProtectedRoute>
                    <JobPreferences />
                  </ProtectedRoute>
                } 
              />
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <main className="main-content">
                    <DashboardNew />
                  </main>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/dashboard/profile" 
              element={
                <ProtectedRoute>
                  <main className="main-content">
                    <ProfileEdit />
                  </main>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/dashboard/preferences" 
              element={
                <ProtectedRoute>
                  <main className="main-content">
                    <JobPreferences />
                  </main>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/dashboard/resume" 
              element={
                <ProtectedRoute>
                  <main className="main-content">
                    <ResumeUpload />
                  </main>
                </ProtectedRoute>
              } 
            />

            {/* Recruiter Routes */}
            <Route path="/recruiter/register" element={<RecruiterRegister />} />
            <Route path="/recruiter/login" element={<RecruiterLogin />} />
            <Route 
              path="/recruiter/dashboard" 
              element={
                <RecruiterProtectedRoute>
                  <RecruiterDashboard />
                </RecruiterProtectedRoute>
              }
            >
              {/* Nested routes for recruiter dashboard */}
              <Route index element={<DashboardOverview />} />
              <Route path="profile" element={<RecruiterProfile />} />
              <Route path="jobs" element={<JobOpenings />} />
              <Route path="jobs/new" element={<JobOpeningForm />} />
              <Route path="jobs/:id/edit" element={<JobOpeningForm />} />
              <Route path="analytics" element={<RecruiterAnalytics />} />
              <Route path="candidates" element={<CandidateSearch />} />
              <Route path="applications" element={<JobApplications />} />
              <Route path="messages" element={<div>Messages Component Coming Soon</div>} />
            </Route>
          </Routes>
          </div>
        </RecruiterAuthProvider>
      </AuthProvider>
    </Router>
  )
}

export default App
