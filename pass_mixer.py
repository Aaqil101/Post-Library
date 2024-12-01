import bpy
from dictionaries import (COLORS_DICT)

#initialize PassMixer node group
def passmixer_node_group(context, operator, group_name):
    
    #enable use nodes
    bpy.context.scene.use_nodes = True

    passmixer = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    passmixer.color_tag = "CONVERTER"
    passmixer.default_group_node_width = 147
    passmixer.description = "A node group for mixing up the gloss, diff, trans and volume passes"

	#passmixer interface

    #Socket Image
    image_socket = passmixer.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Direct
    direct_socket = passmixer.interface.new_socket(name = "Direct", in_out='INPUT', socket_type = 'NodeSocketColor')
    direct_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    direct_socket.attribute_domain = 'POINT'
    direct_socket.hide_value = True

    #Socket Indirect
    indirect_socket = passmixer.interface.new_socket(name = "Indirect", in_out='INPUT', socket_type = 'NodeSocketColor')
    indirect_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    indirect_socket.attribute_domain = 'POINT'
    indirect_socket.hide_value = True

    #Socket Color
    color_socket = passmixer.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
    color_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.hide_value = True


    #initialize passmixer nodes
    #node PMR Group Output
    pmr_group_output = passmixer.nodes.new("NodeGroupOutput")
    pmr_group_output.label = "PMR Group Output"
    pmr_group_output.name = "PMR Group Output"
    pmr_group_output.use_custom_color = True
    pmr_group_output.color = COLORS_DICT["DARK_GRAY"]
    pmr_group_output.is_active_output = True
    pmr_group_output.inputs[1].hide = True

    #node PMR Group Input
    pmr_group_input = passmixer.nodes.new("NodeGroupInput")
    pmr_group_output.label = "PMR Group Input"
    pmr_group_input.name = "PMR Group Input"
    pmr_group_input.use_custom_color = True
    pmr_group_input.color = COLORS_DICT["DARK_GRAY"]
    pmr_group_input.outputs[3].hide = True

    #node add_passmixer
    add_passmixer = passmixer.nodes.new("CompositorNodeMixRGB")
    add_passmixer.label = "Add_PassMixer"
    add_passmixer.name = "add_passmixer"
    add_passmixer.use_custom_color = True
    add_passmixer.color = COLORS_DICT["BROWN"]
    add_passmixer.blend_type = 'ADD'
    add_passmixer.use_alpha = False
    add_passmixer.use_clamp = False
    add_passmixer.inputs[0].hide = True
    #Fac
    add_passmixer.inputs[0].default_value = 1.0

    #node multiply_passmixer
    multiply_passmixer = passmixer.nodes.new("CompositorNodeMixRGB")
    multiply_passmixer.label = "Multiply_PassMixer"
    multiply_passmixer.name = "multiply_passmixer"
    multiply_passmixer.use_custom_color = True
    multiply_passmixer.color = COLORS_DICT["BROWN"]
    multiply_passmixer.blend_type = 'MULTIPLY'
    multiply_passmixer.use_alpha = False
    multiply_passmixer.use_clamp = False
    multiply_passmixer.inputs[0].hide = True
    #Fac
    multiply_passmixer.inputs[0].default_value = 1.0


    #Set locations
    pmr_group_output.location = (280.0, 0.0)
    pmr_group_input.location = (-280.0, 0.0)
    add_passmixer.location = (-80.0, 0.0)
    multiply_passmixer.location = (100.0, 0.0)

    #Set dimensions
    pmr_group_output.width, pmr_group_output.height = 140.0, 100.0
    pmr_group_input.width, pmr_group_input.height = 140.0, 100.0
    add_passmixer.width, add_passmixer.height = 140.0, 100.0
    multiply_passmixer.width, multiply_passmixer.height = 154.79315185546875, 100.0

    #initialize passmixer links
    #add_passmixer.Image -> multiply_passmixer.Image
    passmixer.links.new(add_passmixer.outputs[0], multiply_passmixer.inputs[1])

    #pmr_group_input.Color -> multiply_passmixer.Image
    passmixer.links.new(pmr_group_input.outputs[2], multiply_passmixer.inputs[2])

    #pmr_group_input.Indirect -> add_passmixer.Image
    passmixer.links.new(pmr_group_input.outputs[1], add_passmixer.inputs[2])

    #pmr_group_input.Direct -> add_passmixer.Image
    passmixer.links.new(pmr_group_input.outputs[0], add_passmixer.inputs[1])

    #multiply_passmixer.Image -> pmr_group_output.Image
    passmixer.links.new(multiply_passmixer.outputs[0], pmr_group_output.inputs[0])

    return passmixer