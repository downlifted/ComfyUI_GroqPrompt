import os
import json
import base64
import numpy as np
import torch
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Any
from PIL import Image, ImageEnhance
from groq import Groq

from .utils.base_node import GroqNode, get_model_choices, ModelType

class GroqArtPromptGenerator(GroqNode):
    """GROQ Art Prompt Generator - Analyze images and create detailed art prompts for Stable Diffusion"""
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("art_prompt", "style_notes")
    FUNCTION = "generate_art_prompt"
    CATEGORY = "GroqPrompt/Art Generation"
    
    @classmethod
    def INPUT_TYPES(cls):
        vision_models = get_model_choices(ModelType.VISION)
        
        return {
            "required": {
                "api_key": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "tooltip": "Your GROQ API key. Leave empty to use GROQ_API_KEY environment variable."
                }),
                "model": (vision_models, {
                    "default": "meta-llama/llama-4-maverick-17b-128e-instruct",
                    "tooltip": "Select a vision model for image analysis"
                }),
                "images": ("IMAGE", {
                    "tooltip": "Input image(s) to analyze"
                }),
                "prompt": ("STRING", {
                    "multiline": True, 
                    "default": "Create a detailed art prompt for Stable Diffusion based on this image. Include style, lighting, composition, colors, and artistic techniques.",
                    "tooltip": "Custom prompt for art generation (leave default for best results)"
                }),
                "art_style": (["photorealistic", "digital_art", "oil_painting", "watercolor", "anime", "concept_art", "fantasy", "sci_fi", "portrait", "landscape", "abstract", "vintage", "cyberpunk", "steampunk"], {
                    "default": "photorealistic",
                    "tooltip": "Target art style for the generated prompt"
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
                "prompt_length": (["short", "medium", "detailed", "comprehensive"], {
                    "default": "detailed",
                    "tooltip": "Length and detail level of the generated art prompt"
                }),
                "include_technical": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Include technical photography/art terms (aperture, lighting, etc.)"
                }),
            },
            "optional": {
                "reference_image": ("IMAGE", {
                    "tooltip": "Optional reference image for comparison"
                }),
                "crop_region": ("TUPLE", {
                    "default": None, 
                    "forceInput": False,
                    "tooltip": "Optional region to crop (left, top, right, bottom)"
                }),
            }
        }
    
    def generate_art_prompt(self, api_key, model, images, prompt, art_style, temperature,
                           max_tokens, prompt_length, include_technical, reference_image=None,
                           crop_region=None, **kwargs):
        
        # Use provided API key or fall back to environment variable
        api_key = api_key.strip() or os.getenv('GROQ_API_KEY', '')
        if not api_key:
            raise ValueError("No API key provided. Please set GROQ_API_KEY environment variable or provide it in the node.")
        
        # Initialize GROQ client
        client = Groq(api_key=api_key)
        
        # Process the main image(s)
        if not isinstance(images, (list, tuple)):
            images = [images]
        
        # Convert images to base64
        image_data = []
        for img in images:
            # Convert tensor to PIL Image
            img_pil = self.tensor_to_pil(img)
            
            # Apply cropping if specified
            if crop_region and len(crop_region) == 4:
                img_pil = img_pil.crop(crop_region)
            
            # Encode to base64
            img_data = self.encode_image(img_pil)
            image_data.append(f"data:image/jpeg;base64,{img_data}")
        
        # Process reference image if provided
        if reference_image is not None:
            ref_img_pil = self.tensor_to_pil(reference_image)
            ref_img_data = self.encode_image(ref_img_pil)
            image_data.append(f"data:image/jpeg;base64,{ref_img_data}")
        
        # Create the enhanced prompt based on art style and detail level
        enhanced_prompt = self._create_art_prompt(prompt, art_style, prompt_length, include_technical)
        
        # Prepare messages
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": enhanced_prompt}
                ]
            }
        ]
        
        # Add images to the message
        for img_data in image_data:
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {"url": img_data}
            })
        
        # Make the API call
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Extract the response content
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].message.content
                
                # Extract style notes
                style_notes = f"Style: {art_style}, Length: {prompt_length}"
                if include_technical:
                    style_notes += ", Technical terms included"
                
                return (content, style_notes)
            
            return ("No response generated", "")
            
        except Exception as e:
            return (f"Error: {str(e)}", "")
    
    def _create_art_prompt(self, base_prompt, art_style, prompt_length, include_technical):
        """Create an enhanced prompt for art generation"""
        length_instructions = {
            "short": "Create a concise art prompt (20-40 words)",
            "medium": "Create a moderate art prompt (40-80 words)", 
            "detailed": "Create a detailed art prompt (80-150 words)",
            "comprehensive": "Create a comprehensive art prompt (150+ words with extensive detail)"
        }
        
        style_guidance = {
            "photorealistic": "photorealistic, high resolution, professional photography",
            "digital_art": "digital art, concept art, trending on artstation",
            "oil_painting": "oil painting, traditional art, painterly brushstrokes",
            "watercolor": "watercolor painting, soft washes, artistic medium",
            "anime": "anime style, manga art, cel shading",
            "concept_art": "concept art, matte painting, cinematic",
            "fantasy": "fantasy art, magical, ethereal, mystical",
            "sci_fi": "sci-fi art, futuristic, cyberpunk, high-tech",
            "portrait": "portrait photography, character focus, detailed face",
            "landscape": "landscape art, environmental, scenic vista",
            "abstract": "abstract art, non-representational, artistic interpretation",
            "vintage": "vintage style, retro aesthetic, aged look",
            "cyberpunk": "cyberpunk style, neon lights, dystopian future",
            "steampunk": "steampunk aesthetic, Victorian era, mechanical elements"
        }
        
        technical_terms = ""
        if include_technical:
            technical_terms = " Include technical terms like: lighting (golden hour, rim light, soft shadows), camera settings (shallow depth of field, bokeh, wide angle), and artistic techniques (rule of thirds, leading lines, color grading)."
        
        enhanced_prompt = f"{base_prompt}\n\nTarget style: {style_guidance.get(art_style, art_style)}. {length_instructions[prompt_length]}.{technical_terms} Focus on creating a prompt that would work well with Stable Diffusion or similar AI art generators."
        
        return enhanced_prompt
    
    def _extract_image_metadata(self, image_tensor):
        """Extract basic metadata from image tensor"""
        try:
            img = self.tensor_to_pil(image_tensor)
            
            metadata = {
                "dimensions": f"{img.width}x{img.height}",
                "mode": img.mode,
                "format": getattr(img, 'format', 'unknown'),
                "size_kb": len(img.tobytes()) / 1024 if hasattr(img, 'tobytes') else "unknown"
            }
            
            return json.dumps(metadata, indent=2)
        except Exception as e:
            return f"Error extracting metadata: {str(e)}"

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "GroqArtPromptGenerator": GroqArtPromptGenerator,
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "GroqArtPromptGenerator": "GROQ Art Prompt Generator",
}
