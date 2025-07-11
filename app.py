from flask import Flask
from flask_cors import CORS
from config import Config
import logging
import pyodbc
from urllib.parse import quote_plus

def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize SQLAlchemy database
    try:
        from models import db
        db.init_app(app)
        
        # Test database connection
        with app.app_context():
            db.create_all()
            
        print("✅ SQLAlchemy database initialized successfully")
        app.db_working = True
        
    except Exception as e:
        print(f"⚠️  Database initialization failed: {e}")
        print("⚠️  App will run in fallback mode without database")
        app.db_working = False
        app.db_working = False
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
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
