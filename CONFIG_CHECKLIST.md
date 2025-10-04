# ComfyUI_GroqPrompt - Configuration Checklist

## 📋 Before Upload
- [ ] Git configured with username and email
- [ ] GitHub repository created: "ComfyUI_GroqPrompt"
- [ ] Repository is empty (no README, license, etc.)

## 🔧 After Upload - Required Updates

### 1. Update README.md
Replace these placeholders in README.md:
- `yourusername` → Your actual GitHub username
- Search and replace all instances

### 2. Update setup.py
Replace these in setup.py:
- `author="Your Name"` → Your actual name
- `author_email="your.email@example.com"` → Your email
- `url="https://github.com/yourusername/ComfyUI_GroqPrompt"` → Your GitHub repo URL

### 3. Create GitHub Release (Recommended)
- Go to Releases tab in GitHub
- Create new release with tag: v1.0.0
- Upload ZIP file as asset (optional)

## 🧪 Testing Installation

### Method 1: ComfyUI Manager
1. Open ComfyUI web interface
2. Go to Manager tab
3. Search: ComfyUI_GroqPrompt
4. Install and restart ComfyUI

### Method 2: Manual Installation
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/yourusername/ComfyUI_GroqPrompt.git
cd ComfyUI_GroqPrompt
pip install -r requirements.txt
# Restart ComfyUI
```

### Method 3: ZIP Download
1. Download ZIP from GitHub releases
2. Extract to ComfyUI/custom_nodes/
3. Install dependencies
4. Restart ComfyUI

## ✅ Verification
After installation, verify nodes appear in ComfyUI under:
- GroqPrompt/Text
- GroqPrompt/Vision
- GroqPrompt/Documents
- GroqPrompt/Code
- GroqPrompt/Audio

## 🚀 Usage
1. Set GROQ_API_KEY environment variable or enter in node
2. Add nodes to workflow
3. Configure parameters
4. Run workflow

## 📞 Support
If users have issues:
- Check GitHub Issues
- Verify GROQ API key is valid
- Ensure all dependencies installed
- Check ComfyUI console for errors

---
**🎊 Ready to share your ComfyUI_GroqPrompt package with the world!**
