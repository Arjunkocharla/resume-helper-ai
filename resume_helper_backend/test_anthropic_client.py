#!/usr/bin/env python3
"""Test script to check Anthropic client attributes"""

import os
from anthropic import Anthropic

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_anthropic_client():
    """Test the Anthropic client to see what attributes it has"""
    try:
        # Create client
        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        print("✅ Anthropic client created successfully")
        print(f"Client type: {type(client)}")
        print(f"Client dir: {dir(client)}")
        
        # Check if messages attribute exists
        if hasattr(client, 'messages'):
            print("✅ Client has 'messages' attribute")
            print(f"Messages type: {type(client.messages)}")
            print(f"Messages dir: {dir(client.messages)}")
        else:
            print("❌ Client does NOT have 'messages' attribute")
            
        # Check what attributes the client has
        print("\nClient attributes:")
        for attr in dir(client):
            if not attr.startswith('_'):
                print(f"  - {attr}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_anthropic_client()
