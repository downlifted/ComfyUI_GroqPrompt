import os
import json
import random
import numpy as np
import torch
from typing import Dict, List, Optional, Any
from groq import Groq

from .utils.base_node import GroqNode, get_model_descriptions, get_model_choices, ModelType

class GroqLLMNode(GroqNode):
    """Legacy GroqLLMNode for backward compatibility with old workflows"""
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "generate"
    CATEGORY = "GroqPrompt/Legacy"
    
    @classmethod
    def INPUT_TYPES(cls):
        text_models = get_model_choices(ModelType.TEXT)
        
        return {
            "required": {
                "api_key": ("STRING", {
                    "default": "", 
                    "multiline": False, 
                    "tooltip": "Your GROQ API key. Leave empty to use GROQ_API_KEY environment variable."
                }),
                "model": (text_models, {
                    "default": "llama-3.3-70b-versatile",
                    "tooltip": "Select a text generation model"
                }),
                "prompt": ("STRING", {
                    "multiline": True, 
                    "default": "Hello, how are you?",
                    "tooltip": "Your prompt to the AI"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7, 
                    "min": 0.0, 
                    "max": 2.0, 
                    "step": 0.05,
                    "tooltip": "Lower values make output more deterministic, higher more creative"
                }),
                "max_tokens": ("INT", {
                    "default": 1024, 
                    "min": 1, 
                    "max": 32768, 
                    "step": 1,
                    "tooltip": "Maximum number of tokens to generate"
                }),
                "top_p": ("FLOAT", {
                    "default": 0.9, 
                    "min": 0.1, 
                    "max": 1.0, 
                    "step": 0.01,
                    "tooltip": "Nucleus sampling parameter (0.1-1.0)"
                }),
            },
            "optional": {
                "api_key_override": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "tooltip": "API key from provider node (overrides the manual api_key field)"
                }),
                "conversation_history": ("STRING", {
                    "default": "", 
                    "multiline": True,
                    "tooltip": "Previous conversation context (optional)"
                }),
                "system_message": ("STRING", {
                    "default": "", 
                    "multiline": True,
                    "tooltip": "System message to set AI behavior (optional)"
                }),
                "seed": ("INT", {
                    "default": -1, 
                    "min": -1, 
                    "max": 2**32-1,
                    "tooltip": "Random seed (-1 for random)"
                }),
            }
        }
    
    def generate(self, api_key, model, prompt, temperature, max_tokens, top_p, 
                 api_key_override="", conversation_history="", system_message="", seed=-1, **kwargs):
        """Generate text response with conversation history support"""
        
        # Set random seed if specified
        if seed != -1:
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
        
        # Use API key from provider node, then manual input, then environment variable
        final_api_key = api_key_override.strip() or api_key.strip() or os.getenv('GROQ_API_KEY', '')
        if not final_api_key:
            return ("Error: No API key provided. Please set GROQ_API_KEY environment variable or provide it in the node.",)
        
        # Initialize GROQ client
        try:
            client = Groq(api_key=final_api_key)
        except Exception as e:
            return (f"Error initializing GROQ client: {str(e)}",)
        
        # Prepare messages
        messages = []
        
        # Add system message if provided
        if system_message.strip():
            messages.append({"role": "system", "content": system_message.strip()})
        
        # Parse conversation history if provided
        if conversation_history.strip():
            try:
                # Try to parse as JSON first
                if conversation_history.strip().startswith('['):
                    history = json.loads(conversation_history)
                    if isinstance(history, list):
                        messages.extend(history)
                else:
                    # Treat as plain text context
                    messages.append({"role": "assistant", "content": conversation_history.strip()})
            except json.JSONDecodeError:
                # If not valid JSON, treat as plain text context
                messages.append({"role": "assistant", "content": conversation_history.strip()})
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Prepare request data
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
        }
        
        try:
            # Make the API call
            response = client.chat.completions.create(**data)
            
            # Extract the response content
            if hasattr(response, 'choices') and len(response.choices) > 0:
                choice = response.choices[0]
                content = getattr(choice.message, 'content', '')
                return (content or "No response generated",)
            
            return ("No response generated",)
            
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid_api_key" in error_msg.lower():
                return ("Error: Invalid API Key. Please check your GROQ_API_KEY.",)
            elif "400" in error_msg:
                return (f"Error: Bad request - {error_msg}",)
            else:
                return (f"Error: {error_msg}",)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "GroqLLMNode": GroqLLMNode,
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "GroqLLMNode": "GROQ LLM Node (Legacy)",
}
