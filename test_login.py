#!/usr/bin/env python3
"""
Test script to make HTTP requests to the login endpoint.
"""

import requests
import json

def test_login():
    """Test login endpoint directly."""
    
    # First register a user
    register_url = "http://localhost:5000/api/chat/register"
    
    # Test data with unique username
    import uuid
    username = f"testuser_{uuid.uuid4().hex[:6]}"
    password = "testpassword123"
    
    register_data = {
        "username": username,
        "password": password
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Registering user: {register_data}")
        register_response = requests.post(register_url, json=register_data, headers=headers)
        
        if register_response.status_code != 200:
            print(f"❌ Registration failed: {register_response.text}")
            return
        
        print("✅ Registration successful")
        
        # Now test login
        login_url = "http://localhost:5000/api/chat/login"
        login_data = {
            "username": username,
            "password": password
        }
        
        print(f"Testing login with: {login_data}")
        login_response = requests.post(login_url, json=login_data, headers=headers)
        
        print(f"Status Code: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Test /me endpoint to verify session
            me_response = requests.get("http://localhost:5000/api/chat/me", 
                                     cookies=login_response.cookies)
            print(f"Me endpoint response: {me_response.text}")
            
        else:
            print("❌ Login failed")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure Flask is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_login()
