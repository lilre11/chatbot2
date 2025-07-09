from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
import logging

def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize Flask extensions with error handling
    from models import db
    try:
        db.init_app(app)
        app.db_available = True
    except Exception as e:
        print(f"⚠️  Database extension initialization failed: {e}")
        app.db_available = False
    
    # Configure CORS for React frontend
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
    
    # Register blueprints
    from routes.chat_routes import chat_bp
    from routes.admin_routes import admin_bp
    
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Register main routes
    from routes.main_routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/api')
    
    # Create database tables with better error handling
    if app.db_available:
        with app.app_context():
            try:
                # Import models to ensure they are registered with SQLAlchemy
                from models import User, Conversation, Message, SystemLog
                db.create_all()
                print("✅ Database initialized successfully")
                app.db_working = True
            except Exception as e:
                print(f"⚠️  Database initialization failed: {e}")
                print("⚠️  App will run in fallback mode without database")
                app.db_working = False
    else:
        app.db_working = False
        print("⚠️  Database not available - running in AI-only mode")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
