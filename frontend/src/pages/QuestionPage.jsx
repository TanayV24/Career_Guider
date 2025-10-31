import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import './QuestionPage.css';

function QuestionPage() {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [score, setScore] = useState(0);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);

  const userId = localStorage.getItem('userId');
  const selectedMode = localStorage.getItem('selectedMode') || 'ssc';

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const data = await api.getQuestions(selectedMode);
      console.log('Loaded questions:', data); // Debug
      setQuestions(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load questions:', error);
      setLoading(false);
    }
  };

  const handleAnswerChange = (value) => {
    setAnswer(value);
  };

  const handleSubmit = async () => {
    if (!answer.trim()) {
      alert('Please provide an answer!');
      return;
    }

    setAnalyzing(true);

    try {
      // Analyze with NLP (but don't wait for it)
      api.analyzeAnswer(answer).then(analysis => {
        console.log('NLP Analysis:', analysis);
      }).catch(err => {
        console.error('Analysis error:', err);
      });

      // Submit answer
      const result = await api.submitAnswer(userId, questions[currentIndex].id, answer);
      console.log('Submit result:', result);

      // Wait just a moment for visual feedback
      setTimeout(() => {
        setScore(score + 20);
        
        // Move to next question or finish
        if (currentIndex < questions.length - 1) {
          setCurrentIndex(currentIndex + 1);
          setAnswer('');
        } else {
          navigate('/results');
        }
        setAnalyzing(false);
      }, 800); // Reduced to 0.8 seconds

    } catch (error) {
      console.error('Error:', error);
      alert('Something went wrong. Please try again.');
      setAnalyzing(false);
    }
  };

  const handleBack = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setAnswer('');
    }
  };

  if (loading) {
    return (
      <div className="question-container">
        <div className="loading">Loading questions...</div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="question-container">
        <div className="error">No questions available</div>
      </div>
    );
  }

  const currentQuestion = questions[currentIndex];

  return (
    <div className="question-container">
      <div className="question-card">
        {/* Header */}
        <div className="question-header">
          <h1>Career Guider 🎯</h1>
          <div className="score-badge">Score: {score}</div>
        </div>

        {/* Progress */}
        <div className="progress-section">
          <div className="progress-text">
            Question {currentIndex + 1} of {questions.length}
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Question */}
        <div className="question-content">
          <div className="question-number">Q{currentIndex + 1}</div>
          <h2 className="question-text">{currentQuestion.text}</h2>

          {/* Answer Input */}
          {currentQuestion.type === 'choice' && currentQuestion.options ? (
            <div className="choices">
              {currentQuestion.options.map((option, idx) => (
                <button
                  key={idx}
                  className={`choice-button ${answer === option ? 'selected' : ''}`}
                  onClick={() => handleAnswerChange(option)}
                  disabled={analyzing}
                >
                  {option}
                </button>
              ))}
            </div>
          ) : (
            <textarea
              className="text-input"
              placeholder="Type your answer here..."
              value={answer}
              onChange={(e) => handleAnswerChange(e.target.value)}
              rows={4}
              disabled={analyzing}
            />
          )}
        </div>

        {/* Actions */}
        <div className="question-actions">
          {currentIndex > 0 && (
            <button 
              className="back-button" 
              onClick={handleBack}
              disabled={analyzing}
            >
              ← Back
            </button>
          )}
          <button 
            className="submit-button" 
            onClick={handleSubmit}
            disabled={analyzing || !answer.trim()}
          >
            {analyzing ? 'Processing...' : currentIndex === questions.length - 1 ? 'Finish' : 'Next →'}
          </button>
        </div>

        {/* Analyzing Overlay (simplified) */}
        {analyzing && (
          <div className="analyzing-overlay">
            <div className="analyzing-content">
              <div className="analyzing-spinner"></div>
              <p>Processing...</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default QuestionPage;
