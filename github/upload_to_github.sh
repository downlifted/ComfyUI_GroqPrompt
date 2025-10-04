#!/bin/bash

# ComfyUI_GroqPrompt - GitHub Upload Script
# Run this script to upload your package to GitHub

echo "🚀 ComfyUI_GroqPrompt GitHub Upload Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "setup.py" ]; then
    echo "❌ Error: Please run this script from the ComfyUI_GroqPrompt directory"
    exit 1
fi

echo "📍 Current directory: $(pwd)"
echo "✅ Package files found"

# Check git configuration
echo ""
echo "🔧 Checking Git configuration..."
if ! git config --get user.name > /dev/null; then
    echo "⚠️  Git username not set. Please configure:"
    echo "   git config --global user.name 'Your Name'"
    echo "   git config --global user.email 'your.email@example.com'"
    exit 1
fi

echo "✅ Git configured: $(git config user.name) <$(git config user.email)>"

# Initialize git repository
echo ""
echo "🔧 Initializing Git repository..."
git init
echo "✅ Git repository initialized"

# Add all files
echo ""
echo "📦 Adding files to Git..."
git add .
echo "✅ Files added"

# Create initial commit
echo ""
echo "💾 Creating initial commit..."
git commit -m "Initial release: ComfyUI_GroqPrompt v1.0.0

Advanced GROQ API nodes for ComfyUI featuring:
- Text generation with conversation history
- Vision analysis with multiple image support
- Document processing and analysis
- Code generation and assistance
- Audio transcription and processing
- Flexible API key management
- Professional documentation"
echo "✅ Initial commit created"

# Check if remote origin exists
echo ""
echo "🔗 Setting up GitHub remote..."
if git remote | grep -q origin; then
    echo "✅ Remote origin already exists"
else
    echo "❌ Please add your GitHub repository as remote origin:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/ComfyUI_GroqPrompt.git"
    echo ""
    echo "Replace YOUR_USERNAME with your GitHub username, then run:"
    echo "   git push -u origin main"
    exit 1
fi

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
if git push -u origin main; then
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Next Steps:"
    echo "1. Go to your GitHub repository"
    echo "2. Create a new release (optional but recommended)"
    echo "3. Update README.md with your GitHub username"
    echo "4. Test installation in ComfyUI"
else
    echo "❌ Failed to push to GitHub"
    echo "   Make sure your GitHub repository exists and you have write access"
    exit 1
fi

echo ""
echo "🎊 Upload Complete!"
echo "Your ComfyUI_GroqPrompt package is now on GitHub!"
