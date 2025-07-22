from flask import Blueprint, jsonify

# Initialize blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def root():
    """Root endpoint."""
    return jsonify({
        'message': 'Chatbot API is running',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'documentation': '/api/api-docs',
            'chat': '/api/chat',
            'admin': '/api/admin'
        }
    }), 200

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    from flask import current_app
    from datetime import datetime
 
    db_status = 'healthy' if getattr(current_app, 'db_working', False) else 'unhealthy'

    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@main_bp.route('/api-docs', methods=['GET'])
def api_docs():
    """API documentation endpoint."""
    return jsonify({
        'message': 'API Documentation',
        'endpoints': {
            'health': {
                'method': 'GET',
                'path': '/api/health',
                'description': 'Health check endpoint',
                'response': {
                    'status': 'string - Service health status',
                    'database': 'string - Database connection status',
                    'timestamp': 'string - Current UTC timestamp'
                }
            },
            'auth': {
                'register': {
                    'method': 'POST',
                    'path': '/api/auth/register',
                    'description': 'Register a new user',
                    'body': {
                        'username': 'string - Required',
                        'password': 'string - Required',
                        'email': 'string - Required'
                    }
                },
                'login': {
                    'method': 'POST',
                    'path': '/api/auth/login',
                    'description': 'Authenticate user',
                    'body': {
                        'username': 'string - Required',
                        'password': 'string - Required'
                    }
                },
                'logout': {
                    'method': 'POST',
                    'path': '/api/auth/logout',
                    'description': 'Logout user'
                },
                'profile': {
                    'method': 'GET',
                    'path': '/api/auth/profile',
                    'description': 'Get user profile'
                }
            },
            'chat': {
                'send': {
                    'method': 'POST',
                    'path': '/api/chat/send',
                    'description': 'Send message to AI',
                    'body': {
                        'message': 'string - Required',
                        'conversation_id': 'string - Optional'
                    }
                },
                'conversations': {
                    'method': 'GET',
                    'path': '/api/chat/conversations',
                    'description': 'Get user conversations'
                },
                'messages': {
                    'method': 'GET',
                    'path': '/api/chat/messages/<conversation_id>',
                    'description': 'Get conversation messages'
                }
            },
            'admin': {
                'status': {
                    'method': 'GET',
                    'path': '/api/admin/status',
                    'description': 'Get system status'
                },
                'stats': {
                    'method': 'GET',
                    'path': '/api/admin/stats',
                    'description': 'Get system statistics'
                },
                'users': {
                    'method': 'GET',
                    'path': '/api/admin/users',
                    'description': 'Get all users'
                },
                'logs': {
                    'method': 'GET',
                    'path': '/api/admin/logs',
                    'description': 'Get system logs'
                }
            }
        }
    }), 200
