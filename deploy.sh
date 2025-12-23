#!/bin/bash
# Quick deploy script for Hugging Face Spaces

set -e

echo "🚀 Hugging Face Spaces Deployment Script"
echo "========================================"
echo ""

# Check if HF_USERNAME is set
if [ -z "$HF_USERNAME" ]; then
    echo "❌ Error: HF_USERNAME environment variable not set"
    echo "Usage: export HF_USERNAME=your-huggingface-username"
    echo "       ./deploy.sh"
    exit 1
fi

# Check if space name is provided
SPACE_NAME=${1:-"ai-policy-assistant"}

echo "📦 Deploying to: https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "⚙️  Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Add Hugging Face remote
echo "🔗 Adding Hugging Face remote..."
git remote remove huggingface 2>/dev/null || true
git remote add huggingface https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME

# Rename README for deployment
if [ -f "README_HF.md" ]; then
    echo "📝 Preparing README..."
    cp README.md README_LOCAL.md
    cp README_HF.md README.md
fi

# Commit changes
echo "💾 Committing changes..."
git add .
git commit -m "Deploy to Hugging Face Spaces" || echo "No changes to commit"

# Push to Hugging Face
echo "🚀 Pushing to Hugging Face Spaces..."
git push huggingface main -f

# Restore local README
if [ -f "README_LOCAL.md" ]; then
    mv README_LOCAL.md README.md
    rm -f README_HF.md
fi

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your app will be available at:"
echo "   https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo ""
echo "⚠️  Don't forget to:"
echo "   1. Set OPENAI_API_KEY in Space Settings → Repository secrets"
echo "   2. Wait for Docker build to complete (5-10 minutes)"
echo "   3. Upload your policy documents"
echo ""
