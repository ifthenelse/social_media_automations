#!/bin/bash

# GitHub Star Cleanup Run Script
# This script runs the GitHub star cleanup tool in the virtual environment

set -e

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first:"
    echo "   ./setup.sh"
    exit 1
fi

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo "❌ .env file not found. Please create it from the example:"
    echo "   cp ../.env.example ../.env"
    echo "   # Then edit ../.env and add your GitHub token"
    exit 1
fi

# Activate virtual environment and run the script
echo "🚀 Running GitHub Star Cleanup..."
source venv/bin/activate
python github_star_cleanup_clean.py
