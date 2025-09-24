import os
from typing import Dict, List, Optional, Tuple, Any
from groq import Groq

from .utils.base_node import GroqNode, get_model_choices, ModelType

class GroqMusicToArtPrompter(GroqNode):
    """GROQ Music-to-Art Prompter - Analyze music/audio and generate visual art prompts that match the mood"""
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("art_prompt", "mood_analysis")
    FUNCTION = "generate_music_art_prompt"
    CATEGORY = "GroqPrompt/Art Generation"
    
    @classmethod
    def INPUT_TYPES(cls):
        audio_models = get_model_choices(ModelType.AUDIO)
        
        return {
            "required": {
                "api_key": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "tooltip": "Your GROQ API key. Leave empty to use GROQ_API_KEY environment variable."
                }),
                "music_description": ("STRING", {
                    "multiline": True,
                    "default": "Upbeat jazz with saxophone and piano",
                    "tooltip": "Describe the music/audio or paste lyrics/transcription"
                }),
                "music_genre": (["jazz", "classical", "rock", "electronic", "ambient", "folk", "blues", "hip_hop", "pop", "metal", "reggae", "country", "world", "experimental"], {
                    "default": "jazz",
                    "tooltip": "Primary music genre"
                }),
                "mood_intensity": (["subtle", "moderate", "strong", "intense"], {
                    "default": "moderate",
                    "tooltip": "How strongly the music mood should influence the art"
                }),
                "art_style": (["abstract", "realistic", "impressionist", "surreal", "minimalist", "expressionist", "psychedelic", "geometric"], {
                    "default": "abstract",
                    "tooltip": "Visual art style to match the music"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.0, 
                    "min": 0.0, 
                    "max": 1.0, 
                    "step": 0.1,
                    "tooltip": "Lower values make output more deterministic, higher more creative"
                }),
            }
        }
    
    def generate_music_art_prompt(self, api_key, music_description, music_genre, mood_intensity, art_style, temperature):
        # Use provided API key or fall back to environment variable
        api_key = api_key.strip() or os.getenv('GROQ_API_KEY', '')
        if not api_key:
            raise ValueError("No API key provided. Please set GROQ_API_KEY environment variable or provide it in the node.")
        
        # Initialize GROQ client
        client = Groq(api_key=api_key)
        
        # Create intensity modifiers
        intensity_modifiers = {
            "subtle": "lightly influenced by, hints of musical elements",
            "moderate": "clearly inspired by, moderate musical influence",
            "strong": "heavily influenced by, strong musical characteristics",
            "intense": "completely embodying, intense musical translation"
        }
        
        # Prepare the main prompt
        main_prompt = f"""You are an expert at translating music into visual art concepts. Create a detailed Stable Diffusion art prompt based on this music:

MUSIC DESCRIPTION: {music_description}
GENRE: {music_genre}
VISUAL STYLE: {art_style}
INTENSITY: {intensity_modifiers[mood_intensity]}

Analyze the music and create a visual art prompt that captures:
1. The emotional mood and energy of the music
2. Visual metaphors for the musical elements (rhythm, melody, harmony)
3. Colors that match the musical tone and genre
4. Composition and movement that reflects the music's flow
5. Artistic techniques that embody the musical style

Create a comprehensive Stable Diffusion prompt that would generate art visually representing this music. Include specific artistic terms, colors, lighting, and composition details."""
        
        try:
            # Make the API call for art prompt
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert at synesthesia - translating music into visual art. You understand how musical elements correspond to visual elements and can create compelling art prompts."},
                    {"role": "user", "content": main_prompt}
                ],
                temperature=temperature,
                max_tokens=1024,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            art_prompt = ""
            mood_analysis = ""
            
            # Extract the main response
            if hasattr(response, 'choices') and len(response.choices) > 0:
                art_prompt = response.choices[0].message.content
            
            # Generate mood analysis
            mood_prompt = f"""Analyze the mood and emotional characteristics of this music for artistic reference:

MUSIC: {music_description}
GENRE: {music_genre}

Provide a detailed mood analysis including:
1. Primary emotions conveyed
2. Energy level and tempo feel
3. Color associations
4. Movement and flow characteristics
5. Overall artistic atmosphere

Keep this concise but insightful for artists."""
            
            mood_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a music analyst specializing in emotional and artistic interpretation of music."},
                    {"role": "user", "content": mood_prompt}
                ],
                temperature=0.3,
                max_tokens=512,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            if hasattr(mood_response, 'choices') and len(mood_response.choices) > 0:
                mood_analysis = mood_response.choices[0].message.content
            
            return (art_prompt or "No art prompt generated", mood_analysis or f"Genre: {music_genre}, Style: {art_style}, Intensity: {mood_intensity}")
            
        except Exception as e:
            return (f"Error: {str(e)}", "")

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "GroqMusicToArtPrompter": GroqMusicToArtPrompter,
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "GroqMusicToArtPrompter": "GROQ Music-to-Art Prompter",
}
