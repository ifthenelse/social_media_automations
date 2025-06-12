#!/bin/bash

# Shared utility functions for Instagram Following Cleanup scripts

# Function to find the correct Python command
find_python() {
    if command -v python3 >/dev/null 2>&1; then
        echo "python3"
    elif command -v python >/dev/null 2>&1; then
        # Check if 'python' actually points to Python 3
        if python -c "import sys; sys.exit(0 if sys.version_info.major == 3 else 1)" 2>/dev/null; then
            echo "python"
        fi
    fi
}

# Function to check if Python command is available and is Python 3
validate_python() {
    local python_cmd=$(find_python)
    if [ -z "$python_cmd" ]; then
        echo "❌ Python 3 is not installed. Please install Python 3.8 or later."
        echo "   You can download it from: https://www.python.org/downloads/"
        return 1
    fi
    echo "$python_cmd"
    return 0
}

# Function to validate Python version requirements (3.8+)
validate_python_version() {
    local python_cmd=$(validate_python)
    if [ $? -ne 0 ]; then
        return 1
    fi

    # Check Python version
    local python_version=$($python_cmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo "✅ Found Python $python_version" >&2

    # Check if version is 3.8 or later
    if ! $python_cmd -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        echo "❌ Python 3.8 or later is required. Found Python $python_version" >&2
        return 1
    fi

    echo "$python_cmd"
    return 0
}
