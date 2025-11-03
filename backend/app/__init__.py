from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # CORS Configuration - Allow frontend to access backend
    allowed_origins = [
        'http://localhost:3001',
        'http://localhost:3000',
        'https://career-guider-amber.vercel.app',  # ✅ Your Vercel frontend
        'https://*.vercel.app',
        'https://career-guider-api.onrender.com'  # ✅ ADD THIS - Your Render backend
    ]
    
    CORS(app,
         resources={r"/api/*": {
             "origins": allowed_origins,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True,
             "expose_headers": ["Content-Type", "Authorization"]
         }})
    
    # Import and register routes
    from app.routes.api import bp as api_bp
    from app.routes.quiz_routes import quiz_bp  # ← YOU ALREADY HAVE THIS
    
    app.register_blueprint(api_bp)
    app.register_blueprint(quiz_bp, url_prefix='/api')  # ← ADD THIS LINE!
    
    # Health check route
    @app.route('/')
    def index():
        return {'status': 'Career Guider API is running!', 'version': '1.0'}
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app

