import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './static/StudentDashboard.css';

const StudentDashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('home'); // home, history, profile, recommendations
  const [stats, setStats] = useState({
    total_quizzes: 0,
    completed_quizzes: 0,
    incomplete_quizzes: 0,
    average_score: 0
  });
  const [quizHistory, setQuizHistory] = useState([]);
  const [incompleteSession, setIncompleteSession] = useState(null);
  const [profile, setProfile] = useState({
    phone: '',
    date_of_birth: '',
    gender: '',
    school_college: '',
    city: '',
    state: ''
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const indianStates = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
    'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Puducherry'
  ];

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData) {
      navigate('/login');
      return;
    }
    setUser(userData);
    fetchDashboardData(userData.id);
  }, [navigate]);

  const fetchDashboardData = async (userId) => {
    try {
      // Fetch stats
      const statsRes = await axios.get(`${process.env.REACT_APP_API_URL}/dashboard/stats?user_id=${userId}`);
      setStats(statsRes.data.stats);

      // Fetch quiz history
      const historyRes = await axios.get(`${process.env.REACT_APP_API_URL}/quiz/history?user_id=${userId}`);
      setQuizHistory(historyRes.data.history);
      const incomplete = historyRes.data.history.find(q => !q.is_completed);
      setIncompleteSession(incomplete);

      // Fetch profile
      const profileRes = await axios.get(`${process.env.REACT_APP_API_URL}/profile?user_id=${userId}`);
      if (profileRes.data.success) {
        setProfile(profileRes.data.profile);
      }

      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  const handleProfileChange = (e) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value
    });
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ type: '', text: '' });

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/profile`, {
        user_id: user.id,
        ...profile
      });

      if (response.data.success) {
        setMessage({ type: 'success', text: '✅ Profile updated successfully!' });
        setTimeout(() => setMessage({ type: '', text: '' }), 3000);
      }
    } catch (error) {
      setMessage({ type: 'error', text: '❌ Failed to update profile.' });
    } finally {
      setSaving(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', { year: 'numeric', month: 'short', day: 'numeric' });
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading your dashboard...</p>
      </div>
    );
  }

  return (
    <div className="student-dashboard">
      {/* Welcome Header */}
      <div className="dashboard-header">
        <div className="welcome-section">
          <div className="user-avatar">
            {user?.username?.charAt(0).toUpperCase() || 'S'}
          </div>
          <div className="welcome-text">
            <h1>Welcome back, {user?.username}! 👋</h1>
            <p>Ready to discover your perfect career path?</p>
          </div>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="tabs-container">
        <button 
          className={`tab ${activeTab === 'home' ? 'active' : ''}`}
          onClick={() => setActiveTab('home')}
        >
          <span className="tab-icon">🏠</span>
          Home
        </button>
        <button 
          className={`tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          <span className="tab-icon">📚</span>
          Quiz History
          {stats.incomplete_quizzes > 0 && (
            <span className="tab-badge">{stats.incomplete_quizzes}</span>
          )}
        </button>
        <button 
          className={`tab ${activeTab === 'recommendations' ? 'active' : ''}`}
          onClick={() => setActiveTab('recommendations')}
        >
          <span className="tab-icon">⭐</span>
          Recommendations
        </button>
        <button 
          className={`tab ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          <span className="tab-icon">👤</span>
          Profile
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {/* HOME TAB */}
        {activeTab === 'home' && (
          <div className="home-tab">
            {/* Stats Cards */}
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">📊</div>
                <div className="stat-info">
                  <h3>{stats.total_quizzes}</h3>
                  <p>Total Quizzes</p>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">✅</div>
                <div className="stat-info">
                  <h3>{stats.completed_quizzes}</h3>
                  <p>Completed</p>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">⏳</div>
                <div className="stat-info">
                  <h3>{stats.incomplete_quizzes}</h3>
                  <p>In Progress</p>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">⭐</div>
                <div className="stat-info">
                  <h3>{stats.average_score}%</h3>
                  <p>Avg Score</p>
                </div>
              </div>
            </div>

            {/* Resume Quiz Alert */}
            {incompleteSession && (
              <div className="resume-alert">
                <div className="alert-content">
                  <span className="alert-icon">🔄</span>
                  <div className="alert-text">
                    <h4>Resume Your Quiz</h4>
                    <p>You have an incomplete {incompleteSession.mode.toUpperCase()} quiz. Pick up where you left off!</p>
                  </div>
                  <button 
                    className="btn btn-primary" 
                    onClick={() => navigate('/questions', { 
                      state: { 
                        sessionId: incompleteSession.id,
                        mode: incompleteSession.mode,
                        resume: true
                      } 
                    })}
                  >
                    Continue Quiz
                  </button>
                </div>
              </div>
            )}

            {/* Action Cards */}
            <div className="dashboard-grid">
              <div className="dashboard-card take-quiz-card" onClick={() => navigate('/mode-selection')}>
                <div className="card-icon">🎯</div>
                <h3>Take New Quiz</h3>
                <p>Start your career discovery journey</p>
                <div className="card-arrow">→</div>
              </div>

              <div className="dashboard-card" onClick={() => setActiveTab('history')}>
                <div className="card-icon">📈</div>
                <h3>View History</h3>
                <p>Review your past quizzes</p>
                <div className="card-arrow">→</div>
              </div>

              <div className="dashboard-card" onClick={() => setActiveTab('recommendations')}>
                <div className="card-icon">💼</div>
                <h3>Career Paths</h3>
                <p>Explore recommended careers</p>
                <div className="card-arrow">→</div>
              </div>

              <div className="dashboard-card" onClick={() => setActiveTab('profile')}>
                <div className="card-icon">⚙️</div>
                <h3>Settings</h3>
                <p>Update your profile</p>
                <div className="card-arrow">→</div>
              </div>
            </div>

            {/* Quick Tips */}
            <div className="tips-section">
              <h3>💡 Quick Tips</h3>
              <div className="tips-grid">
                <div className="tip-card">
                  <span className="tip-icon">🎯</span>
                  <p>Complete your profile for better recommendations</p>
                </div>
                <div className="tip-card">
                  <span className="tip-icon">📝</span>
                  <p>Take multiple quizzes to refine suggestions</p>
                </div>
                <div className="tip-card">
                  <span className="tip-icon">🚀</span>
                  <p>Answer honestly for best results</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* QUIZ HISTORY TAB */}
        {activeTab === 'history' && (
          <div className="history-tab">
            <div className="history-header">
              <h2>Quiz History</h2>
              <p>Track your progress and review past quizzes</p>
            </div>

            {quizHistory.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">📝</div>
                <h3>No quizzes yet</h3>
                <p>Start your first quiz to see your history here</p>
                <button className="btn btn-primary" onClick={() => navigate('/mode-selection')}>
                  Take Your First Quiz
                </button>
              </div>
            ) : (
              <div className="history-grid">
                {quizHistory.map((quiz) => (
                  <div key={quiz.id} className={`history-card ${quiz.is_completed ? 'completed' : 'incomplete'}`}>
                    <div className="history-header-row">
                      <div className="quiz-mode-badge">{quiz.mode.toUpperCase()}</div>
                      <div className={`status-badge ${quiz.is_completed ? 'completed' : 'in-progress'}`}>
                        {quiz.is_completed ? '✅ Completed' : '⏳ In Progress'}
                      </div>
                    </div>

                    <div className="history-content">
                      <div className="history-info">
                        <p className="quiz-class">{quiz.class_level || 'General'}</p>
                        <p className="quiz-date">Started: {formatDate(quiz.created_at)}</p>
                        {quiz.completed_at && (
                          <p className="quiz-date">Completed: {formatDate(quiz.completed_at)}</p>
                        )}
                      </div>

                      <div className="history-stats">
                        <div className="stat-item">
                          <span className="stat-label">Progress</span>
                          <span className="stat-value">{quiz.current_question}/{quiz.total_questions}</span>
                        </div>
                        {quiz.is_completed && (
                          <div className="stat-item">
                            <span className="stat-label">Score</span>
                            <span className="stat-value score">{quiz.score}%</span>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="history-actions">
                      {!quiz.is_completed ? (
                        <button 
                          className="btn btn-sm btn-primary"
                          onClick={() => navigate('/questions', { 
                            state: { 
                              sessionId: quiz.id,
                              mode: quiz.mode,
                              resume: true
                            } 
                          })}
                        >
                          Continue Quiz
                        </button>
                      ) : (
                        <button className="btn btn-sm btn-secondary" onClick={() => setActiveTab('recommendations')}>
                          View Recommendations
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* RECOMMENDATIONS TAB */}
        {activeTab === 'recommendations' && (
          <div className="recommendations-tab">
            <div className="recommendations-header">
              <h2>Career Recommendations</h2>
              <p>Based on your quiz responses and interests</p>
            </div>

            <div className="coming-soon">
              <div className="coming-soon-icon">🚀</div>
              <h3>Coming Soon!</h3>
              <p>Complete more quizzes to unlock personalized career recommendations</p>
              <button className="btn btn-primary" onClick={() => navigate('/mode-selection')}>
                Take a Quiz
              </button>
            </div>
          </div>
        )}

        {/* PROFILE TAB */}
        {activeTab === 'profile' && (
          <div className="profile-tab">
            <div className="profile-header-section">
              <h2>Profile Settings</h2>
              <p>Complete your profile for better career recommendations</p>
            </div>

            <form className="profile-form" onSubmit={handleProfileSubmit}>
              {/* Basic Info */}
              <div className="form-section">
                <h3>📋 Basic Information</h3>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Username</label>
                    <input
                      type="text"
                      value={user?.username || ''}
                      disabled
                      className="form-control disabled"
                    />
                  </div>

                  <div className="form-group">
                    <label>Email</label>
                    <input
                      type="email"
                      value={user?.email || ''}
                      disabled
                      className="form-control disabled"
                    />
                  </div>

                  <div className="form-group">
                    <label>Phone Number *</label>
                    <input
                      type="tel"
                      name="phone"
                      value={profile.phone}
                      onChange={handleProfileChange}
                      placeholder="+91 XXXXX XXXXX"
                      className="form-control"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Date of Birth *</label>
                    <input
                      type="date"
                      name="date_of_birth"
                      value={profile.date_of_birth}
                      onChange={handleProfileChange}
                      className="form-control"
                      required
                      max={new Date().toISOString().split('T')[0]}
                    />
                  </div>

                  <div className="form-group">
                    <label>Gender *</label>
                    <select
                      name="gender"
                      value={profile.gender}
                      onChange={handleProfileChange}
                      className="form-control"
                      required
                    >
                      <option value="">Select Gender</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                      <option value="Prefer not to say">Prefer not to say</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Education */}
              <div className="form-section">
                <h3>🎓 Education Details</h3>
                <div className="form-group full-width">
                  <label>School/College Name *</label>
                  <input
                    type="text"
                    name="school_college"
                    value={profile.school_college}
                    onChange={handleProfileChange}
                    placeholder="Enter your school or college name"
                    className="form-control"
                    required
                  />
                </div>
              </div>

              {/* Location */}
              <div className="form-section">
                <h3>📍 Location</h3>
                <div className="form-grid">
                  <div className="form-group">
                    <label>City *</label>
                    <input
                      type="text"
                      name="city"
                      value={profile.city}
                      onChange={handleProfileChange}
                      placeholder="Enter your city"
                      className="form-control"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>State *</label>
                    <select
                      name="state"
                      value={profile.state}
                      onChange={handleProfileChange}
                      className="form-control"
                      required
                    >
                      <option value="">Select State</option>
                      {indianStates.map(state => (
                        <option key={state} value={state}>{state}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              {message.text && (
                <div className={`message ${message.type}`}>
                  {message.text}
                </div>
              )}

              <div className="form-actions">
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? 'Saving...' : 'Save Profile'}
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default StudentDashboard;
