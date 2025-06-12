#!/bin/bash

# Instagram Following Cleanup Run Script
# This script runs the Instagram cleanup tool in the virtual environment

set -e

# Source utility functions
source "$(dirname "$0")/utils.sh"

# Validate Python installation and version
PYTHON_CMD=$(validate_python_version)
if [ $? -ne 0 ]; then
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first:"
    echo "   ./scripts/setup.sh"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it from the example:"
    echo "   cp .env.example .env"
    echo "   # Then edit .env and add your Instagram access token"
    exit 1
fi

# Activate virtual environment and run the script
echo "🚀 Running Instagram Following Cleanup..."
source venv/bin/activate

# Check which file to run (prioritize src/ directory)
if [ -f "src/instagram_cleanup.py" ]; then
    $PYTHON_CMD src/instagram_cleanup.py
elif [ -f "instagram_cleanup.py" ]; then
    $PYTHON_CMD instagram_cleanup.py
else
    echo "❌ instagram_cleanup.py not found in src/ or root directory"
    exit 1
fi
