#!/usr/bin/env python3
"""
Test the chatbot functionality directly without running a server
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_directly():
    """Test Gemini service directly"""
    print("🧪 Testing Gemini service directly...")
    
    try:
        from services.gemini_service import GeminiService
        
        # Create Gemini service
        gemini = GeminiService()
        print("✅ Gemini service created successfully")
        
        # Test with a simple message
        test_message = "Hello! How are you today?"
        print(f"📤 Sending: {test_message}")
        
        response = gemini.generate_response(test_message)
        print(f"📥 Response: {response}")
        
        if response and len(response) > 0:
            print("✅ Gemini is working correctly!")
            return True
        else:
            print("❌ Gemini returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_routes():
    """Test Flask routes without running server"""
    print("\n🧪 Testing Flask routes directly...")
    
    try:
        from app import create_app
        
        # Create app
        app = create_app()
        print("✅ Flask app created successfully")
        
        # Test app context
        with app.app_context():
            print("✅ App context works")
            
        # Test client
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            print(f"Health endpoint status: {response.status_code}")
            print(f"Health response: {response.get_json()}")
            
            # Test chat endpoint
            test_data = {'message': 'Hello, this is a test message'}
            response = client.post('/api/chat/send', 
                                 json=test_data,
                                 headers={'Content-Type': 'application/json'})
            
            print(f"Chat endpoint status: {response.status_code}")
            if response.status_code == 200:
                chat_response = response.get_json()
                print(f"Chat response: {chat_response.get('response', 'No response')[:100]}...")
                print("✅ Chat endpoint is working!")
                return True
            else:
                print(f"❌ Chat endpoint error: {response.get_data(as_text=True)}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing Flask routes: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 DIRECT CHATBOT TEST")
    print("=" * 50)
    
    gemini_works = test_gemini_directly()
    flask_works = test_flask_routes()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"Gemini Service: {'✅ Working' if gemini_works else '❌ Failed'}")
    print(f"Flask Routes: {'✅ Working' if flask_works else '❌ Failed'}")
    
    if gemini_works and flask_works:
        print("\n🎉 All tests passed! The chatbot should work.")
        print("💡 The issue might be with:")
        print("   1. Database connection (which is expected)")
        print("   2. Frontend-backend communication")
        print("   3. CORS configuration")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
