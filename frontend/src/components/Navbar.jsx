import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import './Navbar.css';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const userName = localStorage.getItem('userName') || 'Guest';
  
  const [showModeDropdown, setShowModeDropdown] = useState(false);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const [showComingSoon, setShowComingSoon] = useState(false);
  const [comingSoonMessage, setComingSoonMessage] = useState('');

  const modeRef = useRef(null);
  const userRef = useRef(null);

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (modeRef.current && !modeRef.current.contains(event.target)) {
        setShowModeDropdown(false);
      }
      if (userRef.current && !userRef.current.contains(event.target)) {
        setShowUserDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleComingSoon = (feature) => {
    setComingSoonMessage(`${feature} - Coming Soon! 🚀`);
    setShowComingSoon(true);
    setShowModeDropdown(false);
    setShowUserDropdown(false);
  };

  const handleLogout = () => {
    localStorage.clear();
    sessionStorage.clear();
    navigate('/');
  };

  const handleModeSelect = (mode) => {
    if (mode === 'college') {
      handleComingSoon('College Students Mode');
    } else {
      navigate('/mode-selection');
    }
    setShowModeDropdown(false);
  };

  const showHistory = () => {
    const currentQ = sessionStorage.getItem('currentQuestion') || '1';
    alert(`You are currently on Question ${currentQ}`);
    setShowUserDropdown(false);
  };

  const handleHomeClick = async () => {
    // If on question page, ask to save progress
    if (location.pathname === '/questions') {
      const confirmLeave = window.confirm(
        '⚠️ Your progress will be saved.\n\nDo you want to leave and return to dashboard?'
      );
      
      if (confirmLeave) {
        // Progress is auto-saved, just navigate
        navigate('/dashboard');
      }
    } else {
      // Not on questions page, go directly to dashboard
      navigate('/dashboard');
    }
  };

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          {/* Left Side - Logo */}
          <div className="navbar-logo" onClick={() => navigate('/mode-selection')}>
            <span className="logo-icon">🎯</span>
            <span className="logo-text">Career Guider</span>
          </div>

          {/* Right Side - Menu Items */}
          <div className="navbar-menu">
            {/* Home Button */}
            <button 
              className="nav-btn" 
              onClick={() => handleHomeClick()}
            >
              🏠 Home
            </button>

            {/* Mode Dropdown */}
            <div className="dropdown" ref={modeRef}>
              <button 
                className="nav-btn dropdown-btn"
                onClick={() => setShowModeDropdown(!showModeDropdown)}
              >
                📚 Mode ▼
              </button>
              {showModeDropdown && (
                <div className="dropdown-menu">
                  <div 
                    className="dropdown-item"
                    onClick={() => handleModeSelect('ssc')}
                  >
                    🎓 Class 10-12 Students
                  </div>
                  <div 
                    className="dropdown-item"
                    onClick={() => handleModeSelect('college')}
                  >
                    🎓 College Students
                  </div>
                </div>
              )}
            </div>

            {/* Theme Toggle */}
            <button 
              className="nav-btn theme-toggle"
              onClick={toggleTheme}
              title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            >
              {theme === 'light' ? '🌙' : '☀️'}
            </button>

            {/* User Dropdown */}
            <div className="dropdown" ref={userRef}>
              <button 
                className="nav-btn user-btn dropdown-btn"
                onClick={() => setShowUserDropdown(!showUserDropdown)}
              >
                👤 {userName} ▼
              </button>
              {showUserDropdown && (
                <div className="dropdown-menu user-menu">
                  <div 
                    className="dropdown-item"
                    onClick={() => handleComingSoon('Badges')}
                  >
                    🏆 Badges
                  </div>
                  <div 
                    className="dropdown-item"
                    onClick={showHistory}
                  >
                    📜 History
                  </div>
                  <div className="dropdown-divider"></div>
                  <div 
                    className="dropdown-item logout-item"
                    onClick={handleLogout}
                  >
                    🚪 Logout
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Coming Soon Modal */}
      {showComingSoon && (
        <div className="modal-overlay" onClick={() => setShowComingSoon(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-icon">🚀</div>
            <h2>{comingSoonMessage}</h2>
            <p>This feature is under development and will be available soon!</p>
            <button 
              className="modal-close-btn"
              onClick={() => setShowComingSoon(false)}
            >
              Got it!
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default Navbar;
