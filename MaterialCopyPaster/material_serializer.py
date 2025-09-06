"""
Blender Material Serializer/Deserializer
=======================================

This script provides functionality to serialize Blender node-based materials
into JSON format and deserialize them back into new materials.

Compatible with Blender 4.2+
"""

import bpy
import json
import mathutils
from typing import Dict, List, Any, Optional

# Try to import clipboard functionality
try:
    import pyperclip
    HAS_CLIPBOARD = True
    print("Material Serializer: pyperclip imported successfully")
except ImportError as e:
    HAS_CLIPBOARD = False
    print(f"Material Serializer: pyperclip not available - {e}")
    print("Material Serializer: Clipboard functions will be disabled")


def serialize_material(material: bpy.types.Material) -> str:
    """
    Serialize a Blender material and its node tree into a JSON string.

    Args:
        material: The Blender material to serialize

    Returns:
        JSON string representation of the material

    Raises:
        ValueError: If material is invalid or has no node tree
    """
    if not material:
        raise ValueError("Invalid material provided")

    if not material.use_nodes or not material.node_tree:
        raise ValueError("Material must use nodes and have a node tree")

    material_data = {
        "name": material.name,
        "use_nodes": material.use_nodes,
        "node_tree": _serialize_node_tree(material.node_tree)
    }

    return json.dumps(material_data, indent=2)


def deserialize_material(json_str: str, material_name: Optional[str] = None) -> bpy.types.Material:
    """
    Deserialize a JSON string into a new Blender material.

    Args:
        json_str: JSON string containing material data
        material_name: Optional name for the new material (uses JSON name if None)

    Returns:
        The newly created Blender material

    Raises:
        ValueError: If JSON is invalid or material creation fails
        json.JSONDecodeError: If JSON parsing fails
    """
    try:
        material_data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

    if "node_tree" not in material_data:
        raise ValueError("JSON does not contain valid material data")

    # Create new material
    name = material_name or material_data.get("name", "Deserialized_Material")
    material = bpy.data.materials.new(name=name)
    material.use_nodes = material_data.get("use_nodes", True)

    # Clear default nodes
    material.node_tree.nodes.clear()

    # Deserialize node tree
    _deserialize_node_tree(material.node_tree, material_data["node_tree"])

    return material


def _serialize_node_tree(node_tree: bpy.types.NodeTree) -> Dict[str, Any]:
    """
    Serialize a node tree including nodes and links.

    Args:
        node_tree: The node tree to serialize

    Returns:
        Dictionary containing node tree data
    """
    nodes_data = []
    links_data = []

    # Serialize nodes
    for node in node_tree.nodes:
        node_data = _serialize_node(node)
        nodes_data.append(node_data)

    # Serialize links
    for link in node_tree.links:
        link_data = _serialize_link(link)
        links_data.append(link_data)

    return {
        "nodes": nodes_data,
        "links": links_data
    }


def _serialize_node(node: bpy.types.Node) -> Dict[str, Any]:
    """
    Serialize a single node and its properties.

    Args:
        node: The node to serialize

    Returns:
        Dictionary containing node data
    """
    node_data = {
        "name": node.name,
        "type": node.bl_idname,  # Use bl_idname instead of type for proper node creation
        "location": list(node.location),
        "inputs": [],
        "outputs": []
    }

    # Serialize inputs
    for input_socket in node.inputs:
        input_data = _serialize_socket(input_socket)
        node_data["inputs"].append(input_data)

    # Serialize outputs
    for output_socket in node.outputs:
        output_data = _serialize_socket(output_socket)
        node_data["outputs"].append(output_data)

    # Serialize node-specific properties
    node_data["properties"] = _serialize_node_properties(node)

    return node_data


def _serialize_socket(socket: bpy.types.NodeSocket) -> Dict[str, Any]:
    """
    Serialize a node socket (input or output).

    Args:
        socket: The socket to serialize

    Returns:
        Dictionary containing socket data
    """
    socket_data = {
        "name": socket.name,
        "type": socket.type,
        "identifier": socket.identifier
    }

    # Serialize default values for inputs
    if hasattr(socket, 'default_value'):
        socket_data["default_value"] = _serialize_default_value(socket.default_value)

    return socket_data


