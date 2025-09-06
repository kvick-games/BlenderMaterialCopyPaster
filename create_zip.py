#!/usr/bin/env python3
"""
Zipper script for Blender Material Serializer addon
Creates a zip file for easy addon installation
"""

import zipfile
import os
import datetime

def create_addon_zip():
    """Create zip file from the addon folder"""

    addon_folder = "MaterialCopyPaster"
    zip_filename = f"{addon_folder}.zip"

    # Check if addon folder exists
    if not os.path.exists(addon_folder):
        print(f"❌ Error: {addon_folder} folder not found!")
        return False

    # Check if required files exist
    required_files = [
        f"{addon_folder}/__init__.py",
        f"{addon_folder}/material_serializer.py"
    ]

    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Error: Required file {file} not found!")
            return False

    # Remove old zip if it exists
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        print(f"🗑️  Removed old {zip_filename}")

    # Create new zip file
    print(f"📦 Creating {zip_filename}...")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add addon files
        for root, dirs, files in os.walk(addon_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, ".")
                zipf.write(file_path, arcname)
                print(f"  ✅ Added: {arcname}")

    # Get file info
    zip_size = os.path.getsize(zip_filename)
    file_count = len(list(zipfile.ZipFile(zip_filename, 'r').namelist()))

    print(f"\n🎉 Successfully created {zip_filename}")
    print(",")
    print(f"📁 Files included: {file_count}")
    print(f"📅 Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return True

def create_release_zip():
    """Create a release zip with all files for GitHub"""
    import glob

    release_name = "BlenderMaterialCopyPaster"
    zip_filename = f"{release_name}.zip"

    # Files to include in release
    include_patterns = [
        "MaterialCopyPaster/**/*",
        "README.md",
        "requirements.txt",
        "install_dependencies.py",
        "create_zip.py",
        ".gitignore"
    ]

    # Remove old release zip
    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    print(f"📦 Creating release {zip_filename}...")

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pattern in include_patterns:
            for file_path in glob.glob(pattern, recursive=True):
                if os.path.isfile(file_path):
                    arcname = os.path.relpath(file_path, ".")
                    zipf.write(file_path, arcname)
                    print(f"  ✅ Added: {arcname}")

    zip_size = os.path.getsize(zip_filename)
    file_count = len(list(zipfile.ZipFile(zip_filename, 'r').namelist()))

    print(f"\n🎉 Successfully created {zip_filename}")
    print(",")
    print(f"📁 Files included: {file_count}")

    return True

if __name__ == "__main__":
    print("Blender Material Serializer - Zipper Script")
    print("=" * 50)

    print("\n1. Creating addon zip (for Blender installation)...")
    addon_success = create_addon_zip()

    print("\n2. Creating release zip (for GitHub)...")
    release_success = create_release_zip()

    if addon_success and release_success:
        print("\n🎊 All zips created successfully!")
        print("\nUsage:")
        print("- MaterialCopyPaster.zip → Install in Blender")
        print("- BlenderMaterialCopyPaster.zip → Upload to GitHub releases")
    else:
        print("\n❌ Some zips failed to create")
