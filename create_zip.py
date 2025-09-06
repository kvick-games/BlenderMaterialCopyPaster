#!/usr/bin/env python3
"""
Zipper script for Blender Material Serializer addon
Creates a zip file for easy addon installation
"""

import zipfile
import os
import datetime

def create_blender_zip():
    """Create the main Blender addon zip"""
    import glob

    zip_filename = "BlenderMaterialCopyPaster.zip"

    # Files to include in release
    include_patterns = [
        "MaterialCopyPaster/**/*",
        "README.md",
        "requirements.txt",
        "install_dependencies.py",
        ".gitignore"
    ]

    # Remove old zip
    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    print(f"📦 Creating {zip_filename}...")

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
    print("Blender Material Copy Paster - Zipper Script")
    print("=" * 50)

    print("\nCreating BlenderMaterialCopyPaster.zip...")
    success = create_blender_zip()

    if success:
        print("\n🎊 Zip created successfully!")
        print("\nUsage:")
        print("- BlenderMaterialCopyPaster.zip → Install in Blender or upload to GitHub")
    else:
        print("\n❌ Failed to create zip")
