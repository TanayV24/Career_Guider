import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './SplashScreen.css';

function SplashScreen() {
  const navigate = useNavigate();
  const userName = localStorage.getItem('userName') || 'Friend';

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/mode-selection');
    }, 2000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="splash-container">
      <div className="splash-content">
        <h1 className="splash-title animate-fade-in">
          Welcome, {userName}! 🎉
        </h1>
        <p className="splash-subtitle animate-fade-in-delay">
          Let's discover your perfect career path!
        </p>
        <div className="loader"></div>
      </div>
    </div>
  );
}

export default SplashScreen;
