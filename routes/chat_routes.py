from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime, timedelta
import uuid
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.gemini_service import GeminiService
import logging

# Initialize blueprint
chat_bp = Blueprint('chat', __name__)

# Initialize services
gemini_service = GeminiService()
logger = logging.getLogger(__name__)

def get_db_service():
    """Get database service from app context."""
    try:
        return current_app.db_service
    except:
        return None

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
        db_working = getattr(current_app, 'db_working', False)
        db_service = get_db_service()
        
        # Also check if database service is available
        if db_working and db_service:
            try:
                # Test database connection
                if not db_service.test_connection():
                    db_working = False
            except:
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
            # Get or create user session
            user_id = session.get('user_id')
            if not user_id:
                # Create a guest user for this session
                session_id = session.get('session_id') or str(uuid.uuid4())
                session['session_id'] = session_id
                
                user = db_service.create_user(f"guest_{session_id[:8]}", f"guest_{session_id[:8]}@chatbot.local")
                if user:
                    user_id = user.id
                    session['user_id'] = user_id
                else:
                    raise Exception('Failed to create user session')
            
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
            # Database operation failed, fall back to AI-only mode
            logger.warning(f"Database operation failed, using fallback: {str(db_error)}")
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
            return jsonify({'conversations': []})
        
        db_service = get_db_service()
        if not db_service or not db_service.db_available:
            return jsonify({'conversations': []})
        
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
        
        db_service = get_db_service()
        if not db_service or not db_service.db_available:
            return jsonify({'error': 'Database unavailable'}), 503
        
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
        
        db_service = get_db_service()
        if not db_service or not db_service.db_available:
            return jsonify({'error': 'Database unavailable'}), 503
        
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
        
        db_service = get_db_service()
        if not db_service or not db_service.db_available:
            return jsonify({'error': 'Database unavailable'}), 503
        
        conversation = db_service.create_conversation(user_id, title)
        if not conversation:
            return jsonify({'error': 'Failed to create conversation'}), 500
        
        return jsonify({
            'conversation': conversation.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error in new_conversation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


