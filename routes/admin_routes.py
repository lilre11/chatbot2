from flask import Blueprint, request, jsonify, current_app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.gemini_service import GeminiService
import logging

# Initialize blueprint
admin_bp = Blueprint('admin', __name__)

# Initialize services
gemini_service = GeminiService()
logger = logging.getLogger(__name__)

def get_db_service():
    """Get database service from app context."""
    try:
        return current_app.db_service
    except:
        return None

@admin_bp.route('/status', methods=['GET'])
def system_status():
    """Get system status information."""
    try:
        # Check database connection
        db_service = get_db_service()
        db_status = db_service.test_connection() if db_service else False
        
        # Check Gemini API status
        try:
            ai_status = gemini_service.check_api_status()
        except Exception as ai_error:
            logger.error(f"AI service check failed: {str(ai_error)}")
            ai_status = False
        
        return jsonify({
            'database': {
                'status': 'connected' if db_status else 'disconnected',
                'healthy': db_status,
                'available': db_service.db_available if db_service else False
            },
            'ai_service': {
                'status': 'connected' if ai_status else 'disconnected',
                'healthy': ai_status
            },
            'overall_status': 'healthy' if (db_status and ai_status) else 'degraded'
        })
        
    except Exception as e:
        logger.error(f"Error in system_status: {str(e)}")
        return jsonify({
            'database': {'status': 'error', 'healthy': False, 'available': False},
            'ai_service': {'status': 'error', 'healthy': False},
            'overall_status': 'error',
            'error': str(e)
        }), 500

@admin_bp.route('/logs', methods=['GET'])
def get_logs():
    """Get system logs."""
    try:
        # Check if database is available first
        db_service = get_db_service()
        if not db_service or not db_service.test_connection():
            return jsonify({
                'error': 'Database unavailable',
                'logs': [],
                'count': 0,
                'database_status': 'disconnected'
            })
        
        level = request.args.get('level')
        limit = int(request.args.get('limit', 100))
        
        logs = db_service.get_system_logs(level, limit)
        
        return jsonify({
            'logs': [log.to_dict() for log in logs],
            'count': len(logs),
            'database_status': 'connected'
        })
        
    except Exception as e:
        logger.error(f"Error in get_logs: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'logs': [],
            'count': 0,
            'database_status': 'error'
        }), 500

@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get system statistics."""
    try:
        # Check if database is available first
        db_service = get_db_service()
        if not db_service or not db_service.test_connection():
            return jsonify({
                'error': 'Database unavailable',
                'users': 0,
                'conversations': 0,
                'messages': 0,
                'active_conversations_24h': 0,
                'database_status': 'disconnected'
            })
        
        from datetime import datetime, timedelta
        
        # Get basic counts using PyODBC directly
        conn = db_service._get_connection()
        cursor = conn.cursor()
        
        # Get basic counts
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM conversations")
        conversation_count = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM messages")
        message_count = cursor.fetchone()[0] or 0
        
        # Get active conversations (updated in last 24 hours)
        yesterday = datetime.utcnow() - timedelta(days=1)
        cursor.execute("SELECT COUNT(*) FROM conversations WHERE updated_at >= ?", (yesterday,))
        active_conversations = cursor.fetchone()[0] or 0
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'users': user_count,
            'conversations': conversation_count,
            'messages': message_count,
            'active_conversations_24h': active_conversations,
            'database_status': 'connected'
        })
        
    except Exception as e:
        logger.error(f"Error in get_stats: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'users': 0,
            'conversations': 0,
            'messages': 0,
            'active_conversations_24h': 0,
            'database_status': 'error'
        }), 500

@admin_bp.route('/users', methods=['GET'])
def get_users():
    """Get users list."""
    try:
        # Check if database is available first
        db_service = get_db_service()
        if not db_service or not db_service.test_connection():
            return jsonify({
                'error': 'Database unavailable',
                'users': [],
                'database_status': 'disconnected'
            })
        
        limit = int(request.args.get('limit', 50))
        
        # Get users using PyODBC directly
        conn = db_service._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP (?) * FROM users ORDER BY created_at DESC", (limit,))
        
        results = db_service._fetch_all_as_dict(cursor)
        cursor.close()
        conn.close()
        
        users = []
        for result in results:
            from models import User
            user = User(
                id=result['id'],
                username=result['username'],
                email=result['email'],
                created_at=result['created_at'],
                is_active=result['is_active']
            )
            users.append(user.to_dict())
        
        return jsonify({
            'users': users,
            'database_status': 'connected'
        })
        
    except Exception as e:
        logger.error(f"Error in get_users: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'users': [],
            'database_status': 'error'
        }), 500
