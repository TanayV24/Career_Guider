from flask import Blueprint, request, jsonify, session
from flask_bcrypt import Bcrypt
from datetime import datetime
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
        print(f"📥 Login attempt with data: {data}")
        
        identifier = data.get('identifier')
        password = data.get('password')
        
        print(f"🔑 Identifier: {identifier}, Password length: {len(password) if password else 0}")
        
        if not all([identifier, password]):
            print("❌ Missing fields")
            return jsonify({'success': False, 'error': 'All fields required'}), 400
        
        # Find user by email or username
        user_query = supabase.table('users').select('*')
        if '@' in identifier:
            print(f"🔍 Searching by email: {identifier}")
            user_query = user_query.eq('email', identifier)
        else:
            print(f"🔍 Searching by username: {identifier}")
            user_query = user_query.eq('username', identifier)
        
        user_response = user_query.execute()
        print(f"👤 Users found: {len(user_response.data)}")
        
        if not user_response.data:
            print("❌ User not found")
            return jsonify({'success': False, 'error': 'Invalid login credentials'}), 401
        
        user = user_response.data[0]
        print(f"✅ User found: {user.get('username')} ({user.get('email')})")
        
        # Get password hash
        password_hash = user.get('passwordhash') or user.get('password_hash')
        print(f"🔐 Password hash exists: {bool(password_hash)}")
        
        if not password_hash:
            print("❌ No password hash found")
            return jsonify({'success': False, 'error': 'Password not set'}), 401
        
        # Verify password
        password_valid = bcrypt.check_password_hash(password_hash, password)
        print(f"🔓 Password valid: {password_valid}")
        
        if not password_valid:
            print("❌ Password mismatch")
            return jsonify({'success': False, 'error': 'Invalid login credentials'}), 401
        
        print("✅ Login successful!")
        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'fullname': user.get('fullname', ''),
                'created_at': user.get('created_at', '')
            }
        })
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


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
            return jsonify({'success': False, 'error': 'Invalid login credentials'}), 401
        
        user = user_response.data[0]
        
        # FIX: Use correct column name (passwordhash, not password_hash)
        password_hash = user.get('passwordhash') or user.get('password_hash')
        
        if not password_hash:
            return jsonify({'success': False, 'error': 'Password not set'}), 401
        
        # Verify password
        if not bcrypt.check_password_hash(password_hash, password):
            return jsonify({'success': False, 'error': 'Invalid login credentials'}), 401
        
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
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

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

# Add these new routes to your existing api.py

@bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    try:
        user_id = request.args.get('user_id')
        
        supabase = get_supabase()
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        
        if response.data:
            user = response.data[0]
            return jsonify({
                'success': True,
                'profile': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'phone': user.get('phone'),
                    'date_of_birth': user.get('date_of_birth'),
                    'gender': user.get('gender'),
                    'school_college': user.get('school_college'),
                    'city': user.get('city'),
                    'state': user.get('state'),
                    'profile_completed': user.get('profile_completed', False),
                    'created_at': user['created_at']
                }
            })
        return jsonify({'success': False, 'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/profile', methods=['POST'])
def update_profile():
    """Update user profile"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        update_data = {
            'phone': data.get('phone'),
            'date_of_birth': data.get('date_of_birth'),
            'gender': data.get('gender'),
            'school_college': data.get('school_college'),
            'city': data.get('city'),
            'state': data.get('state'),
            'profile_completed': True
        }
        
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        supabase = get_supabase()
        response = supabase.table('users').update(update_data).eq('id', user_id).execute()
        
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/quiz/start', methods=['POST'])
def start_quiz():
    """Start a new quiz session or resume existing"""
    try:
        data = request.json
        user_id = data.get('user_id')
        mode = data.get('mode')  # 'ssc' or 'hsc'
        class_level = data.get('class_level')
        
        supabase = get_supabase()
        
        # Check for incomplete session
        response = supabase.table('quiz_sessions')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('mode', mode)\
            .eq('is_completed', False)\
            .execute()
        
        if response.data:
            # Resume existing session
            session = response.data[0]
            return jsonify({
                'success': True,
                'session_id': session['id'],
                'current_question': session['current_question'],
                'total_questions': session['total_questions'],
                'is_resume': True,
                'answers': session.get('answers', [])
            })
        else:
            # Create new session
            new_session = {
                'user_id': user_id,
                'mode': mode,
                'class_level': class_level,
                'total_questions': 14,
                'current_question': 0,
                'is_completed': False,
                'answers': []
            }
            
            response = supabase.table('quiz_sessions').insert(new_session).execute()
            session_id = response.data[0]['id']
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'current_question': 0,
                'total_questions': 14,
                'is_resume': False
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/quiz/save-progress', methods=['POST'])
def save_quiz_progress():
    """Save quiz progress"""
    try:
        data = request.json
        session_id = data.get('session_id')
        current_question = data.get('current_question')
        answer = data.get('answer')
        question_id = data.get('question_id')
        
        supabase = get_supabase()
        
        # Get current session
        session_response = supabase.table('quiz_sessions')\
            .select('answers')\
            .eq('id', session_id)\
            .execute()
        
        current_answers = session_response.data[0].get('answers', [])
        
        # Add new answer
        current_answers.append({
            'question_id': question_id,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update session
        update_data = {
            'current_question': current_question,
            'answers': current_answers
        }
        
        supabase.table('quiz_sessions').update(update_data).eq('id', session_id).execute()
        
        # Also save to answers table
        answer_data = {
            'session_id': session_id,
            'user_id': data.get('user_id'),
            'question_id': question_id,
            'answer': answer
        }
        supabase.table('answers').insert(answer_data).execute()
        
        return jsonify({'success': True, 'message': 'Progress saved'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/quiz/complete', methods=['POST'])
def complete_quiz():
    """Mark quiz as completed"""
    try:
        data = request.json
        session_id = data.get('session_id')
        final_score = data.get('score', 0)
        
        supabase = get_supabase()
        
        update_data = {
            'is_completed': True,
            'completed_at': datetime.now().isoformat(),
            'score': final_score
        }
        
        supabase.table('quiz_sessions').update(update_data).eq('id', session_id).execute()
        
        return jsonify({'success': True, 'message': 'Quiz completed!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/quiz/history', methods=['GET'])
def get_quiz_history():
    """Get user's quiz history"""
    try:
        user_id = request.args.get('user_id')
        
        supabase = get_supabase()
        response = supabase.table('quiz_sessions')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .execute()
        
        history = []
        for session in response.data:
            history.append({
                'id': session['id'],
                'mode': session['mode'],
                'class_level': session.get('class_level'),
                'score': session.get('score', 0),
                'total_questions': session['total_questions'],
                'current_question': session['current_question'],
                'is_completed': session['is_completed'],
                'created_at': session['created_at'],
                'completed_at': session.get('completed_at')
            })
        
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        user_id = request.args.get('user_id')
        
        supabase = get_supabase()
        
        # Get total quizzes
        sessions = supabase.table('quiz_sessions')\
            .select('*')\
            .eq('user_id', user_id)\
            .execute()
        
        total_quizzes = len(sessions.data)
        completed_quizzes = len([s for s in sessions.data if s['is_completed']])
        incomplete_quizzes = total_quizzes - completed_quizzes
        
        # Calculate average score
        completed_sessions = [s for s in sessions.data if s['is_completed']]
        avg_score = sum(s.get('score', 0) for s in completed_sessions) / len(completed_sessions) if completed_sessions else 0
        
        return jsonify({
            'success': True,
            'stats': {
                'total_quizzes': total_quizzes,
                'completed_quizzes': completed_quizzes,
                'incomplete_quizzes': incomplete_quizzes,
                'average_score': round(avg_score, 2)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

