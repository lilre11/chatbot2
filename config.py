import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Flask application."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database configuration for PyDapper
    DB_HOST = os.environ.get('DB_HOST', '192.168.1.137')
    DB_PORT = os.environ.get('DB_PORT', '1433')
    DB_NAME = os.environ.get('DB_NAME', 'chatbot_db')
    DB_USER = os.environ.get('DB_USER', 'sa')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_DRIVER = os.environ.get('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    # Gemini AI configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # Chat configuration
    MAX_CONVERSATION_HISTORY = 10
    DEFAULT_RESPONSE = "I'm sorry, I couldn't process your request at the moment. Please try again."
