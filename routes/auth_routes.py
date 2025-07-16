from flask import Blueprint, request, jsonify, session
from logging import getLogger
from hashlib import sha256
from os import urandom

auth_bp = Blueprint('auth', __name__)
logger = getLogger(__name__)

# --- Password Hashing (SHA-256 with Salt) ---

def hash_password(password: str) -> str:
    """Hashes a password with a salt using SHA-256."""
    salt = urandom(16).hex()
    hashed = sha256((password + salt).encode('utf-8')).hexdigest()
    return f"{salt}${hashed}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a password against a SHA-256 hash."""
    try:
        salt, hash_value = hashed_password.split('$', 1)
        return sha256((password + salt).encode('utf-8')).hexdigest() == hash_value
    except (ValueError, TypeError):
        logger.error("Could not verify password due to invalid hash format.")
        return False

# --- Routes ---

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    from models import db, User
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing username, email, or password'}), 400

        username = data['username'].strip()
        email = data['email'].strip().lower()

        if User.query.filter((User.username == username) | (User.email == email)).first(): # pyright: ignore
            return jsonify({'error': 'Username or email already exists'}), 409

        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400

        new_user = User(
            username=username,
            email=email,
            password=hash_password(data['password']),
        )
        db.session.add(new_user)
        db.session.commit()
        
        logger.info(f"New user registered: {username}")
        return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {e}", exc_info=True)
        return jsonify({'error': 'Registration failed due to an internal error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and create session."""
    from models import User
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400

        user = User.query.filter_by(username=data['username']).first() # pyright: ignore

        if user and user.is_active and verify_password(data['password'], user.password):
            session['user_id'] = user.id
            session['username'] = user.username
            logger.info(f"User logged in: {user.username}")
            return jsonify({
                'message': 'Login successful',
                'user': {'id': user.id, 'username': user.username, 'email': user.email}
            }), 200
        else:
            logger.warning(f"Failed login attempt for username: {data.get('username')}")
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        return jsonify({'error': 'Login failed due to an internal error'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user and clear session."""
    username = session.pop('username', 'Unknown')
    session.clear()
    logger.info(f"User logged out: {username}")
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get current user profile."""
    from models import User
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(session['user_id']) # pyright: ignore
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }), 200

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """Change user password."""
    from models import db, User
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    if not data or not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current and new password are required'}), 400

    user = User.query.get(session['user_id']) # pyright: ignore
    if not user or not verify_password(data['current_password'], user.password):
        return jsonify({'error': 'Invalid current password'}), 401

    if len(data['new_password']) < 6:
        return jsonify({'error': 'New password must be at least 6 characters long'}), 400

    user.password = hash_password(data['new_password'])
    db.session.commit()
    logger.info(f"Password changed for user: {user.username}")
    return jsonify({'message': 'Password changed successfully'}), 200
