# GROQ API Key Setup - Easy Node-Based Method

Instead of running commands or editing environment variables, you can now set up your GROQ API key directly within ComfyUI using dedicated nodes!

## 🚀 Quick Setup (Recommended)

### Method 1: Simple One-Node Setup

1. **Add the GROQ API Key Manager node** to your workflow
2. **Enter your API key** in the `api_key` field
3. **Leave action as "set_and_validate"** (default)
4. **Run the workflow** - the node will:
   - Set your API key in the environment
   - Test it with a quick API call
   - Show you a status message

**That's it!** Your API key is now available to all other GROQ nodes in your workflow.

### Method 2: Provider Pattern (Advanced)

For workflows with multiple GROQ nodes, you can use the provider pattern:

1. **Add GROQ API Key Manager** (set up your key once)
2. **Add GROQ API Key Provider** (set source to "environment_variable")
3. **Connect the provider** to other GROQ nodes via the `api_key_override` input

## 📋 Available Nodes

### GROQ API Key Manager
**Purpose**: Set up and validate your API key

**Inputs**:
- `api_key`: Your GROQ API key from https://console.groq.com/keys
- `action`: What to do (set_and_validate, validate_only, clear_key)
- `test_connection`: Whether to test the key (recommended: True)
- `test_model`: Model for testing (default: llama-3.1-8b-instant for speed)

**Outputs**:
- `status_message`: Success/error message with details
- `is_valid`: Boolean indicating if the key works
- `masked_key`: Masked version of your key (for display)

### GROQ API Key Provider  
**Purpose**: Provide API key to other nodes in your workflow

**Inputs**:
- `source`: Where to get the key (environment_variable or manual_input)
- `manual_key`: Manual key input (if source is manual_input)

**Outputs**:
- `api_key`: The API key for other nodes to use

## 🔧 Usage Examples

### Example 1: Basic Setup
```
[GROQ API Key Manager]
├─ api_key: "gsk_your_key_here"
├─ action: "set_and_validate" 
├─ test_connection: True
└─ test_model: "llama-3.1-8b-instant"

↓ (Run this first)

[Any GROQ Node]
├─ api_key: "" (leave empty - will use environment)
└─ other settings...
```

### Example 2: Provider Pattern
```
[GROQ API Key Manager] → (Set up once)
├─ api_key: "gsk_your_key_here"
└─ action: "set_and_validate"

[GROQ API Key Provider]
├─ source: "environment_variable"
└─ api_key → [Connect to multiple GROQ nodes]

[GROQ LLM Node (Legacy)]    [GROQ Art Prompt Enhancer]
├─ api_key_override: ←─────┬─ api_key: ←──────────────┘
├─ prompt: "Hello"         └─ base_prompt: "cat"
└─ other settings...         └─ other settings...
```

### Example 3: Manual Key Per Node
```
[GROQ API Key Provider]
├─ source: "manual_input"
├─ manual_key: "gsk_your_key_here"
└─ api_key → [Connect to GROQ nodes]
```

## ✅ Status Messages Explained

- **✅ API key set in environment | ✅ API key test successful**: Perfect! Ready to use
- **⚠️ Warning: GROQ API keys typically start with 'gsk_'**: Check your key format
- **❌ Invalid API key**: Key is wrong or expired - get a new one
- **⚠️ Valid key but rate limited**: Key works but you're hitting limits
- **⚠️ Valid key but quota exceeded**: Key works but check your billing
- **❌ No API key provided**: Enter a key in the node

## 🛠️ Troubleshooting

### "No API key provided" Error
- Make sure you entered the key in the GROQ API Key Manager node
- Run the API Key Manager node first before other GROQ nodes
- Check that the key was actually saved (look at the status message)

### "Invalid API key" Error  
- Double-check your key from https://console.groq.com/keys
- Make sure there are no extra spaces before/after the key
- Try generating a new API key if the old one expired

### "Connection timeout" Warning
- This usually means your key is valid but the test couldn't complete
- Try again or skip the test by setting `test_connection` to False

### Key Not Persisting Between Sessions
- The API Key Manager sets the key for the current session only
- For permanent setup across restarts, use the external setup script: `python setup_api_key.py`
- Or re-run the API Key Manager node each time you start ComfyUI

## 🔐 Security Notes

- Your API key is stored in memory only (not saved to disk by these nodes)
- The masked display shows only partial key for security
- Never share workflows containing your actual API key
- Use environment variables for shared/production workflows

## 🎯 Get Your API Key

1. Go to https://console.groq.com/keys
2. Sign in or create a free account
3. Click "Create API Key"
4. Copy the key (starts with `gsk_`)
5. Paste it into the GROQ API Key Manager node

**Free tier includes**: Generous limits for testing and development!

---

This node-based approach is much simpler than running external commands - just add a node, enter your key, and you're ready to go! 🚀
