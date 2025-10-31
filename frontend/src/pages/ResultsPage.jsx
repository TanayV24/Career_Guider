import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import './ResultsPage.css';

function ResultsPage() {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState(null);
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

  const handleRetake = () => {
    localStorage.removeItem('userId');
    localStorage.removeItem('userName');
    localStorage.removeItem('selectedMode');
    navigate('/');
  };

  return (
    <div className="results-container">
      <div className="results-card">
        <div className="results-header">
          <h1>🏆 Quiz Completed!</h1>
          <p>Amazing work, {userName}!</p>
        </div>

        {recommendations && (
          <div className="recommendations-section">
            <h2>Your Career Recommendations</h2>
            
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

        <div className="results-actions">
          <button className="retake-button" onClick={handleRetake}>
            🔄 Retake Quiz
          </button>
        </div>
      </div>
    </div>
  );
}

export default ResultsPage;
