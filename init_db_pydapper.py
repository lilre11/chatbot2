#!/usr/bin/env python3
"""
Database initialization script using PyDapper.
Creates tables and sets up the database schema.
"""

import os
import sys
from config import Config
from services.database_service import DatabaseService

def main():
    """Initialize the database."""
    print("🚀 Initializing database with PyDapper...")
    
    try:
        # Create PyDapper connection string
        connection_string = (
            f"DRIVER={{{Config.DB_DRIVER}}};"
            f"SERVER={Config.DB_HOST},{Config.DB_PORT};"
            f"DATABASE={Config.DB_NAME};"
            f"UID={Config.DB_USER};"
            f"PWD={Config.DB_PASSWORD};"
            f"Timeout=5;"
        )
        
        # Initialize database service
        db_service = DatabaseService(connection_string)
        
        if not db_service.db_available:
            print("❌ Database connection failed")
            print("Please check your database configuration in config.py")
            return False
        
        # Create tables
        success = db_service.create_tables()
        
        if success:
            print("✅ Database tables created successfully!")
            print("Database schema:")
            print("  - users: User accounts and session management")
            print("  - conversations: Chat sessions between users and AI")
            print("  - messages: Individual messages in conversations")
            print("  - system_logs: Application logging and monitoring")
            
            # Test the database by creating a sample user
            print("\n🔍 Testing database operations...")
            test_user = db_service.create_user("test_user", "test@example.com")
            if test_user:
                print(f"✅ Successfully created test user: {test_user.username}")
                print("Database is ready to use!")
            else:
                print("⚠️  Warning: Database tables created but test operation failed")
                
        else:
            print("❌ Failed to create database tables")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
