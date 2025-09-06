# Blender Material Copy Paster

A Blender addon that allows you to copy and paste node-based materials to/from JSON format. Includes a convenient toolbar in the Shader Editor for easy material sharing.

## Features

- Shader Editor Toolbar: Copy/paste buttons in the Shader Editor sidebar
- Serialize complete node trees including nodes, properties, and links
- Handle basic node properties (location, input defaults, colors, vectors)
- Export materials to JSON for copy-pasting
- Import materials from JSON strings
- Clipboard integration for seamless material sharing
- Error handling for invalid JSON and missing materials
- Clean, commented code

## Installation

### Option 1: Install as Blender Addon (Recommended)

1. Download or clone all files from this repository
2. Install the `pyperclip` dependency:
   ```bash
   pip install pyperclip
   ```
   Or run the provided installer:
   ```bash
   python install_dependencies.py
   ```
3. In Blender, go to `Edit > Preferences > Add-ons`
4. Click `Install...` and select the `__init__.py` file from this repository
5. Enable the addon by checking the box next to "Material Copy Paster"

### Option 2: Manual Installation

1. Copy `material_serializer.py` to your Blender scripts directory
2. Install pyperclip: `pip install pyperclip`
3. Run the script in Blender's text editor or load it as a module

### Option 3: Run as Script

1. Copy `material_serializer.py` to your Blender scripts directory
2. For testing, also copy `test_material_serializer.py`
3. Run the test script to verify functionality

## Usage

### Shader Editor Toolbar (Easiest Method)

1. Open the Shader Editor
2. Select an object with a node-based material
3. Look for the "Material Copy Paster" panel in the right sidebar (Tool tab)
4. Click "Copy Material to Clipboard" to export
5. Click "Paste Material from Clipboard" to import

### Python API

```python
import material_serializer as ms

# Export a material to JSON
material = bpy.data.materials['MyMaterial']
json_str = ms.serialize_material(material)
print(json_str)  # Copy this JSON string

# Import from JSON
new_material = ms.deserialize_material(json_str, "New_Material_Name")
```

### Clipboard Functions

```python
# Copy to clipboard
ms.copy_material_to_clipboard('MyMaterial')

# Paste from clipboard
new_material = ms.paste_material_from_clipboard("New_Material_Name")
```

### Example Functions

```python
# Export to console (ready for copy-paste)
ms.export_material_to_console('MyMaterial')

# Import from JSON string
json_string = """{"name": "MyMaterial", "use_nodes": true, ...}"""  # Your JSON here
ms.import_material_from_json(json_string, "Imported_Material")
```

### Running Tests

```python
# Run the test script to verify functionality
import test_material_serializer
test_material_serializer.run_tests()
```

## Supported Node Types

The script handles most common Blender shader nodes including:
- ShaderNodeOutputMaterial
- ShaderNodeBsdfPrincipled
- ShaderNodeRGB
- ShaderNodeMix
- ShaderNodeMath
- And many more...

## Dependencies

- **pyperclip**: For clipboard functionality (required for the toolbar buttons)
  ```bash
  pip install pyperclip
  ```

If pyperclip is not installed, the toolbar will show a warning but the basic JSON functions will still work.

## Data Serialized

- Material name and node usage
- All nodes with their types and locations
- Node input/output default values (floats, colors, vectors)
- Links between nodes
- Basic node properties (blend types, operations, etc.)

## Error Handling

- Validates JSON format
- Checks for material existence
- Handles missing nodes gracefully
- Provides clear error messages

## Limitations

- Custom node groups are not fully supported
- Some complex node properties may not serialize completely
- Texture references are stored as paths but not the actual texture data

## Example Workflow

1. Create a material in Blender with nodes
2. Run: `ms.export_material_to_console('MaterialName')`
3. Copy the JSON output from the console
4. In another Blender instance, paste the JSON and run:
   ```python
   ms.import_material_from_json("""[paste JSON here]""")
   ```

## Compatibility

- Tested on Blender 4.5.2
- Python 3.7+

## License

This script is provided as-is for educational and development purposes.
