#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify python-dotenv import works correctly.
This helps VS Code detect the correct Python environment.
"""

try:
    from dotenv import load_dotenv
    print("✅ SUCCESS: python-dotenv imported successfully!")
    load_dotenv()
    print("✅ SUCCESS: load_dotenv() function works!")
except ImportError as e:
    print(f"❌ ERROR: Failed to import python-dotenv: {e}")
except Exception as e:
    print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    print("Python interpreter:", __import__('sys').executable)
    print("Python version:", __import__('sys').version)