def _serialize_default_value(value: Any) -> Any:
    """
    Serialize default values of various types.

    Args:
        value: The default value to serialize

    Returns:
        Serialized value
    """
    if isinstance(value, (int, float, str, bool)):
        return value
    elif isinstance(value, mathutils.Vector):
        return list(value)
    elif isinstance(value, mathutils.Color):
        return list(value)
    elif hasattr(value, '__iter__') and not isinstance(value, str):
        # Handle arrays/lists
        return list(value)
    else:
        # For unsupported types, return string representation
        return str(value)


def _serialize_node_properties(node: bpy.types.Node) -> Dict[str, Any]:
    """
    Serialize node-specific properties.

    Args:
        node: The node to serialize properties for

    Returns:
        Dictionary of node properties
    """
    properties = {}

    # Common properties for different node types
    if hasattr(node, 'blend_type') and node.blend_type:
        properties['blend_type'] = node.blend_type

    if hasattr(node, 'operation') and node.operation:
        properties['operation'] = node.operation

    if hasattr(node, 'inputs') and len(node.inputs) > 0:
        # Serialize input values that aren't connected
        for i, input_socket in enumerate(node.inputs):
            if not input_socket.is_linked and hasattr(input_socket, 'default_value'):
                properties[f'input_{i}_default'] = _serialize_default_value(input_socket.default_value)

    return properties


def _serialize_link(link: bpy.types.NodeLink) -> Dict[str, Any]:
    """
    Serialize a link between nodes.

    Args:
        link: The link to serialize

    Returns:
        Dictionary containing link data
    """
    return {
        "from_node": link.from_node.name,
        "from_socket": link.from_socket.identifier,
        "to_node": link.to_node.name,
        "to_socket": link.to_socket.identifier
    }


def _deserialize_node_tree(node_tree: bpy.types.NodeTree, tree_data: Dict[str, Any]) -> None:
    """
    Deserialize node tree data into a Blender node tree.

    Args:
        node_tree: The Blender node tree to populate
        tree_data: Dictionary containing serialized node tree data
    """
    nodes_dict = {}

    # Create nodes
    for node_data in tree_data.get("nodes", []):
        node = _deserialize_node(node_tree, node_data)
        nodes_dict[node.name] = node

    # Create links
    for link_data in tree_data.get("links", []):
        _deserialize_link(node_tree, link_data, nodes_dict)


def _deserialize_node(node_tree: bpy.types.NodeTree, node_data: Dict[str, Any]) -> bpy.types.Node:
    """
    Deserialize a single node.

    Args:
        node_tree: The node tree to add the node to
        node_data: Dictionary containing serialized node data

    Returns:
        The newly created node
    """
    node_type = node_data.get("type", "ShaderNodeRGB")
    node_name = node_data.get("name", "")

    # Handle legacy node type names (convert old format to new format)
    node_type = _convert_legacy_node_type(node_type)

    # Create the node
    try:
        node = node_tree.nodes.new(type=node_type)
    except Exception as e:
        print(f"Error creating node of type '{node_type}': {e}")
        print("Falling back to ShaderNodeRGB")
        node = node_tree.nodes.new(type="ShaderNodeRGB")

    if node_name:
        node.name = node_name

    # Set location
    if "location" in node_data:
        node.location = node_data["location"]

    # Set properties
    if "properties" in node_data:
        _deserialize_node_properties(node, node_data["properties"])

    # Set input defaults
    if "inputs" in node_data:
        for i, input_data in enumerate(node_data["inputs"]):
            if i < len(node.inputs) and "default_value" in input_data:
                _deserialize_default_value(node.inputs[i], input_data["default_value"])

    return node


