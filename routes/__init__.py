# Routes package
from .main_routes import main_bp
from .chat_routes import chat_bp
from .admin_routes import admin_bp

__all__ = ['main_bp', 'chat_bp', 'admin_bp']
