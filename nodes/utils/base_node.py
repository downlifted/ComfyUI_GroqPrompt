import os
import json
import base64
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union, Any
from enum import Enum
from dataclasses import dataclass
from groq import Groq, GroqError
from PIL import Image, ImageEnhance, ImageOps
import torch
import numpy as np

# Constants
DEFAULT_API_KEY = os.getenv('GROQ_API_KEY', '')
MAX_TOKENS = 8192
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9
DEFAULT_MAX_TOKENS = 1024

class ModelType(Enum):
    TEXT = "text"
    VISION = "vision"
    AUDIO = "audio"
    EMBEDDING = "embedding"
    CODE = "code"

@dataclass
class ModelInfo:
    id: str
    name: str
    type: ModelType
    description: str = ""
    max_tokens: int = 4096
    supports_images: bool = False
    supports_audio: bool = False
    supports_functions: bool = False

# Available GROQ models - Updated from mnemic nodes
LLM_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile", 
    "moonshotai/kimi-k2-instruct-0905",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "deepseek-r1-distill-llama-70b",
    "qwen-qwq-32b",
    "gemma2-9b-it",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "llama3-8b-8192",
    "llama3-70b-8192",
    "llama-guard-3-8b",
    # Additional models for compatibility
    "mixtral-8x7b-32768",
    "gemma-7b-it",
]

VLM_MODELS = [
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llava-v1.5-7b-4096-preview",
]

# Additional UNET model definitions for compatibility (these are typically not GROQ models)
UNET_MODELS = [
    "T2V/Wan2_2-T2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors",
    "T2V/Wan2_2-T2V-A14B_HIGH_fp8_e4m3fn_scaled_KJ.safetensors", 
    "qwen_image_edit_2509_fp8_e4m3fn.safetensors",
    "qwen_image_edit_bf16.safetensors",  # Added missing model
]

# Upscale model definitions for compatibility
UPSCALE_MODELS = [
    "4x-ClearRealityV1.pth",
    "4x-UltraSharp.pth",
    "1x-ITF-SkinDiffDetail-Lite-v1.pth",  # Added missing model
]

# Available GROQ models
AVAILABLE_MODELS = [
    # Text models
    ModelInfo(
        id="llama3-70b-8192",
        name="LLaMA 3 70B",
        type=ModelType.TEXT,
        description="Meta's 70B parameter model, great for complex tasks",
        max_tokens=8192,
        supports_functions=True
    ),
    ModelInfo(
        id="llama3-8b-8192",
        name="LLaMA 3 8B",
        type=ModelType.TEXT,
        description="Meta's 8B parameter model, fast and efficient",
        max_tokens=8192,
    ),
    ModelInfo(
        id="mixtral-8x7b-32768",
        name="Mixtral 8x7B",
        type=ModelType.TEXT,
        description="High-quality mixture of experts model",
        max_tokens=32768,
        supports_functions=True
    ),
    # Vision models
    ModelInfo(
        id="meta-llama/llama-4-maverick-17b-128e-instruct",
        name="LLaMA 4 Maverick 17B",
        type=ModelType.VISION,
        description="Vision-language model for image analysis",
        max_tokens=8192,
        supports_images=True
    ),
    # Code models
    ModelInfo(
        id="llama-3.3-70b",
        name="LLaMA 3.3 70B Versatile",
        type=ModelType.CODE,
        description="Versatile model for code generation and understanding",
        max_tokens=8192,
        supports_functions=True
    ),
]

def get_model_choices(model_type: ModelType) -> List[str]:
    """Get model choices by type"""
    if model_type == ModelType.TEXT:
        return LLM_MODELS
    elif model_type == ModelType.VISION:
        return VLM_MODELS
    elif model_type == ModelType.CODE:
        return LLM_MODELS  # Use LLM models for code tasks
    else:
        return LLM_MODELS  # Default to LLM models

def get_unet_models() -> List[str]:
    """Get UNET model choices"""
    return UNET_MODELS

def get_upscale_models() -> List[str]:
    """Get upscale model choices"""
    return UPSCALE_MODELS

def get_model_descriptions() -> Dict[str, str]:
    """Get descriptions for all models"""
    return {model.id: model.name for model in AVAILABLE_MODELS}

def process_image(image_tensor, crop_region=None, resize_dims=None, enhance=False):
    """Process image tensor with optional cropping, resizing, and enhancement"""
    # Convert tensor to PIL Image
    if isinstance(image_tensor, torch.Tensor):
        image = 255.0 * image_tensor.cpu().numpy()
        image = Image.fromarray(np.clip(image, 0, 255).astype(np.uint8))
    elif isinstance(image_tensor, Image.Image):
        image = image_tensor
    else:
        raise ValueError("Unsupported image format. Expected tensor or PIL Image.")
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Apply cropping if specified
    if crop_region and isinstance(crop_region, (tuple, list)) and len(crop_region) == 4:
        left, top, right, bottom = map(int, crop_region)
        width, height = image.size
        left = max(0, min(left, width - 1))
        top = max(0, min(top, height - 1))
        right = max(left + 1, min(right, width))
        bottom = max(top + 1, min(bottom, height))
        image = image.crop((left, top, right, bottom))
    
    # Apply resizing if specified
    if resize_dims and isinstance(resize_dims, (tuple, list)) and len(resize_dims) == 2:
        image = image.resize(resize_dims, Image.LANCZOS)
    
    # Apply enhancement if requested
    if enhance:
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
    
    return image

class GroqNode:
    """Base class for GROQ nodes with common functionality"""
    
    @classmethod
    def load_prompt_options(cls, prompt_files):
        """Load prompt options from JSON files"""
        prompt_options = {}
        for file_path in prompt_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            prompt_options.update(data)
            except Exception as e:
                print(f"Error loading prompt file {file_path}: {str(e)}")
        return prompt_options
    
    def get_prompt_content(self, prompt_name, prompt_options):
        """Get content for a specific prompt name"""
        return prompt_options.get(prompt_name, "")
    
    def tensor_to_pil(self, image_tensor):
        """Convert a PyTorch tensor to a PIL Image"""
        if image_tensor.dim() == 4:  # Batch of images
            image_tensor = image_tensor[0]  # Take first image in batch
        
        # Convert from CHW to HWC and denormalize if needed
        if image_tensor.shape[0] <= 4:  # CHW format
            image_tensor = image_tensor.permute(1, 2, 0)
        
        # If the image is in [0, 1] range, scale to [0, 255]
        if image_tensor.max() <= 1.0:
            image_tensor = image_tensor * 255.0
        
        # Convert to numpy and ensure it's uint8
        image_np = image_tensor.cpu().numpy().astype(np.uint8)
        return Image.fromarray(image_np)
    
    def encode_image(self, image_pil):
        """Encode PIL Image to base64"""
        buffered = BytesIO()
        image_pil.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
