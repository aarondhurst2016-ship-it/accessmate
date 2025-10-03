@echo off
REM 🚀 AccessMate Repository Setup Script for Windows
REM Run this after creating your GitHub repository

echo 🚀 Setting up AccessMate GitHub Repository...

REM Get GitHub username
set /p GITHUB_USERNAME=Enter your GitHub username: 
set REPO_URL=https://github.com/%GITHUB_USERNAME%/accessmate.git

echo 📁 Repository URL: %REPO_URL%

REM Change to project directory
cd /d "C:\Users\aaron\accessmate"

REM Initialize git if not already done
if not exist ".git" (
    echo 📝 Initializing git repository...
    git init
)

REM Add all files
echo 📦 Adding all files to git...
git add .

REM Make initial commit
echo 💾 Making initial commit...
git commit -m "Initial commit - AccessMate Accessibility Assistant"

REM Set main branch
echo 🌿 Setting main branch...
git branch -M main

REM Remove existing remote if it exists
git remote remove origin 2>nul

REM Add remote origin
echo 🔗 Connecting to GitHub repository...
git remote add origin %REPO_URL%

REM Push to GitHub
echo 📤 Pushing to GitHub...
git push -u origin main

echo.
echo ✅ Repository setup complete!
echo 🌐 Visit your repository: https://github.com/%GITHUB_USERNAME%/accessmate
echo ⚡ Visit GitHub Actions: https://github.com/%GITHUB_USERNAME%/accessmate/actions
echo.
echo 🎯 Next steps:
echo 1. Go to your repository on GitHub
echo 2. Check the Actions tab for automated builds
echo 3. Download APK when build completes
echo 4. Test your accessibility app!
echo.
echo 🎉 Welcome to professional AccessMate development!
pause