import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import AuthCallback from './pages/AuthCallback';
import ModeSelection from './pages/ModeSelection';
import QuestionPage from './pages/QuestionPage';
import ResultsPage from './pages/ResultsPage';
import Navbar from './components/Navbar';
import './App.css';

function AppContent() {
  const isLoggedIn = localStorage.getItem('userId');
  const location = useLocation();

  const showNavbar = isLoggedIn && ['/mode-selection', '/questions', '/results'].includes(location.pathname);

  return (
    <>
      {showNavbar && <Navbar />}
      
      <Routes>
        <Route 
          path="/" 
          element={isLoggedIn ? <Navigate to="/mode-selection" replace /> : <Navigate to="/login" replace />} 
        />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route 
          path="/mode-selection" 
          element={isLoggedIn ? <ModeSelection /> : <Navigate to="/login" replace />} 
        />
        <Route 
          path="/questions" 
          element={isLoggedIn ? <QuestionPage /> : <Navigate to="/login" replace />} 
        />
        <Route 
          path="/results" 
          element={isLoggedIn ? <ResultsPage /> : <Navigate to="/login" replace />} 
        />
        <Route path="*" element={<Navigate to="/" replace />} />
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
