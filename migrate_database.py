#!/usr/bin/env python3
"""
Script to add password column to users table and assign random usernames.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User
import random
import logging

def migrate_database():
    """Add password column and assign random usernames."""
    app = create_app()
    
    with app.app_context():
        try:
            # Add password column to users table using text() for raw SQL
            from sqlalchemy import text
            db.session.execute(text("ALTER TABLE users ADD password NVARCHAR(255) NOT NULL DEFAULT ''"))
            db.session.commit()
            print("✅ Added password column to users table")
        except Exception as e:
            db.session.rollback()
            if "already exists" in str(e) or "duplicate column" in str(e).lower() or "already" in str(e).lower():
                print("✅ Password column already exists")
            else:
                print(f"⚠️  Error adding password column: {str(e)}")
        
        try:
            # Get users without usernames or empty usernames
            users_without_usernames = User.query.filter(
                (User.username == None) | (User.username == '')
            ).all()
            
            # Assign random usernames
            for user in users_without_usernames:
                user.username = f"user_{random.randint(1000,9999)}"
            
            # Get users without passwords (empty password field)
            users_without_passwords = User.query.filter(
                (User.password == None) | (User.password == '')
            ).all()
            
            # Assign default password hash for legacy users (they'll need to reset)
            import secrets
            import hashlib
            
            def hash_password(password: str) -> str:
                salt = secrets.token_hex(8)
                hashed = hashlib.sha256((salt + password).encode()).hexdigest()
                return f"{salt}${hashed}"
            
            default_password_hash = hash_password("changeme123")
            
            for user in users_without_passwords:
                user.password = default_password_hash
            
            db.session.commit()
            
            print(f"✅ Assigned random usernames to {len(users_without_usernames)} users")
            print(f"✅ Assigned default passwords to {len(users_without_passwords)} users")
            print("📝 Legacy users can login with password: 'changeme123'")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {str(e)}")
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success = migrate_database()
    if success:
        print("✅ Database migration completed successfully.")
    else:
        print("❌ Database migration failed.")
        sys.exit(1)
