from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
import uuid
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.gemini_service import GeminiService
from services.database_service import DatabaseService
import logging

# Initialize blueprint
chat_bp = Blueprint('chat', __name__)

# Initialize services
gemini_service = GeminiService()
db_service = DatabaseService()
logger = logging.getLogger(__name__)

@chat_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        logger.info(f"Registration attempt with data: {data}")
        
        if not data or 'username' not in data or 'password' not in data:
            logger.error("Missing username or password in registration data")
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        if not username or not password:
            logger.error("Empty username or password provided")
            return jsonify({'error': 'Username and password cannot be empty'}), 400
        
        logger.info(f"Checking if user exists with username: {username}")
        # Check if user already exists
        existing_user = db_service.get_user_by_username(username)
        if existing_user:
            logger.error(f"User already exists with username: {username}")
            return jsonify({'error': 'User with this username already exists'}), 400
        
        logger.info(f"Creating new user with username: {username}")
        # Create new user
        user = db_service.create_user(username, password)
        if not user:
            logger.error(f"Failed to create user with username: {username}")
            return jsonify({'error': 'Failed to create user'}), 500
        
        # Set session
        session['user_id'] = user.id
        session['username'] = user.username
        logger.info(f"User {user.username} registered successfully")
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username
            }
        })
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Registration failed'}), 500

@chat_bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    try:
        logger.info(f"Login attempt - Session before: {dict(session)}")
        data = request.get_json()
        logger.info(f"Login request data: {data}")
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        if not username or not password:
            return jsonify({'error': 'Username and password cannot be empty'}), 400
        
        # Authenticate user
        user = db_service.authenticate_user(username, password)
        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Set session
        session['user_id'] = user.id
        session['username'] = user.username
        logger.info(f"Login successful - Session after: {dict(session)}")
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username
            }
        })
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@chat_bp.route('/logout', methods=['POST'])
def logout():
    """Logout a user."""
    try:
        session.clear()
        return jsonify({'message': 'Logout successful'})
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500

@chat_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current logged-in user."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Not logged in'}), 401
        
        user = db_service.get_user_by_id(user_id)
        if not user:
            session.clear()
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username
            }
        })
        
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        return jsonify({'error': 'Failed to get user info'}), 500

