from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))
from supabase_client import get_supabase

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quiz/start', methods=['POST', 'OPTIONS'])
def start_quiz():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.json
        user_id = data.get('user_id')
        mode = data.get('mode', 'ssc')
        
        supabase = get_supabase()
        
        response = supabase.table('quiz_sessions')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('mode', mode)\
            .eq('is_completed', False)\
            .execute()
        
        if response.data:
            session = response.data[0]
            return jsonify({
                'success': True,
                'session_id': session['id'],
                'current_question': session.get('current_question', 0),
                'is_resume': True
            })
        else:
            return jsonify({
                'success': True,
                'session_id': None,
                'current_question': 0,
                'is_resume': False
            })
            
    except Exception as e:
        print(f"ERROR in /quiz/start: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@quiz_bp.route('/quiz/save-answer', methods=['POST', 'OPTIONS'])
def save_answer():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.json
        print(f"📩 Received data: {data}")
        
        session_id = data.get('session_id')
        question_id = str(data.get('question_id', ''))
        answer = data.get('answer', '')
        question_index = int(data.get('question_index', 0))
        
        user_id = data.get('user_id')
        mode = data.get('mode')
        class_level = data.get('class_level')
        first_two_answers = data.get('first_two_answers', {})
        
        supabase = get_supabase()
        
        # Q2 (index 1) - CREATE SESSION (WITHOUT is_saved column)
        if question_index == 1 and not session_id:
            print(f"📝 Creating session after Q2")
            first_two_answers[question_id] = answer
            
            new_session = {
                'user_id': str(user_id),
                'mode': str(mode),
                'class_level': str(class_level),
                'current_question': 2,
                'is_completed': False,
                'answers': json.dumps(first_two_answers),
                'score': 0
            }
            
            print(f"Creating session with data: {new_session}")
            
            response = supabase.table('quiz_sessions').insert(new_session).execute()
            new_session_id = response.data[0]['id']
            
            print(f"✅ Session created: {new_session_id}")
            
            return jsonify({
                'success': True,
                'session_id': new_session_id,
                'is_saved': True
            })
        
        # Q3+ - UPDATE SESSION
        if session_id and question_index >= 2:
            print(f"📝 Updating session {session_id} with answer {question_index + 1}")
            
            session_response = supabase.table('quiz_sessions')\
                .select('answers')\
                .eq('id', session_id)\
                .execute()
            
            if not session_response.data:
                return jsonify({'success': False, 'error': 'Session not found'}), 404
            
            # FIX: Handle both string and dict/list types
            answers_data = session_response.data[0].get('answers', '{}')
            if isinstance(answers_data, str):
                current_answers = json.loads(answers_data)
            elif isinstance(answers_data, (dict, list)):
                current_answers = answers_data if isinstance(answers_data, dict) else {}
            else:
                current_answers = {}
            
            current_answers[question_id] = answer
            
            update_data = {
                'current_question': question_index + 1,
                'answers': json.dumps(current_answers)
            }
            
            supabase.table('quiz_sessions').update(update_data).eq('id', session_id).execute()
            
            print(f"✅ Answer saved")
            
            return jsonify({
                'success': True,
                'is_saved': True
            })
        
        # Q1 - Just acknowledge
        print(f"✅ Q1 acknowledged")
        return jsonify({'success': True, 'is_saved': False})
        
    except Exception as e:
        print(f"❌ ERROR in /quiz/save-answer: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@quiz_bp.route('/quiz/get-session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get quiz session details by UUID"""
    try:
        supabase = get_supabase()
        
        # Query by UUID string (not int)
        response = supabase.table('quiz_sessions')\
            .select('*')\
            .eq('id', session_id)\
            .execute()
        
        if response.data and len(response.data) > 0:
            session = response.data[0]
            # Handle answers parsing
            answers_data = session.get('answers', '{}')
            if isinstance(answers_data, str):
                session['answers'] = json.loads(answers_data)
            else:
                session['answers'] = answers_data if isinstance(answers_data, dict) else {}
            
            return jsonify({
                'success': True,
                'session': session
            })
        else:
            return jsonify({'success': False, 'error': 'Session not found'}), 404
            
    except Exception as e:
        print(f"ERROR getting session: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500



@quiz_bp.route('/quiz/history', methods=['GET'])
def get_history():
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
            # Handle answers parsing
            answers_data = session.get('answers', '{}')
            if isinstance(answers_data, str):
                session['answers'] = json.loads(answers_data)
            else:
                session['answers'] = answers_data if isinstance(answers_data, dict) else {}
            history.append(session)
        
        return jsonify({
            'success': True,
            'history': history
        })
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@quiz_bp.route('/quiz/complete', methods=['POST'])
def complete_quiz():
    try:
        data = request.json
        session_id = data.get('session_id')
        
        supabase = get_supabase()
        
        supabase.table('quiz_sessions').update({
            'is_completed': True,
            'completed_at': datetime.now().isoformat()
        }).eq('id', session_id).execute()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
