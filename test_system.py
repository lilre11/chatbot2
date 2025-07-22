#!/usr/bin/env python3
"""
Test script to check for import errors and basic functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all imports to identify any issues"""
    print("🔍 Testing imports...")
    
    try:
        print("Testing Flask imports...")
        from flask import Flask
        print("✅ Flask imported successfully")
        
        print("Testing config...")
        from config import Config
        print("✅ Config imported successfully")
        
        print("Testing models...")
        from models import db, User, Conversation, Message, SystemLog
        print("✅ Models imported successfully")
        
        print("Testing services...")
        from services.gemini_service import GeminiService
        print("✅ GeminiService imported successfully")
        
        from services.database_service import DatabaseService
        print("✅ DatabaseService imported successfully")
        
        print("Testing routes...")
        from routes.chat_routes import chat_bp
        from routes.admin_routes import admin_bp
        from routes.main_routes import main_bp
        print("✅ Routes imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gemini_service():
    """Test Gemini service independently"""
    print("\n🧪 Testing Gemini service...")
    
    try:
        from services.gemini_service import GeminiService
        gemini = GeminiService()
        
        response = gemini.generate_response("Hello")
        print(f"✅ Gemini response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_creation():
    """Test Flask app creation"""
    print("\n🧪 Testing Flask app creation...")
    
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        return True
        
    except Exception as e:
        print(f"❌ App creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 CHATBOT SYSTEM TEST")
    print("=" * 60)
    
    # Test imports
    if not test_imports():
        print("❌ Import test failed - stopping here")
        sys.exit(1)
    
    # Test Gemini service
    test_gemini_service()
    
    # Test app creation
    test_app_creation()
    
    print("\n" + "=" * 60)
    print("✅ System test completed")
