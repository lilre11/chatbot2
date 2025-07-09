#!/usr/bin/env python3
"""
Database initialization script for the AI Chatbot application.
This script creates all database tables and optionally seeds some test data.
"""

from app import create_app
from models import db, User, Conversation, Message, SystemLog
from datetime import datetime

def init_database():
    """Initialize the database with tables."""
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if tables exist by counting records
            user_count = User.query.count()
            print(f"📊 Current users in database: {user_count}")
            
            # Log the initialization
            log_entry = SystemLog(
                level='INFO',
                message='Database initialized successfully',
                module='init_db.py'
            )
            db.session.add(log_entry)
            db.session.commit()
            print("✅ Initialization logged to system_logs table")
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            return False
    
    return True

def create_test_user():
    """Create a test user for development."""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if test user already exists
            test_user = User.query.filter_by(username='testuser').first()
            if test_user:
                print("ℹ️  Test user already exists")
                return test_user
            
            # Create test user
            test_user = User(
                username='testuser',
                email='test@example.com'
            )
            db.session.add(test_user)
            db.session.commit()
            
            print("✅ Test user created successfully!")
            print(f"   Username: {test_user.username}")
            print(f"   Email: {test_user.email}")
            print(f"   ID: {test_user.id}")
            
            return test_user
            
        except Exception as e:
            print(f"❌ Error creating test user: {str(e)}")
            db.session.rollback()
            return None

if __name__ == '__main__':
    print("🚀 Initializing AI Chatbot Database...")
    print("=" * 50)
    
    # Initialize database
    if init_database():
        print("\n🧪 Creating test user...")
        test_user = create_test_user()
        
        if test_user:
            print("\n✨ Database setup complete!")
            print("\n📋 Next steps:")
            print("   1. Start the Flask application: python app.py")
            print("   2. Visit: http://localhost:5000")
            print("   3. Test the chat interface")
            print("   4. Check admin dashboard at: http://localhost:5000/admin")
        else:
            print("\n⚠️  Database initialized but test user creation failed")
    else:
        print("\n❌ Database initialization failed!")
        print("   Please check your database connection settings in .env")
