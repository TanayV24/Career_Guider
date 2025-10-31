import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SplashScreen from './pages/SplashScreen';
import ModeSelection from './pages/ModeSelection';
import MotivationalQuote from './pages/MotivationalQuote';
import QuestionPage from './pages/QuestionPage';
import ResultsPage from './pages/ResultsPage';
import './App.css';

function App() {
  // Check if user is logged in
  const isLoggedIn = localStorage.getItem('userId');

  return (
    <BrowserRouter>
      <Routes>
        {/* Root route - shows login or redirects based on login status */}
        <Route 
          path="/" 
          element={isLoggedIn ? <Navigate to="/mode-selection" replace /> : <LoginPage />} 
        />
        
        {/* Protected routes - only accessible after login */}
        <Route 
          path="/splash" 
          element={isLoggedIn ? <SplashScreen /> : <Navigate to="/" replace />} 
        />

        {/* Protected routes - only accessible after login */}
        <Route 
          path="/mode-selection" 
          element={isLoggedIn ? <ModeSelection /> : <Navigate to="/" replace />} 
        />
        <Route 
          path="/motivational-quote" 
          element={isLoggedIn ? <MotivationalQuote /> : <Navigate to="/" replace />} 
        />
        <Route 
          path="/questions" 
          element={isLoggedIn ? <QuestionPage /> : <Navigate to="/" replace />} 
        />
        <Route 
          path="/results" 
          element={isLoggedIn ? <ResultsPage /> : <Navigate to="/" replace />} 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
