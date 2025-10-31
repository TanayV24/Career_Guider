import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5050/api';

export const api = {
  login: async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/login`, userData);
      console.log('Login response:', response.data);  // Debug log
      return response.data;
    } catch (error) {
      console.error('Login API error:', error.response?.data || error.message);
      throw error;
    }
  },
  
  getQuestions: async (mode) => {
    try {
      const response = await axios.get(`${API_URL}/questions/${mode}`);
      console.log('Questions response:', response.data);  // Debug log
      return response.data;
    } catch (error) {
      console.error('Questions API error:', error.response?.data || error.message);
      throw error;
    }
  },
  
  analyzeAnswer: async (answer) => {
    try {
      const response = await axios.post(`${API_URL}/analyze`, { answer });
      console.log('Analysis response:', response.data);  // Debug log
      return response.data;
    } catch (error) {
      console.error('Analyze API error:', error.response?.data || error.message);
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
      console.error('Submit API error:', error.response?.data || error.message);
      throw error;
    }
  },
  
  getRecommendations: async (userId) => {
    try {
      const response = await axios.post(`${API_URL}/recommend`, { user_id: userId });
      return response.data;
    } catch (error) {
      console.error('Recommend API error:', error.response?.data || error.message);
      throw error;
    }
  }
};
