import os
import re
from typing import Dict, List, Optional, Tuple, Any
from groq import Groq

from .utils.base_node import GroqNode, get_model_choices, ModelType

class GroqWorkflowHelper(GroqNode):
    """GROQ Workflow Helper - Generate ComfyUI workflows, fix issues, and provide technical assistance"""
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("workflow_json", "instructions")
    FUNCTION = "generate_workflow"
    CATEGORY = "GroqPrompt/Workflow"
    
    @classmethod
    def INPUT_TYPES(cls):
        code_models = get_model_choices(ModelType.CODE)
        
        return {
            "required": {
                "api_key": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "tooltip": "Your GROQ API key. Leave empty to use GROQ_API_KEY environment variable."
                }),
                "model": (get_model_choices(ModelType.CODE), {
                    "default": "llama-3.3-70b-versatile",
                    "tooltip": "Select a model for workflow generation"
                }),
                "workflow_request": ("STRING", {
                    "multiline": True, 
                    "default": "Create a basic txt2img workflow with SDXL",
                    "tooltip": "Describe the ComfyUI workflow you want to create or the issue you need help with"
                }),
                "workflow_type": (["txt2img", "img2img", "inpainting", "controlnet", "upscaling", "animation", "batch_processing", "custom", "debug_existing"], {
                    "default": "txt2img",
                    "tooltip": "Type of workflow to generate"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.2, 
                    "min": 0.0, 
                    "max": 1.0, 
                    "step": 0.1,
                    "tooltip": "Lower values make output more deterministic, higher more creative"
                }),
                "max_tokens": ("INT", {
                    "default": 2048, 
                    "min": 1, 
                    "max": 8192,
                    "tooltip": "Maximum number of tokens to generate"
                }),
                "include_instructions": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Include step-by-step instructions for using the workflow"
                }),
                "model_preference": (["SDXL", "SD1.5", "Any", "Latest"], {
                    "default": "SDXL",
                    "tooltip": "Preferred Stable Diffusion model for the workflow"
                }),
            },
            "optional": {
                "existing_workflow": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Paste existing workflow JSON here for debugging/modification"
                }),
            }
        }
    
    def generate_workflow(self, api_key, model, workflow_request, workflow_type, temperature, max_tokens, include_instructions, model_preference, existing_workflow=""):
        # Use provided API key or fall back to environment variable
        api_key = api_key.strip() or os.getenv('GROQ_API_KEY', '')
        if not api_key:
            raise ValueError("No API key provided. Please set GROQ_API_KEY environment variable or provide it in the node.")
        
        # Initialize GROQ client
        client = Groq(api_key=api_key)
        
        # Prepare the prompt based on workflow type
        if existing_workflow.strip():
            # Debug/modify existing workflow
            prompt = f"""You are a ComfyUI workflow expert. Analyze and improve this existing workflow:

EXISTING WORKFLOW:
{existing_workflow}

USER REQUEST: {workflow_request}

Please:
1. Identify any issues or improvements needed
2. Provide the corrected/improved workflow JSON
3. Explain what changes were made and why
4. Ensure all node connections are valid

Focus on ComfyUI-specific nodes and proper JSON structure."""
        else:
            # Generate new workflow
            workflow_templates = {
                "txt2img": "a basic text-to-image generation workflow",
                "img2img": "an image-to-image transformation workflow", 
                "inpainting": "an inpainting workflow for editing parts of images",
                "controlnet": "a ControlNet workflow for guided generation",
                "upscaling": "an upscaling workflow for enhancing image resolution",
                "animation": "an animation workflow for creating video/gif sequences",
                "batch_processing": "a batch processing workflow for multiple images",
                "custom": "a custom workflow based on specific requirements",
                "debug_existing": "help debugging an existing workflow"
            }
            
            prompt = f"""You are a ComfyUI workflow expert. Create {workflow_templates.get(workflow_type, 'a workflow')} for ComfyUI.

USER REQUEST: {workflow_request}
PREFERRED MODEL: {model_preference}
WORKFLOW TYPE: {workflow_type}

Please provide:
1. Complete ComfyUI workflow JSON that can be directly loaded
2. Ensure all node IDs, connections, and parameters are valid
3. Use appropriate nodes for {model_preference} models
4. Include proper VAE, samplers, and schedulers
5. Make sure the workflow is functional and follows ComfyUI standards

The JSON should be ready to copy-paste into ComfyUI."""
        
        try:
            # Make the API call
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a ComfyUI workflow expert with deep knowledge of node connections, parameters, and JSON structure. Always provide valid, working workflows."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            workflow_json = ""
            instructions = ""
            
            # Extract the response content
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].message.content
                
                # Try to extract JSON workflow from the response
                json_blocks = re.findall(r'```(?:json)?\n(.*?)\n```', content, re.DOTALL)
                if json_blocks:
                    workflow_json = json_blocks[0].strip()
                else:
                    # If no code blocks, try to find JSON-like content
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        workflow_json = json_match.group(0)
                    else:
                        workflow_json = content
                
                # Generate instructions if requested
                if include_instructions:
                    instructions_prompt = f"""Based on this ComfyUI workflow request: "{workflow_request}", provide step-by-step instructions for:

1. How to load and use this workflow in ComfyUI
2. What nodes are required (if any custom nodes needed)
3. How to modify key parameters
4. Common troubleshooting tips
5. Expected results and usage tips

Keep instructions clear and beginner-friendly."""
                    
                    inst_response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "You are a helpful ComfyUI instructor. Provide clear, step-by-step guidance."},
                            {"role": "user", "content": instructions_prompt}
                        ],
                        temperature=0.3,
                        max_tokens=1024,
                        top_p=1.0,
                        frequency_penalty=0.0,
                        presence_penalty=0.0
                    )
                    
                    if hasattr(inst_response, 'choices') and len(inst_response.choices) > 0:
                        instructions = inst_response.choices[0].message.content
                
                return (workflow_json or "No workflow generated", instructions)
            
            return ("No workflow generated", "No response received")
            
        except Exception as e:
            return (f"Error: {str(e)}", "")

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "GroqWorkflowHelper": GroqWorkflowHelper,
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "GroqWorkflowHelper": "GROQ Workflow Helper",
}
