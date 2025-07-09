from flask import Blueprint, request, jsonify, session
from services.gemini_service import GeminiService
import logging
import uuid

# Initialize blueprint
chat_simple_bp = Blueprint('chat_simple', __name__)

# Initialize services
gemini_service = GeminiService()
logger = logging.getLogger(__name__)

@chat_simple_bp.route('/send', methods=['POST'])
def send_message_simple():
    """Handle sending a message to the chatbot (simplified, no database)."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Generate a simple session ID for this request
        conversation_id = data.get('conversation_id') or str(uuid.uuid4())
        
        # Generate AI response directly (no database save)
        logger.info(f"Processing message: {user_message[:50]}...")
        ai_response = gemini_service.generate_response(user_message, [])
        
        return jsonify({
            'response': ai_response,
            'conversation_id': conversation_id,
            'message_id': str(uuid.uuid4()),
            'timestamp': '2025-01-07T12:00:00'
        })
        
    except Exception as e:
        logger.error(f"Error in send_message_simple: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@chat_simple_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check."""
    return jsonify({'status': 'healthy', 'service': 'chat_simple'})
