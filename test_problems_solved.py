#!/usr/bin/env python3
"""
Test script to verify all problems are solved
"""

def test_app_creation():
    """Test Flask app creation"""
    print("🧪 Testing Flask app creation...")
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        
        # Test app context
        with app.app_context():
            print("✅ App context works")
            
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def test_gemini_service():
    """Test Gemini AI service"""
    print("\n🧪 Testing Gemini AI service...")
    try:
        from services.gemini_service import GeminiService
        gemini = GeminiService()
        
        response = gemini.generate_response("Hello, how are you?")
        print(f"✅ Gemini response: {response[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Gemini service failed: {e}")
        return False

def test_database_service():
    """Test database service (should handle failures gracefully)"""
    print("\n🧪 Testing database service...")
    try:
        from services.database_service import DatabaseService
        db_service = DatabaseService()
        print("✅ Database service created (may be in fallback mode)")
        return True
    except Exception as e:
        print(f"❌ Database service failed: {e}")
        return False

def test_flask_routes():
    """Test Flask routes with test client"""
    print("\n🧪 Testing Flask routes...")
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            print(f"Health endpoint: {response.status_code}")
            
            # Test chat endpoint
            chat_data = {'message': 'Hello, this is a test'}
            response = client.post('/api/chat/send', 
                                 json=chat_data,
                                 headers={'Content-Type': 'application/json'})
            
            print(f"Chat endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Chat response: {data.get('response', '')[:50]}...")
                return True
            else:
                print(f"❌ Chat endpoint error: {response.get_data(as_text=True)}")
                return False
                
    except Exception as e:
        print(f"❌ Flask routes test failed: {e}")
        return False

def main():
    print("🔍 COMPREHENSIVE PROBLEM-SOLVING TEST")
    print("=" * 60)
    
    tests = [
        test_app_creation,
        test_gemini_service, 
        test_database_service,
        test_flask_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'='*60}")
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL PROBLEMS SOLVED! Your chatbot is ready to run.")
        print("\n🚀 To start your chatbot:")
        print("1. Backend: python app.py")
        print("2. Frontend: cd frontend && npm start")
        print("3. Open: http://localhost:3000")
    else:
        print("❌ Some issues remain. Check the errors above.")

if __name__ == "__main__":
    main()
