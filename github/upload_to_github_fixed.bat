@echo off
REM ComfyUI_GroqPrompt - GitHub Upload Script for Windows
REM Fixed version with better error handling

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

REM Check and configure git
echo.
echo 🔧 Setting up Git configuration...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo Setting Git username...
    git config --global user.name "downlifted"
)

git config user.email >nul 2>&1
if errorlevel 1 (
    echo Setting Git email...
    git config --global user.email "downlifted@gmail.com"
)

REM Verify configuration
for /f "delims=" %%i in ('git config user.name') do set GIT_USER=%%i
for /f "delims=" %%i in ('git config user.email') do set GIT_EMAIL=%%i
echo ✅ Git configured: !GIT_USER! ^<!GIT_EMAIL!^>

REM Initialize git repository (only if not exists)
echo.
echo 🔧 Initializing Git repository...
if exist ".git" (
    echo ✅ Git repository already exists
) else (
    git init
    echo ✅ Git repository initialized
)

REM Add all files
echo.
echo 📦 Adding files to Git...
git add .
echo ✅ Files added

REM Check if there are changes to commit
echo.
echo 💾 Checking for changes...
git status --porcelain > temp_status.txt 2>nul
set /p STATUS=<temp_status.txt
del temp_status.txt

if "!STATUS!"=="" (
    echo ⚠️  No changes to commit
    goto :push
)

echo ✅ Files changed, creating commit...
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

:push
REM Check if remote origin exists
echo.
echo 🔗 Checking GitHub remote...
git remote | findstr origin >nul
if errorlevel 1 (
    echo ❌ Please add your GitHub repository as remote origin:
    echo    git remote add origin https://github.com/Downlifted/ComfyUI_GroqPrompt.git
    echo.
    echo Replace YOUR_USERNAME with your GitHub username, then run:
    echo    git push -u origin main
    pause
    exit /b 1
)

echo ✅ Remote origin found

REM Push to GitHub
echo.
echo 📤 Pushing to GitHub...
git push -u origin main
if errorlevel 1 (
    echo ❌ Failed to push to GitHub
    echo    Make sure your GitHub repository exists and you have write access
    echo    Also check if you have the correct permissions
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
echo.
echo 📋 Don't forget to:
echo    - Update 'yourusername' in README.md with your GitHub username
echo    - Update author information in setup.py
pause
