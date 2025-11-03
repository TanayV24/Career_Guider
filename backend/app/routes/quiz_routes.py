from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import sys
import os

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))
from supabase_client import get_supabase

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quiz/start', methods=['POST'])
def start_quiz():
    """Start a new quiz session"""
    try:
        data = request.json
        user_id = data.get('user_id')
        mode = data.get('mode', 'ssc')
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
                'is_resume': True,
                'message': 'Resuming quiz session'
            })
        else:
            # Create new session
            new_session = {
                'user_id': user_id,
                'mode': mode,
                'class_level': class_level,
                'current_question': 0,
                'is_saved': False,
                'is_completed': False,
                'answers': json.dumps({}),
                'score': 0
            }
            
            response = supabase.table('quiz_sessions').insert(new_session).execute()
            session_id = response.data[0]['id']
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'current_question': 0,
                'is_resume': False,
                'message': 'Quiz session started'
            })
            
    except Exception as e:
        print(f"Error starting quiz: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@quiz_bp.route('/quiz/save-answer', methods=['POST'])
def save_answer():
    """Save answer and progress"""
    try:
        data = request.json
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        answer = data.get('answer')
        question_index = data.get('question_index', 0)
        
        supabase = get_supabase()
        
        # Get current session
        session_response = supabase.table('quiz_sessions')\
            .select('answers')\
            .eq('id', session_id)\
            .execute()
        
        if not session_response.data:
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        # Parse existing answers
        current_answers_str = session_response.data[0].get('answers', '{}')
        current_answers = json.loads(current_answers_str) if current_answers_str else {}
        
        # Add new answer
        current_answers[question_id] = answer
        
        # Mark as saved after 2 questions (name + age)
        is_saved = len(current_answers) >= 2
        
        # Update session
        update_data = {
            'current_question': question_index + 1,
            'answers': json.dumps(current_answers),
            'is_saved': is_saved
        }
        
        supabase.table('quiz_sessions').update(update_data).eq('id', session_id).execute()
        
        return jsonify({
            'success': True,
            'message': 'Answer saved',
            'is_saved': is_saved
        })
        
    except Exception as e:
        print(f"Error saving answer: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@quiz_bp.route('/quiz/get-session/<int:session_id>', methods=['GET'])
def get_session(session_id):
    """Get quiz session details"""
    try:
        supabase = get_supabase()
        
        response = supabase.table('quiz_sessions')\
            .select('*')\
            .eq('id', session_id)\
            .execute()
        
        if response.data:
            session = response.data[0]
            # Parse answers from JSON string
            session['answers'] = json.loads(session['answers']) if session['answers'] else {}
            
            return jsonify({
                'success': True,
                'session': session
            })
        else:
            return jsonify({'success': False, 'error': 'Session not found'}), 404
            
    except Exception as e:
        print(f"Error getting session: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@quiz_bp.route('/quiz/history', methods=['GET'])
def get_history():
    """Get user's quiz history (only saved sessions)"""
    try:
        user_id = request.args.get('user_id')
        supabase = get_supabase()
        
        response = supabase.table('quiz_sessions')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('is_saved', True)\
            .order('created_at', desc=True)\
            .execute()
        
        history = []
        for session in response.data:
            session['answers'] = json.loads(session['answers']) if session['answers'] else {}
            history.append(session)
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        })
        
    except Exception as e:
        print(f"Error getting history: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@quiz_bp.route('/quiz/complete', methods=['POST'])
def complete_quiz():
    """Mark quiz as completed"""
    try:
        data = request.json
        session_id = data.get('session_id')
        score = data.get('score', 0)
        
        supabase = get_supabase()
        
        update_data = {
            'is_completed': True,
            'completed_at': datetime.now().isoformat(),
            'score': score
        }
        
        supabase.table('quiz_sessions').update(update_data).eq('id', session_id).execute()
        
        return jsonify({
            'success': True,
            'message': 'Quiz completed'
        })
        
    except Exception as e:
        print(f"Error completing quiz: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
