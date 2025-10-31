import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ModeSelection.css';

function ModeSelection() {
  const navigate = useNavigate();

  const handleModeSelect = (mode) => {
    localStorage.setItem('selectedMode', mode);
    navigate('/motivational-quote');
  };

  return (
    <div className="mode-container">
      <div className="mode-header">
        <h1>Choose Your Path 🎯</h1>
        <p>Select the category that matches your current education level</p>
      </div>

      <div className="mode-cards">
        <div className="mode-card" onClick={() => handleModeSelect('ssc')}>
          <div className="mode-icon">🎓</div>
          <h2>SSC/HSC</h2>
          <p>Class 10-12 Students</p>
          <button className="mode-button">Start Quiz</button>
        </div>

        <div className="mode-card" onClick={() => handleModeSelect('hsc')}>
          <div className="mode-icon">📚</div>
          <h2>College</h2>
          <p>Undergraduate Students</p>
          <button className="mode-button">Start Quiz</button>
        </div>
      </div>
    </div>
  );
}

export default ModeSelection;