def _convert_legacy_node_type(node_type: str) -> str:
    """
    Convert legacy node type names to proper Blender API names.

    Args:
        node_type: The node type from serialized data

    Returns:
        The proper Blender API node type name
    """
    # Map of legacy node types to proper Blender API names
    legacy_mapping = {
        "OUTPUT_MATERIAL": "ShaderNodeOutputMaterial",
        "BSDF_PRINCIPLED": "ShaderNodeBsdfPrincipled",
        "TEX_IMAGE": "ShaderNodeTexImage",
        "MIX_SHADER": "ShaderNodeMixShader",
        "ADD_SHADER": "ShaderNodeAddShader",
        "RGB": "ShaderNodeRGB",
        "VALUE": "ShaderNodeValue",
        "MATH": "ShaderNodeMath",
        "MIX_RGB": "ShaderNodeMixRGB",
        "INVERT": "ShaderNodeInvert",
        "SEPARATE_RGB": "ShaderNodeSeparateRGB",
        "COMBINE_RGB": "ShaderNodeCombineRGB",
        "HUE_SATURATION": "ShaderNodeHueSaturation",
        "BRIGHT_CONTRAST": "ShaderNodeBrightContrast",
        "GAMMA": "ShaderNodeGamma",
        "TEX_COORD": "ShaderNodeTexCoord",
        "MAPPING": "ShaderNodeMapping",
        "TEX_NOISE": "ShaderNodeTexNoise",
        "TEX_CHECKER": "ShaderNodeTexChecker",
        "TEX_GRADIENT": "ShaderNodeTexGradient",
        "TEX_MAGIC": "ShaderNodeTexMagic",
        "TEX_MUSGRAVE": "ShaderNodeTexMusgrave",
        "TEX_VORONOI": "ShaderNodeTexVoronoi",
        "TEX_WAVE": "ShaderNodeTexWave",
        "NORMAL_MAP": "ShaderNodeNormalMap",
        "BUMP": "ShaderNodeBump",
        "DISPLACEMENT": "ShaderNodeDisplacement",
        "VECTOR_DISPLACEMENT": "ShaderNodeVectorDisplacement",
        "NORMAL": "ShaderNodeNormal",
        "CURVE_RGB": "ShaderNodeRGBCurve",
        "CURVE_VEC": "ShaderNodeVectorCurve",
        "VALTORGB": "ShaderNodeValToRGB",
        "RGBTOBW": "ShaderNodeRGBToBW",
        "LIGHT_PATH": "ShaderNodeLightPath",
        "FRESNEL": "ShaderNodeFresnel",
        "LAYER_WEIGHT": "ShaderNodeLayerWeight",
        "CAMERA_DATA": "ShaderNodeCameraData",
        "TANGENT": "ShaderNodeTangent",
        "GEOMETRY": "ShaderNodeGeometry",
        "HAIR_INFO": "ShaderNodeHairInfo",
        "OBJECT_INFO": "ShaderNodeObjectInfo",
        "PARTICLE_INFO": "ShaderNodeParticleInfo",
        "TEX_ENVIRONMENT": "ShaderNodeTexEnvironment",
        "TEX_SKY": "ShaderNodeTexSky",
        "VOLUME_SCATTER": "ShaderNodeVolumeScatter",
        "VOLUME_ABSORPTION": "ShaderNodeVolumeAbsorption",
        "VOLUME_PRINCIPLED": "ShaderNodeVolumePrincipled",
        "SUBSURFACE_SCATTERING": "ShaderNodeSubsurfaceScattering",
        "GLASS_BSDF": "ShaderNodeBsdfGlass",
        "TRANSPARENT_BSDF": "ShaderNodeBsdfTransparent",
        "REFRACTION_BSDF": "ShaderNodeBsdfRefraction",
        "GLOSSY_BSDF": "ShaderNodeBsdfGlossy",
        "DIFFUSE_BSDF": "ShaderNodeBsdfDiffuse",
        "EMISSION": "ShaderNodeEmission",
        "BACKGROUND": "ShaderNodeBackground",
        "HOLDOUT": "ShaderNodeHoldout",
        "VOLUME_INFO": "ShaderNodeVolumeInfo",
        "ATTRIBUTE": "ShaderNodeAttribute",
        "BEVEL": "ShaderNodeBevel",
        "AMBIENT_OCCLUSION": "ShaderNodeAmbientOcclusion",
        "WIREFRAME": "ShaderNodeWireframe",
        "WAVELENGTH": "ShaderNodeWavelength",
        "BLACKBODY": "ShaderNodeBlackbody",
        "UV_MAP": "ShaderNodeUVMap",
        "VERTEX_COLOR": "ShaderNodeVertexColor",
        "GROUP": "ShaderNodeGroup",
        "GROUP_INPUT": "NodeGroupInput",
        "GROUP_OUTPUT": "NodeGroupOutput",
    }

    # If it's already a proper Blender API name, return as-is
    if node_type.startswith("ShaderNode") or node_type.startswith("Node"):
        return node_type

    # Convert legacy name to proper name
    return legacy_mapping.get(node_type, node_type)


