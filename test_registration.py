#!/usr/bin/env python3
"""
Test script to make HTTP requests to the registration endpoint.
"""

import requests
import json

def test_registration():
    """Test registration endpoint directly."""
    
    url = "http://localhost:5000/api/chat/register"
    
    # Test data with unique username
    import uuid
    data = {
        "username": f"testuser_{uuid.uuid4().hex[:6]}",
        "password": "testpassword123"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Testing registration with: {data}")
        response = requests.post(url, json=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful")
        else:
            print("❌ Registration failed")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure Flask is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_registration()
