from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET_KEY'
    
    CORS(app, supports_credentials=True)
    bcrypt.init_app(app)
    
    from app.routes import api
    app.register_blueprint(api.bp)
    
    return app
