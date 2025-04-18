# Blender Modules
import bpy
from bpy.types import NodeTree

# Helper Modules
from helpers import Color


# initialize Glow node group
def glow_node_group(context, operator, group_name) -> NodeTree:
    # enable use nodes
    bpy.context.scene.use_nodes = True

    glow = bpy.data.node_groups.new(group_name, "CompositorNodeTree")

    glow.color_tag = "FILTER"
    glow.description = ""
    glow.default_group_node_width = 197

    # glow interface
    # Socket Image
    image_socket = glow.interface.new_socket(
        name="Image", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    image_socket.default_value = (
        0.800000011920929,
        0.800000011920929,
        0.800000011920929,
        1.0,
    )
    image_socket.attribute_domain = "POINT"
    image_socket.description = "Standard color output"

    # Socket Image
    image_socket_1 = glow.interface.new_socket(
        name="Image", in_out="INPUT", socket_type="NodeSocketColor"
    )
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = "POINT"
    image_socket_1.description = "Standard color input"

    # Socket Quality
    quality_socket = glow.interface.new_socket(
        name="Quality", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    quality_socket.default_value = 0.0
    quality_socket.min_value = 0.0
    quality_socket.max_value = 1.0
    quality_socket.subtype = "FACTOR"
    quality_socket.attribute_domain = "POINT"
    quality_socket.description = "If not set to something other the High, then the glare effect will only be applied to a low resolution copy of the image. This can be helpful to save render times while only doing preview renders"

    # Socket Global Fac
    global_fac_socket = glow.interface.new_socket(
        name="Global Fac", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    global_fac_socket.default_value = 0.0
    global_fac_socket.min_value = 0.0
    global_fac_socket.max_value = 1.0
    global_fac_socket.subtype = "FACTOR"
    global_fac_socket.attribute_domain = "POINT"
    global_fac_socket.description = (
        "Controls the amount of mixing between the given image and the glow effect"
    )

    # Socket Streaks Fac
    streaks_fac_socket = glow.interface.new_socket(
        name="Streaks Fac", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    streaks_fac_socket.default_value = 0.0
    streaks_fac_socket.min_value = 0.0
    streaks_fac_socket.max_value = 1.0
    streaks_fac_socket.subtype = "FACTOR"
    streaks_fac_socket.attribute_domain = "POINT"
    streaks_fac_socket.description = (
        "Controls the amount of mixing between the given image and the streak effect"
    )

    # Panel Bloom
    bloom_panel = glow.interface.new_panel("Bloom")
    bloom_panel.description = "Simulates the glow around bright objects caused by light scattering in eyes and cameras"
    # Socket BPrevis
    bprevis_socket = glow.interface.new_socket(
        name="BPrevis",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=bloom_panel,
    )
    bprevis_socket.default_value = (
        0.800000011920929,
        0.800000011920929,
        0.800000011920929,
        1.0,
    )
    bprevis_socket.attribute_domain = "POINT"
    bprevis_socket.description = "A preview output for the bloom node"

    # Socket Threshold
    threshold_socket = glow.interface.new_socket(
        name="Threshold",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=bloom_panel,
    )
    threshold_socket.default_value = 1.0
    threshold_socket.min_value = 0.0
    threshold_socket.max_value = 1000.0
    threshold_socket.subtype = "NONE"
    threshold_socket.attribute_domain = "POINT"
    threshold_socket.description = (
        "Pixels brighter than this value will be affected by the glare filter"
    )

    # Socket Size
    size_socket = glow.interface.new_socket(
        name="Size", in_out="INPUT", socket_type="NodeSocketFloat", parent=bloom_panel
    )
    size_socket.default_value = 9.0
    size_socket.min_value = 1.0
    size_socket.max_value = 9.0
    size_socket.subtype = "NONE"
    size_socket.attribute_domain = "POINT"
    size_socket.description = "Scale of the glow relative to the size of the image. 9 means the glow can cover the entire image, 8 means it can only cover half the image, 7 means it can only cover quarter of the image, and so on"

    # Socket Bloom
    bloom_socket = glow.interface.new_socket(
        name="Bloom", in_out="INPUT", socket_type="NodeSocketColor", parent=bloom_panel
    )
    bloom_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    bloom_socket.attribute_domain = "POINT"
    bloom_socket.description = "Input for bloom"

    # Panel Streaks
    streaks_panel = glow.interface.new_panel("Streaks")
    streaks_panel.description = "Creates bright streaks used to simulate lens flares"
    # Socket SPrevis
    sprevis_socket = glow.interface.new_socket(
        name="SPrevis",
        in_out="OUTPUT",
        socket_type="NodeSocketColor",
        parent=streaks_panel,
    )
    sprevis_socket.default_value = (
        0.800000011920929,
        0.800000011920929,
        0.800000011920929,
        1.0,
    )
    sprevis_socket.attribute_domain = "POINT"
    sprevis_socket.description = "A preview output for the streaks node"

    # Socket Iterations
    iterations_socket = glow.interface.new_socket(
        name="Iterations",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streaks_panel,
    )
    iterations_socket.default_value = 3.0
    iterations_socket.min_value = 2.0
    iterations_socket.max_value = 5.0
    iterations_socket.subtype = "NONE"
    iterations_socket.attribute_domain = "POINT"
    iterations_socket.description = "The number of times to run through the filter algorithm. Higher values will give more accurate results but will take longer to compute. Note that, this is not available for Fog Glow as it does not use an iterative-based algorithm"

    # Socket Color Modulation
    color_modulation_socket = glow.interface.new_socket(
        name="Color Modulation",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streaks_panel,
    )
    color_modulation_socket.default_value = 0.25
    color_modulation_socket.min_value = 0.0
    color_modulation_socket.max_value = 1.0
    color_modulation_socket.subtype = "FACTOR"
    color_modulation_socket.attribute_domain = "POINT"
    color_modulation_socket.description = (
        "Used for Streaks and Ghosts to create a special dispersion effect."
    )

    # Socket Threshold
    threshold_socket_1 = glow.interface.new_socket(
        name="Threshold",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streaks_panel,
    )
    threshold_socket_1.default_value = 1.0
    threshold_socket_1.min_value = 0.0
    threshold_socket_1.max_value = 1000.0
    threshold_socket_1.subtype = "NONE"
    threshold_socket_1.attribute_domain = "POINT"
    threshold_socket_1.description = (
        "Pixels brighter than this value will be affected by the glare filter"
    )

    # Socket Streaks
    streaks_socket = glow.interface.new_socket(
        name="Streaks",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streaks_panel,
    )
    streaks_socket.default_value = 16.0
    streaks_socket.min_value = 1.0
    streaks_socket.max_value = 16.0
    streaks_socket.subtype = "NONE"
    streaks_socket.attribute_domain = "POINT"
    streaks_socket.description = "Total number of streaks"

    # Socket Angle Offset
    angle_offset_socket = glow.interface.new_socket(
        name="Angle Offset",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streaks_panel,
    )
    angle_offset_socket.default_value = 0.0
    angle_offset_socket.min_value = 0.0
    angle_offset_socket.max_value = 180.0
    angle_offset_socket.subtype = "ANGLE"
    angle_offset_socket.attribute_domain = "POINT"
    angle_offset_socket.description = (
        "The rotation offset factor of the streaks. Max is 180°"
    )

    # Socket Fade
    fade_socket = glow.interface.new_socket(
        name="Fade", in_out="INPUT", socket_type="NodeSocketFloat", parent=streaks_panel
    )
    fade_socket.default_value = 0.9
    fade_socket.min_value = 0.75
    fade_socket.max_value = 1.0
    fade_socket.subtype = "FACTOR"
    fade_socket.attribute_domain = "POINT"
    fade_socket.description = "Fade out factor for the streaks"

    # Socket Streaks
    streaks_socket_1 = glow.interface.new_socket(
        name="Streaks",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=streaks_panel,
    )
    streaks_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    streaks_socket_1.attribute_domain = "POINT"
    streaks_socket_1.description = "Input for streaks"

    # initialize glow nodes
    # node GGI Opt
    ggi_opt = glow.nodes.new("NodeGroupOutput")
    ggi_opt.label = "GGI Opt"
    ggi_opt.name = "GGI Opt"
    ggi_opt.use_custom_color = True
    ggi_opt.color = Color.DARK_GRAY
    ggi_opt.is_active_output = True
    ggi_opt.inputs[3].hide = True

    # node GGI Streaks
    ggi_streaks = glow.nodes.new("NodeGroupInput")
    ggi_streaks.label = "GGI Streaks"
    ggi_streaks.name = "GGI Streaks"
    ggi_streaks.use_custom_color = True
    ggi_streaks.color = Color.DARK_GRAY
    ggi_streaks.outputs[0].hide = True
    ggi_streaks.outputs[1].hide = True
    ggi_streaks.outputs[2].hide = True
    ggi_streaks.outputs[3].hide = True
    ggi_streaks.outputs[4].hide = True
    ggi_streaks.outputs[5].hide = True
    ggi_streaks.outputs[6].hide = True
    ggi_streaks.outputs[7].hide = True
    ggi_streaks.outputs[8].hide = True
    ggi_streaks.outputs[9].hide = True
    ggi_streaks.outputs[10].hide = True
    ggi_streaks.outputs[11].hide = True
    ggi_streaks.outputs[12].hide = True
    ggi_streaks.outputs[14].hide = True

    # node G Add 00
    g_add_00 = glow.nodes.new("CompositorNodeMixRGB")
    g_add_00.label = "G Add 00"
    g_add_00.name = "G Add 00"
    g_add_00.use_custom_color = True
    g_add_00.color = Color.BROWN
    g_add_00.blend_type = "ADD"
    g_add_00.use_alpha = False
    g_add_00.use_clamp = False

    # node G Add 01
    g_add_01 = glow.nodes.new("CompositorNodeMixRGB")
    g_add_01.label = "G Add 01"
    g_add_01.name = "G Add 01"
    g_add_01.use_custom_color = True
    g_add_01.color = Color.BROWN
    g_add_01.blend_type = "ADD"
    g_add_01.use_alpha = False
    g_add_01.use_clamp = False

    # node G Bloom High
    g_bloom_high = glow.nodes.new("CompositorNodeGlare")
    g_bloom_high.label = "G Bloom High"
    g_bloom_high.name = "G Bloom High"
    g_bloom_high.use_custom_color = True
    g_bloom_high.color = Color.DARK_PURPLE
    g_bloom_high.glare_type = "BLOOM"
    g_bloom_high.mix = 1.0
    g_bloom_high.quality = "HIGH"
    g_bloom_high.size = 9
    g_bloom_high.threshold = 1.0

    # node G Bloom Low
    g_bloom_low = glow.nodes.new("CompositorNodeGlare")
    g_bloom_low.label = "G Bloom Low"
    g_bloom_low.name = "G Bloom Low"
    g_bloom_low.use_custom_color = True
    g_bloom_low.color = Color.DARK_PURPLE
    g_bloom_low.glare_type = "BLOOM"
    g_bloom_low.mix = 1.0
    g_bloom_low.quality = "LOW"
    g_bloom_low.size = 9
    g_bloom_low.threshold = 1.0

    # node G Streaks High
    g_streaks_high = glow.nodes.new("CompositorNodeGlare")
    g_streaks_high.label = "G Streaks High"
    g_streaks_high.name = "G Streaks High"
    g_streaks_high.use_custom_color = True
    g_streaks_high.color = Color.DARK_PURPLE
    g_streaks_high.angle_offset = 0.0
    g_streaks_high.color_modulation = 0.25
    g_streaks_high.fade = 0.9
    g_streaks_high.glare_type = "STREAKS"
    g_streaks_high.iterations = 3
    g_streaks_high.mix = 1.0
    g_streaks_high.quality = "HIGH"
    g_streaks_high.streaks = 16
    g_streaks_high.threshold = 1.0

    # node G Streaks Low
    g_streaks_low = glow.nodes.new("CompositorNodeGlare")
    g_streaks_low.label = "G Streaks Low"
    g_streaks_low.name = "G Streaks Low"
    g_streaks_low.use_custom_color = True
    g_streaks_low.color = Color.DARK_PURPLE
    g_streaks_low.angle_offset = 0.0
    g_streaks_low.color_modulation = 0.25
    g_streaks_low.fade = 0.9
    g_streaks_low.glare_type = "STREAKS"
    g_streaks_low.iterations = 3
    g_streaks_low.mix = 1.0
    g_streaks_low.quality = "LOW"
    g_streaks_low.streaks = 16
    g_streaks_low.threshold = 1.0

    # node G Switch 00
    g_switch_00 = glow.nodes.new("CompositorNodeSwitch")
    g_switch_00.label = "G Switch 00"
    g_switch_00.name = "G Switch 00"
    g_switch_00.use_custom_color = True
    g_switch_00.color = Color.LIGHT_GRAY
    g_switch_00.check = False

    # node G Switch 01
    g_switch_01 = glow.nodes.new("CompositorNodeSwitch")
    g_switch_01.label = "G Switch 01"
    g_switch_01.name = "G Switch 01"
    g_switch_01.use_custom_color = True
    g_switch_01.color = Color.LIGHT_GRAY
    g_switch_01.check = False

    # node G Bloom High && Low
    g_bloom_high____low = glow.nodes.new("NodeFrame")
    g_bloom_high____low.label = "G Bloom High && Low"
    g_bloom_high____low.name = "G Bloom High && Low"
    g_bloom_high____low.use_custom_color = True
    g_bloom_high____low.color = (
        0.27887165546417236,
        0.4313916563987732,
        0.31700167059898376,
    )
    g_bloom_high____low.label_size = 32
    g_bloom_high____low.shrink = True

    # node G Streaks High && Low
    g_streaks_high____low = glow.nodes.new("NodeFrame")
    g_streaks_high____low.label = "G Streaks High && Low"
    g_streaks_high____low.name = "G Streaks High && Low"
    g_streaks_high____low.use_custom_color = True
    g_streaks_high____low.color = (
        0.2788630723953247,
        0.43140727281570435,
        0.31698769330978394,
    )
    g_streaks_high____low.label_size = 32
    g_streaks_high____low.shrink = True

    # node GGI Image
    ggi_image = glow.nodes.new("NodeGroupInput")
    ggi_image.label = "GGI Image"
    ggi_image.name = "GGI Image"
    ggi_image.use_custom_color = True
    ggi_image.color = Color.DARK_GRAY
    ggi_image.outputs[1].hide = True
    ggi_image.outputs[2].hide = True
    ggi_image.outputs[3].hide = True
    ggi_image.outputs[4].hide = True
    ggi_image.outputs[5].hide = True
    ggi_image.outputs[6].hide = True
    ggi_image.outputs[7].hide = True
    ggi_image.outputs[8].hide = True
    ggi_image.outputs[9].hide = True
    ggi_image.outputs[10].hide = True
    ggi_image.outputs[11].hide = True
    ggi_image.outputs[12].hide = True
    ggi_image.outputs[13].hide = True
    ggi_image.outputs[14].hide = True

    # node GGI Global Fac
    ggi_global_fac = glow.nodes.new("NodeGroupInput")
    ggi_global_fac.label = "GGI Global Fac"
    ggi_global_fac.name = "GGI Global Fac"
    ggi_global_fac.use_custom_color = True
    ggi_global_fac.color = Color.DARK_GRAY
    ggi_global_fac.outputs[0].hide = True
    ggi_global_fac.outputs[1].hide = True
    ggi_global_fac.outputs[3].hide = True
    ggi_global_fac.outputs[4].hide = True
    ggi_global_fac.outputs[5].hide = True
    ggi_global_fac.outputs[6].hide = True
    ggi_global_fac.outputs[7].hide = True
    ggi_global_fac.outputs[8].hide = True
    ggi_global_fac.outputs[9].hide = True
    ggi_global_fac.outputs[10].hide = True
    ggi_global_fac.outputs[11].hide = True
    ggi_global_fac.outputs[12].hide = True
    ggi_global_fac.outputs[13].hide = True
    ggi_global_fac.outputs[14].hide = True

    # node GGI Streaks Fac
    ggi_streaks_fac = glow.nodes.new("NodeGroupInput")
    ggi_streaks_fac.label = "GGI Streaks Fac"
    ggi_streaks_fac.name = "GGI Streaks Fac"
    ggi_streaks_fac.use_custom_color = True
    ggi_streaks_fac.color = Color.DARK_GRAY
    ggi_streaks_fac.outputs[0].hide = True
    ggi_streaks_fac.outputs[1].hide = True
    ggi_streaks_fac.outputs[2].hide = True
    ggi_streaks_fac.outputs[4].hide = True
    ggi_streaks_fac.outputs[5].hide = True
    ggi_streaks_fac.outputs[6].hide = True
    ggi_streaks_fac.outputs[7].hide = True
    ggi_streaks_fac.outputs[8].hide = True
    ggi_streaks_fac.outputs[9].hide = True
    ggi_streaks_fac.outputs[10].hide = True
    ggi_streaks_fac.outputs[11].hide = True
    ggi_streaks_fac.outputs[12].hide = True
    ggi_streaks_fac.outputs[13].hide = True
    ggi_streaks_fac.outputs[14].hide = True

    # node GGI Bloom
    ggi_bloom = glow.nodes.new("NodeGroupInput")
    ggi_bloom.label = "GGI Bloom"
    ggi_bloom.name = "GGI Bloom"
    ggi_bloom.use_custom_color = True
    ggi_bloom.color = Color.DARK_GRAY
    ggi_bloom.outputs[0].hide = True
    ggi_bloom.outputs[1].hide = True
    ggi_bloom.outputs[2].hide = True
    ggi_bloom.outputs[3].hide = True
    ggi_bloom.outputs[4].hide = True
    ggi_bloom.outputs[5].hide = True
    ggi_bloom.outputs[7].hide = True
    ggi_bloom.outputs[8].hide = True
    ggi_bloom.outputs[9].hide = True
    ggi_bloom.outputs[10].hide = True
    ggi_bloom.outputs[11].hide = True
    ggi_bloom.outputs[12].hide = True
    ggi_bloom.outputs[13].hide = True
    ggi_bloom.outputs[14].hide = True

    # Set parents
    ggi_streaks.parent = g_streaks_high____low
    g_bloom_high.parent = g_bloom_high____low
    g_bloom_low.parent = g_bloom_high____low
    g_streaks_high.parent = g_streaks_high____low
    g_streaks_low.parent = g_streaks_high____low
    g_switch_00.parent = g_streaks_high____low
    g_switch_01.parent = g_bloom_high____low
    ggi_bloom.parent = g_bloom_high____low

    # Set locations
    ggi_opt.location = (260.0, 112.5940933227539)
    ggi_streaks.location = (-397.0, -75.0)
    g_add_00.location = (-120.0, -30.360008239746094)
    g_add_01.location = (80.0, 112.5940933227539)
    g_bloom_high.location = (-197.3275146484375, -53.2032470703125)
    g_bloom_low.location = (-197.3275146484375, 166.7967529296875)
    g_streaks_high.location = (-187.0, -30.0)
    g_streaks_low.location = (-187.0, 290.0)
    g_switch_00.location = (63.0, 125.0)
    g_switch_01.location = (53.0, 122.0)
    g_bloom_high____low.location = (-443.0, 98.0)
    g_streaks_high____low.location = (-453.0, -545.0)
    ggi_image.location = (-120.0, 48.91996765136719)
    ggi_global_fac.location = (-120.0, 128.199951171875)
    ggi_streaks_fac.location = (-120.0, -220.0)
    ggi_bloom.location = (-407.0, -78.0)

    # Set dimensions
    ggi_opt.width, ggi_opt.height = 140.0, 100.0
    ggi_streaks.width, ggi_streaks.height = 140.0, 100.0
    g_add_00.width, g_add_00.height = 140.0, 100.0
    g_add_01.width, g_add_01.height = 140.0, 100.0
    g_bloom_high.width, g_bloom_high.height = 178.03497314453125, 100.0
    g_bloom_low.width, g_bloom_low.height = 178.03497314453125, 100.0
    g_streaks_high.width, g_streaks_high.height = 178.03497314453125, 100.0
    g_streaks_low.width, g_streaks_low.height = 178.03497314453125, 100.0
    g_switch_00.width, g_switch_00.height = 140.0, 100.0
    g_switch_01.width, g_switch_01.height = 140.0, 100.0
    g_bloom_high____low.width, g_bloom_high____low.height = 660.0, 504.0
    g_streaks_high____low.width, g_streaks_high____low.height = 660.0, 704.0
    ggi_image.width, ggi_image.height = 140.0, 100.0
    ggi_global_fac.width, ggi_global_fac.height = 140.0, 100.0
    ggi_streaks_fac.width, ggi_streaks_fac.height = 140.0, 100.0
    ggi_bloom.width, ggi_bloom.height = 140.0, 100.0

    # initialize glow links
    # g_add_00.Image -> g_add_01.Image
    glow.links.new(g_add_00.outputs[0], g_add_01.inputs[2])

    # g_streaks_high.Image -> g_switch_00.On
    glow.links.new(g_streaks_high.outputs[0], g_switch_00.inputs[1])

    # g_streaks_low.Image -> g_switch_00.Off
    glow.links.new(g_streaks_low.outputs[0], g_switch_00.inputs[0])

    # g_bloom_low.Image -> g_switch_01.Off
    glow.links.new(g_bloom_low.outputs[0], g_switch_01.inputs[0])

    # g_bloom_high.Image -> g_switch_01.On
    glow.links.new(g_bloom_high.outputs[0], g_switch_01.inputs[1])

    # ggi_image.Image -> g_add_01.Image
    glow.links.new(ggi_image.outputs[0], g_add_01.inputs[1])

    # ggi_global_fac.Global Fac -> g_add_01.Fac
    glow.links.new(ggi_global_fac.outputs[2], g_add_01.inputs[0])

    # ggi_streaks_fac.Streaks Fac -> g_add_00.Fac
    glow.links.new(ggi_streaks_fac.outputs[3], g_add_00.inputs[0])

    # ggi_bloom.Bloom -> g_bloom_low.Image
    glow.links.new(ggi_bloom.outputs[6], g_bloom_low.inputs[0])

    # ggi_bloom.Bloom -> g_bloom_high.Image
    glow.links.new(ggi_bloom.outputs[6], g_bloom_high.inputs[0])

    # ggi_streaks.Streaks -> g_streaks_low.Image
    glow.links.new(ggi_streaks.outputs[13], g_streaks_low.inputs[0])

    # ggi_streaks.Streaks -> g_streaks_high.Image
    glow.links.new(ggi_streaks.outputs[13], g_streaks_high.inputs[0])

    # g_add_01.Image -> ggi_opt.Image
    glow.links.new(g_add_01.outputs[0], ggi_opt.inputs[0])

    # g_switch_00.Image -> g_add_00.Image
    glow.links.new(g_switch_00.outputs[0], g_add_00.inputs[2])

    # g_switch_01.Image -> g_add_00.Image
    glow.links.new(g_switch_01.outputs[0], g_add_00.inputs[1])

    # g_switch_01.Image -> ggi_opt.BPrevis
    glow.links.new(g_switch_01.outputs[0], ggi_opt.inputs[1])

    # g_switch_00.Image -> ggi_opt.SPrevis
    glow.links.new(g_switch_00.outputs[0], ggi_opt.inputs[2])

    return glow
