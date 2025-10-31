import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useTheme } from '../context/ThemeContext';
import './QuestionPage.css';

const MOTIVATIONAL_QUOTES = [
  "Your career is a journey, not a destination! 🚀",
  "Dream big, work hard, stay focused! 💪",
  "The future belongs to those who believe in their dreams! ✨",
  "Success is not final, failure is not fatal! 🌟",
  "Believe in yourself and magic will happen! 🎯"
];

function QuestionPage() {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [score, setScore] = useState(0);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  
  const [showMotivational, setShowMotivational] = useState(true);
  const [motivationalQuote] = useState(
    MOTIVATIONAL_QUOTES[Math.floor(Math.random() * MOTIVATIONAL_QUOTES.length)]
  );

  const userId = localStorage.getItem('userId') || 'guest_' + Date.now();
  const selectedMode = localStorage.getItem('selectedMode') || 'ssc';

  useEffect(() => {
    localStorage.setItem('userId', userId);
    loadQuestions();

    const timer = setTimeout(() => {
      setShowMotivational(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    sessionStorage.setItem('currentQuestion', currentIndex + 1);
  }, [currentIndex]);

  const loadQuestions = async () => {
    try {
      const data = await api.getQuestions(selectedMode);
      console.log('✅ Questions loaded:', data.length);
      setQuestions(data);
      setLoading(false);
    } catch (error) {
      console.error('❌ Load error:', error);
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
      console.log('📝 Submitting:', answer);

      api.analyzeAnswer(answer).then(analysis => {
        console.log('🧠 NLP Analysis:', analysis);
      }).catch(err => {
        console.error('Analysis error (non-critical):', err);
      });

      const result = await api.submitAnswer(userId, questions[currentIndex].id, answer);
      console.log('✅ Submitted successfully');

      setScore(result.score);

      setTimeout(() => {
        if (currentIndex < questions.length - 1) {
          setCurrentIndex(currentIndex + 1);
          setAnswer('');
        } else {
          navigate('/results');
        }
        setAnalyzing(false);
      }, 500);

    } catch (error) {
      console.error('❌ Error:', error);
      alert('Error: ' + error.message);
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
        <div className="animated-background"></div>
        <div className="loading">Loading questions...</div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="question-container">
        <div className="animated-background"></div>
        <div className="error">
          <p>No questions found!</p>
          <button onClick={() => navigate('/')}>Go Back</button>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[currentIndex];

  return (
    <div className="question-container">
      {/* Animated Background */}
      <div className="animated-background">
        <div className="floating-shape shape-1"></div>
        <div className="floating-shape shape-2"></div>
        <div className="floating-shape shape-3"></div>
        <div className="floating-shape shape-4"></div>
        <div className="floating-shape shape-5"></div>
      </div>

      {/* Motivational Overlay */}
      {showMotivational && (
        <div className="motivational-overlay">
          <div className="motivational-content">
            <div className="motivational-icon">💡</div>
            <h2 className="motivational-quote">{motivationalQuote}</h2>
            <p className="motivational-subtitle">Let's begin your journey!</p>
          </div>
        </div>
      )}

      {/* Question Card */}
      <div className="question-card">
        <div className="question-header">
          <h1 className="header-title">Career Guider 🎯</h1>
          <div className="score-badge">
            <span className="score-label">Score</span>
            <span className="score-value">{score}</span>
          </div>
        </div>

        <div className="progress-section">
          <div className="progress-text">
            Question {currentIndex + 1} of {questions.length}
          </div>
          <div className="progress-bar-container">
            <div 
              className="progress-bar-fill" 
              style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>

        <div className="question-content">
          <div className="question-number-badge">Q{currentIndex + 1}</div>
          <h2 className="question-text">{currentQuestion.text}</h2>

          {currentQuestion.type === 'choice' && currentQuestion.options ? (
            <div className="choices">
              {currentQuestion.options.map((option, idx) => (
                <button
                  key={idx}
                  className={`choice-button ${answer === option ? 'selected' : ''}`}
                  onClick={() => handleAnswerChange(option)}
                  disabled={analyzing}
                >
                  <span className="choice-icon">
                    {answer === option ? '✓' : String.fromCharCode(65 + idx)}
                  </span>
                  <span className="choice-text">{option}</span>
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
            {analyzing ? (
              <>
                <span className="button-spinner"></span>
                Processing...
              </>
            ) : currentIndex === questions.length - 1 ? (
              '✓ Finish'
            ) : (
              'Next →'
            )}
          </button>
        </div>
      </div>

      {analyzing && (
        <div className="analyzing-overlay">
          <div className="analyzing-content">
            <div className="analyzing-spinner"></div>
            <p>Analyzing with NLP... 🧠</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default QuestionPage;
