import bpy, mathutils
from dictionaries import COLORS_DICT

#initialize Halation node group
def halation_node_group(context, operator, group_name):
    #enable use nodes
    bpy.context.scene.use_nodes = True

    halation = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    halation.color_tag = 'FILTER'
    halation.description = "Halation is a color grading filter that adds a warm glow around the edges of the frame, giving it a retro look."
    halation.default_group_node_width = 151

    #halation interface
    #Socket Image
    image_socket = halation.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'
    image_socket.hide_value = True

    #Socket Image
    image_socket_1 = halation.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'

    #Socket Size X
    size_x_socket = halation.interface.new_socket(name = "Size X", in_out='INPUT', socket_type = 'NodeSocketFloat')
    size_x_socket.default_value = 20.0
    size_x_socket.min_value = 0.0
    size_x_socket.max_value = 2048.0
    size_x_socket.subtype = 'NONE'
    size_x_socket.attribute_domain = 'POINT'

    #Socket Size Y
    size_y_socket = halation.interface.new_socket(name = "Size Y", in_out='INPUT', socket_type = 'NodeSocketFloat')
    size_y_socket.default_value = 20.0
    size_y_socket.min_value = 0.0
    size_y_socket.max_value = 2048.0
    size_y_socket.subtype = 'NONE'
    size_y_socket.attribute_domain = 'POINT'

    #Socket Fac
    fac_socket = halation.interface.new_socket(name = "Fac", in_out='INPUT', socket_type = 'NodeSocketFloat')
    fac_socket.default_value = 1.0
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = 'FACTOR'
    fac_socket.attribute_domain = 'POINT'
    fac_socket.description = "Color Balance Factor"

    #initialize halation nodes
    #node H Group Output
    h_group_output = halation.nodes.new("NodeGroupOutput")
    h_group_output.label = "H Group Output"
    h_group_output.name = "H Group Output"
    h_group_output.use_custom_color = True
    h_group_output.color = COLORS_DICT["DARK_GRAY"]
    h_group_output.is_active_output = True
    h_group_output.inputs[1].hide = True

    #node H Group Input
    h_group_input = halation.nodes.new("NodeGroupInput")
    h_group_input.label = "H Group Input"
    h_group_input.name = "H Group Input"
    h_group_input.use_custom_color = True
    h_group_input.color = COLORS_DICT["DARK_GRAY"]
    h_group_input.outputs[1].hide = True
    h_group_input.outputs[2].hide = True
    h_group_input.outputs[4].hide = True

    #node H Blur
    h_blur = halation.nodes.new("CompositorNodeBlur")
    h_blur.label = "H Blur"
    h_blur.name = "H Blur"
    h_blur.use_custom_color = True
    h_blur.color = COLORS_DICT["DARK_PURPLE"]
    h_blur.filter_type = 'GAUSS'
    h_blur.size_x = 20
    h_blur.size_y = 20
    h_blur.use_extended_bounds = False
    h_blur.use_gamma_correction = False
    h_blur.use_relative = False
    h_blur.use_variable_size = True

    #node H Combine Color
    h_combine_color = halation.nodes.new("CompositorNodeCombineColor")
    h_combine_color.label = "H Combine Color"
    h_combine_color.name = "H Combine Color"
    h_combine_color.use_custom_color = True
    h_combine_color.color = COLORS_DICT["DARK_BLUE"]
    h_combine_color.mode = 'RGB'
    #Alpha
    h_combine_color.inputs[3].default_value = 1.0

    #node H Separate Color
    h_separate_color = halation.nodes.new("CompositorNodeSeparateColor")
    h_separate_color.label = "H Separate Color"
    h_separate_color.name = "H Separate Color"
    h_separate_color.use_custom_color = True
    h_separate_color.color = COLORS_DICT["DARK_BLUE"]
    h_separate_color.mode = 'RGB'

    #node H Color Ramp
    h_color_ramp = halation.nodes.new("CompositorNodeValToRGB")
    h_color_ramp.label = "H Color Ramp"
    h_color_ramp.name = "H Color Ramp"
    h_color_ramp.use_custom_color = True
    h_color_ramp.color = COLORS_DICT["DARK_BLUE"]
    h_color_ramp.color_ramp.color_mode = 'RGB'
    h_color_ramp.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    h_color_ramp.color_ramp.elements.remove(h_color_ramp.color_ramp.elements[0])
    h_color_ramp_cre_0 = h_color_ramp.color_ramp.elements[0]
    h_color_ramp_cre_0.position = 0.0
    h_color_ramp_cre_0.alpha = 1.0
    h_color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    h_color_ramp_cre_1 = h_color_ramp.color_ramp.elements.new(1.0)
    h_color_ramp_cre_1.alpha = 1.0
    h_color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)

    #node H Color Balance
    h_color_balance = halation.nodes.new("CompositorNodeColorBalance")
    h_color_balance.label = "H Color Balance"
    h_color_balance.name = "H Color Balance"
    h_color_balance.use_custom_color = True
    h_color_balance.color = COLORS_DICT["BROWN"]
    h_color_balance.correction_method = 'LIFT_GAMMA_GAIN'
    h_color_balance.gain = mathutils.Color((1.0625041723251343, 0.9746971726417542, 0.9597135186195374))
    h_color_balance.gamma = mathutils.Color((1.0547555685043335, 0.9844463467597961, 0.95830899477005))
    h_color_balance.lift = mathutils.Color((1.0, 1.0, 1.0))

    #Set locations
    h_group_output.location = (1060.0, -120.0)
    h_group_input.location = (-820.0, -240.0)
    h_blur.location = (90.0, 120.0)
    h_combine_color.location = (430.0, -120.0)
    h_separate_color.location = (-630.0, -120.0)
    h_color_ramp.location = (-250.0, 120.0)
    h_color_balance.location = (630.0, -120.0)

    #Set dimensions
    h_group_output.width, h_group_output.height = 140.0, 100.0
    h_group_input.width, h_group_input.height = 140.0, 100.0
    h_blur.width, h_blur.height = 140.0, 100.0
    h_combine_color.width, h_combine_color.height = 140.0, 100.0
    h_separate_color.width, h_separate_color.height = 140.0, 100.0
    h_color_ramp.width, h_color_ramp.height = 240.0, 100.0
    h_color_balance.width, h_color_balance.height = 400.0, 100.0

    #initialize halation links
    #h_separate_color.Red -> h_color_ramp.Fac
    halation.links.new(h_separate_color.outputs[0], h_color_ramp.inputs[0])

    #h_separate_color.Red -> h_blur.Image
    halation.links.new(h_separate_color.outputs[0], h_blur.inputs[0])

    #h_combine_color.Image -> h_color_balance.Image
    halation.links.new(h_combine_color.outputs[0], h_color_balance.inputs[1])

    #h_separate_color.Blue -> h_combine_color.Blue
    halation.links.new(h_separate_color.outputs[2], h_combine_color.inputs[2])

    #h_separate_color.Green -> h_combine_color.Green
    halation.links.new(h_separate_color.outputs[1], h_combine_color.inputs[1])

    #h_blur.Image -> h_combine_color.Red
    halation.links.new(h_blur.outputs[0], h_combine_color.inputs[0])

    #h_color_balance.Image -> h_group_output.Image
    halation.links.new(h_color_balance.outputs[0], h_group_output.inputs[0])

    #h_group_input.Image -> h_separate_color.Image
    halation.links.new(h_group_input.outputs[0], h_separate_color.inputs[0])

    #h_color_ramp.Image -> h_blur.Size
    halation.links.new(h_color_ramp.outputs[0], h_blur.inputs[1])

    #h_group_input.Fac -> h_color_balance.Fac
    halation.links.new(h_group_input.outputs[3], h_color_balance.inputs[0])

    return halation