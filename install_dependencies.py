#!/usr/bin/env python3
"""
Installation script for Material Serializer dependencies
"""

import subprocess
import sys

def install_pyperclip():
    """Install pyperclip using pip"""
    try:
        print("Installing pyperclip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
        print("✓ pyperclip installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install pyperclip: {e}")
        return False

def check_pyperclip():
    """Check if pyperclip is already installed"""
    try:
        import pyperclip
        print("✓ pyperclip is already installed")
        return True
    except ImportError:
        return False

if __name__ == "__main__":
    print("Material Serializer - Dependency Installer")
    print("=" * 40)

    if check_pyperclip():
        print("All dependencies are installed!")
    else:
        print("pyperclip not found. Installing...")
        if install_pyperclip():
            print("\nInstallation complete!")
            print("You can now use the Material Serializer addon.")
        else:
            print("\nInstallation failed.")
            print("Please install pyperclip manually: pip install pyperclip")
