import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useTheme } from '../context/ThemeContext';
import './ResultsPage.css';

function ResultsPage() {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const [recommendations, setRecommendations] = useState(null);
  const [showResults, setShowResults] = useState(false);
  const [showRetakeModal, setShowRetakeModal] = useState(false);
  const [showComingSoon, setShowComingSoon] = useState(false);
  const userName = localStorage.getItem('userName') || 'Friend';
  const userId = localStorage.getItem('userId');

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      const data = await api.getRecommendations(userId);
      setRecommendations(data);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
    }
  };

  const handleContinueSession = () => {
    setShowRetakeModal(false);
    navigate('/mode-selection');
  };

  const handleNewSession = () => {
    localStorage.clear();
    sessionStorage.clear();
    navigate('/');
  };

  return (
    <div className="results-container">
      <div className="results-card">
        {/* Completion Section */}
        <div className="completion-section">
          <div className="completion-icon">🎉</div>
          <h1 className="completion-title">Quiz Completed!</h1>
          <p className="completion-subtitle">Amazing work, {userName}!</p>
          <p className="completion-text">You've successfully completed all questions</p>
        </div>

        {/* Action Buttons */}
        <div className="results-actions-top">
          <button 
            className="action-btn primary-btn"
            onClick={() => setShowResults(!showResults)}
          >
            {showResults ? '🔼 Hide Results' : '📊 Show Results'}
          </button>
          <button 
            className="action-btn secondary-btn"
            onClick={() => setShowComingSoon(true)}
          >
            📥 Download Results
          </button>
          <button 
            className="action-btn retake-btn"
            onClick={() => setShowRetakeModal(true)}
          >
            🔄 Retake Quiz
          </button>
        </div>

        {/* Results Section (Expandable) */}
        {showResults && recommendations && (
          <div className="recommendations-section">
            <div className="recommendation-box">
              <h3>📚 Recommended Streams</h3>
              <ul>
                {recommendations.streams.map((stream, idx) => (
                  <li key={idx}>{stream}</li>
                ))}
              </ul>
            </div>

            <div className="recommendation-box">
              <h3>💼 Suggested Careers</h3>
              <ul>
                {recommendations.careers.map((career, idx) => (
                  <li key={idx}>{career}</li>
                ))}
              </ul>
            </div>

            <div className="recommendation-box">
              <h3>📊 Analysis</h3>
              <p>{recommendations.analysis}</p>
            </div>
          </div>
        )}
      </div>

      {/* Retake Quiz Modal */}
      {showRetakeModal && (
        <div className="modal-overlay" onClick={() => setShowRetakeModal(false)}>
          <div className="modal-content retake-modal" onClick={(e) => e.stopPropagation()}>
            <h2>Retake Quiz 🔄</h2>
            <p>How would you like to proceed?</p>
            <div className="retake-options">
              <button 
                className="retake-option-btn"
                onClick={handleContinueSession}
              >
                <span className="option-icon">👤</span>
                <span className="option-title">Continue as {userName}</span>
                <span className="option-desc">Keep your current profile</span>
              </button>
              <button 
                className="retake-option-btn"
                onClick={handleNewSession}
              >
                <span className="option-icon">✨</span>
                <span className="option-title">Start New Session</span>
                <span className="option-desc">Create a fresh profile</span>
              </button>
            </div>
            <button 
              className="modal-back-btn"
              onClick={() => setShowRetakeModal(false)}
            >
              ← Cancel
            </button>
          </div>
        </div>
      )}

      {/* Coming Soon Modal */}
      {showComingSoon && (
        <div className="modal-overlay" onClick={() => setShowComingSoon(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-icon">🚀</div>
            <h2>Download Results - Coming Soon!</h2>
            <p>Soon you'll be able to download your results as a PDF report!</p>
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

export default ResultsPage;
