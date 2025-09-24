import os
import json
from typing import Dict, List, Optional, Any
from groq import Groq

from .utils.base_node import GroqNode

class GroqStyleTransferPrompter(GroqNode):
    """GROQ Style Transfer Prompter - Convert art descriptions into consistent Stable Diffusion prompts"""
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("style_prompt", "negative_prompt")
    FUNCTION = "generate_style_prompt"
    CATEGORY = "GroqPrompt/Art Generation"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "tooltip": "Your GROQ API key. Leave empty to use GROQ_API_KEY environment variable."
                }),
                "style_description": ("STRING", {
                    "multiline": True, 
                    "default": "Van Gogh's Starry Night style with swirling brushstrokes and vibrant colors",
                    "tooltip": "Describe the art style, artist, or reference you want to emulate"
                }),
                "art_medium": (["digital_art", "oil_painting", "watercolor", "acrylic", "pencil_drawing", "charcoal", "pastel", "mixed_media", "photography", "3d_render"], {
                    "default": "digital_art",
                    "tooltip": "Target art medium for the style"
                }),
                "subject_matter": (["portrait", "landscape", "still_life", "abstract", "fantasy", "sci_fi", "architecture", "nature", "urban", "character"], {
                    "default": "portrait",
                    "tooltip": "Main subject matter for the artwork"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.2, 
                    "min": 0.0, 
                    "max": 1.0, 
                    "step": 0.1,
                    "tooltip": "Lower values make output more deterministic, higher more creative"
                }),
                "max_tokens": ("INT", {
                    "default": 1024, 
                    "min": 1, 
                    "max": 4096,
                    "tooltip": "Maximum number of tokens to generate"
                }),
                "include_negative": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Generate negative prompt to avoid unwanted elements"
                }),
                "prompt_strength": (["subtle", "moderate", "strong", "extreme"], {
                    "default": "moderate",
                    "tooltip": "How strongly to apply the style characteristics"
                }),
            }
        }
    
    def generate_style_prompt(self, api_key, style_description, art_medium, subject_matter, temperature, max_tokens, include_negative, prompt_strength):
        # Use provided API key or fall back to environment variable
        api_key = api_key.strip() or os.getenv('GROQ_API_KEY', '')
        if not api_key:
            raise ValueError("No API key provided. Please set GROQ_API_KEY environment variable or provide it in the node.")
        
        # Initialize GROQ client
        client = Groq(api_key=api_key)
        
        # Create strength modifiers
        strength_modifiers = {
            "subtle": "lightly inspired by, hints of",
            "moderate": "in the style of, influenced by", 
            "strong": "heavily inspired by, strong characteristics of",
            "extreme": "exact style of, perfect emulation of"
        }
        
        # Prepare the main prompt
        main_prompt = f"""Convert this art style description into a detailed Stable Diffusion prompt for {subject_matter} artwork:

Style Description: {style_description}
Art Medium: {art_medium}
Strength: {strength_modifiers[prompt_strength]}

Create a comprehensive prompt that captures:
1. The visual characteristics of the style
2. Technical art terms and techniques
3. Color palette and lighting
4. Composition and mood
5. Quality and detail descriptors

Format as a single, comma-separated prompt optimized for AI art generation."""
        
        try:
            # Make the API call for main prompt
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert art prompt engineer specializing in Stable Diffusion prompts. Create detailed, effective prompts that capture artistic styles accurately."},
                    {"role": "user", "content": main_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            style_prompt = ""
            negative_prompt = ""
            
            # Extract the main response
            if hasattr(response, 'choices') and len(response.choices) > 0:
                style_prompt = response.choices[0].message.content
            
            # Generate negative prompt if requested
            if include_negative:
                negative_prompt_request = f"""Create a negative prompt to avoid unwanted elements when generating {subject_matter} artwork in {art_medium} style. Include common issues like:
- Poor quality descriptors
- Unwanted artistic styles that conflict with {style_description}
- Technical problems (blurry, distorted, etc.)
- Inappropriate elements for {subject_matter}

Format as comma-separated negative terms."""
                
                neg_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert at creating negative prompts for AI art generation."},
                        {"role": "user", "content": negative_prompt_request}
                    ],
                    temperature=0.3,
                    max_tokens=512,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                
                if hasattr(neg_response, 'choices') and len(neg_response.choices) > 0:
                    negative_prompt = neg_response.choices[0].message.content
            
            return (style_prompt or "No style prompt generated", negative_prompt)
            
        except Exception as e:
            return (f"Error: {str(e)}", "")

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "GroqStyleTransferPrompter": GroqStyleTransferPrompter,
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "GroqStyleTransferPrompter": "GROQ Style Transfer Prompter",
}
