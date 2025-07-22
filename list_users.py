#!/usr/bin/env python3
"""
Script to list existing users in the database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import User

def list_users():
    """List all users in the database."""
    app = create_app()
    
    with app.app_context():
        try:
            users = User.query.all()
            print(f"Found {len(users)} users in the database:")
            print("-" * 50)
            
            for user in users:
                print(f"ID: {user.id}")
                print(f"Username: {user.username}")
                print(f"Email: {user.email}")
                print(f"Active: {user.is_active}")
                print(f"Created: {user.created_at}")
                print("-" * 30)
                
        except Exception as e:
            print(f"Error listing users: {str(e)}")

if __name__ == "__main__":
    list_users()
