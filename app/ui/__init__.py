"""
Flask Application Factory
"""
from flask import Flask
import os

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
    app.config['DEBUG'] = app.config['ENV'] == 'development'
    
    # Register routes
    from app.ui import routes
    app.register_blueprint(routes.bp)
    
    return app