def _deserialize_node_properties(node: bpy.types.Node, properties: Dict[str, Any]) -> None:
    """
    Deserialize node properties.

    Args:
        node: The node to set properties on
        properties: Dictionary of properties to set
    """
    for key, value in properties.items():
        if hasattr(node, key):
            try:
                setattr(node, key, value)
            except (AttributeError, TypeError):
                # Skip properties that can't be set
                pass


def _deserialize_default_value(socket: bpy.types.NodeSocket, value: Any) -> None:
    """
    Deserialize a default value for a socket.

    Args:
        socket: The socket to set the default value on
        value: The serialized default value
    """
    try:
        if isinstance(value, list):
            if len(value) == 3:
                # Handle RGB values
                if socket.type == 'RGBA':
                    # For RGBA sockets, add alpha component
                    socket.default_value = list(value) + [1.0]
                else:
                    # For other sockets, use as vector or color
                    socket.default_value = mathutils.Vector(value)
            elif len(value) == 4:
                # Handle RGBA values
                if socket.type == 'RGBA':
                    socket.default_value = value
                else:
                    # For non-RGBA sockets, use RGB part only
                    socket.default_value = mathutils.Vector(value[:3]) if hasattr(socket, 'default_value') else value[:3]
            else:
                socket.default_value = value
        else:
            socket.default_value = value
    except (AttributeError, TypeError) as e:
        # Skip if can't set the value, but log for debugging
        print(f"Warning: Could not set default value for socket {socket.name}: {e}")
        pass


def _deserialize_link(node_tree: bpy.types.NodeTree, link_data: Dict[str, Any], nodes_dict: Dict[str, bpy.types.Node]) -> None:
    """
    Deserialize a link between nodes.

    Args:
        node_tree: The node tree to add the link to
        link_data: Dictionary containing serialized link data
        nodes_dict: Dictionary mapping node names to node objects
    """
    from_node_name = link_data.get("from_node")
    to_node_name = link_data.get("to_node")
    from_socket_id = link_data.get("from_socket")
    to_socket_id = link_data.get("to_socket")

    if from_node_name not in nodes_dict or to_node_name not in nodes_dict:
        return  # Skip if nodes don't exist

    from_node = nodes_dict[from_node_name]
    to_node = nodes_dict[to_node_name]

    # Find the sockets
    from_socket = None
    to_socket = None

    for output in from_node.outputs:
        if output.identifier == from_socket_id:
            from_socket = output
            break

    for input_socket in to_node.inputs:
        if input_socket.identifier == to_socket_id:
            to_socket = input_socket
            break

    if from_socket and to_socket:
        node_tree.links.new(from_socket, to_socket)


# Clipboard functions

def copy_material_to_clipboard(material_name: str) -> bool:
    """
    Copy a material to the system clipboard as JSON.

    Args:
        material_name: Name of the material to copy

    Returns:
        True if successful, False otherwise
    """
    if not HAS_CLIPBOARD:
        print("Error: pyperclip not installed. Install with: pip install pyperclip")
        return False

    try:
        material = bpy.data.materials[material_name]
        json_str = serialize_material(material)
        pyperclip.copy(json_str)
        print(f"✓ Material '{material_name}' copied to clipboard")
        return True
    except KeyError:
        print(f"Error: Material '{material_name}' not found")
        return False
    except ValueError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def paste_material_from_clipboard(material_name: Optional[str] = None) -> Optional[bpy.types.Material]:
    """
    Paste a material from the system clipboard.

    Args:
        material_name: Optional name for the new material

    Returns:
        The newly created material, or None if failed
    """
    if not HAS_CLIPBOARD:
        print("Error: pyperclip not installed. Install with: pip install pyperclip")
        return None

    try:
        json_str = pyperclip.paste()
        material = deserialize_material(json_str, material_name)
        print(f"✓ Material pasted from clipboard: {material.name}")
        return material
    except Exception as e:
        print(f"Error pasting material: {e}")
        return None


