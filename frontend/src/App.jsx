import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import AuthCallback from './pages/AuthCallback';
import ModeSelection from './pages/ModeSelection';
import QuestionPage from './pages/QuestionPage';
import ResultsPage from './pages/ResultsPage';
import StudentDashboard from './pages/StudentDashboard'; // ← ADD THIS
import Navbar from './components/Navbar';
import './App.css';

function AppContent() {
  const isLoggedIn = localStorage.getItem('userId');
  const location = useLocation();
  
  const showNavbar = isLoggedIn && [
    '/dashboard',        // ← ADD THIS
    '/mode-selection', 
    '/questions', 
    '/results'
  ].includes(location.pathname);

  return (
    <>
      {showNavbar && <Navbar />}
      <Routes>
        {/* Home route - redirect to dashboard if logged in */}
        <Route 
          path="/" 
          element={isLoggedIn ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} 
        />
        
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        
        {/* Protected routes */}
        <Route 
          path="/dashboard" 
          element={isLoggedIn ? <StudentDashboard /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/mode-selection" 
          element={isLoggedIn ? <ModeSelection /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/questions" 
          element={isLoggedIn ? <QuestionPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/results" 
          element={isLoggedIn ? <ResultsPage /> : <Navigate to="/login" />} 
        />
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
