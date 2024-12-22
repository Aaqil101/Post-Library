import bpy
from dictionaries import COLORS_DICT

#initialize Contrast node group
def contrast_node_group(context, operator, group_name):
    #enable use nodes
    bpy.context.scene.use_nodes = True

    contrast = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    contrast.color_tag = 'COLOR'
    contrast.description = "This node group is used to add contrast to an image. It works by multiplying the color values of the image by a contrast factor."
    contrast.default_group_node_width = 149
    

    #contrast interface
    #Socket Image
    image_socket = contrast.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'
    image_socket.hide_value = True

    #Socket Image
    image_socket_1 = contrast.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'

    #Socket Fac
    fac_socket = contrast.interface.new_socket(name = "Fac", in_out='INPUT', socket_type = 'NodeSocketFloat')
    fac_socket.default_value = 0.3
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = 'FACTOR'
    fac_socket.attribute_domain = 'POINT'

    #Socket Size X
    size_x_socket = contrast.interface.new_socket(name = "Size X", in_out='INPUT', socket_type = 'NodeSocketFloat')
    size_x_socket.default_value = 20.0
    size_x_socket.min_value = 0.0
    size_x_socket.max_value = 2048.0
    size_x_socket.subtype = 'NONE'
    size_x_socket.attribute_domain = 'POINT'

    #Socket Size Y
    size_y_socket = contrast.interface.new_socket(name = "Size Y", in_out='INPUT', socket_type = 'NodeSocketFloat')
    size_y_socket.default_value = 20.0
    size_y_socket.min_value = 0.0
    size_y_socket.max_value = 2048.0
    size_y_socket.subtype = 'NONE'
    size_y_socket.attribute_domain = 'POINT'


    #initialize contrast nodes
    #node C Group Output
    c_group_output = contrast.nodes.new("NodeGroupOutput")
    c_group_output.label = "C Group Output"
    c_group_output.name = "C Group Output"
    c_group_output.use_custom_color = True
    c_group_output.color = COLORS_DICT["DARK_GRAY"]
    c_group_output.is_active_output = True
    c_group_output.inputs[1].hide = True

    #node C Group Input
    c_group_input = contrast.nodes.new("NodeGroupInput")
    c_group_input.label = "C Group Input"
    c_group_input.name = "C Group Input"
    c_group_input.use_custom_color = True
    c_group_input.color = COLORS_DICT["DARK_GRAY"]
    c_group_input.outputs[2].hide = True
    c_group_input.outputs[3].hide = True
    c_group_input.outputs[4].hide = True

    #node C Blur
    c_blur = contrast.nodes.new("CompositorNodeBlur")
    c_blur.label = "C Blur"
    c_blur.name = "C Blur"
    c_blur.use_custom_color = True
    c_blur.color = COLORS_DICT["DARK_PURPLE"]
    c_blur.aspect_correction = 'NONE'
    c_blur.factor = 0.0
    c_blur.factor_x = 0.0
    c_blur.factor_y = 0.0
    c_blur.filter_type = 'GAUSS'
    c_blur.size_x = 20
    c_blur.size_y = 20
    c_blur.use_bokeh = False
    c_blur.use_extended_bounds = False
    c_blur.use_gamma_correction = False
    c_blur.use_relative = False
    c_blur.use_variable_size = False
    c_blur.inputs[1].hide = True
    #Size
    c_blur.inputs[1].default_value = 1.0

    #node C Overlay
    c_overlay = contrast.nodes.new("CompositorNodeMixRGB")
    c_overlay.label = "C Overlay"
    c_overlay.name = "C Overlay"
    c_overlay.use_custom_color = True
    c_overlay.color = COLORS_DICT["BROWN"]
    c_overlay.blend_type = 'OVERLAY'
    c_overlay.use_alpha = False
    c_overlay.use_clamp = False


    #Set locations
    c_group_output.location = (340.0, 60.0)
    c_group_input.location = (-340.0, 20.0)
    c_blur.location = (-60.0, -80.0)
    c_overlay.location = (140.0, 60.0)

    #Set dimensions
    c_group_output.width, c_group_output.height = 140.0, 100.0
    c_group_input.width, c_group_input.height = 140.0, 100.0
    c_blur.width, c_blur.height = 140.0, 100.0
    c_overlay.width, c_overlay.height = 140.0, 100.0

    #initialize contrast links
    #c_blur.Image -> c_overlay.Image
    contrast.links.new(c_blur.outputs[0], c_overlay.inputs[2])

    #c_group_input.Image -> c_blur.Image
    contrast.links.new(c_group_input.outputs[0], c_blur.inputs[0])

    #c_overlay.Image -> c_group_output.Image
    contrast.links.new(c_overlay.outputs[0], c_group_output.inputs[0])

    #c_group_input.Image -> c_overlay.Image
    contrast.links.new(c_group_input.outputs[0], c_overlay.inputs[1])

    #c_group_input.Fac -> c_overlay.Fac
    contrast.links.new(c_group_input.outputs[1], c_overlay.inputs[0])

    return contrast