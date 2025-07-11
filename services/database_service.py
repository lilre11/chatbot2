import pyodbc
from models import User, Conversation, Message, SystemLog
from datetime import datetime
from typing import List, Optional, Dict
import logging

class DatabaseService:
    """Service class for database operations using PyODBC directly."""
    
    def __init__(self, connection_string: str):
        """Initialize database service with connection string."""
        self.connection_string = connection_string
        self.logger = logging.getLogger(__name__)
        self.db_available = False
        self._check_db_connection()
    
    def _check_db_connection(self):
        """Check if database connection is available."""
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            self.db_available = True
            self.logger.info("Database connection established successfully")
        except Exception as e:
            self.db_available = False
            self.logger.error(f"Database connection failed: {str(e)}")
    
    def _handle_db_error(self, operation: str, error: Exception):
        """Handle database errors gracefully."""
        self.logger.error(f"Database error in {operation}: {str(error)}")
        self.db_available = False
        return None

    def _get_connection(self):
        """Get database connection."""
        return pyodbc.connect(self.connection_string)

    def _fetch_one_as_dict(self, cursor):
        """Fetch one row as dictionary."""
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None

    def _fetch_all_as_dict(self, cursor):
        """Fetch all rows as list of dictionaries."""
        rows = cursor.fetchall()
        if rows:
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []

    # User operations
    def create_user(self, username: str, email: str) -> Optional[User]:
        """Create a new user."""
        if not self.db_available:
            return None
        try:
            sql = """
            INSERT INTO users (username, email, created_at, is_active)
            VALUES (?, ?, ?, ?)
            """
            created_at = datetime.utcnow()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (username, email, created_at, True))
            
            # Get the inserted ID
            cursor.execute("SELECT @@IDENTITY")
            user_id = cursor.fetchone()[0]
            
            conn.commit()
            cursor.close()
            conn.close()
            
            if user_id:
                user = User(
                    id=int(user_id),
                    username=username,
                    email=email,
                    created_at=created_at,
                    is_active=True
                )
                self.logger.info(f"Created user: {username}")
                return user
            return None
        except Exception as e:
            return self._handle_db_error("create_user", e)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        if not self.db_available:
            return None
        try:
            sql = "SELECT * FROM users WHERE id = ?"
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            
            result = self._fetch_one_as_dict(cursor)
            cursor.close()
            conn.close()
            
            if result:
                return User(
                    id=result['id'],
                    username=result['username'],
                    email=result['email'],
                    created_at=result['created_at'],
                    is_active=result['is_active']
                )
            return None
        except Exception as e:
            self.logger.error(f"Error getting user by ID: {str(e)}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        if not self.db_available:
            return None
        try:
            sql = "SELECT * FROM users WHERE username = ?"
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (username,))
            
            result = self._fetch_one_as_dict(cursor)
            cursor.close()
            conn.close()
            
            if result:
                return User(
                    id=result['id'],
                    username=result['username'],
                    email=result['email'],
                    created_at=result['created_at'],
                    is_active=result['is_active']
                )
            return None
        except Exception as e:
            self.logger.error(f"Error getting user by username: {str(e)}")
            return None
    
    # Conversation operations
    def create_conversation(self, user_id: int, title: str = None) -> Optional[Conversation]:
        """Create a new conversation."""
        if not self.db_available:
            return None
        try:
            if not title:
                title = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            sql = """
            INSERT INTO conversations (user_id, title, created_at, updated_at, is_active)
            VALUES (?, ?, ?, ?, ?)
            """
            created_at = datetime.utcnow()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, title, created_at, created_at, True))
            
            # Get the inserted ID
            cursor.execute("SELECT @@IDENTITY")
            conversation_id = cursor.fetchone()[0]
            
            conn.commit()
            cursor.close()
            conn.close()
            
            if conversation_id:
                conversation = Conversation(
                    id=int(conversation_id),
                    user_id=user_id,
                    title=title,
                    created_at=created_at,
                    updated_at=created_at,
                    is_active=True
                )
                self.logger.info(f"Created conversation for user {user_id}")
                return conversation
            return None
        except Exception as e:
            self.logger.error(f"Error creating conversation: {str(e)}")
            return None
    
    def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """Get conversation by ID."""
        if not self.db_available:
            return None
        try:
            sql = """
            SELECT c.*, COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            WHERE c.id = ?
            GROUP BY c.id, c.user_id, c.title, c.created_at, c.updated_at, c.is_active
            """
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (conversation_id,))
            
            result = self._fetch_one_as_dict(cursor)
            cursor.close()
            conn.close()
            
            if result:
                return Conversation(
                    id=result['id'],
                    user_id=result['user_id'],
                    title=result['title'],
                    created_at=result['created_at'],
                    updated_at=result['updated_at'],
                    is_active=result['is_active'],
                    message_count=result['message_count'] or 0
                )
            return None
        except Exception as e:
            self.logger.error(f"Error getting conversation: {str(e)}")
            return None
    
    def get_user_conversations(self, user_id: int, limit: int = None) -> List[Conversation]:
        """Get all user's conversations, including old ones. Unlimited if limit=None."""
        if not self.db_available:
            return []
        try:
            sql = """
            SELECT c.*, COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            WHERE c.user_id = ?
            GROUP BY c.id, c.user_id, c.title, c.created_at, c.updated_at, c.is_active
            ORDER BY c.updated_at DESC
            """
            
            if limit is not None:
                sql += f" OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY"
            
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            
            results = self._fetch_all_as_dict(cursor)
            cursor.close()
            conn.close()
            
            conversations = []
            for result in results:
                conversation = Conversation(
                    id=result['id'],
                    user_id=result['user_id'],
                    title=result['title'],
                    created_at=result['created_at'],
                    updated_at=result['updated_at'],
                    is_active=result['is_active'],
                    message_count=result['message_count'] or 0
                )
                conversations.append(conversation)
            
            self.logger.info(f"get_user_conversations: user_id={user_id}, count={len(conversations)}, titles={[c.title for c in conversations]}")
            return conversations
        except Exception as e:
            self.logger.error(f"Error getting user conversations: {str(e)}")
            return []
    
    def update_conversation_title(self, conversation_id: int, title: str) -> bool:
        """Update conversation title."""
        if not self.db_available:
            return False
        try:
            sql = """
            UPDATE conversations 
            SET title = ?, updated_at = ? 
            WHERE id = ?
            """
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (title, datetime.utcnow(), conversation_id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            return rows_affected > 0
        except Exception as e:
            self.logger.error(f"Error updating conversation title: {str(e)}")
            return False
    
    # Message operations
    def add_message(self, conversation_id: int, content: str, sender_type: str, token_count: int = 0) -> Optional[Message]:
        """Add a message to a conversation."""
        if not self.db_available:
            return None
        try:
            # Insert message
            sql = """
            INSERT INTO messages (conversation_id, content, sender_type, timestamp, token_count)
            VALUES (?, ?, ?, ?, ?)
            """
            timestamp = datetime.utcnow()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (conversation_id, content, sender_type, timestamp, token_count))
            
            # Get the inserted ID
            cursor.execute("SELECT @@IDENTITY")
            message_id = cursor.fetchone()[0]
            
            # Update conversation timestamp
            cursor.execute(
                "UPDATE conversations SET updated_at = ? WHERE id = ?",
                (timestamp, conversation_id)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            if message_id:
                return Message(
                    id=int(message_id),
                    conversation_id=conversation_id,
                    content=content,
                    sender_type=sender_type,
                    timestamp=timestamp,
                    token_count=token_count
                )
            return None
        except Exception as e:
            self.logger.error(f"Error adding message: {str(e)}")
            return None
    
    def get_conversation_messages(self, conversation_id: int, limit: int = 50) -> List[Message]:
        """Get messages for a conversation."""
        if not self.db_available:
            return []
        try:
            sql = """
            SELECT TOP (?) * FROM messages 
            WHERE conversation_id = ? 
            ORDER BY timestamp ASC
            """
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (limit, conversation_id))
            
            results = self._fetch_all_as_dict(cursor)
            cursor.close()
            conn.close()
            
            messages = []
            for result in results:
                message = Message(
                    id=result['id'],
                    conversation_id=result['conversation_id'],
                    content=result['content'],
                    sender_type=result['sender_type'],
                    timestamp=result['timestamp'],
                    token_count=result['token_count']
                )
                messages.append(message)
            
            return messages
        except Exception as e:
            self.logger.error(f"Error getting conversation messages: {str(e)}")
            return []
    
    def get_conversation_history(self, conversation_id: int, limit: int = 10) -> List[Dict]:
        """Get formatted conversation history for AI context."""
        if not self.db_available:
            return []
        try:
            sql = """
            SELECT TOP (?) * FROM messages 
            WHERE conversation_id = ? 
            ORDER BY timestamp DESC
            """
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (limit, conversation_id))
            
            results = self._fetch_all_as_dict(cursor)
            cursor.close()
            conn.close()
            
            # Reverse to get chronological order
            messages = []
            for result in reversed(results):
                message = Message(
                    id=result['id'],
                    conversation_id=result['conversation_id'],
                    content=result['content'],
                    sender_type=result['sender_type'],
                    timestamp=result['timestamp'],
                    token_count=result['token_count']
                )
                messages.append(message.to_dict())
            
            return messages
        except Exception as e:
            self.logger.error(f"Error getting conversation history: {str(e)}")
            return []
    
    # System log operations
    def log_system_event(self, level: str, message: str, module: str = None, user_id: int = None) -> bool:
        """Log a system event."""
        if not self.db_available:
            return False
        try:
            sql = """
            INSERT INTO system_logs (level, message, module, user_id, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (level, message, module, user_id, datetime.utcnow()))
            
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            return rows_affected > 0
        except Exception as e:
            self.logger.error(f"Error logging system event: {str(e)}")
            return False
    
    def get_system_logs(self, level: str = None, limit: int = 100) -> List[SystemLog]:
        """Get system logs."""
        if not self.db_available:
            return []
        try:
            if level:
                sql = """
                SELECT TOP (?) * FROM system_logs 
                WHERE level = ? 
                ORDER BY timestamp DESC
                """
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute(sql, (limit, level))
            else:
                sql = """
                SELECT TOP (?) * FROM system_logs 
                ORDER BY timestamp DESC
                """
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute(sql, (limit,))
            
            results = self._fetch_all_as_dict(cursor)
            cursor.close()
            conn.close()
            
            logs = []
            for result in results:
                log = SystemLog(
                    id=result['id'],
                    level=result['level'],
                    message=result['message'],
                    module=result['module'],
                    user_id=result['user_id'],
                    timestamp=result['timestamp']
                )
                logs.append(log)
            
            return logs
        except Exception as e:
            self.logger.error(f"Error getting system logs: {str(e)}")
            return []
    
    # Database maintenance
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            self._check_db_connection()
            return self.db_available
        except Exception as e:
            self.logger.error(f"Database connection test failed: {str(e)}")
            return False

    def create_tables(self) -> bool:
        """Create database tables if they don't exist."""
        if not self.db_available:
            return False
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
            CREATE TABLE users (
                id INT IDENTITY(1,1) PRIMARY KEY,
                username NVARCHAR(80) UNIQUE NOT NULL,
                email NVARCHAR(120) UNIQUE NOT NULL,
                created_at DATETIME NOT NULL,
                is_active BIT DEFAULT 1
            )
            """)
            
            # Create conversations table
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='conversations' AND xtype='U')
            CREATE TABLE conversations (
                id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT NOT NULL,
                title NVARCHAR(200),
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                is_active BIT DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)
            
            # Create messages table
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='messages' AND xtype='U')
            CREATE TABLE messages (
                id INT IDENTITY(1,1) PRIMARY KEY,
                conversation_id INT NOT NULL,
                content NTEXT NOT NULL,
                sender_type NVARCHAR(20) NOT NULL,
                timestamp DATETIME NOT NULL,
                token_count INT DEFAULT 0,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
            """)
            
            # Create system_logs table
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='system_logs' AND xtype='U')
            CREATE TABLE system_logs (
                id INT IDENTITY(1,1) PRIMARY KEY,
                level NVARCHAR(20) NOT NULL,
                message NTEXT NOT NULL,
                module NVARCHAR(100),
                user_id INT,
                timestamp DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            self.logger.info("Database tables created successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error creating tables: {str(e)}")
            return False
