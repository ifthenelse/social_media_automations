#!/bin/bash

# GitHub Star Cleanup Setup Script
# This script sets up the environment for running the GitHub star cleanup tool

set -e # Exit on any error

echo "🌟 GitHub Star Cleanup Setup"
echo "=============================="

# Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or later."
    echo "   You can download it from: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Found Python $PYTHON_VERSION"

# Check if version is 3.8 or later
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo "❌ Python 3.8 or later is required. Found Python $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
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
