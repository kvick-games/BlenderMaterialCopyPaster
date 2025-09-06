"""
Material Copy Paster Addon
==========================

Blender addon for copying and pasting node-based materials to/from JSON.
Includes a toolbar in the Shader Editor for easy copy/paste functionality.

Compatible with Blender 4.2+
"""

bl_info = {
    "name": "Material Copy Paster",
    "author": "kvick and grok",
    "description": "Copy and paste node-based materials to/from JSON with clipboard support",
    "blender": (4, 0, 0),
    "version": (1, 0, 0),
    "location": "Shader Editor > Tool Panel",
    "warning": "",
    "doc_url": "",
    "category": "Material",
}

import bpy

def register():
    """Register the addon."""
    # Import here to avoid issues during module loading
    try:
        from . import material_serializer
        material_serializer.register()
        print("Material Copy Paster: Addon registered successfully")
    except Exception as e:
        print(f"Material Copy Paster: Failed to register - {e}")

def unregister():
    """Unregister the addon."""
    try:
        from . import material_serializer
        material_serializer.unregister()
        print("Material Copy Paster: Addon unregistered successfully")
    except Exception as e:
        print(f"Material Copy Paster: Failed to unregister - {e}")

if __name__ == "__main__":
    register()
