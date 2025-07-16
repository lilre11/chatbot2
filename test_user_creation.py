#!/usr/bin/env python3
"""
Test script to debug user creation issues.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from services.database_service import DatabaseService
import logging

def test_user_creation():
    """Test user creation to debug issues."""
    logging.basicConfig(level=logging.DEBUG)
    
    app = create_app()
    
    with app.app_context():
        db_service = DatabaseService()
        
        print(f"Database available: {db_service.db_available}")
        
        if not db_service.db_available:
            print("❌ Database not available")
            return
        
        try:
            # Test creating a user with a unique email
            import uuid
            test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
            test_password = "testpassword123"
            
            print(f"Testing user creation with email: {test_email}")
            
            user = db_service.create_user(test_email, test_password)
            
            if user:
                print(f"✅ Successfully created user: {user.username} with email: {user.email}")
            else:
                print("❌ Failed to create user")
                
        except Exception as e:
            print(f"❌ Exception during user creation: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_user_creation()
