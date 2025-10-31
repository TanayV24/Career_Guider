import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5050/api';

export const api = {
  // Authentication
  signup: async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/auth/signup`, userData);
      return response.data;
    } catch (error) {
      console.error('Signup error:', error.response?.data || error.message);
      throw error;
    }
  },

  login: async (credentials) => {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, credentials);
      return response.data;
    } catch (error) {
      console.error('Login error:', error.response?.data || error.message);
      throw error;
    }
  },

  googleAuth: async () => {
    try {
      const response = await axios.post(`${API_URL}/auth/google`);
      return response.data;
    } catch (error) {
      console.error('Google auth error:', error.response?.data || error.message);
      throw error;
    }
  },

  googleCallback: async (tokens) => {
    try {
      const response = await axios.post(`${API_URL}/auth/google/callback`, tokens);
      return response.data;
    } catch (error) {
      console.error('Google callback error:', error.response?.data || error.message);
      throw error;
    }
  },

  logout: async () => {
    try {
      const response = await axios.post(`${API_URL}/auth/logout`);
      return response.data;
    } catch (error) {
      console.error('Logout error:', error.response?.data || error.message);
      throw error;
    }
  },

  // Questions
  getQuestions: async (mode) => {
    try {
      const response = await axios.get(`${API_URL}/questions/${mode}`);
      return response.data;
    } catch (error) {
      console.error('Questions error:', error.response?.data || error.message);
      throw error;
    }
  },

  analyzeAnswer: async (answer) => {
    try {
      const response = await axios.post(`${API_URL}/analyze`, { answer });
      return response.data;
    } catch (error) {
      console.error('Analyze error:', error.response?.data || error.message);
      throw error;
    }
  },

  submitAnswer: async (userId, questionId, answer) => {
    try {
      const response = await axios.post(`${API_URL}/submit-answer`, {
        user_id: userId,
        question_id: questionId,
        answer
      });
      return response.data;
    } catch (error) {
      console.error('Submit answer error:', error.response?.data || error.message);
      throw error;
    }
  },

  getRecommendations: async (userId) => {
    try {
      const response = await axios.post(`${API_URL}/recommend`, { user_id: userId });
      return response.data;
    } catch (error) {
      console.error('Recommendations error:', error.response?.data || error.message);
      throw error;
    }
  }
};
