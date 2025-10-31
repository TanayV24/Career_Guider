import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './ModeSelection.css';

function ModeSelection() {
  const navigate = useNavigate();
  const [showSplash, setShowSplash] = useState(true);
  const [showComingSoon, setShowComingSoon] = useState(false);
  const [showClassSelection, setShowClassSelection] = useState(false);
  const userName = localStorage.getItem('userName') || 'Friend';

  useEffect(() => {
    const hasSeenSplash = sessionStorage.getItem('hasSeenSplash');
    
    if (hasSeenSplash) {
      setShowSplash(false);
    } else {
      const timer = setTimeout(() => {
        setShowSplash(false);
        sessionStorage.setItem('hasSeenSplash', 'true');
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleCollegeClick = () => {
    setShowComingSoon(true);
  };

  const handleSSCClick = () => {
    setShowClassSelection(true);
  };

  const handleClassSelect = (classLevel) => {
    localStorage.setItem('selectedMode', 'ssc');
    localStorage.setItem('classLevel', classLevel);
    navigate('/questions');
  };

  return (
    <div className="mode-container">
      {/* Splash Overlay */}
      {showSplash && (
        <div className="splash-overlay">
          <div className="splash-content">
            <h1 className="splash-title">Welcome, {userName}! 🎉</h1>
            <p className="splash-subtitle">Let's discover your perfect career path!</p>
            <div className="splash-loader"></div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className={`mode-content ${showSplash ? 'hidden' : 'visible'}`}>
        <div className="mode-header">
          <h1>Choose Your Path 🎯</h1>
          <p>Select the category that matches your current education level</p>
        </div>

        <div className="mode-cards">
          <div className="mode-card" onClick={handleSSCClick}>
            <div className="mode-icon">🎓</div>
            <h2>Class 10-12</h2>
            <p>SSC/HSC Students</p>
            <ul className="mode-features">
              <li>✓ Stream selection guidance</li>
              <li>✓ Career exploration</li>
              <li>✓ Interest assessment</li>
            </ul>
            <button className="mode-button">Start Quiz</button>
          </div>

          <div className="mode-card" onClick={handleCollegeClick}>
            <div className="mode-icon">📚</div>
            <h2>College</h2>
            <p>Undergraduate Students</p>
            <ul className="mode-features">
              <li>✓ Career path planning</li>
              <li>✓ Skill assessment</li>
              <li>✓ Job recommendations</li>
            </ul>
            <button className="mode-button">Coming Soon</button>
          </div>
        </div>
      </div>

      {/* Class Selection Modal */}
      {showClassSelection && (
        <div className="modal-overlay" onClick={() => setShowClassSelection(false)}>
          <div className="modal-content class-selection" onClick={(e) => e.stopPropagation()}>
            <h2>Select Your Class 📚</h2>
            <p>Which class are you currently in?</p>
            <div className="class-buttons">
              <button 
                className="class-btn"
                onClick={() => handleClassSelect('10')}
              >
                <span className="class-number">10</span>
                <span className="class-label">Class 10 (SSC)</span>
              </button>
              <button 
                className="class-btn"
                onClick={() => handleClassSelect('12')}
              >
                <span className="class-number">12</span>
                <span className="class-label">Class 12 (HSC)</span>
              </button>
            </div>
            <button 
              className="modal-back-btn"
              onClick={() => setShowClassSelection(false)}
            >
              ← Back
            </button>
          </div>
        </div>
      )}

      {/* Coming Soon Modal */}
      {showComingSoon && (
        <div className="modal-overlay" onClick={() => setShowComingSoon(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-icon">🚀</div>
            <h2>College Mode - Coming Soon!</h2>
            <p>We're working on an amazing experience for college students. Stay tuned!</p>
            <button 
              className="modal-close-btn"
              onClick={() => setShowComingSoon(false)}
            >
              Got it!
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ModeSelection;
