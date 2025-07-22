from flask import Flask
from flask_cors import CORS
from config import Config

def create_simple_app():
    """Simple Flask app for testing without database."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS for React frontend
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
    
    # Register simplified chat routes
    from routes.chat_simple_routes import chat_simple_bp
    app.register_blueprint(chat_simple_bp, url_prefix='/api/chat')
    
    # Register main routes
    from routes.main_routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    print("🚀 Starting simplified Flask app (no database)...")
    app = create_simple_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