# Example usage functions

def export_material_to_console(material_name: str) -> None:
    """
    Export a material to JSON and print it to the console.

    Args:
        material_name: Name of the material to export
    """
    try:
        material = bpy.data.materials[material_name]
        json_str = serialize_material(material)
        print("=" * 50)
        print(f"EXPORTED MATERIAL: {material_name}")
        print("=" * 50)
        print(json_str)
        print("=" * 50)
    except KeyError:
        print(f"Error: Material '{material_name}' not found")
    except ValueError as e:
        print(f"Error: {e}")


def import_material_from_json(json_str: str, new_material_name: Optional[str] = None) -> None:
    """
    Import a material from JSON string.

    Args:
        json_str: JSON string containing material data
        new_material_name: Optional name for the new material
    """
    try:
        material = deserialize_material(json_str, new_material_name)
        print(f"Successfully imported material: {material.name}")
    except ValueError as e:
        print(f"Error importing material: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


class MATERIAL_SERIALIZER_OT_copy(bpy.types.Operator):
    """Copy the active material to clipboard as JSON"""
    bl_idname = "material_serializer.copy"
    bl_label = "Copy Material to Clipboard"
    bl_description = "Copy the active material to clipboard as JSON"

    @classmethod
    def poll(cls, context):
        return (context.active_object and
                context.active_object.active_material and
                context.active_object.active_material.use_nodes)

    def execute(self, context):
        material = context.active_object.active_material
        if copy_material_to_clipboard(material.name):
            self.report({'INFO'}, f"Material '{material.name}' copied to clipboard")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to copy material")
            return {'CANCELLED'}


class MATERIAL_SERIALIZER_OT_paste(bpy.types.Operator):
    """Paste material from clipboard"""
    bl_idname = "material_serializer.paste"
    bl_label = "Paste Material from Clipboard"
    bl_description = "Paste material from clipboard JSON"

    def execute(self, context):
        material = paste_material_from_clipboard()
        if material:
            # Assign to active object if it exists
            if context.active_object:
                context.active_object.active_material = material
            self.report({'INFO'}, f"Material '{material.name}' pasted from clipboard")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to paste material")
            return {'CANCELLED'}


class MATERIAL_SERIALIZER_PT_panel(bpy.types.Panel):
    """Material Serializer Panel in Shader Editor"""
    bl_label = "Material Serializer"
    bl_idname = "MATERIAL_SERIALIZER_PT_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ShaderNodeTree'

    def draw(self, context):
        layout = self.layout

        # Copy button
        row = layout.row()
        row.operator("material_serializer.copy", icon='COPYDOWN')

        # Paste button
        row = layout.row()
        row.operator("material_serializer.paste", icon='PASTEDOWN')

        # Status info
        if not HAS_CLIPBOARD:
            box = layout.box()
            box.label(text="Warning: pyperclip not installed", icon='ERROR')
            box.label(text="Install with: pip install pyperclip")


# Registration functions for Blender addon

def register():
    """Register the addon."""
    bpy.utils.register_class(MATERIAL_SERIALIZER_OT_copy)
    bpy.utils.register_class(MATERIAL_SERIALIZER_OT_paste)
    bpy.utils.register_class(MATERIAL_SERIALIZER_PT_panel)


def unregister():
    """Unregister the addon."""
    bpy.utils.unregister_class(MATERIAL_SERIALIZER_PT_panel)
    bpy.utils.unregister_class(MATERIAL_SERIALIZER_OT_paste)
    bpy.utils.unregister_class(MATERIAL_SERIALIZER_OT_copy)


if __name__ == "__main__":
    # Example usage when run as script
    print("Material Serializer/Deserializer loaded")
    print("Use export_material_to_console('MaterialName') to export")
    print("Use import_material_from_json(json_string) to import")
