from flask import Blueprint, jsonify

# Initialize blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """API health check endpoint."""
    return jsonify({
        'message': 'AI Chatbot API is running',
        'status': 'healthy',
        'version': '1.0.0'
    })

@main_bp.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})
