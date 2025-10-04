@echo off
REM ComfyUI_GroqPrompt - GitHub Upload Script for Windows
REM Run this script to upload your package to GitHub

echo 🚀 ComfyUI_GroqPrompt GitHub Upload Script
echo ==========================================

REM Check if we're in the right directory
if not exist "README.md" (
    echo ❌ Error: Please run this script from the ComfyUI_GroqPrompt directory
    pause
    exit /b 1
)

if not exist "setup.py" (
    echo ❌ Error: Please run this script from the ComfyUI_GroqPrompt directory
    pause
    exit /b 1
)

echo 📍 Current directory: %cd%
echo ✅ Package files found

REM Check git configuration
echo.
echo 🔧 Checking Git configuration...
git config --get user.name >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Git username not set. Please configure:
    echo    git config --global user.name "downlifted"
    echo    git config --global user.email "downlifted@gmail.com"
    pause
    exit /b 1
)

for /f "delims=" %%i in ('git config user.name') do set GIT_USER=%%i
for /f "delims=" %%i in ('git config user.email') do set GIT_EMAIL=%%i
echo ✅ Git configured: %GIT_USER% ^<%GIT_EMAIL%^>

REM Initialize git repository
echo.
echo 🔧 Initializing Git repository...
git init
echo ✅ Git repository initialized

REM Add all files
echo.
echo 📦 Adding files to Git...
git add .
echo ✅ Files added

REM Create initial commit
echo.
echo 💾 Creating initial commit...
git commit -m "Initial release: ComfyUI_GroqPrompt v1.0.0

Advanced GROQ API nodes for ComfyUI featuring:
- Text generation with conversation history
- Vision analysis with multiple image support
- Document processing and analysis
- Code generation and assistance
- Audio transcription and processing
- Flexible API key management
- Professional documentation"
echo ✅ Initial commit created

REM Check if remote origin exists
echo.
echo 🔗 Setting up GitHub remote...
git remote | findstr origin >nul
if errorlevel 1 (
    echo ❌ Please add your GitHub repository as remote origin:
    echo    git remote add origin https://github.com/YOUR_USERNAME/ComfyUI_GroqPrompt.git
    echo.
    echo Replace YOUR_USERNAME with your GitHub username, then run:
    echo    git push -u origin main
    pause
    exit /b 1
)

REM Push to GitHub
echo.
echo 📤 Pushing to GitHub...
git push -u origin main
if errorlevel 1 (
    echo ❌ Failed to push to GitHub
    echo    Make sure your GitHub repository exists and you have write access
    pause
    exit /b 1
)

echo.
echo ✅ Successfully pushed to GitHub!
echo.
echo 🎉 Next Steps:
echo 1. Go to your GitHub repository
echo 2. Create a new release (optional but recommended)
echo 3. Update README.md with your GitHub username
echo 4. Test installation in ComfyUI
echo.
echo 🎊 Upload Complete!
echo Your ComfyUI_GroqPrompt package is now on GitHub!
pause
