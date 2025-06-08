#!/bin/bash

# GitHub Star Cleanup Setup Script
# This script sets up the environment for running the GitHub star cleanup tool

set -e # Exit on any error

# Source utility functions
source "$(dirname "$0")/utils.sh"

echo "🌟 GitHub Star Cleanup Setup"
echo "=============================="

# Check if Python 3 is installed and validate version
PYTHON_CMD=$(validate_python_version)
if [ $? -ne 0 ]; then
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env: cp .env.example .env"
echo "2. Edit .env and add your GitHub token"
echo "3. Run the script:"
echo "   source venv/bin/activate"
echo "   python github_star_cleanup_clean.py"
echo ""
echo "To get a GitHub token:"
echo "• Go to GitHub Settings > Developer settings > Personal access tokens"
echo "• Generate a new token with 'user' scope"
echo "• Copy the token to your .env file"
