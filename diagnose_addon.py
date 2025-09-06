#!/usr/bin/env python3
"""
Diagnostic script for Material Serializer addon
"""

def check_pyperclip():
    """Check if pyperclip is installed"""
    try:
        import pyperclip
        print("✓ pyperclip is installed")
        return True
    except ImportError as e:
        print(f"✗ pyperclip not found: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    import os
    required_files = ['__init__.py', 'material_serializer.py']
    missing = []

    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            missing.append(file)

    return len(missing) == 0

def test_syntax():
    """Test syntax of Python files"""
    import subprocess
    import sys

    files = ['__init__.py', 'material_serializer.py']
    all_good = True

    for file in files:
        try:
            result = subprocess.run([sys.executable, '-m', 'py_compile', file],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {file} syntax OK")
            else:
                print(f"✗ {file} syntax error: {result.stderr}")
                all_good = False
        except Exception as e:
            print(f"✗ Error checking {file}: {e}")
            all_good = False

    return all_good

if __name__ == "__main__":
    print("Material Serializer Addon Diagnostics")
    print("=" * 40)

    print("\n1. Checking dependencies...")
    pyperclip_ok = check_pyperclip()

    print("\n2. Checking files...")
    files_ok = check_files()

    print("\n3. Checking syntax...")
    syntax_ok = test_syntax()

    print("\n" + "=" * 40)
    if pyperclip_ok and files_ok and syntax_ok:
        print("✓ All checks passed! Addon should work.")
        print("\nNext steps:")
        print("1. Restart Blender")
        print("2. Go to Edit > Preferences > Add-ons")
        print("3. Search for 'Material Serializer'")
        print("4. Enable the addon")
    else:
        print("✗ Some issues found. Please fix them before installing.")

        if not pyperclip_ok:
            print("\nTo fix pyperclip:")
            print("  pip install pyperclip")
            print("  or run: python install_dependencies.py")

        if not files_ok:
            print("\nMissing files detected!")

        if not syntax_ok:
            print("\nSyntax errors found in files!")
