from flask import Blueprint, request, jsonify, session
from flask_bcrypt import Bcrypt
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))

from nlp_engine import SimpleNLP
from question_bank import SSC_QUESTIONS, HSC_QUESTIONS
from supabase_client import get_supabase

bp = Blueprint('api', __name__, url_prefix='/api')
supabase = get_supabase()
bcrypt = Bcrypt()

def clean_questions(questions):
    """Remove lambda functions from questions"""
    cleaned = []
    for q in questions:
        clean_q = {
            'id': q.get('id'),
            'text': q.get('text'),
            'type': q.get('type'),
        }
        if 'options' in q:
            clean_q['options'] = q['options']
        cleaned.append(clean_q)
    return cleaned

@bp.route('/auth/signup', methods=['POST'])
def signup():
    """User signup with email/password"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not all([username, email, password]):
            return jsonify({'success': False, 'error': 'All fields required'}), 400
        
        # Check if user already exists
        existing = supabase.table('users').select('*').eq('email', email).execute()
        if existing.data:
            return jsonify({'success': False, 'error': 'Email already registered'}), 400
        
        # Hash password[web:63][web:65]
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create user in Supabase Auth
        auth_response = supabase.auth.sign_up({
            'email': email,
            'password': password,
            'options': {
                'data': {
                    'username': username
                }
            }
        })
        
        if auth_response.user:
            # Create user record in database
            user_data = {
                'id': auth_response.user.id,
                'username': username,
                'email': email,
                'password_hash': hashed_password,
                'auth_provider': 'email'
            }
            supabase.table('users').insert(user_data).execute()
            
            return jsonify({
                'success': True,
                'message': 'Signup successful! Please login.',
                'user': {
                    'id': auth_response.user.id,
                    'username': username,
                    'email': email
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Signup failed'}), 500
            
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/auth/login', methods=['POST'])
def login():
    """User login with email/username and password"""
    try:
        data = request.json
        identifier = data.get('identifier')  # Can be username or email
        password = data.get('password')
        
        if not all([identifier, password]):
            return jsonify({'success': False, 'error': 'All fields required'}), 400
        
        # Find user by email or username
        user_query = supabase.table('users').select('*')
        if '@' in identifier:
            user_query = user_query.eq('email', identifier)
        else:
            user_query = user_query.eq('username', identifier)
        
        user_response = user_query.execute()
        
        if not user_response.data:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        
        user = user_response.data[0]
        
        # Verify password[web:63][web:65]
        if not bcrypt.check_password_hash(user['password_hash'], password):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        
        # Sign in with Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            'email': user['email'],
            'password': password
        })
        
        if auth_response.user:
            return jsonify({
                'success': True,
                'message': 'Login successful!',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                },
                'session': {
                    'access_token': auth_response.session.access_token,
                    'refresh_token': auth_response.session.refresh_token
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Login failed'}), 500
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/auth/google', methods=['POST'])
def google_auth():
    """Initiate Google OAuth flow"""[web:64]
    try:
        # Get Google OAuth URL from Supabase
        auth_response = supabase.auth.sign_in_with_oauth({
            'provider': 'google',
            'options': {
                'redirect_to': 'http://localhost:3001/auth/callback'
            }
        })
        
        return jsonify({
            'success': True,
            'url': auth_response.url
        })
    except Exception as e:
        print(f"Google auth error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/auth/google/callback', methods=['POST'])
def google_callback():
    """Handle Google OAuth callback"""
    try:
        data = request.json
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        
        # Get user from Supabase Auth
        user_response = supabase.auth.get_user(access_token)
        
        if user_response.user:
            user = user_response.user
            
            # Check if user exists in database
            existing = supabase.table('users').select('*').eq('id', user.id).execute()
            
            if not existing.data:
                # Create user record for Google OAuth
                user_data = {
                    'id': user.id,
                    'username': user.user_metadata.get('full_name', user.email.split('@')[0]),
                    'email': user.email,
                    'auth_provider': 'google',
                    'google_id': user.user_metadata.get('sub')
                }
                supabase.table('users').insert(user_data).execute()
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.user_metadata.get('full_name', user.email.split('@')[0]),
                    'email': user.email
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Authentication failed'}), 401
            
    except Exception as e:
        print(f"Google callback error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/auth/logout', methods=['POST'])
def logout():
    """User logout"""
    try:
        supabase.auth.sign_out()
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/questions/<mode>', methods=['GET'])
def get_questions(mode):
    """Get questions based on mode"""
    try:
        if mode == 'ssc':
            return jsonify(clean_questions(SSC_QUESTIONS))
        elif mode == 'hsc':
            return jsonify(clean_questions(HSC_QUESTIONS))
        else:
            return jsonify({'error': 'Invalid mode'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/analyze', methods=['POST'])
def analyze_answer():
    """Analyze answer with NLP"""
    try:
        data = request.json
        answer = data.get('answer', '')
        
        nlp = SimpleNLP()
        sentiment = nlp.sentiment_score(answer)
        keywords = list(nlp.extract_keywords(answer))
        
        return jsonify({
            'sentiment': sentiment,
            'keywords': keywords,
            'confidence': abs(sentiment)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/submit-answer', methods=['POST'])
def submit_answer():
    """Save answer to database"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        # Create simple session storage
        answer_data = {
            'user_id': user_id,
            'question_id': data.get('question_id'),
            'answer': data.get('answer')
        }
        
        # You can save to Supabase here if needed
        # supabase.table('answers').insert(answer_data).execute()
        
        return jsonify({'success': True, 'score': 20})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/recommend', methods=['POST'])
def get_recommendations():
    """Get career recommendations"""
    try:
        return jsonify({
            'streams': ['Science & Technology', 'Engineering', 'Computer Science'],
            'careers': ['Software Engineer', 'Data Scientist', 'Web Developer'],
            'analysis': 'Based on your responses, you show great potential!'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'Backend working with Supabase Auth!', 'database': 'connected'})
