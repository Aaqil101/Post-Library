import bpy
from dictionaries import (COLORS_DICT)

#initialize LensDistortion node group
def lensdistortion_node(context, operator):

    #enable use nodes
    bpy.context.scene.use_nodes = True

    # variables
    scene = bpy.context.scene
    compositor_node_tree = scene.node_tree

    # Add Lens Distortion node
    lensdistortion_node = compositor_node_tree.nodes.new('CompositorNodeLensdist')

    # Enable fit option
    lensdistortion_node.use_fit = True

    # Adjust the distortion and dispersion values
    lensdistortion_node.inputs[1].default_value = 0.01
    lensdistortion_node.inputs[2].default_value = 0.005

    # Set a custom color for the Lens Distortion node
    lensdistortion_node.use_custom_color = True # Enable custom color
    lensdistortion_node.color = COLORS_DICT["LIGHT_BLUE"] # Set to a light blue color (R, G, B)

    # Resize the node
    lensdistortion_node.width = 150

    # Deselect the Lens Distortion node
    lensdistortion_node.select = False

    return lensdistortion_node


"""
! Deprecated code, do not use it
!# initialize LensDistortion node group
!def lensdistortion_node(context, operator):
!
!    #enable use nodes
!    bpy.context.scene.use_nodes = True
!
!    # variables
!    scene = bpy.context.scene
!    compositor_node_tree = scene.node_tree
!
!    # Add Lens Distortion node
!    lensdistortion_node = compositor_node_tree.nodes.new('CompositorNodeLensdist')
!
!    # Get the Lens Distortion node
!    lens_distortion_node = context.scene.node_tree.nodes.get("Lens Distortion")
!
!    for node in context.scene.node_tree.nodes:
!        if node.type == 'LENSDIST':
!            # Adjust the distortion and dispersion values
!            node.inputs[1].default_value = 0.01
!            node.inputs[2].default_value = 0.005
!
!            # Enable fit option
!            node.use_fit = True
!
!            # Set a custom color for the Lens Distortion node
!            node.use_custom_color = True # Enable custom color
!            node.color = COLORS_DICT["LIGHT_BLUE"] # Set to a light blue color (R, G, B)
!            lens_distortion_node.select = False
!
!    return lensdistortion_node
"""