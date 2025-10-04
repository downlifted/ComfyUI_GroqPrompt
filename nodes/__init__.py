import os
import importlib.util
from typing import Dict, Any

# Initialize empty mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# List of node files to import
NODE_FILES = [
    'api_key_node',       # GROQ API Key Manager & Provider
    'llm_node',           # GROQ Art Prompt Enhancer
    'vision_node',        # GROQ Art Prompt Generator  
    'document_analyzer_node',  # GROQ Style Transfer Prompter
    'code_assistant_node',     # GROQ Workflow Helper
    'audio_processor_node',    # GROQ Music-to-Art Prompter
    'legacy_node',        # Legacy GroqLLMNode for backward compatibility
]

# Import all node files and combine their mappings
for node_file in NODE_FILES:
    try:
        module_name = f"{__name__}.{node_file}"
        module_path = os.path.join(os.path.dirname(__file__), f"{node_file}.py")
        
        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Update the mappings
            if hasattr(module, 'NODE_CLASS_MAPPINGS'):
                NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
            if hasattr(module, 'NODE_DISPLAY_NAME_MAPPINGS'):
                NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
                
    except Exception as e:
        print(f"Error loading node module {node_file}: {str(e)}")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
