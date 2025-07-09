from models import User, Conversation, Message, SystemLog, db
from datetime import datetime
from typing import List, Optional, Dict
import logging

class DatabaseService:
    """Service class for database operations."""
    
    def __init__(self):
        """Initialize database service."""
        self.logger = logging.getLogger(__name__)
        self._check_db_connection()
    
    def _check_db_connection(self):
        """Check if database connection is available."""
        try:
            from flask import current_app
            self.db_available = getattr(current_app, 'db_working', False)
        except:
            self.db_available = False
    
    def _handle_db_error(self, operation: str, error: Exception):
        """Handle database errors gracefully."""
        self.logger.error(f"Database error in {operation}: {str(error)}")
        self.db_available = False
        return None

    # User operations
    def create_user(self, username: str, email: str) -> Optional[User]:
        """Create a new user."""
        if not self.db_available:
            return None
        try:
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            self.logger.info(f"Created user: {username}")
            return user
        except Exception as e:
            db.session.rollback()
            return self._handle_db_error("create_user", e)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        try:
            return User.query.get(user_id)
        except Exception as e:
            self.logger.error(f"Error getting user by ID: {str(e)}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        try:
            return User.query.filter_by(username=username).first()
        except Exception as e:
            self.logger.error(f"Error getting user by username: {str(e)}")
            return None
    
    # Conversation operations
    def create_conversation(self, user_id: int, title: str = None) -> Optional[Conversation]:
        """Create a new conversation."""
        try:
            conversation = Conversation(
                user_id=user_id,
                title=title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            db.session.add(conversation)
            db.session.commit()
            self.logger.info(f"Created conversation for user {user_id}")
            return conversation
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error creating conversation: {str(e)}")
            return None
    
    def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """Get conversation by ID."""
        try:
            return Conversation.query.get(conversation_id)
        except Exception as e:
            self.logger.error(f"Error getting conversation: {str(e)}")
            return None
    
    def get_user_conversations(self, user_id: int, limit: int = 20) -> List[Conversation]:
        """Get user's conversations."""
        try:
            return Conversation.query.filter_by(
                user_id=user_id, 
                is_active=True
            ).order_by(Conversation.updated_at.desc()).limit(limit).all()
        except Exception as e:
            self.logger.error(f"Error getting user conversations: {str(e)}")
            return []
    
    def update_conversation_title(self, conversation_id: int, title: str) -> bool:
        """Update conversation title."""
        try:
            conversation = Conversation.query.get(conversation_id)
            if conversation:
                conversation.title = title
                conversation.updated_at = datetime.utcnow()
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error updating conversation title: {str(e)}")
            return False
    
    # Message operations
    def add_message(self, conversation_id: int, content: str, sender_type: str, token_count: int = 0) -> Optional[Message]:
        """Add a message to a conversation."""
        try:
            message = Message(
                conversation_id=conversation_id,
                content=content,
                sender_type=sender_type,
                token_count=token_count
            )
            db.session.add(message)
            
            # Update conversation timestamp
            conversation = Conversation.query.get(conversation_id)
            if conversation:
                conversation.updated_at = datetime.utcnow()
            
            db.session.commit()
            return message
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error adding message: {str(e)}")
            return None
    
    def get_conversation_messages(self, conversation_id: int, limit: int = 50) -> List[Message]:
        """Get messages for a conversation."""
        try:
            return Message.query.filter_by(
                conversation_id=conversation_id
            ).order_by(Message.timestamp.asc()).limit(limit).all()
        except Exception as e:
            self.logger.error(f"Error getting conversation messages: {str(e)}")
            return []
    
    def get_conversation_history(self, conversation_id: int, limit: int = 10) -> List[Dict]:
        """Get formatted conversation history for AI context."""
        try:
            messages = Message.query.filter_by(
                conversation_id=conversation_id
            ).order_by(Message.timestamp.desc()).limit(limit).all()
            
            # Reverse to get chronological order
            messages.reverse()
            
            return [msg.to_dict() for msg in messages]
        except Exception as e:
            self.logger.error(f"Error getting conversation history: {str(e)}")
            return []
    
    # System log operations
    def log_system_event(self, level: str, message: str, module: str = None, user_id: int = None) -> bool:
        """Log a system event."""
        try:
            log_entry = SystemLog(
                level=level,
                message=message,
                module=module,
                user_id=user_id
            )
            db.session.add(log_entry)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error logging system event: {str(e)}")
            return False
    
    def get_system_logs(self, level: str = None, limit: int = 100) -> List[SystemLog]:
        """Get system logs."""
        try:
            query = SystemLog.query
            if level:
                query = query.filter_by(level=level)
            return query.order_by(SystemLog.timestamp.desc()).limit(limit).all()
        except Exception as e:
            self.logger.error(f"Error getting system logs: {str(e)}")
            return []
    
    # Database maintenance
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            # Use the existing _check_db_connection method which is more reliable
            self._check_db_connection()
            return self.db_available
        except Exception as e:
            self.logger.error(f"Database connection test failed: {str(e)}")
            return False
