#!/usr/bin/env python3
"""
Debug script to test Gemini API and identify issues.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Gemini API connection and response."""
    try:
        import google.generativeai as genai
        
        api_key = os.environ.get('GEMINI_API_KEY')
        print(f"API Key present: {'Yes' if api_key else 'No'}")
        
        if not api_key:
            print("❌ GEMINI_API_KEY not found in environment variables")
            return False
        
        print(f"API Key length: {len(api_key)} characters")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        print("✅ Gemini configured successfully")
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("✅ Model initialized successfully")
        
        # Test with a simple prompt
        print("🧪 Testing with simple prompt...")
        response = model.generate_content("Say hello")
        
        if response.text:
            print(f"✅ API Response: {response.text}")
            return True
        else:
            print("❌ Empty response from Gemini API")
            print(f"Response object: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini API: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test database connection."""
    try:
        from config import Config
        print(f"Database Host: {Config.DB_HOST}")
        print(f"Database Name: {Config.DB_NAME}")
        print(f"Database URI: {Config.SQLALCHEMY_DATABASE_URI[:50]}...")
        
        from services.database_service import DatabaseService
        db_service = DatabaseService()
        
        if db_service.test_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing database: {str(e)}")
        return False

def test_chat_flow():
    """Test the full chat flow."""
    try:
        from services.gemini_service import GeminiService
        from services.database_service import DatabaseService
        
        print("🧪 Testing full chat flow...")
        
        # Test services
        gemini_service = GeminiService()
        db_service = DatabaseService()
        
        # Test message generation
        test_message = "Hello, how are you?"
        response = gemini_service.generate_response(test_message)
        
        print(f"✅ Generated response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error in chat flow: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🔍 AI Chatbot Debug Script")
    print("=" * 50)
    
    print("\n1. Testing Gemini API...")
    gemini_ok = test_gemini_api()
    
    print("\n2. Testing Database Connection...")
    db_ok = test_database_connection()
    
    print("\n3. Testing Chat Flow...")
    chat_ok = test_chat_flow()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Gemini API: {'✅ OK' if gemini_ok else '❌ FAILED'}")
    print(f"Database: {'✅ OK' if db_ok else '❌ FAILED'}")
    print(f"Chat Flow: {'✅ OK' if chat_ok else '❌ FAILED'}")
    
    if all([gemini_ok, db_ok, chat_ok]):
        print("\n🎉 All tests passed! Your chatbot should work correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
