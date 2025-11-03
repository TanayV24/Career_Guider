import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { supabase } from '../services/supabase';
import './static/AuthPage.css';

function SignupPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    } else if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
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
      const response = await api.signup({
        username: formData.username,
        email: formData.email,
        password: formData.password
      });

      if (response.success) {
        alert('Signup successful! Please login.');
        navigate('/login');
      }
    } catch (error) {
      setErrors({ 
        submit: error.response?.data?.error || 'Signup failed. Please try again.' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignup = async () => {
    try {
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`
        }
      });

      if (error) throw error;
    } catch (error) {
      console.error('Google signup error:', error);
      setErrors({ submit: 'Google signup failed. Please try again.' });
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Create Account 🎯</h1>
          <p>Join Career Guider to discover your perfect path</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {/* Username */}
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className={errors.username ? 'error' : ''}
              placeholder="Choose a username"
            />
            {errors.username && <span className="error-text">{errors.username}</span>}
          </div>

          {/* Email */}
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'error' : ''}
              placeholder="your.email@example.com"
            />
            {errors.email && <span className="error-text">{errors.email}</span>}
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
              placeholder="Minimum 6 characters"
            />
            {errors.password && <span className="error-text">{errors.password}</span>}
          </div>

          {/* Confirm Password */}
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              className={errors.confirmPassword ? 'error' : ''}
              placeholder="Re-enter your password"
            />
            {errors.confirmPassword && <span className="error-text">{errors.confirmPassword}</span>}
          </div>

          {/* Submit Error */}
          {errors.submit && (
            <div className="error-box">
              {errors.submit}
            </div>
          )}

          {/* Submit Button */}
          <button type="submit" className="auth-button primary" disabled={loading}>
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        {/* Divider */}
        <div className="divider">
          <span>OR</span>
        </div>

        {/* Google Signup */}
        <button 
          type="button" 
          className="auth-button google"
          onClick={handleGoogleSignup}
        >
          <img 
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" 
            alt="Google"
            className="google-icon"
          />
          Continue with Google
        </button>

        {/* Login Link */}
        <div className="auth-footer">
          <p>
            Already have an account?{' '}
            <button 
              type="button"
              className="link-button" 
              onClick={() => navigate('/login')}
            >
              Login here
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default SignupPage;
