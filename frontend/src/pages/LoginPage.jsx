import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { supabase } from '../services/supabase';
import './static/AuthPage.css';

function LoginPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    identifier: '', // Can be username or email
    password: ''
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.identifier.trim()) {
      newErrors.identifier = 'Username or email is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const response = await api.login({
        identifier: formData.identifier,
        password: formData.password
      });

      if (response.success) {
      // Store user data in MULTIPLE formats for compatibility
      const userData = {
        id: response.user.id,
        username: response.user.username,
        email: response.user.email
      };
      
      // Store as object (for QuestionPage & Dashboard)
      localStorage.setItem('user', JSON.stringify(userData));
      
      // Also store individual values (for backward compatibility)
      localStorage.setItem('userId', response.user.id);
      localStorage.setItem('userName', response.user.username);
      localStorage.setItem('userEmail', response.user.email);
      localStorage.setItem('accessToken', response.session.access_token);

      // Redirect to dashboard (not mode-selection)
      navigate('/dashboard');
      }
    } catch (error) {
      setErrors({ 
        submit: error.response?.data?.error || 'Login failed. Please check your credentials.' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`
        }
      });

      if (error) throw error;
    } catch (error) {
      console.error('Google login error:', error);
      setErrors({ submit: 'Google login failed. Please try again.' });
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Welcome Back! 👋</h1>
          <p>Login to continue your career journey</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {/* Username/Email */}
          <div className="form-group">
            <label htmlFor="identifier">Username or Email</label>
            <input
              type="text"
              id="identifier"
              name="identifier"
              value={formData.identifier}
              onChange={handleChange}
              className={errors.identifier ? 'error' : ''}
              placeholder="Enter username or email"
            />
            {errors.identifier && <span className="error-text">{errors.identifier}</span>}
          </div>

          {/* Password */}
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className={errors.password ? 'error' : ''}
              placeholder="Enter your password"
            />
            {errors.password && <span className="error-text">{errors.password}</span>}
          </div>

          {/* Submit Error */}
          {errors.submit && (
            <div className="error-box">
              {errors.submit}
            </div>
          )}

          {/* Submit Button */}
          <button type="submit" className="auth-button primary" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        {/* Divider */}
        <div className="divider">
          <span>OR</span>
        </div>

        {/* Google Login */}
        <button 
          type="button" 
          className="auth-button google"
          onClick={handleGoogleLogin}
        >
          <img 
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" 
            alt="Google"
            className="google-icon"
          />
          Continue with Google
        </button>

        {/* Signup Link */}
        <div className="auth-footer">
          <p>
            Don't have an account?{' '}
            <button 
              type="button"
              className="link-button" 
              onClick={() => navigate('/signup')}
            >
              Sign up here
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
