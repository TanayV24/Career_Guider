import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../services/supabase';

function AuthCallback() {
  const navigate = useNavigate();

  useEffect(() => {
    handleCallback();
  }, []);

  const handleCallback = async () => {
    try {
      const { data: { session }, error } = await supabase.auth.getSession();

      if (error) throw error;

      if (session) {
        // Store user data
        localStorage.setItem('userId', session.user.id);
        localStorage.setItem('userName', session.user.user_metadata.full_name || session.user.email);
        localStorage.setItem('userEmail', session.user.email);
        localStorage.setItem('accessToken', session.access_token);

        // Redirect to mode selection
        navigate('/mode-selection');
      } else {
        navigate('/login');
      }
    } catch (error) {
      console.error('Callback error:', error);
      navigate('/login');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Authenticating...</h2>
        <p>Please wait while we sign you in.</p>
      </div>
    </div>
  );
}

export default AuthCallback;
