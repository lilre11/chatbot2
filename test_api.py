#!/usr/bin/env python3
"""
Simple test script to test the chatbot API directly
"""

import requests
import json

def test_chatbot_api():
    """Test the chatbot API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🔍 Testing Chatbot API")
    print("=" * 50)
    
    # Test if server is running
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        print(f"✅ Server health check: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not reachable: {e}")
        return
    
    # Test chat endpoint
    try:
        chat_data = {
            "message": "Hello, how are you?"
        }
        
        print("\n🧪 Testing chat endpoint...")
        print(f"Sending: {chat_data['message']}")
        
        response = requests.post(
            f"{base_url}/api/chat/send",
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat Response: {result.get('response', 'No response field')}")
            print(f"Conversation ID: {result.get('conversation_id')}")
        else:
            print(f"❌ Error Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"Raw response: {response.text}")

if __name__ == "__main__":
    test_chatbot_api()
