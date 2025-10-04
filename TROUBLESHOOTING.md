# ComfyUI GroqPrompt Troubleshooting Guide

This guide helps you resolve common issues with the ComfyUI GroqPrompt extension.

## Quick Fixes for Common Errors

### 1. `GroqLLMNode.generate() got an unexpected keyword argument 'conversation_history'`

**What it means**: You're using an old workflow that references a legacy node structure.

**Solution**: 
- ✅ **Fixed**: We've added a backward-compatible `GroqLLMNode` class
- The legacy node now accepts the `conversation_history` parameter
- Your old workflows should work without modification

### 2. `Response status: 401, Response body: {"error":{"message":"Invalid API Key"...}}`

**What it means**: Your GROQ API key is missing, invalid, or expired.

**Solutions**:

#### Option A: Use the Setup Script
```bash
python setup_api_key.py
```

#### Option B: Manual Setup (Windows)
```cmd
setx GROQ_API_KEY "your_api_key_here"
```

#### Option C: Manual Setup (Linux/Mac)
```bash
echo 'export GROQ_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

#### Option D: Set in Node
- Enter your API key directly in the node's "api_key" field
- Leave empty to use environment variable

**Get API Key**: https://console.groq.com/keys

### 3. Model Validation Errors

#### `unet_name: 'qwen_image_edit_bf16.safetensors' not in [...] `

**What it means**: The workflow is trying to use a UNET model that's not in the expected list.

**Solution**: 
- ✅ **Fixed**: We've added the missing models to the compatibility lists
- Models like `qwen_image_edit_bf16.safetensors` are now recognized

#### `model_name: '1x-ITF-SkinDiffDetail-Lite-v1.pth' not in [...]`

**What it means**: The workflow is trying to use an upscale model that's not in the expected list.

**Solution**: 
- ✅ **Fixed**: We've added the missing upscale models
- Models like `1x-ITF-SkinDiffDetail-Lite-v1.pth` are now recognized

### 4. `Required input is missing: text`

**What it means**: A node is expecting text input but isn't receiving it.

**Solutions**:
- Check that all text inputs are connected properly
- Ensure ShowText nodes have text inputs connected
- Verify prompt nodes are generating output

## Node Reference

### Available Nodes

1. **GroqArtPromptEnhancer** - Enhance art prompts
2. **GroqArtPromptGenerator** - Generate prompts from images  
3. **GroqStyleTransferPrompter** - Convert descriptions to prompts
4. **GroqWorkflowHelper** - ComfyUI workflow assistance
5. **GroqMusicToArtPrompter** - Music-inspired art prompts
6. **GroqLLMNode (Legacy)** - Backward compatibility node

### Common Parameters

- **api_key**: Your GROQ API key (optional if set in environment)
- **model**: Choose from available GROQ models
- **temperature**: 0.0 (deterministic) to 2.0 (creative)
- **max_tokens**: Maximum response length
- **top_p**: Nucleus sampling (0.1-1.0)

## Environment Setup

### Check Current Setup
```python
import os
print("GROQ_API_KEY:", "SET" if os.getenv('GROQ_API_KEY') else "NOT SET")
```

### Test API Connection
```python
from groq import Groq

client = Groq(api_key="your_key_here")
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Test"}],
    max_tokens=10
)
print(response.choices[0].message.content)
```

## Supported Models

### Text Generation Models
- `llama-3.3-70b-versatile` (recommended)
- `llama-3.1-8b-instant`
- `llama3-70b-8192`
- `llama3-8b-8192`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`
- And more...

### Vision Models
- `meta-llama/llama-4-maverick-17b-128e-instruct`
- `meta-llama/llama-4-scout-17b-16e-instruct`
- `llava-v1.5-7b-4096-preview`

## Performance Tips

1. **Model Selection**:
   - Use `llama-3.1-8b-instant` for speed
   - Use `llama-3.3-70b-versatile` for quality
   - Use `mixtral-8x7b-32768` for long context

2. **Token Management**:
   - Start with 1024 max_tokens
   - Increase only if needed
   - Monitor your API usage

3. **Temperature Settings**:
   - 0.1-0.3: Consistent, predictable output
   - 0.7: Balanced creativity
   - 1.0-1.5: More creative and varied

## Getting Help

1. **Check Logs**: Look at ComfyUI console for detailed error messages
2. **Verify Setup**: Run `python setup_api_key.py` to test configuration
3. **Update Extension**: Make sure you have the latest version
4. **Community**: Check ComfyUI community forums for similar issues

## Common Workflow Issues

### Workflow Won't Load
- Check for typos in node names
- Ensure all required inputs are connected
- Verify model names match available options

### Slow Response Times
- Try a faster model like `llama-3.1-8b-instant`
- Reduce `max_tokens`
- Check your internet connection

### Inconsistent Results
- Set a fixed `seed` value
- Lower `temperature` for more consistency
- Use `top_p` between 0.8-0.95

## Version Compatibility

This troubleshooting guide is for ComfyUI GroqPrompt v2.0+. If you're using an older version, consider updating for the latest fixes and features.
