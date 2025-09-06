#!/usr/bin/env python3
"""
Install pyperclip for Blender's Python environment
Run this script inside Blender's Text Editor
"""

import subprocess
import sys
import os

def install_pyperclip():
    """Install pyperclip in Blender's Python environment"""
    try:
        # Get Blender's Python executable path
        python_exe = sys.executable
        print(f"Blender Python: {python_exe}")

        # Install pyperclip using Blender's pip
        result = subprocess.run([
            python_exe, "-m", "pip", "install", "pyperclip"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ pyperclip installed successfully!")
            print("Restart Blender and the Material Serializer addon should work without warnings.")
            return True
        else:
            print("❌ Installation failed:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False

    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return False

def check_pyperclip():
    """Check if pyperclip is already available"""
    try:
        import pyperclip
        print("✅ pyperclip is already installed and working!")
        return True
    except ImportError:
        print("❌ pyperclip is not installed")
        return False

if __name__ == "__main__":
    print("Pyperclip Installation for Blender")
    print("=" * 40)

    print("\nChecking current status...")
    if check_pyperclip():
        print("No installation needed!")
    else:
        print("\nInstalling pyperclip...")
        if install_pyperclip():
            print("\n🎉 Installation complete!")
        else:
            print("\n❌ Installation failed. Try manual installation:")
            print("1. Open command prompt as Administrator")
            print(f"2. Run: {sys.executable} -m pip install pyperclip")
            print("3. Restart Blender")
