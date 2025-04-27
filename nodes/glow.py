# Blender Modules
import bpy
import mathutils
from bpy.types import NodeTree

# Helper Modules
from helpers import Color


# initialize Glow node group
def glow_node_group() -> NodeTree:
    glow = bpy.data.node_groups.new(type="CompositorNodeTree", name="Glow")

    glow.color_tag = "FILTER"
    glow.description = ""
    glow.default_group_node_width = 180

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

    # Socket Bloom Preview
    bloom_preview_socket = glow.interface.new_socket(
        name="Bloom Preview", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    bloom_preview_socket.default_value = (
        0.800000011920929,
        0.800000011920929,
        0.800000011920929,
        1.0,
    )
    bloom_preview_socket.attribute_domain = "POINT"
    bloom_preview_socket.description = "Shows a preview of the bloom effect"

    # Socket Streaks Preview
    streaks_preview_socket = glow.interface.new_socket(
        name="Streaks Preview", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    streaks_preview_socket.default_value = (
        0.800000011920929,
        0.800000011920929,
        0.800000011920929,
        1.0,
    )
    streaks_preview_socket.attribute_domain = "POINT"
    streaks_preview_socket.description = "Shows a preview of the streaks effect"

    # Socket Image
    image_socket_1 = glow.interface.new_socket(
        name="Image", in_out="INPUT", socket_type="NodeSocketColor"
    )
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = "POINT"
    image_socket_1.description = "Standard color input"

    # Socket Quality
    quality_socket = glow.interface.new_socket(
        name="Quality", in_out="INPUT", socket_type="NodeSocketInt"
    )
    quality_socket.default_value = 3
    quality_socket.min_value = 1
    quality_socket.max_value = 3
    quality_socket.subtype = "NONE"
    quality_socket.attribute_domain = "POINT"
    quality_socket.description = "Controls the resolution at which the glare effect is processed. This can be helpful to save render times while only doing preview renders"

    # Socket Glow Amount
    glow_amount_socket = glow.interface.new_socket(
        name="Glow Amount", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    glow_amount_socket.default_value = 1.0
    glow_amount_socket.min_value = 0.0
    glow_amount_socket.max_value = 1.0
    glow_amount_socket.subtype = "FACTOR"
    glow_amount_socket.attribute_domain = "POINT"
    glow_amount_socket.description = (
        "Controls the amount of\xa0mixing between the given image and the glow effect"
    )

    # Socket In-Between
    in_between_socket = glow.interface.new_socket(
        name="In-Between", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    in_between_socket.default_value = 1.0
    in_between_socket.min_value = 0.0
    in_between_socket.max_value = 1.0
    in_between_socket.subtype = "FACTOR"
    in_between_socket.attribute_domain = "POINT"
    in_between_socket.description = (
        "Controls the amount of\xa0mixing between the Bloom and the streak effect"
    )

    # Socket ----Bloom----
    ____bloom_____socket = glow.interface.new_socket(
        name="----Bloom----", in_out="INPUT", socket_type="NodeSocketColor"
    )
    ____bloom_____socket.default_value = (0.0, 0.0, 0.0, 1.0)
    ____bloom_____socket.attribute_domain = "POINT"
    ____bloom_____socket.hide_value = True
    ____bloom_____socket.description = "Core options for the bloom effect"

    # Socket Threshold
    threshold_socket = glow.interface.new_socket(
        name="Threshold", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    threshold_socket.default_value = 1.0
    threshold_socket.min_value = 0.0
    threshold_socket.max_value = 3.4028234663852886e38
    threshold_socket.subtype = "NONE"
    threshold_socket.attribute_domain = "POINT"
    threshold_socket.description = "Defines the minimum luminance required for an area to contribute to the glare effect. Lower values include more areas, while higher values restrict glare to the brightest regions"

    # Socket Strength
    strength_socket = glow.interface.new_socket(
        name="Strength", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    strength_socket.default_value = 8.0
    strength_socket.min_value = 0.0
    strength_socket.max_value = 1.0
    strength_socket.subtype = "FACTOR"
    strength_socket.attribute_domain = "POINT"
    strength_socket.description = "Adjusts the overall intensity of the glare effect. Values greater than 1 boost the luminance of the glare, while values less than 1 blends the glare with the original image"

    # Socket Size
    size_socket = glow.interface.new_socket(
        name="Size", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    size_socket.default_value = 1.0
    size_socket.min_value = 0.0
    size_socket.max_value = 1.0
    size_socket.subtype = "FACTOR"
    size_socket.attribute_domain = "POINT"
    size_socket.description = "Defines the relative spread of the glare across the image. A value of 1 makes the glare cover the full image, while 0.5 restricts it to half, and so on"

    # Socket ----Streaks----
    ____streaks_____socket = glow.interface.new_socket(
        name="----Streaks----", in_out="INPUT", socket_type="NodeSocketColor"
    )
    ____streaks_____socket.default_value = (0.0, 0.0, 0.0, 1.0)
    ____streaks_____socket.attribute_domain = "POINT"
    ____streaks_____socket.hide_value = True
    ____streaks_____socket.description = "Core options for the streaks effect"

    # Socket Threshold
    threshold_socket_1 = glow.interface.new_socket(
        name="Threshold", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    threshold_socket_1.default_value = 1.0
    threshold_socket_1.min_value = 0.0
    threshold_socket_1.max_value = 3.4028234663852886e38
    threshold_socket_1.subtype = "NONE"
    threshold_socket_1.attribute_domain = "POINT"
    threshold_socket_1.description = "Defines the minimum luminance required for an area to contribute to the glare effect. Lower values include more areas, while higher values restrict glare to the brightest regions"

    # Socket Strength
    strength_socket_1 = glow.interface.new_socket(
        name="Strength", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    strength_socket_1.default_value = 1.0
    strength_socket_1.min_value = 0.0
    strength_socket_1.max_value = 1.0
    strength_socket_1.subtype = "FACTOR"
    strength_socket_1.attribute_domain = "POINT"
    strength_socket_1.description = "Adjusts the overall intensity of the glare effect. Values greater than 1 boost the luminance of the glare, while values less than 1 blends the glare with the original image"

    # Socket Streaks
    streaks_socket = glow.interface.new_socket(
        name="Streaks", in_out="INPUT", socket_type="NodeSocketInt"
    )
    streaks_socket.default_value = 16
    streaks_socket.min_value = 1
    streaks_socket.max_value = 16
    streaks_socket.subtype = "NONE"
    streaks_socket.attribute_domain = "POINT"
    streaks_socket.description = "The number of streaks radiating from highlights"

    # Panel Bloom Extras
    bloom_extras_panel = glow.interface.new_panel("Bloom Extras", default_closed=True)
    bloom_extras_panel.description = (
        "Additional controls for fine-tuning the bloom effect."
    )
    # Socket Smoothness
    smoothness_socket = glow.interface.new_socket(
        name="Smoothness",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=bloom_extras_panel,
    )
    smoothness_socket.default_value = 0.10000000149011612
    smoothness_socket.min_value = 0.0
    smoothness_socket.max_value = 1.0
    smoothness_socket.subtype = "FACTOR"
    smoothness_socket.attribute_domain = "POINT"
    smoothness_socket.description = "Controls how gradually pixels transition into the glare effect. Higher values create a smoother highlight extraction"

    # Socket Maximum
    maximum_socket = glow.interface.new_socket(
        name="Maximum",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=bloom_extras_panel,
    )
    maximum_socket.default_value = 0.0
    maximum_socket.min_value = 0.0
    maximum_socket.max_value = 3.4028234663852886e38
    maximum_socket.subtype = "NONE"
    maximum_socket.attribute_domain = "POINT"
    maximum_socket.description = "Place"

    # Socket Saturation
    saturation_socket = glow.interface.new_socket(
        name="Saturation",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=bloom_extras_panel,
    )
    saturation_socket.default_value = 1.0
    saturation_socket.min_value = 0.0
    saturation_socket.max_value = 1.0
    saturation_socket.subtype = "FACTOR"
    saturation_socket.attribute_domain = "POINT"
    saturation_socket.description = "Modifies the color saturation of the glare effect"

    # Socket Tint
    tint_socket = glow.interface.new_socket(
        name="Tint",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=bloom_extras_panel,
    )
    tint_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    tint_socket.attribute_domain = "POINT"
    tint_socket.description = "Tints the glare effect, allowing for colored highlights"

    # Panel Streak Extras
    streak_extras_panel = glow.interface.new_panel("Streak Extras", default_closed=True)
    streak_extras_panel.description = (
        "Additional controls for fine-tuning the streaks effect"
    )
    # Socket Smoothness
    smoothness_socket_1 = glow.interface.new_socket(
        name="Smoothness",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streak_extras_panel,
    )
    smoothness_socket_1.default_value = 0.10000000149011612
    smoothness_socket_1.min_value = 0.0
    smoothness_socket_1.max_value = 1.0
    smoothness_socket_1.subtype = "FACTOR"
    smoothness_socket_1.attribute_domain = "POINT"
    smoothness_socket_1.description = "Controls how gradually pixels transition into the glare effect. Higher values create a smoother highlight extraction"

    # Socket Maximum
    maximum_socket_1 = glow.interface.new_socket(
        name="Maximum",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streak_extras_panel,
    )
    maximum_socket_1.default_value = 0.0
    maximum_socket_1.min_value = 0.0
    maximum_socket_1.max_value = 3.4028234663852886e38
    maximum_socket_1.subtype = "NONE"
    maximum_socket_1.attribute_domain = "POINT"
    maximum_socket_1.description = "Place"

    # Socket Saturation
    saturation_socket_1 = glow.interface.new_socket(
        name="Saturation",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streak_extras_panel,
    )
    saturation_socket_1.default_value = 1.0
    saturation_socket_1.min_value = 0.0
    saturation_socket_1.max_value = 1.0
    saturation_socket_1.subtype = "FACTOR"
    saturation_socket_1.attribute_domain = "POINT"
    saturation_socket_1.description = (
        "Modifies the color saturation of the glare effect"
    )

    # Socket Tint
    tint_socket_1 = glow.interface.new_socket(
        name="Tint",
        in_out="INPUT",
        socket_type="NodeSocketColor",
        parent=streak_extras_panel,
    )
    tint_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    tint_socket_1.attribute_domain = "POINT"
    tint_socket_1.description = (
        "Tints the glare effect, allowing for colored highlights"
    )

    # Socket Streaks Angle
    streaks_angle_socket = glow.interface.new_socket(
        name="Streaks Angle",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streak_extras_panel,
    )
    streaks_angle_socket.default_value = 0.0
    streaks_angle_socket.min_value = -3.4028234663852886e38
    streaks_angle_socket.max_value = 3.4028234663852886e38
    streaks_angle_socket.subtype = "ANGLE"
    streaks_angle_socket.attribute_domain = "POINT"
    streaks_angle_socket.description = (
        "The angle that the first streak makes with the horizontal axis"
    )

    # Socket Iterations
    iterations_socket = glow.interface.new_socket(
        name="Iterations",
        in_out="INPUT",
        socket_type="NodeSocketInt",
        parent=streak_extras_panel,
    )
    iterations_socket.default_value = 3
    iterations_socket.min_value = 2
    iterations_socket.max_value = 5
    iterations_socket.subtype = "NONE"
    iterations_socket.attribute_domain = "POINT"
    iterations_socket.description = "The number of ghosts for Ghost glare or the quality and spread of glare for Streaks and Simple Star glare types"

    # Socket Fade
    fade_socket = glow.interface.new_socket(
        name="Fade",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streak_extras_panel,
    )
    fade_socket.default_value = 0.8999999761581421
    fade_socket.min_value = 0.75
    fade_socket.max_value = 1.0
    fade_socket.subtype = "FACTOR"
    fade_socket.attribute_domain = "POINT"
    fade_socket.description = "The fade-out intensity of the streaks"

    # Socket Color Modulation
    color_modulation_socket = glow.interface.new_socket(
        name="Color Modulation",
        in_out="INPUT",
        socket_type="NodeSocketFloat",
        parent=streak_extras_panel,
    )
    color_modulation_socket.default_value = 0.25
    color_modulation_socket.min_value = 0.0
    color_modulation_socket.max_value = 1.0
    color_modulation_socket.subtype = "FACTOR"
    color_modulation_socket.attribute_domain = "POINT"
    color_modulation_socket.description = (
        "Introduces subtle color variations, simulating chromatic dispersion effects"
    )

    # initialize glow nodes
    # node Group Output
    group_output = glow.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.use_custom_color = True
    group_output.color = (0.23529097437858582, 0.2235269844532013, 0.21568608283996582)
    group_output.is_active_output = True
    group_output.inputs[3].hide = True

    # node Group Input
    group_input = glow.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.use_custom_color = True
    group_input.color = (0.23529097437858582, 0.2235269844532013, 0.21568608283996582)
    group_input.outputs[1].hide = True
    group_input.outputs[2].hide = True
    group_input.outputs[3].hide = True
    group_input.outputs[4].hide = True
    group_input.outputs[8].hide = True
    group_input.outputs[9].hide = True
    group_input.outputs[10].hide = True
    group_input.outputs[11].hide = True
    group_input.outputs[16].hide = True
    group_input.outputs[17].hide = True
    group_input.outputs[18].hide = True
    group_input.outputs[19].hide = True
    group_input.outputs[20].hide = True
    group_input.outputs[21].hide = True
    group_input.outputs[22].hide = True
    group_input.outputs[23].hide = True
    group_input.outputs[24].hide = True

    # node Streaks
    streaks = glow.nodes.new("CompositorNodeGlare")
    streaks.label = "Streaks"
    streaks.name = "Streaks"
    streaks.use_custom_color = True
    streaks.color = (0.4666634798049927, 0.32548609375953674, 0.37254956364631653)
    streaks.angle_offset = 0.0
    streaks.color_modulation = 0.25
    streaks.fade = 0.8999999761581421
    streaks.glare_type = "STREAKS"
    streaks.iterations = 3
    streaks.mix = 0.0
    streaks.quality = "LOW"
    streaks.size = 8
    streaks.streaks = 16
    streaks.threshold = 0.0
    streaks.use_rotate_45 = True

    # node Bloom
    bloom = glow.nodes.new("CompositorNodeGlare")
    bloom.label = "Bloom"
    bloom.name = "Bloom"
    bloom.use_custom_color = True
    bloom.color = (0.4666634798049927, 0.32548609375953674, 0.37254956364631653)
    bloom.angle_offset = 0.0
    bloom.color_modulation = 0.25
    bloom.fade = 0.8999999761581421
    bloom.glare_type = "BLOOM"
    bloom.iterations = 3
    bloom.mix = 7.0
    bloom.quality = "LOW"
    bloom.size = 9
    bloom.streaks = 4
    bloom.threshold = 0.0
    bloom.use_rotate_45 = True

    # node Add Bloom and Streaks
    add_bloom_and_streaks = glow.nodes.new("CompositorNodeMixRGB")
    add_bloom_and_streaks.label = "Add Bloom and Streaks"
    add_bloom_and_streaks.name = "Add Bloom and Streaks"
    add_bloom_and_streaks.use_custom_color = True
    add_bloom_and_streaks.color = (
        0.5254849791526794,
        0.41176897287368774,
        0.21568608283996582,
    )
    add_bloom_and_streaks.blend_type = "ADD"
    add_bloom_and_streaks.use_alpha = False
    add_bloom_and_streaks.use_clamp = False

    # node Add Glow and Image
    add_glow_and_image = glow.nodes.new("CompositorNodeMixRGB")
    add_glow_and_image.label = "Add Glow and Image"
    add_glow_and_image.name = "Add Glow and Image"
    add_glow_and_image.use_custom_color = True
    add_glow_and_image.color = (
        0.5254849791526794,
        0.41176897287368774,
        0.21568608283996582,
    )
    add_glow_and_image.blend_type = "ADD"
    add_glow_and_image.use_alpha = False
    add_glow_and_image.use_clamp = False

    # node Group Input.001
    group_input_001 = glow.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.use_custom_color = True
    group_input_001.color = (
        0.23529097437858582,
        0.2235269844532013,
        0.21568608283996582,
    )
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[3].hide = True
    group_input_001.outputs[4].hide = True
    group_input_001.outputs[5].hide = True
    group_input_001.outputs[6].hide = True
    group_input_001.outputs[7].hide = True
    group_input_001.outputs[8].hide = True
    group_input_001.outputs[9].hide = True
    group_input_001.outputs[10].hide = True
    group_input_001.outputs[11].hide = True
    group_input_001.outputs[12].hide = True
    group_input_001.outputs[13].hide = True
    group_input_001.outputs[14].hide = True
    group_input_001.outputs[15].hide = True
    group_input_001.outputs[16].hide = True
    group_input_001.outputs[17].hide = True
    group_input_001.outputs[18].hide = True
    group_input_001.outputs[19].hide = True
    group_input_001.outputs[20].hide = True
    group_input_001.outputs[21].hide = True
    group_input_001.outputs[22].hide = True
    group_input_001.outputs[23].hide = True
    group_input_001.outputs[24].hide = True

    # node Group Input.002
    group_input_002 = glow.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.use_custom_color = True
    group_input_002.color = (
        0.23529097437858582,
        0.2235269844532013,
        0.21568608283996582,
    )
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[3].hide = True
    group_input_002.outputs[4].hide = True
    group_input_002.outputs[5].hide = True
    group_input_002.outputs[6].hide = True
    group_input_002.outputs[7].hide = True
    group_input_002.outputs[8].hide = True
    group_input_002.outputs[12].hide = True
    group_input_002.outputs[13].hide = True
    group_input_002.outputs[14].hide = True
    group_input_002.outputs[15].hide = True
    group_input_002.outputs[24].hide = True

    # node Group Input.003
    group_input_003 = glow.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.use_custom_color = True
    group_input_003.color = (
        0.23529097437858582,
        0.2235269844532013,
        0.21568608283996582,
    )
    group_input_003.outputs[0].hide = True
    group_input_003.outputs[1].hide = True
    group_input_003.outputs[2].hide = True
    group_input_003.outputs[4].hide = True
    group_input_003.outputs[5].hide = True
    group_input_003.outputs[6].hide = True
    group_input_003.outputs[7].hide = True
    group_input_003.outputs[8].hide = True
    group_input_003.outputs[9].hide = True
    group_input_003.outputs[10].hide = True
    group_input_003.outputs[11].hide = True
    group_input_003.outputs[12].hide = True
    group_input_003.outputs[13].hide = True
    group_input_003.outputs[14].hide = True
    group_input_003.outputs[15].hide = True
    group_input_003.outputs[16].hide = True
    group_input_003.outputs[17].hide = True
    group_input_003.outputs[18].hide = True
    group_input_003.outputs[19].hide = True
    group_input_003.outputs[20].hide = True
    group_input_003.outputs[21].hide = True
    group_input_003.outputs[22].hide = True
    group_input_003.outputs[23].hide = True
    group_input_003.outputs[24].hide = True

    # node Group Input.004
    group_input_004 = glow.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.use_custom_color = True
    group_input_004.color = (
        0.23529097437858582,
        0.2235269844532013,
        0.21568608283996582,
    )
    group_input_004.outputs[0].hide = True
    group_input_004.outputs[1].hide = True
    group_input_004.outputs[3].hide = True
    group_input_004.outputs[4].hide = True
    group_input_004.outputs[5].hide = True
    group_input_004.outputs[6].hide = True
    group_input_004.outputs[7].hide = True
    group_input_004.outputs[8].hide = True
    group_input_004.outputs[9].hide = True
    group_input_004.outputs[10].hide = True
    group_input_004.outputs[11].hide = True
    group_input_004.outputs[12].hide = True
    group_input_004.outputs[13].hide = True
    group_input_004.outputs[14].hide = True
    group_input_004.outputs[15].hide = True
    group_input_004.outputs[16].hide = True
    group_input_004.outputs[17].hide = True
    group_input_004.outputs[18].hide = True
    group_input_004.outputs[19].hide = True
    group_input_004.outputs[20].hide = True
    group_input_004.outputs[21].hide = True
    group_input_004.outputs[22].hide = True
    group_input_004.outputs[23].hide = True
    group_input_004.outputs[24].hide = True

    # node Group Input.005
    group_input_005 = glow.nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.use_custom_color = True
    group_input_005.color = (
        0.23529097437858582,
        0.2235269844532013,
        0.21568608283996582,
    )
    group_input_005.outputs[0].hide = True
    group_input_005.outputs[2].hide = True
    group_input_005.outputs[3].hide = True
    group_input_005.outputs[5].hide = True
    group_input_005.outputs[6].hide = True
    group_input_005.outputs[7].hide = True
    group_input_005.outputs[9].hide = True
    group_input_005.outputs[10].hide = True
    group_input_005.outputs[11].hide = True
    group_input_005.outputs[12].hide = True
    group_input_005.outputs[13].hide = True
    group_input_005.outputs[14].hide = True
    group_input_005.outputs[15].hide = True
    group_input_005.outputs[16].hide = True
    group_input_005.outputs[17].hide = True
    group_input_005.outputs[18].hide = True
    group_input_005.outputs[19].hide = True
    group_input_005.outputs[20].hide = True
    group_input_005.outputs[21].hide = True
    group_input_005.outputs[22].hide = True
    group_input_005.outputs[23].hide = True
    group_input_005.outputs[24].hide = True

    # node File Output
    file_output = glow.nodes.new("CompositorNodeOutputFile")
    file_output.name = "File Output"
    file_output.use_custom_color = True
    file_output.color = (0.5098000168800354, 0.22744795680046082, 0.207844078540802)
    file_output.active_input_index = 0
    file_output.base_path = ""
    file_output.save_as_render = True

    # Set locations
    group_output.location = (450.0, 210.0)
    group_input.location = (-580.0, 210.0)
    streaks.location = (-270.0, -30.0)
    bloom.location = (-270.0, 210.0)
    add_bloom_and_streaks.location = (0.0, 160.0)
    add_glow_and_image.location = (240.0, 210.0)
    group_input_001.location = (240.0, 277.0)
    group_input_002.location = (-580.0, -30.0)
    group_input_003.location = (0.0, 227.0)
    group_input_004.location = (240.0, 30.0)
    group_input_005.location = (-580.0, -339.0)
    file_output.location = (-270.0, -270.0)

    # Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    streaks.width, streaks.height = 180.0, 100.0
    bloom.width, bloom.height = 180.0, 100.0
    add_bloom_and_streaks.width, add_bloom_and_streaks.height = 180.0, 100.0
    add_glow_and_image.width, add_glow_and_image.height = 180.0, 100.0
    group_input_001.width, group_input_001.height = 180.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0
    group_input_003.width, group_input_003.height = 180.0, 100.0
    group_input_004.width, group_input_004.height = 180.0, 100.0
    group_input_005.width, group_input_005.height = 140.0, 100.0
    file_output.width, file_output.height = 180.0, 100.0

    # initialize glow links
    # streaks.Glare -> add_bloom_and_streaks.Image
    glow.links.new(streaks.outputs[1], add_bloom_and_streaks.inputs[2])
    # bloom.Glare -> add_bloom_and_streaks.Image
    glow.links.new(bloom.outputs[1], add_bloom_and_streaks.inputs[1])
    # add_bloom_and_streaks.Image -> add_glow_and_image.Image
    glow.links.new(add_bloom_and_streaks.outputs[0], add_glow_and_image.inputs[2])
    # add_glow_and_image.Image -> group_output.Image
    glow.links.new(add_glow_and_image.outputs[0], group_output.inputs[0])
    # group_input.Image -> bloom.Image
    glow.links.new(group_input.outputs[0], bloom.inputs[0])
    # group_input_001.Image -> add_glow_and_image.Image
    glow.links.new(group_input_001.outputs[0], add_glow_and_image.inputs[1])
    # group_input.Threshold -> bloom.Threshold
    glow.links.new(group_input.outputs[5], bloom.inputs[1])
    # group_input.Smoothness -> bloom.Smoothness
    glow.links.new(group_input.outputs[12], bloom.inputs[2])
    # group_input.Maximum -> bloom.Maximum
    glow.links.new(group_input.outputs[13], bloom.inputs[3])
    # group_input.Strength -> bloom.Strength
    glow.links.new(group_input.outputs[6], bloom.inputs[4])
    # group_input.Saturation -> bloom.Saturation
    glow.links.new(group_input.outputs[14], bloom.inputs[5])
    # group_input.Tint -> bloom.Tint
    glow.links.new(group_input.outputs[15], bloom.inputs[6])
    # group_input.Size -> bloom.Size
    glow.links.new(group_input.outputs[7], bloom.inputs[7])
    # group_input_002.Threshold -> streaks.Threshold
    glow.links.new(group_input_002.outputs[9], streaks.inputs[1])
    # group_input_002.Smoothness -> streaks.Smoothness
    glow.links.new(group_input_002.outputs[16], streaks.inputs[2])
    # group_input_002.Maximum -> streaks.Maximum
    glow.links.new(group_input_002.outputs[17], streaks.inputs[3])
    # group_input_002.Strength -> streaks.Strength
    glow.links.new(group_input_002.outputs[10], streaks.inputs[4])
    # group_input_002.Saturation -> streaks.Saturation
    glow.links.new(group_input_002.outputs[18], streaks.inputs[5])
    # group_input_002.Tint -> streaks.Tint
    glow.links.new(group_input_002.outputs[19], streaks.inputs[6])
    # group_input_002.Streaks -> streaks.Streaks
    glow.links.new(group_input_002.outputs[11], streaks.inputs[8])
    # group_input_002.Streaks Angle -> streaks.Streaks Angle
    glow.links.new(group_input_002.outputs[20], streaks.inputs[9])
    # group_input_002.Iterations -> streaks.Iterations
    glow.links.new(group_input_002.outputs[21], streaks.inputs[10])
    # group_input_002.Fade -> streaks.Fade
    glow.links.new(group_input_002.outputs[22], streaks.inputs[11])
    # group_input_002.Color Modulation -> streaks.Color Modulation
    glow.links.new(group_input_002.outputs[23], streaks.inputs[12])
    # group_input_002.Image -> streaks.Image
    glow.links.new(group_input_002.outputs[0], streaks.inputs[0])
    # group_input_003.In-Between -> add_bloom_and_streaks.Fac
    glow.links.new(group_input_003.outputs[3], add_bloom_and_streaks.inputs[0])
    # group_input_004.Glow Amount -> add_glow_and_image.Fac
    glow.links.new(group_input_004.outputs[2], add_glow_and_image.inputs[0])
    # streaks.Glare -> group_output.Streaks Preview
    glow.links.new(streaks.outputs[1], group_output.inputs[2])
    # bloom.Glare -> group_output.Bloom Preview
    glow.links.new(bloom.outputs[1], group_output.inputs[1])
    # group_input_005.----Bloom---- -> file_output.Image
    glow.links.new(group_input_005.outputs[4], file_output.inputs[1])
    # group_input_005.----Streaks---- -> file_output.Image
    glow.links.new(group_input_005.outputs[8], file_output.inputs[2])
    # group_input_005.Quality -> file_output.Image
    glow.links.new(group_input_005.outputs[1], file_output.inputs[0])
    return glow
