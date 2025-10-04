import os
import json
from typing import Dict, List, Optional, Any
from groq import Groq

class GroqAPIKeyManager:
    """GROQ API Key Manager - Set and validate your GROQ API key within ComfyUI"""
    
    RETURN_TYPES = ("STRING", "BOOLEAN", "STRING")
    RETURN_NAMES = ("status_message", "is_valid", "masked_key")
    FUNCTION = "manage_api_key"
    CATEGORY = "GroqPrompt/Setup"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "default": "", 
                    "multiline": False, 
                    "tooltip": "Enter your GROQ API key here. Get one from https://console.groq.com/keys"
                }),
                "action": (["set_and_validate", "validate_only", "clear_key"], {
                    "default": "set_and_validate",
                    "tooltip": "What to do with the API key"
                }),
                "test_connection": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Test the API key with a simple request"
                }),
            },
            "optional": {
                "test_model": (["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama3-8b-8192"], {
                    "default": "llama-3.1-8b-instant",
                    "tooltip": "Model to use for testing (faster models = quicker validation)"
                }),
            }
        }
    
    def manage_api_key(self, api_key, action, test_connection, test_model="llama-3.1-8b-instant", **kwargs):
        """Manage GROQ API key - set, validate, or clear"""
        
        # Get current environment key
        current_env_key = os.getenv('GROQ_API_KEY', '')
        
        if action == "clear_key":
            # Clear the environment variable
            if 'GROQ_API_KEY' in os.environ:
                del os.environ['GROQ_API_KEY']
            return ("✅ API key cleared from environment", False, "")
        
        # Use provided key or fall back to environment
        working_key = api_key.strip() if api_key.strip() else current_env_key
        
        if not working_key:
            return ("❌ No API key provided. Please enter your GROQ API key.", False, "")
        
        # Basic format validation
        if not working_key.startswith('gsk_'):
            return ("⚠️ Warning: GROQ API keys typically start with 'gsk_'. Key may be invalid.", False, f"{working_key[:8]}...{working_key[-4:]}")
        
        # Set in environment if requested
        if action == "set_and_validate" and api_key.strip():
            os.environ['GROQ_API_KEY'] = working_key
            status_msg = "✅ API key set in environment"
        else:
            status_msg = "🔍 Using existing environment key" if not api_key.strip() else "🔍 Key provided"
        
        # Create masked version for display
        masked_key = f"{working_key[:8]}...{working_key[-4:]}" if len(working_key) > 12 else "KEY_TOO_SHORT"
        
        # Test connection if requested
        if test_connection:
            is_valid, test_msg = self._test_api_key(working_key, test_model)
            status_msg += f" | {test_msg}"
            return (status_msg, is_valid, masked_key)
        else:
            # Skip testing, assume valid if format is correct
            is_valid = working_key.startswith('gsk_') and len(working_key) > 20
            return (status_msg + " | (not tested)", is_valid, masked_key)
    
    def _test_api_key(self, api_key, model):
        """Test the API key with a simple request"""
        try:
            client = Groq(api_key=api_key)
            
            # Make a minimal test request
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "Say 'OK' if you can read this."}
                ],
                max_tokens=5,
                temperature=0.1
            )
            
            if response.choices and response.choices[0].message.content:
                return True, "✅ API key test successful"
            else:
                return False, "❌ API key test failed: No response"
                
        except Exception as e:
            error_msg = str(e).lower()
            if "401" in error_msg or "invalid_api_key" in error_msg:
                return False, "❌ Invalid API key"
            elif "429" in error_msg or "rate_limit" in error_msg:
                return True, "⚠️ Valid key but rate limited"
            elif "quota" in error_msg or "billing" in error_msg:
                return True, "⚠️ Valid key but quota exceeded"
            elif "timeout" in error_msg or "connection" in error_msg:
                return None, "⚠️ Connection timeout - key likely valid"
            else:
                return False, f"❌ Test failed: {str(e)[:50]}"

class GroqAPIKeyProvider:
    """GROQ API Key Provider - Provides API key to other nodes in the workflow"""
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("api_key",)
    FUNCTION = "provide_api_key"
    CATEGORY = "GroqPrompt/Setup"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source": (["environment_variable", "manual_input"], {
                    "default": "environment_variable",
                    "tooltip": "Where to get the API key from"
                }),
            },
            "optional": {
                "manual_key": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "tooltip": "Enter API key manually (only used if source is manual_input)"
                }),
            }
        }
    
    def provide_api_key(self, source, manual_key="", **kwargs):
        """Provide API key for other nodes"""
        
        if source == "manual_input":
            if manual_key.strip():
                return (manual_key.strip(),)
            else:
                return ("",)  # Empty if no manual key provided
        else:
            # Get from environment variable
            env_key = os.getenv('GROQ_API_KEY', '')
            return (env_key,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "GroqAPIKeyManager": GroqAPIKeyManager,
    "GroqAPIKeyProvider": GroqAPIKeyProvider,
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "GroqAPIKeyManager": "GROQ API Key Manager",
    "GroqAPIKeyProvider": "GROQ API Key Provider",
}
