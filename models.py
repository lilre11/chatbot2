from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class User:
    """User model for storing user information."""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    created_at: Optional[datetime] = None
    is_active: bool = True
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert user to dictionary."""
        # Convert UTC timestamp to UTC+3 for display
        utc_plus_3_created_at = (self.created_at + timedelta(hours=3)).isoformat()
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': utc_plus_3_created_at,
            'is_active': self.is_active
        }

@dataclass
class Conversation:
    """Conversation model for storing chat sessions."""
    id: Optional[int] = None
    user_id: int = 0
    title: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True
    message_count: int = 0
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert conversation to dictionary."""
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
            'message_count': self.message_count
        }

@dataclass
class Message:
    """Message model for storing individual chat messages."""
    id: Optional[int] = None
    conversation_id: int = 0
    content: str = ""
    sender_type: str = "user"  # 'user' or 'bot'
    timestamp: Optional[datetime] = None
    token_count: int = 0
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
    
    def to_dict(self):
        """Convert message to dictionary."""
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

@dataclass
class SystemLog:
    """System log model for tracking application events."""
    id: Optional[int] = None
    level: str = "INFO"  # 'INFO', 'WARNING', 'ERROR'
    message: str = ""
    module: Optional[str] = None
    user_id: Optional[int] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
    
    def to_dict(self):
        """Convert system log to dictionary."""
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
