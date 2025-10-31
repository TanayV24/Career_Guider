import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './MotivationalQuote.css';

const quotes = [
  "Your career is a journey, not a destination! 🚀",
  "Dream big, work hard, stay focused! 💪",
  "The future belongs to those who believe in their dreams! ✨",
  "Success is not final, failure is not fatal! 🌟",
  "Believe in yourself and magic will happen! 🎯"
];

function MotivationalQuote() {
  const navigate = useNavigate();
  const [quote] = useState(quotes[Math.floor(Math.random() * quotes.length)]);

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/questions');
    }, 3000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="quote-container">
      <div className="quote-content">
        <div className="quote-icon">💡</div>
        <h2 className="quote-text">{quote}</h2>
        <p className="quote-subtitle">Let's begin your journey!</p>
      </div>
    </div>
  );
}

export default MotivationalQuote;
