#!/usr/bin/env python3
"""
GROQ API Key Setup Helper

This script helps you set up your GROQ API key for the ComfyUI GroqPrompt extension.
"""

import os
import sys
import subprocess

def main():
    print("=== GROQ API Key Setup Helper ===")
    print()
    
    # Check if API key is already set
    current_key = os.getenv('GROQ_API_KEY', '')
    if current_key:
        print(f"✓ GROQ API key is already set: {current_key[:10]}...{current_key[-4:]}")
        response = input("Do you want to update it? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Keeping existing API key.")
            return
    else:
        print("✗ No GROQ API key found in environment variables.")
    
    print()
    print("To get your GROQ API key:")
    print("1. Go to https://console.groq.com/keys")
    print("2. Sign in or create an account")
    print("3. Create a new API key")
    print("4. Copy the key")
    print()
    
    # Get API key from user
    api_key = input("Enter your GROQ API key: ").strip()
    
    if not api_key:
        print("No API key provided. Exiting.")
        return
    
    # Validate API key format (basic check)
    if not api_key.startswith('gsk_'):
        print("Warning: GROQ API keys typically start with 'gsk_'")
        response = input("Continue anyway? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            return
    
    # Set environment variable for current session
    os.environ['GROQ_API_KEY'] = api_key
    
    # Try to set permanently
    try:
        if sys.platform == "win32":
            # Windows
            result = subprocess.run([
                'setx', 'GROQ_API_KEY', api_key
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ API key set permanently for Windows")
                print("✓ Please restart your terminal/ComfyUI for changes to take effect")
            else:
                print("✗ Failed to set permanently. You may need to run as administrator.")
                print("Manual setup instructions:")
                print(f"  Run: setx GROQ_API_KEY {api_key}")
        else:
            # Linux/Mac
            shell_config = os.path.expanduser("~/.bashrc")
            if os.path.exists(os.path.expanduser("~/.zshrc")):
                shell_config = os.path.expanduser("~/.zshrc")
            
            with open(shell_config, 'a') as f:
                f.write(f'\nexport GROQ_API_KEY="{api_key}"\n')
            
            print(f"✓ API key added to {shell_config}")
            print("✓ Please restart your terminal or run: source ~/.bashrc")
            
    except Exception as e:
        print(f"✗ Failed to set permanently: {e}")
        print("Manual setup instructions:")
        if sys.platform == "win32":
            print(f"  Run: setx GROQ_API_KEY {api_key}")
        else:
            print(f"  Add to ~/.bashrc: export GROQ_API_KEY=\"{api_key}\"")
    
    print()
    print("=== Setup Complete ===")
    print("Your GROQ API key is now configured for this session.")
    
    # Test the API key
    test_response = input("Do you want to test the API key? (Y/n): ")
    if test_response.lower() not in ['n', 'no']:
        test_api_key(api_key)

def test_api_key(api_key):
    """Test the API key by making a simple request"""
    print("\nTesting API key...")
    
    try:
        from groq import Groq
        
        client = Groq(api_key=api_key)
        
        # Make a simple test request
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API key test successful!' if you can read this."}
            ],
            max_tokens=20,
            temperature=0.1
        )
        
        if response.choices:
            result = response.choices[0].message.content
            print(f"✓ API key test successful!")
            print(f"  Response: {result}")
        else:
            print("✗ API key test failed: No response received")
            
    except ImportError:
        print("✗ Cannot test API key: 'groq' package not installed")
        print("  Install with: pip install groq")
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid_api_key" in error_msg.lower():
            print("✗ API key test failed: Invalid API key")
        elif "429" in error_msg or "rate_limit" in error_msg.lower():
            print("✗ API key test failed: Rate limit exceeded")
        else:
            print(f"✗ API key test failed: {error_msg}")

if __name__ == "__main__":
    main()
