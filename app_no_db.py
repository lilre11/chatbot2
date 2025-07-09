from flask import Flask
from flask_cors import CORS
from config import Config

def create_app(skip_db=False):
    """Application factory pattern with optional database skip."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS for React frontend
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
    
    if not skip_db:
        # Initialize Flask extensions
        from models import db
        db.init_app(app)
        
        # Create database tables
        with app.app_context():
            try:
                # Import models to ensure they are registered with SQLAlchemy
                from models import User, Conversation, Message, SystemLog
                db.create_all()
                print("✅ Database initialized successfully")
            except Exception as e:
                print(f"⚠️  Database initialization failed: {e}")
                print("⚠️  Running without database - some features may not work")
    
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
    import sys
    skip_db = '--skip-db' in sys.argv
    
    if skip_db:
        print("🔧 Starting Flask app without database connection...")
    
    app = create_app(skip_db=skip_db)
    app.run(debug=True, host='0.0.0.0', port=5000)
