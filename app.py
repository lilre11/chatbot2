from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
import logging
import pyodbc
from urllib.parse import quote_plus
import os
import warnings
from sqlalchemy.exc import SAWarning

# Suppress SQLAlchemy warnings about unrecognized SQL Server version
warnings.filterwarnings("ignore", category=SAWarning, message=".*Unrecognized server version info.*")

def setup_logging(app):
    """Configure structured logging."""
    logging.basicConfig(
        level=getattr(logging, app.config.get('LOG_LEVEL', 'INFO')),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app.logger.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO')))

def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Session configuration for development
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_DOMAIN'] = None  # Allow localhost domains
    
    # Setup logging
    setup_logging(app)
    
    # Configure CORS for React frontend
    CORS(app, 
         origins=app.config.get('CORS_ORIGINS', ['http://localhost:3000']), 
         supports_credentials=True,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Initialize SQLAlchemy database
    try:
        from models import db
        db.init_app(app)
        
        # Test database connection
        with app.app_context():
            db.create_all()
            
        app.logger.info("✅ SQLAlchemy database initialized successfully")
        app.config['DB_WORKING'] = True
        app.db_working = True
        
    except Exception as e:
        app.logger.error(f"⚠️  Database initialization failed: {e}")
        app.logger.warning("⚠️  App will run in fallback mode without database")
        app.config['DB_WORKING'] = False
        app.config['DB_AVAILABLE'] = False
        app.db_working = False
    
    # Register blueprints
    from routes.chat_routes import chat_bp
    from routes.admin_routes import admin_bp
    from routes.auth_routes import auth_bp
    
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Register main routes
    from routes.main_routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/api')
    
    # Root route
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Chatbot API is running',
            'version': '1.0.0',
            'api_base': '/api',
            'endpoints': {
                'health': '/api/health',
                'documentation': '/api/api-docs',
                'chat': '/api/chat',
                'admin': '/api/admin',
                'auth': '/api/auth'
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    # Request logging middleware
    @app.before_request
    def log_request():
        app.logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
    
    @app.after_request
    def log_response(response):
        app.logger.info(f"Response: {response.status_code} for {request.method} {request.path}")
        return response
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
