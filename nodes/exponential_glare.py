# Blender Modules
import bpy
from bpy.types import NodeTree

# Helper Modules
from helpers import Color


# initialize Exponential Glare node group
def exponential_glare_node_group(context, operator, group_name) -> NodeTree:
    # enable use nodes
    bpy.context.scene.use_nodes = True

    exponential_glare = bpy.data.node_groups.new(group_name, "CompositorNodeTree")

    exponential_glare.color_tag = "FILTER"
    exponential_glare.description = "This node group is used to add exponential glare to an image, enhancing its highlights with a radiant glow effect."
    exponential_glare.default_group_node_width = 194

    # exponential_glare interface
    # Socket Image
    image_socket = exponential_glare.interface.new_socket(
        name="Image", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = "POINT"

    # Socket Image
    image_socket_1 = exponential_glare.interface.new_socket(
        name="Image", in_out="INPUT", socket_type="NodeSocketColor"
    )
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = "POINT"

    # Socket Strength
    strength_socket = exponential_glare.interface.new_socket(
        name="Strength", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    strength_socket.default_value = 0.0
    strength_socket.min_value = 0.0
    strength_socket.max_value = 1.0
    strength_socket.subtype = "FACTOR"
    strength_socket.attribute_domain = "POINT"

    # initialize exponential_glare nodes
    # node Group Input
    group_input = exponential_glare.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.use_custom_color = True
    group_input.color = Color.DARK_GRAY
    group_input.outputs[2].hide = True

    # node Blur 2p
    blur_2p = exponential_glare.nodes.new("CompositorNodeBlur")
    blur_2p.label = "Blur 2p"
    blur_2p.name = "Blur 2p"
    blur_2p.use_custom_color = True
    blur_2p.color = Color.DARK_PURPLE
    blur_2p.hide = True
    blur_2p.aspect_correction = "NONE"
    blur_2p.factor = 0.0
    blur_2p.factor_x = 0.0
    blur_2p.factor_y = 0.0
    blur_2p.filter_type = "FAST_GAUSS"
    blur_2p.size_x = 2
    blur_2p.size_y = 2
    blur_2p.use_bokeh = False
    blur_2p.use_extended_bounds = False
    blur_2p.use_gamma_correction = False
    blur_2p.use_relative = False
    blur_2p.use_variable_size = False
    # Size
    blur_2p.inputs[1].default_value = 1.0

    # node EG Add 00
    eg_add_00 = exponential_glare.nodes.new("CompositorNodeMixRGB")
    eg_add_00.label = "EG Add 00"
    eg_add_00.name = "EG Add 00"
    eg_add_00.use_custom_color = True
    eg_add_00.color = Color.BROWN
    eg_add_00.hide = True
    eg_add_00.blend_type = "ADD"
    eg_add_00.use_alpha = False
    eg_add_00.use_clamp = False
    # Fac
    eg_add_00.inputs[0].default_value = 0.4000000059604645
    # Image
    eg_add_00.inputs[1].default_value = (1.0, 1.0, 1.0, 1.0)

    # node EG Add 01
    eg_add_01 = exponential_glare.nodes.new("CompositorNodeMixRGB")
    eg_add_01.label = "EG Add 01"
    eg_add_01.name = "EG Add 01"
    eg_add_01.use_custom_color = True
    eg_add_01.color = Color.BROWN
    eg_add_01.hide = True
    eg_add_01.blend_type = "ADD"
    eg_add_01.use_alpha = False
    eg_add_01.use_clamp = False
    # Fac
    eg_add_01.inputs[0].default_value = 0.20000000298023224

    # node Blur 4p
    blur_4p = exponential_glare.nodes.new("CompositorNodeBlur")
    blur_4p.label = "Blur 4p"
    blur_4p.name = "Blur 4p"
    blur_4p.use_custom_color = True
    blur_4p.color = Color.DARK_PURPLE
    blur_4p.hide = True
    blur_4p.aspect_correction = "NONE"
    blur_4p.factor = 0.0
    blur_4p.factor_x = 0.0
    blur_4p.factor_y = 0.0
    blur_4p.filter_type = "FAST_GAUSS"
    blur_4p.size_x = 4
    blur_4p.size_y = 4
    blur_4p.use_bokeh = False
    blur_4p.use_extended_bounds = False
    blur_4p.use_gamma_correction = False
    blur_4p.use_relative = False
    blur_4p.use_variable_size = False
    # Size
    blur_4p.inputs[1].default_value = 1.0

    # node Blur 8p
    blur_8p = exponential_glare.nodes.new("CompositorNodeBlur")
    blur_8p.label = "Blur 8p"
    blur_8p.name = "Blur 8p"
    blur_8p.use_custom_color = True
    blur_8p.color = Color.DARK_PURPLE
    blur_8p.hide = True
    blur_8p.filter_type = "FAST_GAUSS"
    blur_8p.size_x = 8
    blur_8p.size_y = 8
    blur_8p.use_extended_bounds = False
    blur_8p.use_relative = False
    # Size
    blur_8p.inputs[1].default_value = 1.0

    # node Blur 16p
    blur_16p = exponential_glare.nodes.new("CompositorNodeBlur")
    blur_16p.label = "Blur 16p"
    blur_16p.name = "Blur 16p"
    blur_16p.use_custom_color = True
    blur_16p.color = Color.DARK_PURPLE
    blur_16p.hide = True
    blur_16p.filter_type = "FAST_GAUSS"
    blur_16p.size_x = 16
    blur_16p.size_y = 16
    blur_16p.use_extended_bounds = False
    blur_16p.use_relative = False
    # Size
    blur_16p.inputs[1].default_value = 1.0

    # node Blur 32p
    blur_32p = exponential_glare.nodes.new("CompositorNodeBlur")
    blur_32p.label = "Blur 32p"
    blur_32p.name = "Blur 32p"
    blur_32p.use_custom_color = True
    blur_32p.color = Color.DARK_PURPLE
    blur_32p.hide = True
    blur_32p.filter_type = "FAST_GAUSS"
    blur_32p.size_x = 32
    blur_32p.size_y = 32
    blur_32p.use_extended_bounds = False
    blur_32p.use_relative = False
    # Size
    blur_32p.inputs[1].default_value = 1.0

    # node Blur 64p
    blur_64p = exponential_glare.nodes.new("CompositorNodeBlur")
    blur_64p.label = "Blur 64p"
    blur_64p.name = "Blur 64p"
    blur_64p.use_custom_color = True
    blur_64p.color = Color.DARK_PURPLE
    blur_64p.hide = True
    blur_64p.filter_type = "FAST_GAUSS"
    blur_64p.size_x = 64
    blur_64p.size_y = 64
    blur_64p.use_extended_bounds = False
    blur_64p.use_relative = False
    # Size
    blur_64p.inputs[1].default_value = 1.0

    # node Blur 128p
    blur_128p = exponential_glare.nodes.new("CompositorNodeBlur")
    blur_128p.label = "Blur 128p"
    blur_128p.name = "Blur 128p"
    blur_128p.use_custom_color = True
    blur_128p.color = Color.DARK_PURPLE
    blur_128p.hide = True
    blur_128p.filter_type = "FAST_GAUSS"
    blur_128p.size_x = 128
    blur_128p.size_y = 128
    blur_128p.use_extended_bounds = False
    blur_128p.use_relative = False
    # Size
    blur_128p.inputs[1].default_value = 1.0

    # node Blur 256p
    blur_256p = exponential_glare.nodes.new("CompositorNodeBlur")
    blur_256p.label = "Blur 256p"
    blur_256p.name = "Blur 256p"
    blur_256p.use_custom_color = True
    blur_256p.color = Color.DARK_PURPLE
    blur_256p.hide = True
    blur_256p.filter_type = "FAST_GAUSS"
    blur_256p.size_x = 256
    blur_256p.size_y = 256
    blur_256p.use_extended_bounds = False
    blur_256p.use_relative = False
    # Size
    blur_256p.inputs[1].default_value = 1.0

    # node Blur 512p
    blur_512p = exponential_glare.nodes.new("CompositorNodeBlur")
    blur_512p.label = "Blur 512p"
    blur_512p.name = "Blur 512p"
    blur_512p.use_custom_color = True
    blur_512p.color = Color.DARK_PURPLE
    blur_512p.hide = True
    blur_512p.filter_type = "FAST_GAUSS"
    blur_512p.size_x = 512
    blur_512p.size_y = 512
    blur_512p.use_extended_bounds = False
    blur_512p.use_relative = False
    # Size
    blur_512p.inputs[1].default_value = 1.0

    # node EG Add 02
    eg_add_02 = exponential_glare.nodes.new("CompositorNodeMixRGB")
    eg_add_02.label = "EG Add 02"
    eg_add_02.name = "EG Add 02"
    eg_add_02.use_custom_color = True
    eg_add_02.color = Color.BROWN
    eg_add_02.hide = True
    eg_add_02.blend_type = "ADD"
    eg_add_02.use_alpha = False
    eg_add_02.use_clamp = False
    # Fac
    eg_add_02.inputs[0].default_value = 0.10000000149011612

    # node EG Add 03
    eg_add_03 = exponential_glare.nodes.new("CompositorNodeMixRGB")
    eg_add_03.label = "EG Add 03"
    eg_add_03.name = "EG Add 03"
    eg_add_03.use_custom_color = True
    eg_add_03.color = Color.BROWN
    eg_add_03.hide = True
    eg_add_03.blend_type = "ADD"
    eg_add_03.use_alpha = False
    eg_add_03.use_clamp = False
    # Fac
    eg_add_03.inputs[0].default_value = 0.05000000074505806

    # node EG Add 04
    eg_add_04 = exponential_glare.nodes.new("CompositorNodeMixRGB")
    eg_add_04.label = "EG Add 04"
    eg_add_04.name = "EG Add 04"
    eg_add_04.use_custom_color = True
    eg_add_04.color = Color.BROWN
    eg_add_04.hide = True
    eg_add_04.blend_type = "ADD"
    eg_add_04.use_alpha = False
    eg_add_04.use_clamp = False
    # Fac
    eg_add_04.inputs[0].default_value = 0.02500000037252903

    # node EG Add 05
    eg_add_05 = exponential_glare.nodes.new("CompositorNodeMixRGB")
    eg_add_05.label = "EG Add 05"
    eg_add_05.name = "EG Add 05"
    eg_add_05.use_custom_color = True
    eg_add_05.color = Color.BROWN
    eg_add_05.hide = True
    eg_add_05.blend_type = "ADD"
    eg_add_05.use_alpha = False
    eg_add_05.use_clamp = False
    # Fac
    eg_add_05.inputs[0].default_value = 0.013000000268220901

    # node EG Add 06
    eg_add_06 = exponential_glare.nodes.new("CompositorNodeMixRGB")
    eg_add_06.label = "EG Add 06"
    eg_add_06.name = "EG Add 06"
    eg_add_06.use_custom_color = True
    eg_add_06.color = Color.BROWN
    eg_add_06.hide = True
    eg_add_06.blend_type = "ADD"
    eg_add_06.use_alpha = False
    eg_add_06.use_clamp = False
    # Fac
    eg_add_06.inputs[0].default_value = 0.006000000052154064

    # node EG Add 07
    eg_add_07 = exponential_glare.nodes.new("CompositorNodeMixRGB")
    eg_add_07.label = "EG Add 07"
    eg_add_07.name = "EG Add 07"
    eg_add_07.use_custom_color = True
    eg_add_07.color = Color.BROWN
    eg_add_07.hide = True
    eg_add_07.blend_type = "ADD"
    eg_add_07.use_alpha = False
    eg_add_07.use_clamp = False
    # Fac
    eg_add_07.inputs[0].default_value = 0.003000000026077032

    # node EG Add 08
    eg_add_08 = exponential_glare.nodes.new("CompositorNodeMixRGB")
    eg_add_08.label = "EG Add 08"
    eg_add_08.name = "EG Add 08"
    eg_add_08.use_custom_color = True
    eg_add_08.color = Color.BROWN
    eg_add_08.hide = True
    eg_add_08.blend_type = "ADD"
    eg_add_08.use_alpha = False
    eg_add_08.use_clamp = False
    # Fac
    eg_add_08.inputs[0].default_value = 0.0020000000949949026

    # node EG Mix
    eg_mix = exponential_glare.nodes.new("CompositorNodeMixRGB")
    eg_mix.label = "EG Mix"
    eg_mix.name = "EG Mix"
    eg_mix.use_custom_color = True
    eg_mix.color = Color.BROWN
    eg_mix.blend_type = "MIX"
    eg_mix.use_alpha = False
    eg_mix.use_clamp = False

    # node EG Reroute 00
    eg_reroute_00 = exponential_glare.nodes.new("NodeReroute")
    eg_reroute_00.name = "EG Reroute 00"
    eg_reroute_00.socket_idname = "NodeSocketColor"
    # node EG Reroute 01
    eg_reroute_01 = exponential_glare.nodes.new("NodeReroute")
    eg_reroute_01.name = "EG Reroute 01"
    eg_reroute_01.socket_idname = "NodeSocketFloatFactor"
    # node EG Reroute 02
    eg_reroute_02 = exponential_glare.nodes.new("NodeReroute")
    eg_reroute_02.name = "EG Reroute 02"
    eg_reroute_02.socket_idname = "NodeSocketFloatFactor"
    # node Group Output
    group_output = exponential_glare.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.use_custom_color = True
    group_output.color = Color.DARK_GRAY
    group_output.is_active_output = True
    group_output.inputs[1].hide = True

    # Set locations
    group_input.location = (-213.36361694335938, 97.65576934814453)
    blur_2p.location = (78.29545593261719, 250.23533630371094)
    eg_add_00.location = (362.1622314453125, 261.17877197265625)
    eg_add_01.location = (362.1622314453125, 216.17877197265625)
    blur_4p.location = (78.29545593261719, 205.23533630371094)
    blur_8p.location = (78.29545593261719, 160.23533630371094)
    blur_16p.location = (78.29545593261719, 115.23533630371094)
    blur_32p.location = (78.29545593261719, 70.23533630371094)
    blur_64p.location = (78.29545593261719, 25.235336303710938)
    blur_128p.location = (78.29545593261719, -19.764663696289062)
    blur_256p.location = (78.29545593261719, -64.76466369628906)
    blur_512p.location = (78.29545593261719, -109.76466369628906)
    eg_add_02.location = (362.1622314453125, 171.17877197265625)
    eg_add_03.location = (362.1622314453125, 126.17877197265625)
    eg_add_04.location = (362.1622314453125, 81.17877197265625)
    eg_add_05.location = (362.1622314453125, 36.17877197265625)
    eg_add_06.location = (362.1622314453125, -8.82122802734375)
    eg_add_07.location = (362.1622314453125, -53.82122802734375)
    eg_add_08.location = (362.1622314453125, -98.82122802734375)
    eg_mix.location = (556.7327270507812, -33.36434555053711)
    eg_reroute_00.location = (80.0, -160.0)
    eg_reroute_01.location = (80.0, -200.0)
    eg_reroute_02.location = (420.0, -200.0)
    group_output.location = (734.046875, -33.36434555053711)

    # Set dimensions
    group_input.width, group_input.height = 140.0, 100.0
    blur_2p.width, blur_2p.height = 140.0, 100.0
    eg_add_00.width, eg_add_00.height = 140.0, 100.0
    eg_add_01.width, eg_add_01.height = 140.0, 100.0
    blur_4p.width, blur_4p.height = 140.0, 100.0
    blur_8p.width, blur_8p.height = 140.0, 100.0
    blur_16p.width, blur_16p.height = 140.0, 100.0
    blur_32p.width, blur_32p.height = 140.0, 100.0
    blur_64p.width, blur_64p.height = 140.0, 100.0
    blur_128p.width, blur_128p.height = 140.0, 100.0
    blur_256p.width, blur_256p.height = 140.0, 100.0
    blur_512p.width, blur_512p.height = 140.0, 100.0
    eg_add_02.width, eg_add_02.height = 140.0, 100.0
    eg_add_03.width, eg_add_03.height = 140.0, 100.0
    eg_add_04.width, eg_add_04.height = 140.0, 100.0
    eg_add_05.width, eg_add_05.height = 140.0, 100.0
    eg_add_06.width, eg_add_06.height = 140.0, 100.0
    eg_add_07.width, eg_add_07.height = 140.0, 100.0
    eg_add_08.width, eg_add_08.height = 140.0, 100.0
    eg_mix.width, eg_mix.height = 140.0, 100.0
    eg_reroute_00.width, eg_reroute_00.height = 16.0, 100.0
    eg_reroute_01.width, eg_reroute_01.height = 16.0, 100.0
    eg_reroute_02.width, eg_reroute_02.height = 16.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0

    # initialize exponential_glare links
    # group_input.Image -> blur_2p.Image
    exponential_glare.links.new(group_input.outputs[0], blur_2p.inputs[0])

    # blur_2p.Image -> eg_add_00.Image
    exponential_glare.links.new(blur_2p.outputs[0], eg_add_00.inputs[2])

    # eg_add_00.Image -> eg_add_01.Image
    exponential_glare.links.new(eg_add_00.outputs[0], eg_add_01.inputs[1])

    # group_input.Image -> blur_4p.Image
    exponential_glare.links.new(group_input.outputs[0], blur_4p.inputs[0])

    # group_input.Image -> blur_8p.Image
    exponential_glare.links.new(group_input.outputs[0], blur_8p.inputs[0])

    # group_input.Image -> blur_16p.Image
    exponential_glare.links.new(group_input.outputs[0], blur_16p.inputs[0])

    # group_input.Image -> blur_32p.Image
    exponential_glare.links.new(group_input.outputs[0], blur_32p.inputs[0])

    # group_input.Image -> blur_64p.Image
    exponential_glare.links.new(group_input.outputs[0], blur_64p.inputs[0])

    # group_input.Image -> blur_128p.Image
    exponential_glare.links.new(group_input.outputs[0], blur_128p.inputs[0])

    # group_input.Image -> blur_256p.Image
    exponential_glare.links.new(group_input.outputs[0], blur_256p.inputs[0])

    # group_input.Image -> blur_512p.Image
    exponential_glare.links.new(group_input.outputs[0], blur_512p.inputs[0])

    # blur_4p.Image -> eg_add_01.Image
    exponential_glare.links.new(blur_4p.outputs[0], eg_add_01.inputs[2])

    # eg_add_01.Image -> eg_add_02.Image
    exponential_glare.links.new(eg_add_01.outputs[0], eg_add_02.inputs[1])

    # blur_8p.Image -> eg_add_02.Image
    exponential_glare.links.new(blur_8p.outputs[0], eg_add_02.inputs[2])

    # blur_16p.Image -> eg_add_03.Image
    exponential_glare.links.new(blur_16p.outputs[0], eg_add_03.inputs[2])

    # eg_add_02.Image -> eg_add_03.Image
    exponential_glare.links.new(eg_add_02.outputs[0], eg_add_03.inputs[1])

    # eg_add_03.Image -> eg_add_04.Image
    exponential_glare.links.new(eg_add_03.outputs[0], eg_add_04.inputs[1])

    # eg_add_04.Image -> eg_add_05.Image
    exponential_glare.links.new(eg_add_04.outputs[0], eg_add_05.inputs[1])

    # eg_add_05.Image -> eg_add_06.Image
    exponential_glare.links.new(eg_add_05.outputs[0], eg_add_06.inputs[1])

    # eg_add_06.Image -> eg_add_07.Image
    exponential_glare.links.new(eg_add_06.outputs[0], eg_add_07.inputs[1])

    # eg_add_07.Image -> eg_add_08.Image
    exponential_glare.links.new(eg_add_07.outputs[0], eg_add_08.inputs[1])

    # eg_add_08.Image -> eg_mix.Image
    exponential_glare.links.new(eg_add_08.outputs[0], eg_mix.inputs[2])

    # blur_32p.Image -> eg_add_04.Image
    exponential_glare.links.new(blur_32p.outputs[0], eg_add_04.inputs[2])

    # blur_64p.Image -> eg_add_05.Image
    exponential_glare.links.new(blur_64p.outputs[0], eg_add_05.inputs[2])

    # blur_128p.Image -> eg_add_06.Image
    exponential_glare.links.new(blur_128p.outputs[0], eg_add_06.inputs[2])

    # blur_256p.Image -> eg_add_07.Image
    exponential_glare.links.new(blur_256p.outputs[0], eg_add_07.inputs[2])

    # blur_512p.Image -> eg_add_08.Image
    exponential_glare.links.new(blur_512p.outputs[0], eg_add_08.inputs[2])

    # eg_reroute_00.Output -> eg_mix.Image
    exponential_glare.links.new(eg_reroute_00.outputs[0], eg_mix.inputs[1])

    # group_input.Image -> eg_reroute_00.Input
    exponential_glare.links.new(group_input.outputs[0], eg_reroute_00.inputs[0])

    # eg_reroute_02.Output -> eg_mix.Fac
    exponential_glare.links.new(eg_reroute_02.outputs[0], eg_mix.inputs[0])

    # group_input.Strength -> eg_reroute_01.Input
    exponential_glare.links.new(group_input.outputs[1], eg_reroute_01.inputs[0])

    # eg_reroute_01.Output -> eg_reroute_02.Input
    exponential_glare.links.new(eg_reroute_01.outputs[0], eg_reroute_02.inputs[0])

    # eg_mix.Image -> group_output.Image
    exponential_glare.links.new(eg_mix.outputs[0], group_output.inputs[0])

    return exponential_glare
