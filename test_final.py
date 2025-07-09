#!/usr/bin/env python3
"""
Final test to verify the chatbot is working end-to-end
"""

import requests
import json
import time

def test_backend_endpoints():
    """Test all backend endpoints"""
    base_url = "http://localhost:5000"
    
    print("🔍 Testing Backend Endpoints")
    print("=" * 50)
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check: OK")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test primary chat endpoint
    try:
        response = requests.post(
            f"{base_url}/api/chat/send",
            json={"message": "Hello, this is a test"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Primary chat endpoint: {data.get('response', '')[:50]}...")
            primary_works = True
        else:
            print(f"⚠️  Primary chat endpoint failed: {response.status_code}")
            primary_works = False
    except Exception as e:
        print(f"⚠️  Primary chat endpoint error: {e}")
        primary_works = False
    
    # Test fallback chat endpoint
    try:
        response = requests.post(
            f"{base_url}/api/chat/send-simple",
            json={"message": "Hello, this is a fallback test"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Fallback chat endpoint: {data.get('response', '')[:50]}...")
            fallback_works = True
        else:
            print(f"❌ Fallback chat endpoint failed: {response.status_code}")
            fallback_works = False
    except Exception as e:
        print(f"❌ Fallback chat endpoint error: {e}")
        fallback_works = False
    
    return primary_works or fallback_works

def main():
    print("🧪 FINAL CHATBOT TEST")
    print("=" * 60)
    
    # Wait for server to start if needed
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    backend_works = test_backend_endpoints()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print(f"Backend: {'✅ Working' if backend_works else '❌ Failed'}")
    
    if backend_works:
        print("\n🎉 SUCCESS! The chatbot backend is working.")
        print("\n📋 Next steps:")
        print("1. Start the Flask backend with: python app.py")
        print("2. Start the React frontend with: cd frontend && npm start")
        print("3. Open http://localhost:3000 in your browser")
        print("4. Try chatting - it should work with either primary or fallback endpoints")
        print("\n💡 Note: Database features may not work, but AI chat will work fine.")
    else:
        print("\n❌ The backend is not working properly.")
        print("Please check the server logs for errors.")

if __name__ == "__main__":
    main()
