# Blender Modules
import bpy
from bpy.types import Node

# Helper Modules
from helpers import Color


# initialize LensDistortion node group
def lensdistortion_node(context, operator) -> Node:
    # enable use nodes
    bpy.context.scene.use_nodes = True

    # variables
    scene = bpy.context.scene
    compositor_node_tree = scene.node_tree

    # Add Lens Distortion node
    lensdistortion_node = compositor_node_tree.nodes.new("CompositorNodeLensdist")

    # Enable fit option
    lensdistortion_node.use_fit = True

    # Adjust the distortion and dispersion values
    lensdistortion_node.inputs[1].default_value = 0.01
    lensdistortion_node.inputs[2].default_value = 0.005

    # Set a custom color for the Lens Distortion node
    lensdistortion_node.use_custom_color = True  # Enable custom color
    lensdistortion_node.color = Color.LIGHT_BLUE

    # Resize the node
    lensdistortion_node.width = 150

    # Deselect the Lens Distortion node
    lensdistortion_node.select = False

    return lensdistortion_node
