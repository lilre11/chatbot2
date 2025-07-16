#!/usr/bin/env python3
"""
Test script to test conversation rename functionality directly.
"""

import requests
import json

def test_rename():
    """Test the rename conversation functionality."""
    base_url = "http://localhost:5000/api/chat"
    
    # Step 1: Register a user
    username = "rename_test_user"
    password = "testpass123"
    
    # Register
    register_response = requests.post(f"{base_url}/register", json={
        "username": username,
        "password": password
    })
    
    if register_response.status_code != 200:
        print(f"Registration failed: {register_response.text}")
        return
    
    print("User registered successfully")
    
    # Step 2: Login
    login_response = requests.post(f"{base_url}/login", json={
        "username": username,
        "password": password
    })
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    
    cookies = login_response.cookies
    print("Login successful")
    
    # Step 3: Send a message to create a conversation
    message_response = requests.post(f"{base_url}/send", json={
        "message": "Hello, this is a test conversation"
    }, cookies=cookies)
    
    if message_response.status_code != 200:
        print(f"Message failed: {message_response.text}")
        return
    
    conversation_id = message_response.json().get('conversation_id')
    print(f"Conversation created with ID: {conversation_id}")
    
    # Step 4: Rename the conversation
    rename_response = requests.put(f"{base_url}/conversations/{conversation_id}", json={
        "title": "Renamed Test Conversation"
    }, cookies=cookies)
    
    print(f"Rename response status: {rename_response.status_code}")
    print(f"Rename response body: {rename_response.text}")
    
    if rename_response.status_code == 200:
        print("✅ Conversation renamed successfully")
    else:
        print("❌ Conversation rename failed")

if __name__ == "__main__":
    test_rename()
