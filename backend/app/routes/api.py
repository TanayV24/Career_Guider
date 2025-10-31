from flask import Blueprint, request, jsonify
import sys
import os

# Add services to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))

from nlp_engine import SimpleNLP
from question_bank import SSC_QUESTIONS, HSC_QUESTIONS, MOTIVATIONAL_QUOTES
from stream_analyzer import StreamAnalyzer

bp = Blueprint('api', __name__, url_prefix='/api')

# Global storage
sessions = {}

# Convert questions to JSON-safe format (remove lambda functions)
def clean_questions(questions):
    """Remove lambda functions and make questions JSON-serializable"""
    cleaned = []
    for q in questions:
        clean_q = {
            'id': q.get('id'),
            'text': q.get('text'),
            'type': q.get('type'),
        }
        # Add options if they exist
        if 'options' in q:
            clean_q['options'] = q['options']
        
        cleaned.append(clean_q)
    return cleaned

@bp.route('/login', methods=['POST'])
def login():
    """Handle user login/registration"""
    try:
        data = request.json
        user_id = data.get('email', 'user_' + str(len(sessions)))
        
        sessions[user_id] = {
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone', ''),
            'school': data.get('school', ''),
            'answers': [],
            'score': 0
        }
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': f"Welcome, {data.get('name')}!"
        })
    except Exception as e:
        print(f"Login error: {e}")  # Debug print
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/questions/<mode>', methods=['GET'])
def get_questions(mode):
    """Get questions based on mode (ssc/hsc)"""
    try:
        if mode == 'ssc':
            questions = clean_questions(SSC_QUESTIONS)
            return jsonify(questions)
        elif mode == 'hsc':
            questions = clean_questions(HSC_QUESTIONS)
            return jsonify(questions)
        else:
            return jsonify({'error': 'Invalid mode. Use ssc or hsc'}), 400
    except Exception as e:
        print(f"Questions error: {e}")  # Debug print
        return jsonify({'error': str(e)}), 500

@bp.route('/analyze', methods=['POST'])
def analyze_answer():
    """Analyze user's answer using NLP"""
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
        print(f"Analyze error: {e}")  # Debug print
        return jsonify({'error': str(e)}), 500

@bp.route('/submit-answer', methods=['POST'])
def submit_answer():
    """Save user's answer"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if user_id in sessions:
            sessions[user_id]['answers'].append({
                'question_id': data.get('question_id'),
                'answer': data.get('answer')
            })
            sessions[user_id]['score'] += 20
            
            return jsonify({
                'success': True,
                'score': sessions[user_id]['score']
            })
        
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        print(f"Submit answer error: {e}")  # Debug print
        return jsonify({'error': str(e)}), 500

@bp.route('/recommend', methods=['POST'])
def get_recommendations():
    """Get career recommendations"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if user_id not in sessions:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = sessions[user_id]
        
        # Simple recommendation logic
        recommendations = {
            'streams': ['Science & Technology', 'Engineering', 'Computer Science'],
            'careers': ['Software Engineer', 'Data Scientist', 'AI Researcher', 'Product Manager'],
            'analysis': f'Based on your {len(user_data["answers"])} responses, you show strong analytical and problem-solving abilities. Your interests align well with technology and innovation fields. Consider exploring careers in STEM where you can combine creativity with technical skills!'
        }
        
        return jsonify(recommendations)
    except Exception as e:
        print(f"Recommend error: {e}")  # Debug print
        return jsonify({'error': str(e)}), 500

# Test endpoint to check if backend is running
@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'Backend is running!', 'port': 5050})
