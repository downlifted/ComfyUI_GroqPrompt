# ComfyUI_GROQ-PromptWizard 🎨

![GitHub](https://img.shields.io/github/license/downlifted/ComfyUI_GROQ-PromptWizard)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/downlifted/ComfyUI_GROQ-PromptWizard)
![GitHub issues](https://img.shields.io/github/issues/downlifted/ComfyUI_GROQ-PromptWizard)
![GitHub stars](https://img.shields.io/github/stars/downlifted/ComfyUI_GROQ-PromptWizard?style=social)

**The ultimate ComfyUI custom node package for AI-powered art creation!** Transform your creative workflow with GROQ's powerful AI models, specifically designed for artists, prompt engineers, and ComfyUI enthusiasts.

## 🎨 Art-Focused Features

- **🖼️ Art Prompt Generator**: Analyze images and create detailed Stable Diffusion prompts
- **✨ Art Prompt Enhancer**: Transform basic prompts into masterpiece-quality descriptions  
- **🎭 Style Transfer Prompter**: Convert art descriptions into consistent, usable prompts
- **⚙️ Workflow Helper**: Generate complete ComfyUI workflows and debug existing ones
- **🎵 Music-to-Art Prompter**: Translate music and audio into visual art concepts
- **🔑 Easy API Key Setup**: New dedicated nodes - just paste your key and go! No command line needed
- **🎯 ComfyUI Optimized**: Built specifically for art generation workflows

## 📦 Installation

### Method 1: ComfyUI Manager (Recommended)
1. Open ComfyUI Manager in your ComfyUI web interface
2. Go to "Install Custom Nodes"
3. Search for `ComfyUI_GROQ-PromptWizard`
4. Click "Install"
5. Restart ComfyUI

### Method 2: Manual Installation
1. Navigate to your ComfyUI `custom_nodes` directory:
   ```bash
   cd ComfyUI/custom_nodes
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/downlifted/ComfyUI_GROQ-PromptWizard.git
   ```

3. Install the required dependencies:
   ```bash
   cd ComfyUI_GROQ-PromptWizard
   pip install -r requirements.txt
   ```

4. Restart ComfyUI

### Method 3: Direct Download
1. Download the latest release from the [Releases](https://github.com/downlifted/ComfyUI_GROQ-PromptWizard/releases) page
2. Extract the ZIP file to your ComfyUI `custom_nodes` directory
3. Install dependencies: `pip install -r requirements.txt`
4. Restart ComfyUI

## 🚀 Usage

### Setting Up Your API Key

**🎯 NEW: Easy Node-Based Setup!** 

The simplest way is to use our **GROQ API Key Manager** node:

1. Add **GROQ API Key Manager** to your workflow
2. Enter your API key from [console.groq.com/keys](https://console.groq.com/keys)
3. Run the node - it will validate and set up your key automatically!

**Alternative methods:**
- **Per-node**: Enter your API key directly in any GROQ node's input field  
- **Environment Variable**: Set `GROQ_API_KEY` in your system environment
- **Provider Pattern**: Use **GROQ API Key Provider** for complex workflows

📖 **[See detailed setup guide →](API_KEY_SETUP.md)**

### 🎨 Art-Focused Nodes

#### 🖼️ GROQ Art Prompt Generator
Transform reference images into detailed Stable Diffusion prompts.

**Perfect for:** "I love this photo, create a prompt for it!"

**Key Features:**
- Upload any image and get art prompts
- Multiple art styles (photorealistic, digital art, anime, etc.)
- Technical photography terms included
- Customizable prompt length and creativity

#### ✨ GROQ Art Prompt Enhancer  
Take basic prompts and make them amazing.

**Perfect for:** "woman portrait" → "masterpiece portrait, detailed face, professional lighting, 8k"

**Key Features:**
- Quality boost, style enhancement, detail addition
- Optimized for SDXL, SD1.5, Midjourney, DALL-E
- Multiple creativity levels
- Target-specific enhancements

#### 🎭 GROQ Style Transfer Prompter
Convert art descriptions into consistent Stable Diffusion prompts.

**Perfect for:** "Van Gogh style" → Complete prompt with brushstrokes, colors, techniques

**Key Features:**
- Art style analysis and conversion
- Multiple art mediums (oil, watercolor, digital, etc.)
- Automatic negative prompt generation
- Style strength control

#### ⚙️ GROQ Workflow Helper
Generate complete ComfyUI workflows and debug existing ones.

**Perfect for:** "Create SDXL img2img workflow" → Get working JSON + instructions

**Key Features:**
- Auto-generate workflows (txt2img, img2img, ControlNet, etc.)
- Debug and fix broken workflows
- Step-by-step usage instructions
- Model-specific optimization

#### 🎵 GROQ Music-to-Art Prompter
Translate music and audio into visual art prompts.

**Perfect for:** "Jazz music" → "flowing curves, warm amber tones, smooth composition"

**Key Features:**
- Music genre analysis
- Synesthetic translation (sound → visual)
- Mood and energy interpretation
- Multiple art styles for music visualization

## 💡 Real-World Examples

### 🖼️ Image-to-Prompt Workflow
1. Upload a reference photo to **Art Prompt Generator**
2. Select "photorealistic" style, "detailed" length
3. Get: "cinematic landscape, golden hour lighting, dramatic clouds, professional photography, 8k detail"
4. Use in your favorite AI art generator!

### ✨ Prompt Enhancement Pipeline  
1. Start with basic prompt: "cat"
2. Use **Art Prompt Enhancer** with "quality_boost" 
3. Get: "adorable fluffy cat, detailed fur texture, professional pet photography, high resolution, masterpiece"
4. Perfect for SDXL generation!

### 🎭 Style Transfer Creation
1. Input "Van Gogh's Starry Night style" to **Style Transfer Prompter**
2. Select "oil_painting" medium, "strong" intensity
3. Get complete prompt with swirling brushstrokes, vibrant blues and yellows
4. Plus negative prompt to avoid unwanted elements!

### ⚙️ Workflow Generation
1. Ask **Workflow Helper**: "Create SDXL face swap workflow with ReActor"
2. Get complete ComfyUI JSON + step-by-step instructions
3. Load directly into ComfyUI and start creating!

### 🎵 Music Visualization
1. Describe music to **Music-to-Art Prompter**: "Dark ambient electronic"
2. Select "abstract" art style, "strong" intensity  
3. Get: "ethereal shadows, deep blues and purples, mysterious atmosphere, flowing abstract forms"
4. Create art that matches your music's mood!

## 🤖 GROQ Model Support

### LLM Models (13 available)
- **llama-3.3-70b-versatile** ⭐ (default) - Latest versatile model
- **llama-3.1-8b-instant** - Fast responses
- **deepseek-r1-distill-llama-70b** - Advanced reasoning
- **qwen-qwq-32b** - Large context window
- **gemma2-9b-it** - Efficient instruction following
- **meta-llama/llama-4-scout-17b-16e-instruct** - Latest LLaMA 4
- And 7 more cutting-edge models!

### VLM Models (Vision-Language)
- **meta-llama/llama-4-maverick-17b-128e-instruct** ⭐ (default)
- **meta-llama/llama-4-scout-17b-16e-instruct**

*All models updated to match the latest GROQ API offerings*

## 🎯 Categories in ComfyUI

Find your nodes under these categories:
- **GroqPrompt/Setup** - API key management nodes ⭐ *NEW*
- **GroqPrompt/Art Generation** - All art-focused nodes
- **GroqPrompt/Workflow** - Workflow helper tools
- **GroqPrompt/Legacy** - Backward compatibility nodes

## 🔧 Requirements

- Python 3.8+
- ComfyUI
- GROQ API key ([Get one free](https://console.groq.com/))

## 📝 Dependencies

```bash
groq>=0.4.1
torch>=1.9.0  
numpy>=1.21.0
Pillow>=8.0.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for the ComfyUI community
- Powered by GROQ's lightning-fast AI models
- Inspired by the original [ComfyUI-mnemic-nodes](https://github.com/MNeMoNiCuZ/ComfyUI-mnemic-nodes)

## 🆘 Support

- 🐛 [Report Issues](https://github.com/downlifted/ComfyUI_GROQ-PromptWizard/issues)
- 💬 [Discussions](https://github.com/downlifted/ComfyUI_GROQ-PromptWizard/discussions)
- 📖 [Documentation](https://github.com/downlifted/ComfyUI_GROQ-PromptWizard/wiki)

---

**Made with ❤️ for the ComfyUI art community** 🎨
