from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

# This will be initialized by the app factory
db = SQLAlchemy()

class User(db.Model):
    """User model for storing user information."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with conversations
    conversations = db.relationship('Conversation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        # Convert UTC timestamp to UTC+3 for display
        utc_plus_3_created_at = (self.created_at + timedelta(hours=3)).isoformat()
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': utc_plus_3_created_at,
            'is_active': self.is_active
        }

class Conversation(db.Model):
    """Conversation model for storing chat sessions."""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with messages
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Conversation {self.id}: {self.title}>'
    
    def to_dict(self):
        # Convert UTC timestamps to UTC+3 for display
        utc_plus_3_created_at = (self.created_at + timedelta(hours=3)).isoformat()
        utc_plus_3_updated_at = (self.updated_at + timedelta(hours=3)).isoformat()
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'created_at': utc_plus_3_created_at,
            'updated_at': utc_plus_3_updated_at,
            'is_active': self.is_active,
            'message_count': len(self.messages)
        }

class Message(db.Model):
    """Message model for storing individual chat messages."""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sender_type = db.Column(db.String(20), nullable=False)  # 'user' or 'bot'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    token_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Message {self.id}: {self.sender_type}>'
    
    def to_dict(self):
        # Convert UTC timestamp to UTC+3 for display
        utc_plus_3_timestamp = (self.timestamp + timedelta(hours=3)).isoformat()
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'content': self.content,
            'sender_type': self.sender_type,
            'timestamp': utc_plus_3_timestamp,
            'token_count': self.token_count
        }

class SystemLog(db.Model):
    """System log model for tracking application events."""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20), nullable=False)  # 'INFO', 'WARNING', 'ERROR'
    message = db.Column(db.Text, nullable=False)
    module = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemLog {self.id}: {self.level}>'
    
    def to_dict(self):
        # Convert UTC timestamp to UTC+3 for display
        utc_plus_3_timestamp = (self.timestamp + timedelta(hours=3)).isoformat()
        return {
            'id': self.id,
            'level': self.level,
            'message': self.message,
            'module': self.module,
            'user_id': self.user_id,
            'timestamp': utc_plus_3_timestamp
        }
