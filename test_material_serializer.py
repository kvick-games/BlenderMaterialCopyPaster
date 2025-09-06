"""
Test script for the Material Serializer/Deserializer
===================================================

This script demonstrates and tests the functionality of the material serializer.
"""

import bpy
import sys
import os

# Add the current directory to Python path to import the serializer
sys.path.append(os.path.dirname(__file__))
from material_serializer import serialize_material, deserialize_material, export_material_to_console, import_material_from_json


def create_test_material():
    """Create a simple test material with nodes."""
    # Create new material
    test_mat = bpy.data.materials.new(name="Test_Material")
    test_mat.use_nodes = True

    # Clear default nodes
    nodes = test_mat.node_tree.nodes
    nodes.clear()

    # Create nodes
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    output_node.location = (400, 0)

    principled_node = nodes.new(type="ShaderNodeBsdfPrincipled")
    principled_node.location = (0, 0)

    # Set some properties
    principled_node.inputs['Base Color'].default_value = (1.0, 0.5, 0.0, 1.0)  # Orange color
    principled_node.inputs['Metallic'].default_value = 0.8
    principled_node.inputs['Roughness'].default_value = 0.2

    # Create links
    links = test_mat.node_tree.links
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

    return test_mat


def test_serialization():
    """Test the serialization functionality."""
    print("Creating test material...")
    test_mat = create_test_material()

    print("Serializing material...")
    try:
        json_str = serialize_material(test_mat)
        print("✓ Serialization successful!")
        print(f"JSON length: {len(json_str)} characters")
        return json_str
    except Exception as e:
        print(f"✗ Serialization failed: {e}")
        return None


def test_deserialization(json_str):
    """Test the deserialization functionality."""
    if not json_str:
        print("No JSON string to deserialize")
        return

    print("\nDeserializing material...")
    try:
        new_mat = deserialize_material(json_str, "Deserialized_Test_Material")
        print("✓ Deserialization successful!")
        print(f"New material name: {new_mat.name}")
        print(f"Node count: {len(new_mat.node_tree.nodes)}")
        print(f"Link count: {len(new_mat.node_tree.links)}")

        # Verify the material has the expected properties
        nodes = new_mat.node_tree.nodes
        principled_nodes = [n for n in nodes if n.type == 'BSDF_PRINCIPLED']
        if principled_nodes:
            principled = principled_nodes[0]
            base_color = principled.inputs['Base Color'].default_value
            print(f"Base color: {base_color}")
            print(f"Metallic: {principled.inputs['Metallic'].default_value}")
            print(f"Roughness: {principled.inputs['Roughness'].default_value}")

        return new_mat
    except Exception as e:
        print(f"✗ Deserialization failed: {e}")
        return None


def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("MATERIAL SERIALIZER/Deserializer TEST")
    print("=" * 60)

    # Test serialization
    json_str = test_serialization()

    # Test deserialization
    new_mat = test_deserialization(json_str)

    # Test example functions
    print("\n" + "=" * 60)
    print("TESTING EXAMPLE FUNCTIONS")
    print("=" * 60)

    if json_str:
        print("Testing import_material_from_json...")
        try:
            import_material_from_json(json_str, "Example_Imported_Material")
            print("✓ Import function works!")
        except Exception as e:
            print(f"✗ Import function failed: {e}")

    # Test export function
    test_mat = bpy.data.materials.get("Test_Material")
    if test_mat:
        print("\nTesting export_material_to_console...")
        export_material_to_console("Test_Material")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
