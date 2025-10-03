#!/bin/bash
# 🚀 AccessMate Repository Setup Script
# Run this after creating your GitHub repository

echo "🚀 Setting up AccessMate GitHub Repository..."

# Get GitHub username and repository URL
read -p "Enter your GitHub username: " GITHUB_USERNAME
REPO_URL="https://github.com/$GITHUB_USERNAME/accessmate.git"

echo "📁 Repository URL: $REPO_URL"

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📝 Initializing git repository..."
    git init
fi

# Add all files
echo "📦 Adding all files to git..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "⚠️  No changes to commit"
else
    # Make initial commit
    echo "💾 Making initial commit..."
    git commit -m "Initial commit - AccessMate Accessibility Assistant

Features:
- Desktop application with GUI and speech synthesis
- Android APK build pipeline with GitHub Actions
- Cross-platform accessibility tools
- Voice recognition and TTS support
- Object detection and screen reading capabilities
- Support for Windows, Android, macOS, and Linux"
fi

# Set main branch
echo "🌿 Setting main branch..."
git branch -M main

# Add remote origin
echo "🔗 Connecting to GitHub repository..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Repository setup complete!"
echo "🌐 Visit your repository: https://github.com/$GITHUB_USERNAME/accessmate"
echo "⚡ Visit GitHub Actions: https://github.com/$GITHUB_USERNAME/accessmate/actions"
echo ""
echo "🎯 Next steps:"
echo "1. Go to your repository on GitHub"
echo "2. Check the Actions tab for automated builds"
echo "3. Download APK when build completes"
echo "4. Test your accessibility app!"
echo ""
echo "🎉 Welcome to professional AccessMate development!"