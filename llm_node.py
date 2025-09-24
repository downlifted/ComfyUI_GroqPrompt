import os
import json
import random
import numpy as np
import torch
import re
from typing import Dict, List, Optional, Any
from groq import Groq

from .utils.base_node import GroqNode, get_model_descriptions, get_model_choices, ModelType

class GroqArtPromptEnhancer(GroqNode):
    """GROQ Art Prompt Enhancer - Enhance and refine art prompts for better AI generation results"""
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("enhanced_prompt",)
    FUNCTION = "enhance_prompt"
    CATEGORY = "GroqPrompt/Art Generation"
    
    @classmethod
    def INPUT_TYPES(cls):
        # Get model descriptions for tooltips
        model_descriptions = get_model_descriptions()
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
                "base_prompt": ("STRING", {
                    "multiline": True, 
                    "default": "beautiful woman, portrait",
                    "tooltip": "Your basic art prompt to enhance"
                }),
                "enhancement_type": (["quality_boost", "style_enhance", "detail_add", "lighting_improve", "composition_fix", "color_enhance", "artistic_refine"], {
                    "default": "quality_boost",
                    "tooltip": "Type of enhancement to apply"
                }),
                "target_model": (["SDXL", "SD1.5", "Midjourney", "DALL-E", "Any"], {
                    "default": "SDXL",
                    "tooltip": "Target AI art model for optimization"
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
                "frequency_penalty": ("FLOAT", {
                    "default": 0.0, 
                    "min": -2.0, 
                    "max": 2.0, 
                    "step": 0.1,
                    "tooltip": "Positive values reduce repetition"
                }),
                "presence_penalty": ("FLOAT", {
                    "default": 0.0, 
                    "min": -2.0, 
                    "max": 2.0, 
                    "step": 0.1,
                    "tooltip": "Positive values encourage new topics"
                }),
                "seed": ("INT", {
                    "default": -1, 
                    "min": -1, 
                    "max": 2**32-1,
                    "tooltip": "Random seed (-1 for random)"
                }),
                "prompt_length": (["short", "medium", "long", "very_long"], {
                    "default": "medium",
                    "tooltip": "Target length for the enhanced prompt"
                }),
                "creativity_level": (["conservative", "moderate", "creative", "experimental"], {
                    "default": "moderate",
                    "tooltip": "How creative to be with enhancements"
                }),
            }
        }
    
    def enhance_prompt(self, api_key, model, base_prompt, enhancement_type, target_model,
                      temperature, max_tokens, top_p, frequency_penalty, presence_penalty,
                      seed, prompt_length, creativity_level, **kwargs):
        
        # Set random seed if specified
        if seed != -1:
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
        
        # Use provided API key or fall back to environment variable
        api_key = api_key.strip() or os.getenv('GROQ_API_KEY', '')
        if not api_key:
            raise ValueError("No API key provided. Please set GROQ_API_KEY environment variable or provide it in the node.")
        
        # Initialize GROQ client
        client = Groq(api_key=api_key)
        
        # Create enhancement instructions based on type
        enhancement_instructions = {
            "quality_boost": "Add quality descriptors like 'high resolution', 'detailed', 'professional', 'masterpiece'",
            "style_enhance": "Add artistic style descriptors and technique specifications",
            "detail_add": "Add specific details about textures, materials, and fine elements",
            "lighting_improve": "Add sophisticated lighting descriptions and atmosphere",
            "composition_fix": "Add composition rules like rule of thirds, framing, perspective",
            "color_enhance": "Add rich color descriptions and palette specifications",
            "artistic_refine": "Add artistic medium specifications and technique details"
        }
        
        length_targets = {
            "short": "20-40 words",
            "medium": "40-80 words", 
            "long": "80-150 words",
            "very_long": "150+ words with extensive detail"
        }
        
        creativity_levels = {
            "conservative": "Stay close to the original, add minimal safe enhancements",
            "moderate": "Add moderate enhancements while keeping the core concept",
            "creative": "Be creative with additions and interpretations",
            "experimental": "Be very creative and add unique artistic elements"
        }
        
        # Create the enhancement prompt
        enhancement_prompt = f"""You are an expert AI art prompt engineer. Enhance this basic art prompt for {target_model}:

ORIGINAL PROMPT: {base_prompt}

ENHANCEMENT TYPE: {enhancement_instructions[enhancement_type]}
TARGET LENGTH: {length_targets[prompt_length]}
CREATIVITY LEVEL: {creativity_levels[creativity_level]}
TARGET MODEL: {target_model}

Please enhance this prompt by:
1. {enhancement_instructions[enhancement_type]}
2. Optimizing for {target_model} specifically
3. Maintaining the core concept while improving quality
4. Using effective prompt engineering techniques
5. Ensuring the result is {length_targets[prompt_length]}

Return only the enhanced prompt, no explanations."""
        
        # Prepare messages
        messages = [
            {"role": "system", "content": "You are an expert AI art prompt engineer specializing in creating high-quality prompts for various AI art models. You understand what makes prompts effective and how to optimize them for different platforms."},
            {"role": "user", "content": enhancement_prompt}
        ]
        
        # Prepare request data
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }
        
        # Remove function calling - not needed for art prompt enhancement
        
        try:
            # Make the API call
            response = client.chat.completions.create(**data)
            
            # Extract the response content
            if hasattr(response, 'choices') and len(response.choices) > 0:
                choice = response.choices[0]
                content = getattr(choice.message, 'content', '')
                
                # Clean up the response - remove any explanatory text, just return the prompt
                content = content.strip()
                
                return (content,)
            
            return ("No response generated",)
            
        except Exception as e:
            return (f"Error: {str(e)}",)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "GroqArtPromptEnhancer": GroqArtPromptEnhancer,
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "GroqArtPromptEnhancer": "GROQ Art Prompt Enhancer",
}
