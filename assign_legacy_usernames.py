#!/usr/bin/env python3
"""
Script to assign random usernames to legacy users and add password field.
Run this script after updating the User model to include password field.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from services.database_service import DatabaseService
import logging

def assign_legacy_usernames():
    """Assign random usernames to users who don't have them."""
    app = create_app()
    
    with app.app_context():
        try:
            # Import here to avoid circular imports
            from models import User, db
            import random
            
            # Get users without usernames
            users = User.query.filter((User.username == None) | (User.username == '')).all()
            
            for user in users:
                user.username = f"user_{random.randint(1000,9999)}"
            
            db.session.commit()
            print(f"Successfully assigned random usernames to {len(users)} legacy users.")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error assigning usernames: {str(e)}")
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success = assign_legacy_usernames()
    if success:
        print("Legacy username assignment completed successfully.")
    else:
        print("Legacy username assignment failed.")
        sys.exit(1)
