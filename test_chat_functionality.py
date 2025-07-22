#!/usr/bin/env python3
"""
Test script to verify chat functionality works correctly.
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_chat_functionality():
    """Test the complete chat workflow."""
    session = requests.Session()
    
    print("Testing chat functionality...")
    
    # 1. Register a test user
    print("\n1. Registering test user...")
    register_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    response = session.post(f"{BASE_URL}/chat/register", json=register_data)
    if response.status_code == 200:
        print("✓ User registered successfully")
    elif response.status_code == 400 and "already exists" in response.text:
        print("✓ User already exists, proceeding...")
    else:
        print(f"✗ Registration failed: {response.status_code} - {response.text}")
        return False
    
    # 2. Login
    print("\n2. Logging in...")
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    response = session.post(f"{BASE_URL}/chat/login", json=login_data)
    if response.status_code == 200:
        print("✓ Login successful")
        user_data = response.json()
        print(f"  User ID: {user_data['user']['id']}")
    else:
        print(f"✗ Login failed: {response.status_code} - {response.text}")
        return False
    
    # 3. Send a message (this should create a new conversation)
    print("\n3. Sending a message...")
    message_data = {
        "message": "Hello, this is a test message!"
    }
    
    response = session.post(f"{BASE_URL}/chat/send", json=message_data)
    if response.status_code == 200:
        chat_response = response.json()
        print("✓ Message sent successfully")
        print(f"  Conversation ID: {chat_response.get('conversation_id')}")
        print(f"  Bot response: {chat_response.get('response')[:100]}...")
        conversation_id = chat_response.get('conversation_id')
    else:
        print(f"✗ Message send failed: {response.status_code} - {response.text}")
        return False
    
    # 4. Get conversations list
    print("\n4. Getting conversations list...")
    response = session.get(f"{BASE_URL}/chat/conversations")
    if response.status_code == 200:
        conversations_data = response.json()
        conversations = conversations_data.get('conversations', [])
        print(f"✓ Retrieved {len(conversations)} conversations")
        for conv in conversations:
            print(f"  - ID: {conv['id']}, Title: {conv['title']}")
    else:
        print(f"✗ Failed to get conversations: {response.status_code} - {response.text}")
        return False
    
    # 5. Get messages for the conversation
    if conversation_id:
        print(f"\n5. Getting messages for conversation {conversation_id}...")
        response = session.get(f"{BASE_URL}/chat/conversations/{conversation_id}/messages")
        if response.status_code == 200:
            messages_data = response.json()
            messages = messages_data.get('messages', [])
            print(f"✓ Retrieved {len(messages)} messages")
            for msg in messages:
                print(f"  - {msg['sender_type']}: {msg['content'][:50]}...")
        else:
            print(f"✗ Failed to get messages: {response.status_code} - {response.text}")
            return False
    
    # 6. Send another message to the same conversation
    print("\n6. Sending another message to the same conversation...")
    message_data = {
        "message": "This is a second message in the same conversation.",
        "conversation_id": conversation_id
    }
    
    response = session.post(f"{BASE_URL}/chat/send", json=message_data)
    if response.status_code == 200:
        chat_response = response.json()
        print("✓ Second message sent successfully")
        print(f"  Conversation ID: {chat_response.get('conversation_id')}")
        print(f"  Bot response: {chat_response.get('response')[:100]}...")
    else:
        print(f"✗ Second message send failed: {response.status_code} - {response.text}")
        return False
    
    print("\n✓ All tests passed! Chat functionality is working correctly.")
    return True

if __name__ == "__main__":
    test_chat_functionality()
