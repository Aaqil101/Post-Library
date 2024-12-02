import bpy
from dictionaries import COLORS_DICT

#initialize Chromatic Aberration node group
def chromatic_aberration_node_group(context, operator, group_name):
    #enable use nodes
    bpy.context.scene.use_nodes = True

    chromatic_aberration = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    chromatic_aberration.color_tag = 'FILTER'
    chromatic_aberration.description = "This node group is used to create a chromatic aberration effect. The effect is based on the principles of optics and creates a color fringing effect on the image."
    chromatic_aberration.default_group_node_width = 197

    #chromatic_aberration interface
    #Socket Image
    image_socket = chromatic_aberration.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket_1 = chromatic_aberration.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'


    #initialize chromatic_aberration nodes
    #node CA Group Input
    ca_group_input = chromatic_aberration.nodes.new("NodeGroupInput")
    ca_group_input.label = "CA Group Input"
    ca_group_input.name = "CA Group Input"
    ca_group_input.use_custom_color = True
    ca_group_input.color = (0.23529097437858582, 0.2235269844532013, 0.21568608283996582)

    #node CA Separate Color
    ca_separate_color = chromatic_aberration.nodes.new("CompositorNodeSeparateColor")
    ca_separate_color.label = "CA Separate Color"
    ca_separate_color.name = "CA Separate Color"
    ca_separate_color.use_custom_color = True
    ca_separate_color.color = (0.3019622266292572, 0.3803923726081848, 0.3764711916446686)
    ca_separate_color.mode = 'RGB'
    ca_separate_color.ycc_mode = 'ITUBT709'

    #node CA Directional Blur 00
    ca_directional_blur_00 = chromatic_aberration.nodes.new("CompositorNodeDBlur")
    ca_directional_blur_00.label = "CA Directional Blur 00"
    ca_directional_blur_00.name = "CA Directional Blur 00"
    ca_directional_blur_00.use_custom_color = True
    ca_directional_blur_00.color = COLORS_DICT["DARK_PURPLE"]
    ca_directional_blur_00.angle = 0.0
    ca_directional_blur_00.center_x = 0.5
    ca_directional_blur_00.center_y = 0.5
    ca_directional_blur_00.distance = 0.0
    ca_directional_blur_00.iterations = 3
    ca_directional_blur_00.spin = 0.0
    ca_directional_blur_00.zoom = 0.0

    #node CA Directional Blur 01
    ca_directional_blur_01 = chromatic_aberration.nodes.new("CompositorNodeDBlur")
    ca_directional_blur_01.label = "CA Directional Blur 01"
    ca_directional_blur_01.name = "CA Directional Blur 01"
    ca_directional_blur_01.use_custom_color = True
    ca_directional_blur_01.color = COLORS_DICT["DARK_PURPLE"]
    ca_directional_blur_01.angle = 0.0
    ca_directional_blur_01.center_x = 0.5
    ca_directional_blur_01.center_y = 0.5
    ca_directional_blur_01.distance = 0.0
    ca_directional_blur_01.iterations = 3
    ca_directional_blur_01.spin = 0.00017453292093705386
    ca_directional_blur_01.zoom = 0.004999999888241291

    #node CA Directional Blur 02
    ca_directional_blur_02 = chromatic_aberration.nodes.new("CompositorNodeDBlur")
    ca_directional_blur_02.label = "CA Directional Blur 02"
    ca_directional_blur_02.name = "CA Directional Blur 02"
    ca_directional_blur_02.use_custom_color = True
    ca_directional_blur_02.color = COLORS_DICT["DARK_PURPLE"]
    ca_directional_blur_02.angle = 0.0
    ca_directional_blur_02.center_x = 0.5
    ca_directional_blur_02.center_y = 0.5
    ca_directional_blur_02.distance = 0.0
    ca_directional_blur_02.iterations = 3
    ca_directional_blur_02.spin = 0.00017453292093705386
    ca_directional_blur_02.zoom = 0.004000000189989805

    #node CA Blur 00
    ca_blur_00 = chromatic_aberration.nodes.new("CompositorNodeBlur")
    ca_blur_00.label = "CA Blur 00"
    ca_blur_00.name = "CA Blur 00"
    ca_blur_00.use_custom_color = True
    ca_blur_00.color = (0.4627402424812317, 0.3294066786766052, 0.37254956364631653)
    ca_blur_00.aspect_correction = 'NONE'
    ca_blur_00.factor = 0.0
    ca_blur_00.factor_x = 0.0
    ca_blur_00.factor_y = 0.0
    ca_blur_00.filter_type = 'FAST_GAUSS'
    ca_blur_00.size_x = 0
    ca_blur_00.size_y = 0
    ca_blur_00.use_bokeh = False
    ca_blur_00.use_extended_bounds = False
    ca_blur_00.use_gamma_correction = False
    ca_blur_00.use_relative = False
    ca_blur_00.use_variable_size = False
    #Size
    ca_blur_00.inputs[1].default_value = 1.0

    #node CA Blur 01
    ca_blur_01 = chromatic_aberration.nodes.new("CompositorNodeBlur")
    ca_blur_01.label = "CA Blur 01"
    ca_blur_01.name = "CA Blur 01"
    ca_blur_01.use_custom_color = True
    ca_blur_01.color = (0.46277910470962524, 0.32939282059669495, 0.3725355267524719)
    ca_blur_01.aspect_correction = 'NONE'
    ca_blur_01.factor = 0.0
    ca_blur_01.factor_x = 0.0
    ca_blur_01.factor_y = 0.0
    ca_blur_01.filter_type = 'FAST_GAUSS'
    ca_blur_01.size_x = 1
    ca_blur_01.size_y = 1
    ca_blur_01.use_bokeh = False
    ca_blur_01.use_extended_bounds = False
    ca_blur_01.use_gamma_correction = False
    ca_blur_01.use_relative = False
    ca_blur_01.use_variable_size = False
    #Size
    ca_blur_01.inputs[1].default_value = 1.0

    #node CA Blur 02
    ca_blur_02 = chromatic_aberration.nodes.new("CompositorNodeBlur")
    ca_blur_02.label = "CA Blur 02"
    ca_blur_02.name = "CA Blur 02"
    ca_blur_02.use_custom_color = True
    ca_blur_02.color = COLORS_DICT["DARK_PURPLE"]
    ca_blur_02.aspect_correction = 'NONE'
    ca_blur_02.factor = 0.0
    ca_blur_02.factor_x = 0.0
    ca_blur_02.factor_y = 0.0
    ca_blur_02.filter_type = 'FAST_GAUSS'
    ca_blur_02.size_x = 1
    ca_blur_02.size_y = 1
    ca_blur_02.use_bokeh = False
    ca_blur_02.use_extended_bounds = False
    ca_blur_02.use_gamma_correction = False
    ca_blur_02.use_relative = False
    ca_blur_02.use_variable_size = False
    #Size
    ca_blur_02.inputs[1].default_value = 1.0

    #node CA Combine Color
    ca_combine_color = chromatic_aberration.nodes.new("CompositorNodeCombineColor")
    ca_combine_color.label = "CA Combine Color"
    ca_combine_color.name = "CA Combine Color"
    ca_combine_color.use_custom_color = True
    ca_combine_color.color = (0.3019486963748932, 0.38037946820259094, 0.37645700573921204)
    ca_combine_color.mode = 'RGB'

    #node CA Reroute 00
    ca_reroute_00 = chromatic_aberration.nodes.new("NodeReroute")
    ca_reroute_00.name = "CA Reroute 00"
    ca_reroute_00.socket_idname = "NodeSocketFloat"
    #node CA Reroute 01
    ca_reroute_01 = chromatic_aberration.nodes.new("NodeReroute")
    ca_reroute_01.name = "CA Reroute 01"
    ca_reroute_01.socket_idname = "NodeSocketFloat"
    #node CA Group Output
    ca_group_output = chromatic_aberration.nodes.new("NodeGroupOutput")
    ca_group_output.label = "CA Group Output"
    ca_group_output.name = "CA Group Output"
    ca_group_output.use_custom_color = True
    ca_group_output.color = (0.23529097437858582, 0.2235269844532013, 0.21568608283996582)
    ca_group_output.is_active_output = True


    #Set locations
    ca_group_input.location = (-200.0, 0.0)
    ca_separate_color.location = (0.0, 0.0)
    ca_directional_blur_00.location = (300.0, 560.0)
    ca_directional_blur_01.location = (440.0, 260.0)
    ca_directional_blur_02.location = (594.5105590820312, -48.480064392089844)
    ca_blur_00.location = (631.17578125, 560.0)
    ca_blur_01.location = (772.6263427734375, 260.0)
    ca_blur_02.location = (903.1117553710938, -48.480064392089844)
    ca_combine_color.location = (1431.571044921875, 238.14013671875)
    ca_reroute_00.location = (620.0, -360.0)
    ca_reroute_01.location = (1000.0, -360.0)
    ca_group_output.location = (1628.959716796875, 236.7657012939453)

    #Set dimensions
    ca_group_input.width, ca_group_input.height = 140.0, 100.0
    ca_separate_color.width, ca_separate_color.height = 140.0, 100.0
    ca_directional_blur_00.width, ca_directional_blur_00.height = 153.22442626953125, 100.0
    ca_directional_blur_01.width, ca_directional_blur_01.height = 156.596923828125, 100.0
    ca_directional_blur_02.width, ca_directional_blur_02.height = 155.35626220703125, 100.0
    ca_blur_00.width, ca_blur_00.height = 140.0, 100.0
    ca_blur_01.width, ca_blur_01.height = 140.0, 100.0
    ca_blur_02.width, ca_blur_02.height = 140.0, 100.0
    ca_combine_color.width, ca_combine_color.height = 140.0, 100.0
    ca_reroute_00.width, ca_reroute_00.height = 16.0, 100.0
    ca_reroute_01.width, ca_reroute_01.height = 16.0, 100.0
    ca_group_output.width, ca_group_output.height = 140.0, 100.0

    #initialize chromatic_aberration links
    #ca_group_input.Image -> ca_separate_color.Image
    chromatic_aberration.links.new(ca_group_input.outputs[0], ca_separate_color.inputs[0])

    #ca_separate_color.Red -> ca_directional_blur_00.Image
    chromatic_aberration.links.new(ca_separate_color.outputs[0], ca_directional_blur_00.inputs[0])

    #ca_separate_color.Green -> ca_directional_blur_01.Image
    chromatic_aberration.links.new(ca_separate_color.outputs[1], ca_directional_blur_01.inputs[0])

    #ca_separate_color.Blue -> ca_directional_blur_02.Image
    chromatic_aberration.links.new(ca_separate_color.outputs[2], ca_directional_blur_02.inputs[0])

    #ca_directional_blur_00.Image -> ca_blur_00.Image
    chromatic_aberration.links.new(ca_directional_blur_00.outputs[0], ca_blur_00.inputs[0])

    #ca_directional_blur_01.Image -> ca_blur_01.Image
    chromatic_aberration.links.new(ca_directional_blur_01.outputs[0], ca_blur_01.inputs[0])

    #ca_directional_blur_02.Image -> ca_blur_02.Image
    chromatic_aberration.links.new(ca_directional_blur_02.outputs[0], ca_blur_02.inputs[0])

    #ca_blur_02.Image -> ca_combine_color.Blue
    chromatic_aberration.links.new(ca_blur_02.outputs[0], ca_combine_color.inputs[2])

    #ca_blur_01.Image -> ca_combine_color.Green
    chromatic_aberration.links.new(ca_blur_01.outputs[0], ca_combine_color.inputs[1])

    #ca_blur_00.Image -> ca_combine_color.Red
    chromatic_aberration.links.new(ca_blur_00.outputs[0], ca_combine_color.inputs[0])

    #ca_reroute_01.Output -> ca_combine_color.Alpha
    chromatic_aberration.links.new(ca_reroute_01.outputs[0], ca_combine_color.inputs[3])

    #ca_separate_color.Alpha -> ca_reroute_00.Input
    chromatic_aberration.links.new(ca_separate_color.outputs[3], ca_reroute_00.inputs[0])

    #ca_reroute_00.Output -> ca_reroute_01.Input
    chromatic_aberration.links.new(ca_reroute_00.outputs[0], ca_reroute_01.inputs[0])

    #ca_combine_color.Image -> ca_group_output.Image
    chromatic_aberration.links.new(ca_combine_color.outputs[0], ca_group_output.inputs[0])

    return chromatic_aberration