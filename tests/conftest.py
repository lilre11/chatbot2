import pytest
from app import create_app
from models import db as _db
from models import User, Conversation, Message
import bcrypt


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def db(app):
    """Create database for testing."""
    with app.app_context():
        yield _db


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test runner."""
    return app.test_cli_runner()


@pytest.fixture
def sample_user(db):
    """Create a sample user for testing."""
    hashed_password = bcrypt.hashpw('testpassword'.encode('utf-8'), bcrypt.gensalt())
    user = User(
        username='testuser',
        email='test@example.com',
        password=hashed_password.decode('utf-8'),
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_conversation(db, sample_user):
    """Create a sample conversation for testing."""
    conversation = Conversation(
        user_id=sample_user.id,
        title='Test Conversation',
        is_active=True
    )
    db.session.add(conversation)
    db.session.commit()
    return conversation


@pytest.fixture
def sample_message(db, sample_conversation):
    """Create a sample message for testing."""
    message = Message(
        conversation_id=sample_conversation.id,
        content='Hello, this is a test message',
        sender_type='user',
        token_count=10
    )
    db.session.add(message)
    db.session.commit()
    return message 