@chat_bp.route('/send', methods=['POST'])
def send_message():
    """Handle sending a message to the chatbot."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Check if database is available
        from flask import current_app
        db_working = getattr(current_app, 'db_working', False)
        
        # Also check if database service is available
        if db_working:
            try:
                # Test database connection
                db_service._check_db_connection()
                if not db_service.db_available:
                    db_working = False
            except Exception as e:
                db_working = False
        
        if not db_working:
            # Fallback mode: AI-only response without database
            try:
                ai_response = gemini_service.generate_response(user_message, [])
                return jsonify({
                    'response': ai_response,
                    'conversation_id': str(uuid.uuid4()),
                    'message_id': str(uuid.uuid4()),
                    'timestamp': (datetime.utcnow() + timedelta(hours=3)).isoformat(),
                    'mode': 'fallback'
                })
            except Exception as e:
                logger.error(f"Fallback mode failed: {str(e)}")
                return jsonify({'error': 'AI service unavailable'}), 500
        
        # Normal mode with database
        try:
            # Check if user is logged in
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Authentication required. Please login first.'}), 401
            
            # Get or create conversation
            conversation_id = data.get('conversation_id')
            
            if not conversation_id:
                conversation = db_service.create_conversation(user_id)
                if not conversation:
                    raise Exception('Failed to create conversation')
                conversation_id = conversation.id
            
            # Save user message
            user_msg = db_service.add_message(conversation_id, user_message, 'user')
            if not user_msg:
                raise Exception('Failed to save user message')
            
            # Get conversation history for context
            conversation_history = db_service.get_conversation_history(conversation_id)
            
            # Generate AI response
            ai_response = gemini_service.generate_response(user_message, conversation_history)
            
            # Save AI response
            token_count = gemini_service.count_tokens(ai_response)
            ai_msg = db_service.add_message(conversation_id, ai_response, 'bot', token_count)
            
            if not ai_msg:
                raise Exception('Failed to save AI response')
            
            # Log the interaction
            db_service.log_system_event('INFO', f'Chat interaction completed', 'chat_routes', user_id)
            
            # Get UTC+3 timestamp for response
            utc_plus_3_timestamp = (datetime.utcnow() + timedelta(hours=3)).isoformat()
            
            return jsonify({
                'response': ai_response,
                'conversation_id': conversation_id,
                'message_id': ai_msg.id,
                'timestamp': utc_plus_3_timestamp
            })
            
        except Exception as db_error:
            logger.error(f"Database operation failed: {str(db_error)}")
            # Database operation failed, fall back to AI-only mode
            try:
                ai_response = gemini_service.generate_response(user_message, [])
                return jsonify({
                    'response': ai_response,
                    'conversation_id': str(uuid.uuid4()),
                    'message_id': str(uuid.uuid4()),
                    'timestamp': (datetime.utcnow() + timedelta(hours=3)).isoformat(),
                    'mode': 'fallback',
                    'warning': 'Database unavailable - using AI-only mode'
                })
            except Exception as ai_error:
                logger.error(f"Both database and AI failed: {str(ai_error)}")
                return jsonify({'error': 'Service temporarily unavailable'}), 500
    
    except Exception as e:
        # Final fallback for any unexpected errors
        logger.error(f"Unexpected error in send_message: {str(e)}")
        try:
            ai_response = gemini_service.generate_response(user_message, [])
            return jsonify({
                'response': ai_response,
                'conversation_id': str(uuid.uuid4()),
                'message_id': str(uuid.uuid4()),
                'timestamp': (datetime.utcnow() + timedelta(hours=3)).isoformat(),
                'mode': 'emergency_fallback'
            })
        except:
            return jsonify({'error': 'Service temporarily unavailable'}), 500

@chat_bp.route('/conversations', methods=['GET'])
def get_conversations():
    """Get user's conversations."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required. Please login first.'}), 401
        
        conversations = db_service.get_user_conversations(user_id)
        
        return jsonify({
            'conversations': [conv.to_dict() for conv in conversations]
        })
        
    except Exception as e:
        logger.error(f"Error in get_conversations: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    """Get messages for a specific conversation."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User session required'}), 401
        
        # Verify conversation belongs to user
        conversation = db_service.get_conversation(conversation_id)
        if not conversation or conversation.user_id != user_id:
            return jsonify({'error': 'Conversation not found'}), 404
        
        messages = db_service.get_conversation_messages(conversation_id)
        
        return jsonify({
            'messages': [msg.to_dict() for msg in messages],
            'conversation': conversation.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error in get_conversation_messages: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@chat_bp.route('/conversations/<int:conversation_id>', methods=['PUT'])
def update_conversation(conversation_id):
    """Update conversation details."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User session required'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request data required'}), 400
        
        # Verify conversation belongs to user
        conversation = db_service.get_conversation(conversation_id)
        if not conversation or conversation.user_id != user_id:
            return jsonify({'error': 'Conversation not found'}), 404
        
        # Update title if provided
        if 'title' in data:
            success = db_service.update_conversation_title(conversation_id, data['title'])
            if not success:
                return jsonify({'error': 'Failed to update conversation'}), 500
        
        # Get updated conversation
        updated_conversation = db_service.get_conversation(conversation_id)
        
        return jsonify({
            'conversation': updated_conversation.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error in update_conversation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@chat_bp.route('/new-conversation', methods=['POST'])
def new_conversation():
    """Create a new conversation."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User session required'}), 401
        
        data = request.get_json() or {}
        title = data.get('title')
        
        conversation = db_service.create_conversation(user_id, title)
        if not conversation:
            return jsonify({'error': 'Failed to create conversation'}), 500
        
        return jsonify({
            'conversation': conversation.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error in new_conversation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@chat_bp.route('/debug/session', methods=['GET'])
def debug_session():
    """Debug endpoint to check session information."""
    return jsonify({
        'session_data': dict(session),
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'has_session': len(session) > 0
    })


