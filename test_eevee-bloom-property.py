import bpy
from typing import Tuple
from bpy.props import BoolProperty

def toggle_bloom_mute(self, context):
    """
    Callback function to mute or unmute the OE_Bloom node group in the Compositor node tree.

    Args:
        self: The current context owner (usually the scene).
        context: The Blender context.
    """
    scene = context.scene
    node_tree = bpy.context.scene.node_tree  # Access the active Compositor node tree

    if node_tree:  # Ensure the node tree exists
        for node in node_tree.nodes:
            if node.type == 'GROUP' and node.name == OE_Bloom_Names.OE_Bloom:  # Check for the specific node group
                node.mute = scene.bloom_mute_unmute_bool  # Set the mute property
                self.report({'INFO'}, f"Node group 'OE_Bloom' is now {'muted' if node.mute else 'unmuted'}.")
                return
        print("OE_Bloom node group not found in the Compositor node tree.")
    else:
        print("Compositor node tree is not active.")

# what I did is that I downloaded the bpy Building Blocks from Victor Stepanov's github repository.
# (https://github.com/CGArtPython/bpy-building-blocks)

# and then I modified the code to fit my needs based on this tutorial.
# (https://youtu.be/knc1CGBhJeU?list=TLPQMTcwOTIwMjRqvGTVRWN4sg)

def hexcode_to_rgb(hexcode: str) -> Tuple[float]:
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB

    Supports: "#RRGGBB" or "RRGGBB"

    Note: We are converting into Linear RGB since Blender uses a Linear Color Space internally
    https://docs.blender.org/manual/en/latest/render/color_management.html
    """
    # remove the leading "#" symbol if present
    if hexcode.startswith("#"):
        hexcode = hexcode[1:]

    assert len(hexcode) == 6, f"RRGGBB is the supported hex color format: {hexcode}"

    # extracting the Red color component - RRxxxx
    red = int(hexcode[:2], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_red = red / 255

    # extracting the Green color component - xxGGxx
    green = int(hexcode[2:4], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_green = green / 255

    # extracting the Blue color component - xxxxBB
    blue = int(hexcode[4:6], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_blue = blue / 255

    return tuple([srgb_red, srgb_green, srgb_blue])

# Class to store color values converted from hex codes to RGB
class Color:
    LIGHT_RED = hexcode_to_rgb("#94493E")
    DARK_RED = hexcode_to_rgb("#823A35")
    LIGHT_BLUE = hexcode_to_rgb("#646E66")
    DARK_BLUE = hexcode_to_rgb("#4C6160")
    LIGHT_PURPLE = hexcode_to_rgb("#846167")
    DARK_PURPLE = hexcode_to_rgb("#77535F")
    BROWN = hexcode_to_rgb("#866937")
    DARK_GRAY = hexcode_to_rgb("#3C3937")
    LIGHT_GRAY = hexcode_to_rgb("#59514B")

# Class to store the names of various nodes and sockets used in the bloom node group
class OE_Bloom_Names:
    OE_Bloom = "OE_Bloom"
    Image = "Image"
    Color = "Color"
    Quality = "Quality"
    Knee = "Knee"
    Threshold = "Threshold"
    Radius = "Radius"
    Blur = "Blur"
    Blur_Mix = "Blur Mix"
    Intensity = "Intensity"
    Bloom_Size = "Bloom Size"
    Group_Output = "Group Output"
    Group_Input_00 = "Group Input 00"
    Original_Bloom_High = "Original Bloom High"
    Knee_Bloom_High = "Knee Bloom High"
    Knee_Mix = "Knee Mix"
    Group_Input_01 = "Group Input 01"
    Group_Input_02 = "Group Input 02"
    Group_Input_03 = "Group Input 03"
    Group_Input_04 = "Group Input 04"
    Bloom_High_Low = "Bloom High && Low"
    Knee_Bloom_Low = "Knee Bloom Low"
    KB_Switch = "KB Switch"
    OB_Switch = "OB Switch"
    Original_Bloom_Low = "Original Bloom Low"
    Group_Input_04 = "Group Input 04"
    Reroute_00 = "Reroute_00"
    Reroute_01 = "Reroute_01"
    Clamp = "Clamp"

#initialize OE_Bloom node group
def oe_bloom_node_group(context, operator, group_name):
    scene = bpy.context.scene
    oe_bloom = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    #enable use nodes
    if scene.use_nodes == False:
        scene.use_nodes = True

    oe_bloom.color_tag = 'FILTER'
    oe_bloom.description = "Replication of the legacy eevee bloom option"
    oe_bloom.default_group_node_width = 149

    #oe_bloom interface
    #Socket Image
    image_socket = oe_bloom.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket_1 = oe_bloom.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.description = "Standard color output"

    #Socket Quality
    quality_socket = oe_bloom.interface.new_socket(name = "Quality", in_out='INPUT', socket_type = 'NodeSocketFloat')
    quality_socket.default_value = 0.0
    quality_socket.min_value = 0.0
    quality_socket.max_value = 1.0
    quality_socket.subtype = 'FACTOR'
    quality_socket.attribute_domain = 'POINT'
    quality_socket.description = "If not set to something other the High, then the glare effect will only be applied to a low resolution copy of the image. This can be helpful to save render times while only doing preview renders"

    #Socket Threshold
    threshold_socket = oe_bloom.interface.new_socket(name = "Threshold", in_out='INPUT', socket_type = 'NodeSocketFloat')
    threshold_socket.default_value = 1.0
    threshold_socket.min_value = 0.0
    threshold_socket.max_value = 1000.0
    threshold_socket.subtype = 'NONE'
    threshold_socket.attribute_domain = 'POINT'
    threshold_socket.description = "Filters out pixels under this level of brightness"

    #Socket Knee
    knee_socket = oe_bloom.interface.new_socket(name = "Knee", in_out='INPUT', socket_type = 'NodeSocketFloat')
    knee_socket.default_value = 0.0
    knee_socket.min_value = 0.0
    knee_socket.max_value = 1.0
    knee_socket.subtype = 'FACTOR'
    knee_socket.attribute_domain = 'POINT'
    knee_socket.description = "Makes transition between under/over-threshold gradual"

    #Socket Radius
    radius_socket = oe_bloom.interface.new_socket(name = "Radius", in_out='INPUT', socket_type = 'NodeSocketFloat')
    radius_socket.default_value = 0.0
    radius_socket.min_value = 0.0
    radius_socket.max_value = 2048.0
    radius_socket.subtype = 'NONE'
    radius_socket.attribute_domain = 'POINT'
    radius_socket.description = "Bloom spread distance"

    #Socket Color
    color_socket = oe_bloom.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
    color_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.description = "Color applied to the bloom effect"

    #Socket Intensity
    intensity_socket = oe_bloom.interface.new_socket(name = "Intensity", in_out='INPUT', socket_type = 'NodeSocketFloat')
    intensity_socket.default_value = 1.0
    intensity_socket.min_value = 0.0
    intensity_socket.max_value = 1.0
    intensity_socket.subtype = 'FACTOR'
    intensity_socket.attribute_domain = 'POINT'
    intensity_socket.description = "Blend factor"

    #Panel Clamp
    clamp_panel = oe_bloom.interface.new_panel("Clamp", default_closed=True)
    #Socket Clamp
    clamp_socket = oe_bloom.interface.new_socket(name = "Clamp", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_panel)
    clamp_socket.default_value = 1.0
    clamp_socket.min_value = 0.0
    clamp_socket.max_value = 2.0
    clamp_socket.subtype = 'FACTOR'
    clamp_socket.attribute_domain = 'POINT'
    clamp_socket.description = "Maximum intensity a bloom pixel can have."

    #Socket BM Clamp
    bm_clamp_socket = oe_bloom.interface.new_socket(name = "BM Clamp", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_panel)
    bm_clamp_socket.default_value = 1.0
    bm_clamp_socket.min_value = 0.0
    bm_clamp_socket.max_value = 1.0
    bm_clamp_socket.subtype = 'FACTOR'
    bm_clamp_socket.attribute_domain = 'POINT'
    bm_clamp_socket.description = "Blur Mix Clamp"

    #Socket KM Clamp
    km_clamp_socket = oe_bloom.interface.new_socket(name = "KM Clamp", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_panel)
    km_clamp_socket.default_value = 0.0
    km_clamp_socket.min_value = 0.0
    km_clamp_socket.max_value = 1.0
    km_clamp_socket.subtype = 'FACTOR'
    km_clamp_socket.attribute_domain = 'POINT'
    km_clamp_socket.description = "Knee Mix Clamp"

    #Socket CR Clamp
    cr_clamp_socket = oe_bloom.interface.new_socket(name = "CR Clamp", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_panel)
    cr_clamp_socket.default_value = 0.0
    cr_clamp_socket.min_value = 0.0
    cr_clamp_socket.max_value = 1.0
    cr_clamp_socket.subtype = 'FACTOR'
    cr_clamp_socket.attribute_domain = 'POINT'
    cr_clamp_socket.description = "Color Clamp"


    #Panel Other
    other_panel = oe_bloom.interface.new_panel("Other", default_closed=True)
    #Socket Hue
    hue_socket = oe_bloom.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    hue_socket.default_value = 0.5
    hue_socket.min_value = 0.0
    hue_socket.max_value = 1.0
    hue_socket.subtype = 'FACTOR'
    hue_socket.attribute_domain = 'POINT'
    hue_socket.description = "The hue rotation offset, from 0 (-180°) to 1 (+180°). Note that 0 and 1 have the same result"

    #Socket Saturation
    saturation_socket = oe_bloom.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    saturation_socket.default_value = 1.0
    saturation_socket.min_value = 0.0
    saturation_socket.max_value = 2.0
    saturation_socket.subtype = 'FACTOR'
    saturation_socket.attribute_domain = 'POINT'
    saturation_socket.description = "A value of 0 removes color from the image, making it black-and-white. A value greater than 1.0 increases saturation"

    #Socket Fac
    fac_socket = oe_bloom.interface.new_socket(name = "Fac", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    fac_socket.default_value = 1.0
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = 'FACTOR'
    fac_socket.attribute_domain = 'POINT'
    fac_socket.description = "The amount of influence the node exerts on the image"

    #Socket Blur Mix
    blur_mix_socket = oe_bloom.interface.new_socket(name = "Blur Mix", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    blur_mix_socket.default_value = 1.0
    blur_mix_socket.min_value = 0.0
    blur_mix_socket.max_value = 1.0
    blur_mix_socket.subtype = 'NONE'
    blur_mix_socket.attribute_domain = 'POINT'
    blur_mix_socket.description = "The optional Size input will be multiplied with the X and Y blur radius values. It also accepts a value image, to control the blur radius with a mask. The values should be mapped between (0 to 1) for an optimal effect"

    #Socket Bloom Size
    bloom_size_socket = oe_bloom.interface.new_socket(name = "Bloom Size", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    bloom_size_socket.default_value = 9.0
    bloom_size_socket.min_value = 1.0
    bloom_size_socket.max_value = 9.0
    bloom_size_socket.subtype = 'NONE'
    bloom_size_socket.attribute_domain = 'POINT'
    bloom_size_socket.description = "Scale of the glow relative to the size of the image. 9 means the glow can cover the entire image, 8 means it can only cover half the image, 7 means it can only cover quarter of the image, and so on."

    #initialize oe_bloom nodes
    #node Group Output
    group_output = oe_bloom.nodes.new("NodeGroupOutput")
    group_output.label = "Group Output"
    group_output.name = "Group Output"
    group_output.use_custom_color = True
    group_output.color = (0.23529411852359772, 0.2235294133424759, 0.21568627655506134)
    group_output.is_active_output = True

    #node Group Input 00
    group_input_00 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_00.label = "Group Input 00"
    group_input_00.name = "Group Input 00"
    group_input_00.use_custom_color = True
    group_input_00.color = (0.23529411852359772, 0.2235294133424759, 0.21568627655506134)
    group_input_00.outputs[1].hide = True
    group_input_00.outputs[2].hide = True
    group_input_00.outputs[3].hide = True
    group_input_00.outputs[4].hide = True
    group_input_00.outputs[5].hide = True
    group_input_00.outputs[6].hide = True
    group_input_00.outputs[7].hide = True
    group_input_00.outputs[8].hide = True
    group_input_00.outputs[9].hide = True
    group_input_00.outputs[10].hide = True
    group_input_00.outputs[11].hide = True
    group_input_00.outputs[12].hide = True
    group_input_00.outputs[13].hide = True
    group_input_00.outputs[14].hide = True
    group_input_00.outputs[15].hide = True
    group_input_00.outputs[16].hide = True

    #node Original Bloom High
    original_bloom_high = oe_bloom.nodes.new("CompositorNodeGlare")
    original_bloom_high.label = "Original Bloom High"
    original_bloom_high.name = "Original Bloom High"
    original_bloom_high.use_custom_color = True
    original_bloom_high.color = (0.46666666865348816, 0.32549020648002625, 0.37254902720451355)
    original_bloom_high.angle_offset = 0.0
    original_bloom_high.color_modulation = 0.25
    original_bloom_high.fade = 0.8999999761581421
    original_bloom_high.glare_type = 'BLOOM'
    original_bloom_high.iterations = 3
    original_bloom_high.mix = 1.0
    original_bloom_high.quality = 'HIGH'
    original_bloom_high.size = 1
    original_bloom_high.streaks = 4
    original_bloom_high.threshold = 0.0
    original_bloom_high.use_rotate_45 = True

    #node Color
    color = oe_bloom.nodes.new("CompositorNodeMixRGB")
    color.label = "Color"
    color.name = "Color"
    color.use_custom_color = True
    color.color = (0.5254902243614197, 0.4117647111415863, 0.21568627655506134)
    color.blend_type = 'COLOR'
    color.use_alpha = False
    color.use_clamp = False
    color.inputs[0].hide = True
    #Fac
    color.inputs[0].default_value = 1.0

    #node Blur
    blur = oe_bloom.nodes.new("CompositorNodeBlur")
    blur.label = "Blur"
    blur.name = "Blur"
    blur.use_custom_color = True
    blur.color = (0.46666666865348816, 0.32549020648002625, 0.37254902720451355)
    blur.aspect_correction = 'NONE'
    blur.factor = 0.0
    blur.factor_x = 0.0
    blur.factor_y = 0.0
    blur.filter_type = 'FAST_GAUSS'
    blur.size_x = 0
    blur.size_y = 0
    blur.use_bokeh = False
    blur.use_extended_bounds = False
    blur.use_gamma_correction = False
    blur.use_relative = False
    blur.use_variable_size = False

    #node Blur Mix
    blur_mix = oe_bloom.nodes.new("CompositorNodeMixRGB")
    blur_mix.label = "Blur Mix"
    blur_mix.name = "Blur Mix"
    blur_mix.use_custom_color = True
    blur_mix.color = (0.5254902243614197, 0.4117647111415863, 0.21568627655506134)
    blur_mix.blend_type = 'SCREEN'
    blur_mix.use_alpha = False
    blur_mix.use_clamp = True
    blur_mix.inputs[0].hide = True
    #Fac
    blur_mix.inputs[0].default_value = 1.0

    #node Intensity
    intensity = oe_bloom.nodes.new("CompositorNodeMixRGB")
    intensity.label = "Intensity"
    intensity.name = "Intensity"
    intensity.use_custom_color = True
    intensity.color = (0.5254902243614197, 0.4117647111415863, 0.21568627655506134)
    intensity.blend_type = 'ADD'
    intensity.use_alpha = False
    intensity.use_clamp = False

    #node Knee Bloom High
    knee_bloom_high = oe_bloom.nodes.new("CompositorNodeGlare")
    knee_bloom_high.label = "Knee Bloom High"
    knee_bloom_high.name = "Knee Bloom High"
    knee_bloom_high.use_custom_color = True
    knee_bloom_high.color = (0.46666666865348816, 0.32549020648002625, 0.37254902720451355)
    knee_bloom_high.angle_offset = 0.0
    knee_bloom_high.color_modulation = 0.25
    knee_bloom_high.fade = 0.8999999761581421
    knee_bloom_high.glare_type = 'BLOOM'
    knee_bloom_high.iterations = 3
    knee_bloom_high.mix = 1.0
    knee_bloom_high.quality = 'HIGH'
    knee_bloom_high.size = 9
    knee_bloom_high.streaks = 4
    knee_bloom_high.threshold = 0.0
    knee_bloom_high.use_rotate_45 = True

    #node Knee Mix
    knee_mix = oe_bloom.nodes.new("CompositorNodeMixRGB")
    knee_mix.label = "Knee Mix"
    knee_mix.name = "Knee Mix"
    knee_mix.use_custom_color = True
    knee_mix.color = (0.5254902243614197, 0.4117647111415863, 0.21568627655506134)
    knee_mix.blend_type = 'ADD'
    knee_mix.use_alpha = False
    knee_mix.use_clamp = False

    #node Group Input 05
    group_input_05 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_05.label = "Group Input 05"
    group_input_05.name = "Group Input 05"
    group_input_05.use_custom_color = True
    group_input_05.color = (0.23529411852359772, 0.2235294133424759, 0.21568627655506134)
    group_input_05.outputs[1].hide = True
    group_input_05.outputs[2].hide = True
    group_input_05.outputs[3].hide = True
    group_input_05.outputs[4].hide = True
    group_input_05.outputs[5].hide = True
    group_input_05.outputs[7].hide = True
    group_input_05.outputs[8].hide = True
    group_input_05.outputs[9].hide = True
    group_input_05.outputs[10].hide = True
    group_input_05.outputs[11].hide = True
    group_input_05.outputs[12].hide = True
    group_input_05.outputs[13].hide = True
    group_input_05.outputs[14].hide = True
    group_input_05.outputs[15].hide = True
    group_input_05.outputs[16].hide = True

    #node Group Input 03
    group_input_03 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_03.label = "Group Input 03"
    group_input_03.name = "Group Input 03"
    group_input_03.use_custom_color = True
    group_input_03.color = (0.23529411852359772, 0.2235294133424759, 0.21568627655506134)
    group_input_03.outputs[0].hide = True
    group_input_03.outputs[1].hide = True
    group_input_03.outputs[2].hide = True
    group_input_03.outputs[3].hide = True
    group_input_03.outputs[4].hide = True
    group_input_03.outputs[6].hide = True
    group_input_03.outputs[7].hide = True
    group_input_03.outputs[8].hide = True
    group_input_03.outputs[9].hide = True
    group_input_03.outputs[10].hide = True
    group_input_03.outputs[11].hide = True
    group_input_03.outputs[12].hide = True
    group_input_03.outputs[13].hide = True
    group_input_03.outputs[14].hide = True
    group_input_03.outputs[15].hide = True
    group_input_03.outputs[16].hide = True

    #node Group Input 02
    group_input_02 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_02.label = "Group Input 02"
    group_input_02.name = "Group Input 02"
    group_input_02.use_custom_color = True
    group_input_02.color = (0.23529411852359772, 0.2235294133424759, 0.21568627655506134)
    group_input_02.outputs[0].hide = True
    group_input_02.outputs[1].hide = True
    group_input_02.outputs[2].hide = True
    group_input_02.outputs[4].hide = True
    group_input_02.outputs[5].hide = True
    group_input_02.outputs[6].hide = True
    group_input_02.outputs[7].hide = True
    group_input_02.outputs[8].hide = True
    group_input_02.outputs[9].hide = True
    group_input_02.outputs[10].hide = True
    group_input_02.outputs[11].hide = True
    group_input_02.outputs[12].hide = True
    group_input_02.outputs[13].hide = True
    group_input_02.outputs[14].hide = True
    group_input_02.outputs[15].hide = True
    group_input_02.outputs[16].hide = True

    #node Bloom High && Low
    bloom_high____low = oe_bloom.nodes.new("NodeFrame")
    bloom_high____low.label = "Bloom High && Low"
    bloom_high____low.name = "Bloom High && Low"
    bloom_high____low.use_custom_color = True
    bloom_high____low.color = (0.27887165546417236, 0.4313916563987732, 0.31700167059898376)
    bloom_high____low.label_size = 32
    bloom_high____low.shrink = True

    #node Knee Bloom Low
    knee_bloom_low = oe_bloom.nodes.new("CompositorNodeGlare")
    knee_bloom_low.label = "Knee Bloom Low"
    knee_bloom_low.name = "Knee Bloom Low"
    knee_bloom_low.use_custom_color = True
    knee_bloom_low.color = (0.46666666865348816, 0.32549020648002625, 0.37254902720451355)
    knee_bloom_low.angle_offset = 0.0
    knee_bloom_low.color_modulation = 0.25
    knee_bloom_low.fade = 0.8999999761581421
    knee_bloom_low.glare_type = 'BLOOM'
    knee_bloom_low.iterations = 3
    knee_bloom_low.mix = 1.0
    knee_bloom_low.quality = 'LOW'
    knee_bloom_low.size = 9
    knee_bloom_low.streaks = 4
    knee_bloom_low.threshold = 0.0
    knee_bloom_low.use_rotate_45 = True

    #node KB Switch
    kb_switch = oe_bloom.nodes.new("CompositorNodeSwitch")
    kb_switch.label = "KB Switch"
    kb_switch.name = "KB Switch"
    kb_switch.use_custom_color = True
    kb_switch.color = (0.3490196168422699, 0.3176470696926117, 0.29411765933036804)
    kb_switch.check = True

    #node OB Switch
    ob_switch = oe_bloom.nodes.new("CompositorNodeSwitch")
    ob_switch.label = "OB Switch"
    ob_switch.name = "OB Switch"
    ob_switch.use_custom_color = True
    ob_switch.color = (0.3490196168422699, 0.3176470696926117, 0.29411765933036804)
    ob_switch.check = True

    #node Original Bloom Low
    original_bloom_low = oe_bloom.nodes.new("CompositorNodeGlare")
    original_bloom_low.label = "Original Bloom Low"
    original_bloom_low.name = "Original Bloom Low"
    original_bloom_low.use_custom_color = True
    original_bloom_low.color = (0.46666666865348816, 0.32549020648002625, 0.37254902720451355)
    original_bloom_low.angle_offset = 0.0
    original_bloom_low.color_modulation = 0.25
    original_bloom_low.fade = 0.8999999761581421
    original_bloom_low.glare_type = 'BLOOM'
    original_bloom_low.iterations = 3
    original_bloom_low.mix = 1.0
    original_bloom_low.quality = 'LOW'
    original_bloom_low.size = 1
    original_bloom_low.streaks = 4
    original_bloom_low.threshold = 0.0
    original_bloom_low.use_rotate_45 = True

    #node Group Input 01
    group_input_01 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_01.label = "Group Input 01"
    group_input_01.name = "Group Input 01"
    group_input_01.use_custom_color = True
    group_input_01.color = (0.23529411852359772, 0.2235294133424759, 0.21568627655506134)
    group_input_01.outputs[0].hide = True
    group_input_01.outputs[1].hide = True
    group_input_01.outputs[2].hide = True
    group_input_01.outputs[3].hide = True
    group_input_01.outputs[4].hide = True
    group_input_01.outputs[5].hide = True
    group_input_01.outputs[6].hide = True
    group_input_01.outputs[7].hide = True
    group_input_01.outputs[8].hide = True
    group_input_01.outputs[9].hide = True
    group_input_01.outputs[10].hide = True
    group_input_01.outputs[11].hide = True
    group_input_01.outputs[12].hide = True
    group_input_01.outputs[13].hide = True
    group_input_01.outputs[15].hide = True
    group_input_01.outputs[16].hide = True

    #node Reroute_00
    reroute_00 = oe_bloom.nodes.new("NodeReroute")
    reroute_00.name = "Reroute_00"
    reroute_00.label = "KB Switch"
    reroute_00.socket_idname = "NodeSocketColor"
    #node Reroute_01
    reroute_01 = oe_bloom.nodes.new("NodeReroute")
    reroute_01.name = "Reroute_01"
    reroute_01.label = "KB Switch"
    reroute_01.socket_idname = "NodeSocketColor"
    #node Clamp
    clamp = oe_bloom.nodes.new("CompositorNodeHueSat")
    clamp.label = "Clamp"
    clamp.name = "Clamp"
    clamp.use_custom_color = True
    clamp.color = (0.5254849791526794, 0.41176897287368774, 0.21568608283996582)

    #node Group Input 04
    group_input_04 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_04.label = "Group Input 04"
    group_input_04.name = "Group Input 04"
    group_input_04.use_custom_color = True
    group_input_04.color = (0.23529411852359772, 0.2235294133424759, 0.21568627655506134)
    group_input_04.outputs[0].hide = True
    group_input_04.outputs[1].hide = True
    group_input_04.outputs[2].hide = True
    group_input_04.outputs[3].hide = True
    group_input_04.outputs[4].hide = True
    group_input_04.outputs[5].hide = True
    group_input_04.outputs[6].hide = True
    group_input_04.outputs[8].hide = True
    group_input_04.outputs[9].hide = True
    group_input_04.outputs[10].hide = True
    group_input_04.outputs[14].hide = True
    group_input_04.outputs[15].hide = True
    group_input_04.outputs[16].hide = True

    #Set parents
    original_bloom_high.parent = bloom_high____low
    knee_bloom_high.parent = bloom_high____low
    knee_bloom_low.parent = bloom_high____low
    kb_switch.parent = bloom_high____low
    ob_switch.parent = bloom_high____low
    original_bloom_low.parent = bloom_high____low

    #Set locations
    group_output.location = (800.0, 120.0)
    group_input_00.location = (-1040.0, -300.0)
    original_bloom_high.location = (53.0, -48.0)
    color.location = (220.0, -40.0)
    blur.location = (-320.0, -40.0)
    blur_mix.location = (-140.0, -40.0)
    intensity.location = (620.0, 120.0)
    knee_bloom_high.location = (53.0, -488.0)
    knee_mix.location = (40.0, -40.0)
    group_input_05.location = (620.0, 220.0)
    group_input_03.location = (220.0, -200.0)
    group_input_02.location = (40.0, -220.0)
    bloom_high____low.location = (-833.0, -52.0)
    knee_bloom_low.location = (53.0, -268.0)
    kb_switch.location = (273.0, -328.0)
    ob_switch.location = (273.0, 112.0)
    original_bloom_low.location = (53.0, 172.0)
    group_input_01.location = (-320.0, -260.0)
    reroute_00.location = (-180.0, -340.0)
    reroute_01.location = (0.0, -220.0)
    clamp.location = (400.0, -40.0)
    group_input_04.location = (400.0, -220.0)

    #Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    group_input_00.width, group_input_00.height = 140.0, 100.0
    original_bloom_high.width, original_bloom_high.height = 154.0098876953125, 100.0
    color.width, color.height = 140.0, 100.0
    blur.width, blur.height = 151.06350708007812, 100.0
    blur_mix.width, blur_mix.height = 140.0, 100.0
    intensity.width, intensity.height = 140.0, 100.0
    knee_bloom_high.width, knee_bloom_high.height = 152.26959228515625, 100.0
    knee_mix.width, knee_mix.height = 140.0, 100.0
    group_input_05.width, group_input_05.height = 140.0, 100.0
    group_input_03.width, group_input_03.height = 140.0, 100.0
    group_input_02.width, group_input_02.height = 140.0, 100.0
    bloom_high____low.width, bloom_high____low.height = 420.0, 944.0
    knee_bloom_low.width, knee_bloom_low.height = 153.29302978515625, 100.0
    kb_switch.width, kb_switch.height = 140.0, 100.0
    ob_switch.width, ob_switch.height = 140.0, 100.0
    original_bloom_low.width, original_bloom_low.height = 154.0098876953125, 100.0
    group_input_01.width, group_input_01.height = 150.76458740234375, 100.0
    reroute_00.width, reroute_00.height = 16.0, 100.0
    reroute_01.width, reroute_01.height = 16.0, 100.0
    clamp.width, clamp.height = 152.98968505859375, 100.0
    group_input_04.width, group_input_04.height = 140.0, 100.0

    #initialize oe_bloom links
    #ob_switch.Image -> blur_mix.Image
    oe_bloom.links.new(ob_switch.outputs[0], blur_mix.inputs[2])
    #blur_mix.Image -> knee_mix.Image
    oe_bloom.links.new(blur_mix.outputs[0], knee_mix.inputs[1])
    #blur.Image -> blur_mix.Image
    oe_bloom.links.new(blur.outputs[0], blur_mix.inputs[1])
    #knee_mix.Image -> color.Image
    oe_bloom.links.new(knee_mix.outputs[0], color.inputs[1])
    #ob_switch.Image -> blur.Image
    oe_bloom.links.new(ob_switch.outputs[0], blur.inputs[0])
    #group_input_00.Image -> original_bloom_high.Image
    oe_bloom.links.new(group_input_00.outputs[0], original_bloom_high.inputs[0])
    #group_input_00.Image -> knee_bloom_high.Image
    oe_bloom.links.new(group_input_00.outputs[0], knee_bloom_high.inputs[0])
    #intensity.Image -> group_output.Image
    oe_bloom.links.new(intensity.outputs[0], group_output.inputs[0])
    #group_input_05.Image -> intensity.Image
    oe_bloom.links.new(group_input_05.outputs[0], intensity.inputs[1])
    #group_input_05.Intensity -> intensity.Fac
    oe_bloom.links.new(group_input_05.outputs[6], intensity.inputs[0])
    #group_input_03.Color -> color.Image
    oe_bloom.links.new(group_input_03.outputs[5], color.inputs[2])
    #group_input_02.Knee -> knee_mix.Fac
    oe_bloom.links.new(group_input_02.outputs[3], knee_mix.inputs[0])
    #group_input_00.Image -> knee_bloom_low.Image
    oe_bloom.links.new(group_input_00.outputs[0], knee_bloom_low.inputs[0])
    #knee_bloom_high.Image -> kb_switch.On
    oe_bloom.links.new(knee_bloom_high.outputs[0], kb_switch.inputs[1])
    #knee_bloom_low.Image -> kb_switch.Off
    oe_bloom.links.new(knee_bloom_low.outputs[0], kb_switch.inputs[0])
    #original_bloom_high.Image -> ob_switch.On
    oe_bloom.links.new(original_bloom_high.outputs[0], ob_switch.inputs[1])
    #original_bloom_low.Image -> ob_switch.Off
    oe_bloom.links.new(original_bloom_low.outputs[0], ob_switch.inputs[0])
    #group_input_01.Blur Mix -> blur.Size
    oe_bloom.links.new(group_input_01.outputs[14], blur.inputs[1])
    #kb_switch.Image -> reroute_00.Input
    oe_bloom.links.new(kb_switch.outputs[0], reroute_00.inputs[0])
    #group_input_00.Image -> original_bloom_low.Image
    oe_bloom.links.new(group_input_00.outputs[0], original_bloom_low.inputs[0])
    #reroute_00.Output -> reroute_01.Input
    oe_bloom.links.new(reroute_00.outputs[0], reroute_01.inputs[0])
    #reroute_01.Output -> knee_mix.Image
    oe_bloom.links.new(reroute_01.outputs[0], knee_mix.inputs[2])
    #color.Image -> clamp.Image
    oe_bloom.links.new(color.outputs[0], clamp.inputs[0])
    #clamp.Image -> intensity.Image
    oe_bloom.links.new(clamp.outputs[0], intensity.inputs[2])
    #group_input_04.Fac -> clamp.Fac
    oe_bloom.links.new(group_input_04.outputs[13], clamp.inputs[4])
    #group_input_04.Clamp -> clamp.Value
    oe_bloom.links.new(group_input_04.outputs[7], clamp.inputs[3])
    #group_input_04.Saturation -> clamp.Saturation
    oe_bloom.links.new(group_input_04.outputs[12], clamp.inputs[2])
    #group_input_04.Hue -> clamp.Hue
    oe_bloom.links.new(group_input_04.outputs[11], clamp.inputs[1])
    return oe_bloom

#initialize Bloom node group
def oe_bloom_node_group(context, operator, group_name):
    scene = bpy.context.scene
    oe_bloom = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    #enable use nodes
    if scene.use_nodes == False:
        scene.use_nodes = True

    oe_bloom.color_tag = "FILTER"
    oe_bloom.default_group_node_width = 149
    oe_bloom.description = "Replication of the legacy eevee bloom option"
        
    #oe_bloom interface
    #Socket Image
    image_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Image, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket_1 = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Image, in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.description = "Standard color output"

    #Socket Color
    color_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Color, in_out='INPUT', socket_type = 'NodeSocketColor')
    color_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.description = "oe_bloom Color"

    #Socket Quality
    quality_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Quality, in_out='INPUT', socket_type = 'NodeSocketFloat')
    quality_socket.default_value = 0.0
    quality_socket.min_value = 0.0
    quality_socket.max_value = 1.0
    quality_socket.subtype = 'FACTOR'
    quality_socket.attribute_domain = 'POINT'
    quality_socket.description = "If not set to something other the High, then the glare effect will only be applied to a low resolution copy of the image. This can be helpful to save render times while only doing preview renders"

    #Socket Knee
    knee_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Knee, in_out='INPUT', socket_type = 'NodeSocketFloat')
    knee_socket.default_value = 0.0
    knee_socket.min_value = 0.0
    knee_socket.max_value = 1.0
    knee_socket.subtype = 'FACTOR'
    knee_socket.attribute_domain = 'POINT'

    #Socket Threshold
    threshold_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Threshold, in_out='INPUT', socket_type = 'NodeSocketFloat')
    threshold_socket.default_value = 1.0
    threshold_socket.min_value = 0.0
    threshold_socket.max_value = 1000.0
    threshold_socket.subtype = 'NONE'
    threshold_socket.attribute_domain = 'POINT'

    #Socket Radius
    radius_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Radius, in_out='INPUT', socket_type = 'NodeSocketFloat')
    radius_socket.default_value = 0.0
    radius_socket.min_value = 0.0
    radius_socket.max_value = 2048
    radius_socket.subtype = 'NONE'
    radius_socket.attribute_domain = 'POINT'

    #Socket Blur Mix
    blur_mix_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Blur_Mix, in_out='INPUT', socket_type = 'NodeSocketFloat')
    blur_mix_socket.default_value = 1.0
    blur_mix_socket.min_value = 0.0
    blur_mix_socket.max_value = 1.0
    blur_mix_socket.subtype = 'NONE'
    blur_mix_socket.attribute_domain = 'POINT'

    #Socket Intensity
    intensity_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Intensity, in_out='INPUT', socket_type = 'NodeSocketFloat')
    intensity_socket.default_value = 1.0
    intensity_socket.min_value = 0.0
    intensity_socket.max_value = 1.0
    intensity_socket.subtype = 'FACTOR'
    intensity_socket.attribute_domain = 'POINT'

    #Socket oe_bloom Size
    oe_bloom_size_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Bloom_Size, in_out='INPUT', socket_type = 'NodeSocketFloat')
    oe_bloom_size_socket.default_value = 9.0
    oe_bloom_size_socket.min_value = 1.0
    oe_bloom_size_socket.max_value = 9.0
    oe_bloom_size_socket.subtype = 'NONE'
    oe_bloom_size_socket.attribute_domain = 'POINT'
    oe_bloom_size_socket.description = "Scale of the glow relative to the size of the image. 9 means the glow can cover the entire image, 8 means it can only cover half the image, 7 means it can only cover quarter of the image, and so on."


    #initialize oe_bloom nodes
    #node Group Output
    group_output = oe_bloom.nodes.new("NodeGroupOutput")
    group_output.label = OE_Bloom_Names.Group_Output
    group_output.name = OE_Bloom_Names.Group_Output
    group_output.use_custom_color = True
    group_output.color = Color.DARK_GRAY
    group_output.is_active_output = True

    #node Group Input 00
    group_input_00 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_00.label = OE_Bloom_Names.Group_Input_00
    group_input_00.name = OE_Bloom_Names.Group_Input_00
    group_input_00.use_custom_color = True
    group_input_00.color = Color.DARK_GRAY
    group_input_00.outputs[1].hide = True
    group_input_00.outputs[2].hide = True
    group_input_00.outputs[3].hide = True
    group_input_00.outputs[4].hide = True
    group_input_00.outputs[5].hide = True
    group_input_00.outputs[6].hide = True
    group_input_00.outputs[7].hide = True
    group_input_00.outputs[8].hide = True
    group_input_00.outputs[9].hide = True

    #node Original Bloom High
    original_oe_bloom_high = oe_bloom.nodes.new("CompositorNodeGlare")
    original_oe_bloom_high.label = OE_Bloom_Names.Original_Bloom_High
    original_oe_bloom_high.name = OE_Bloom_Names.Original_Bloom_High
    original_oe_bloom_high.use_custom_color = True
    original_oe_bloom_high.color = Color.DARK_PURPLE
    original_oe_bloom_high.glare_type = 'BLOOM'
    original_oe_bloom_high.mix = 1.0
    original_oe_bloom_high.quality = 'HIGH'
    original_oe_bloom_high.size = 9
    original_oe_bloom_high.threshold = 1.0

    #node Color
    color = oe_bloom.nodes.new("CompositorNodeMixRGB")
    color.label = OE_Bloom_Names.Color
    color.name = OE_Bloom_Names.Color
    color.use_custom_color = True
    color.color = Color.BROWN
    color.blend_type = 'COLOR'
    color.use_alpha = False
    color.use_clamp = False
    color.inputs[0].hide = True
    #Fac
    color.inputs[0].default_value = 1.0

    #node Blur
    blur = oe_bloom.nodes.new("CompositorNodeBlur")
    blur.label = OE_Bloom_Names.Blur
    blur.name = OE_Bloom_Names.Blur
    blur.use_custom_color = True
    blur.color = Color.DARK_PURPLE
    blur.aspect_correction = 'NONE'
    blur.filter_type = 'FAST_GAUSS'
    blur.size_x = 0
    blur.size_y = 0
    blur.use_extended_bounds = False
    blur.use_relative = False

    #node Blur Mix
    blur_mix = oe_bloom.nodes.new("CompositorNodeMixRGB")
    blur_mix.label = OE_Bloom_Names.Blur_Mix
    blur_mix.name = OE_Bloom_Names.Blur_Mix
    blur_mix.use_custom_color = True
    blur_mix.color = Color.BROWN
    blur_mix.blend_type = 'SCREEN'
    blur_mix.use_alpha = False
    blur_mix.use_clamp = True
    blur_mix.inputs[0].hide = True
    #Fac
    blur_mix.inputs[0].default_value = 1.0

    #node Intensity
    intensity = oe_bloom.nodes.new("CompositorNodeMixRGB")
    intensity.label = OE_Bloom_Names.Intensity
    intensity.name = OE_Bloom_Names.Intensity
    intensity.use_custom_color = True
    intensity.color = Color.BROWN
    intensity.blend_type = 'ADD'
    intensity.use_alpha = False
    intensity.use_clamp = False

    #node Knee Bloom High
    knee_oe_bloom_high = oe_bloom.nodes.new("CompositorNodeGlare")
    knee_oe_bloom_high.label = OE_Bloom_Names.Knee_Bloom_High
    knee_oe_bloom_high.name = OE_Bloom_Names.Knee_Bloom_High
    knee_oe_bloom_high.use_custom_color = True
    knee_oe_bloom_high.color = Color.DARK_PURPLE
    knee_oe_bloom_high.angle_offset = 0.0
    knee_oe_bloom_high.color_modulation = 0.25
    knee_oe_bloom_high.fade = 0.8999999761581421
    knee_oe_bloom_high.glare_type = 'BLOOM'
    knee_oe_bloom_high.mix = 1.0
    knee_oe_bloom_high.quality = 'HIGH'
    knee_oe_bloom_high.size = 9
    knee_oe_bloom_high.threshold = 0.0

    #node Knee Mix
    knee_mix = oe_bloom.nodes.new("CompositorNodeMixRGB")
    knee_mix.label = OE_Bloom_Names.Knee_Mix
    knee_mix.name = OE_Bloom_Names.Knee_Mix
    knee_mix.use_custom_color = True
    knee_mix.color = Color.BROWN
    knee_mix.blend_type = 'ADD'
    knee_mix.use_alpha = False
    knee_mix.use_clamp = False

    #node Group Input 01
    group_input_01 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_01.label = OE_Bloom_Names.Group_Input_01
    group_input_01.name = OE_Bloom_Names.Group_Input_01
    group_input_01.use_custom_color = True
    group_input_01.color = Color.DARK_GRAY
    group_input_01.outputs[1].hide = True
    group_input_01.outputs[2].hide = True
    group_input_01.outputs[3].hide = True
    group_input_01.outputs[4].hide = True
    group_input_01.outputs[5].hide = True
    group_input_01.outputs[6].hide = True
    group_input_01.outputs[8].hide = True
    group_input_01.outputs[9].hide = True

    #node Group Input 02
    group_input_02 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_02.label = OE_Bloom_Names.Group_Input_02
    group_input_02.name = OE_Bloom_Names.Group_Input_02
    group_input_02.use_custom_color = True
    group_input_02.color = Color.DARK_GRAY
    group_input_02.outputs[0].hide = True
    group_input_02.outputs[2].hide = True
    group_input_02.outputs[3].hide = True
    group_input_02.outputs[4].hide = True
    group_input_02.outputs[5].hide = True
    group_input_02.outputs[6].hide = True
    group_input_02.outputs[7].hide = True
    group_input_02.outputs[8].hide = True
    group_input_02.outputs[9].hide = True

    #node Group Input 03
    group_input_03 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_03.label = OE_Bloom_Names.Group_Input_03
    group_input_03.name = OE_Bloom_Names.Group_Input_03
    group_input_03.use_custom_color = True
    group_input_03.color = Color.DARK_GRAY
    group_input_03.outputs[0].hide = True
    group_input_03.outputs[1].hide = True
    group_input_03.outputs[2].hide = True
    group_input_03.outputs[4].hide = True
    group_input_03.outputs[5].hide = True
    group_input_03.outputs[6].hide = True
    group_input_03.outputs[7].hide = True
    group_input_03.outputs[8].hide = True
    group_input_03.outputs[9].hide = True

    #node Bloom High && Low
    oe_bloom_high____low = oe_bloom.nodes.new("NodeFrame")
    oe_bloom_high____low.label = OE_Bloom_Names.Bloom_High_Low
    oe_bloom_high____low.name = OE_Bloom_Names.Bloom_High_Low
    oe_bloom_high____low.use_custom_color = True
    oe_bloom_high____low.color = (0.27887165546417236, 0.4313916563987732, 0.31700167059898376)
    oe_bloom_high____low.label_size = 32
    oe_bloom_high____low.shrink = True

    #node Knee Bloom Low
    knee_oe_bloom_low = oe_bloom.nodes.new("CompositorNodeGlare")
    knee_oe_bloom_low.label = OE_Bloom_Names.Knee_Bloom_Low
    knee_oe_bloom_low.name = OE_Bloom_Names.Knee_Bloom_Low
    knee_oe_bloom_low.use_custom_color = True
    knee_oe_bloom_low.color = Color.DARK_PURPLE
    knee_oe_bloom_low.glare_type = 'BLOOM'
    knee_oe_bloom_low.mix = 1.0
    knee_oe_bloom_low.quality = 'LOW'
    knee_oe_bloom_low.size = 9
    knee_oe_bloom_low.threshold = 0.0

    #node KB Switch
    kb_switch = oe_bloom.nodes.new("CompositorNodeSwitch")
    kb_switch.label = OE_Bloom_Names.KB_Switch
    kb_switch.name = OE_Bloom_Names.KB_Switch
    kb_switch.use_custom_color = True
    kb_switch.color = Color.LIGHT_GRAY
    kb_switch.check = False

    #node OB Switch
    ob_switch = oe_bloom.nodes.new("CompositorNodeSwitch")
    ob_switch.label = OE_Bloom_Names.OB_Switch
    ob_switch.name = OE_Bloom_Names.OB_Switch
    ob_switch.use_custom_color = True
    ob_switch.color = Color.LIGHT_GRAY
    ob_switch.check = False

    #node Original oe_bloom Low
    original_oe_bloom_low = oe_bloom.nodes.new("CompositorNodeGlare")
    original_oe_bloom_low.label = OE_Bloom_Names.Original_Bloom_Low
    original_oe_bloom_low.name = OE_Bloom_Names.Original_Bloom_Low
    original_oe_bloom_low.use_custom_color = True
    original_oe_bloom_low.color = Color.DARK_PURPLE
    original_oe_bloom_low.glare_type = 'BLOOM'
    original_oe_bloom_low.mix = 1.0
    original_oe_bloom_low.quality = 'LOW'
    original_oe_bloom_low.threshold = 1.0
    original_oe_bloom_low.size = 9

    #node Group Input 04
    group_input_04 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_04.label = OE_Bloom_Names.Group_Input_04
    group_input_04.name = OE_Bloom_Names.Group_Input_04
    group_input_04.use_custom_color = True
    group_input_04.color = Color.DARK_GRAY
    group_input_04.outputs[0].hide = True
    group_input_04.outputs[1].hide = True
    group_input_04.outputs[2].hide = True
    group_input_04.outputs[3].hide = True
    group_input_04.outputs[4].hide = True
    group_input_04.outputs[5].hide = True
    group_input_04.outputs[7].hide = True
    group_input_04.outputs[8].hide = True
    group_input_04.outputs[9].hide = True

    #node Reroute_00
    reroute_00 = oe_bloom.nodes.new("NodeReroute")
    reroute_00.name = OE_Bloom_Names.Reroute_00
    reroute_00.socket_idname = "NodeSocketColor"

    #node Reroute_01
    reroute_01 = oe_bloom.nodes.new("NodeReroute")
    reroute_01.name = OE_Bloom_Names.Reroute_01
    reroute_01.socket_idname = "NodeSocketColor"

    #node Clamp
    clamp = oe_bloom.nodes.new("CompositorNodeCurveRGB")
    clamp.label = OE_Bloom_Names.Clamp
    clamp.name = OE_Bloom_Names.Clamp
    clamp.use_custom_color = True
    clamp.color = Color.BROWN

    #mapping settings
    clamp.mapping.extend = 'EXTRAPOLATED'
    clamp.mapping.tone = 'STANDARD'
    clamp.mapping.black_level = (0.0, 0.0, 0.0)
    clamp.mapping.white_level = (1.0, 1.0, 1.0)
    clamp.mapping.clip_min_x = 0.0
    clamp.mapping.clip_min_y = 0.0
    clamp.mapping.clip_max_x = 1.0
    clamp.mapping.clip_max_y = 1.0
    clamp.mapping.use_clip = True

    #curve 0
    clamp_curve_0 = clamp.mapping.curves[0]
    clamp_curve_0_point_0 = clamp_curve_0.points[0]
    clamp_curve_0_point_0.location = (0.0, 0.0)
    clamp_curve_0_point_0.handle_type = 'AUTO'
    clamp_curve_0_point_1 = clamp_curve_0.points[1]
    clamp_curve_0_point_1.location = (1.0, 1.0)
    clamp_curve_0_point_1.handle_type = 'AUTO'

    #curve 1
    clamp_curve_1 = clamp.mapping.curves[1]
    clamp_curve_1_point_0 = clamp_curve_1.points[0]
    clamp_curve_1_point_0.location = (0.0, 0.0)
    clamp_curve_1_point_0.handle_type = 'AUTO'
    clamp_curve_1_point_1 = clamp_curve_1.points[1]
    clamp_curve_1_point_1.location = (1.0, 1.0)
    clamp_curve_1_point_1.handle_type = 'AUTO'

    #curve 2
    clamp_curve_2 = clamp.mapping.curves[2]
    clamp_curve_2_point_0 = clamp_curve_2.points[0]
    clamp_curve_2_point_0.location = (0.0, 0.0)
    clamp_curve_2_point_0.handle_type = 'AUTO'
    clamp_curve_2_point_1 = clamp_curve_2.points[1]
    clamp_curve_2_point_1.location = (1.0, 1.0)
    clamp_curve_2_point_1.handle_type = 'AUTO'

    #curve 3
    clamp_curve_3 = clamp.mapping.curves[3]
    clamp_curve_3_point_0 = clamp_curve_3.points[0]
    clamp_curve_3_point_0.location = (0.0, 0.0)
    clamp_curve_3_point_0.handle_type = 'AUTO'
    clamp_curve_3_point_1 = clamp_curve_3.points[1]
    clamp_curve_3_point_1.location = (1.0, 1.0)
    clamp_curve_3_point_1.handle_type = 'AUTO'

    #update curve after changes
    clamp.mapping.update()
    clamp.inputs[0].hide = True
    clamp.inputs[2].hide = True
    clamp.inputs[3].hide = True

    #Fac
    clamp.inputs[0].default_value = 1.0
    #Black Level
    clamp.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
    #White Level
    clamp.inputs[3].default_value = (1.0, 1.0, 1.0, 1.0)

    #Set parents
    original_oe_bloom_high.parent = oe_bloom_high____low
    knee_oe_bloom_high.parent = oe_bloom_high____low
    knee_oe_bloom_low.parent = oe_bloom_high____low
    kb_switch.parent = oe_bloom_high____low
    ob_switch.parent = oe_bloom_high____low
    original_oe_bloom_low.parent = oe_bloom_high____low

    #Set locations
    group_output.location = (820.0, 120.0)
    group_input_00.location = (-1040.0, -300.0)
    original_oe_bloom_high.location = (53.0, -48.0)
    color.location = (220.0, -40.0)
    blur.location = (-320.0, -40.0)
    blur_mix.location = (-140.0, -40.0)
    intensity.location = (640.0, 120.0)
    knee_oe_bloom_high.location = (53.0, -488.0)
    knee_mix.location = (40.0, -40.0)
    group_input_01.location = (640.0, 220.0)
    group_input_02.location = (220.0, -200.0)
    group_input_03.location = (40.0, -220.0)
    oe_bloom_high____low.location = (-833.0, -52.0)
    knee_oe_bloom_low.location = (53.0, -268.0)
    kb_switch.location = (273.0, -328.0)
    ob_switch.location = (273.0, 112.0)
    original_oe_bloom_low.location = (53.0, 172.0)
    group_input_04.location = (-320.0, -260.0)
    reroute_00.location = (-180.0, -340.0)
    reroute_01.location = (0.0, -220.0)
    clamp.location = (400.0, -40.0)

    #Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    group_input_00.width, group_input_00.height = 140.0, 100.0
    original_oe_bloom_high.width, original_oe_bloom_high.height = 154.0098876953125, 100.0
    color.width, color.height = 140.0, 100.0
    blur.width, blur.height = 151.06350708007812, 100.0
    blur_mix.width, blur_mix.height = 140.0, 100.0
    intensity.width, intensity.height = 140.0, 100.0
    knee_oe_bloom_high.width, knee_oe_bloom_high.height = 152.26959228515625, 100.0
    knee_mix.width, knee_mix.height = 140.0, 100.0
    group_input_01.width, group_input_01.height = 140.0, 100.0
    group_input_02.width, group_input_02.height = 140.0, 100.0
    group_input_03.width, group_input_03.height = 140.0, 100.0
    oe_bloom_high____low.width, oe_bloom_high____low.height = 420.0, 944.0
    knee_oe_bloom_low.width, knee_oe_bloom_low.height = 153.29302978515625, 100.0
    kb_switch.width, kb_switch.height = 140.0, 100.0
    ob_switch.width, ob_switch.height = 140.0, 100.0
    original_oe_bloom_low.width, original_oe_bloom_low.height = 154.0098876953125, 100.0
    group_input_04.width, group_input_04.height = 150.76458740234375, 100.0
    reroute_00.width, reroute_00.height = 16.0, 100.0
    reroute_01.width, reroute_01.height = 16.0, 100.0
    clamp.width, clamp.height = 200.0, 100.0

    #initialize oe_bloom links
    #ob_switch.Image -> blur_mix.Image
    oe_bloom.links.new(ob_switch.outputs[0], blur_mix.inputs[2])

    #blur_mix.Image -> knee_mix.Image
    oe_bloom.links.new(blur_mix.outputs[0], knee_mix.inputs[1])

    #blur.Image -> blur_mix.Image
    oe_bloom.links.new(blur.outputs[0], blur_mix.inputs[1])

    #knee_mix.Image -> color.Image
    oe_bloom.links.new(knee_mix.outputs[0], color.inputs[1])

    #ob_switch.Image -> blur.Image
    oe_bloom.links.new(ob_switch.outputs[0], blur.inputs[0])

    #group_input_00.Image -> original_oe_bloom_high.Image
    oe_bloom.links.new(group_input_00.outputs[0], original_oe_bloom_high.inputs[0])

    #group_input_00.Image -> knee_oe_bloom_high.Image
    oe_bloom.links.new(group_input_00.outputs[0], knee_oe_bloom_high.inputs[0])

    #intensity.Image -> group_output.Image
    oe_bloom.links.new(intensity.outputs[0], group_output.inputs[0])

    #group_input_01.Image -> intensity.Image
    oe_bloom.links.new(group_input_01.outputs[0], intensity.inputs[1])

    #group_input_01.Intensity -> intensity.Fac
    oe_bloom.links.new(group_input_01.outputs[7], intensity.inputs[0])

    #group_input_02.Color -> color.Image
    oe_bloom.links.new(group_input_02.outputs[1], color.inputs[2])

    #group_input_03.Knee -> knee_mix.Fac
    oe_bloom.links.new(group_input_03.outputs[3], knee_mix.inputs[0])

    #group_input_00.Image -> knee_oe_bloom_low.Image
    oe_bloom.links.new(group_input_00.outputs[0], knee_oe_bloom_low.inputs[0])
    
    #knee_oe_bloom_high.Image -> kb_switch.On
    oe_bloom.links.new(knee_oe_bloom_high.outputs[0], kb_switch.inputs[1])

    #knee_oe_bloom_low.Image -> kb_switch.Off
    oe_bloom.links.new(knee_oe_bloom_low.outputs[0], kb_switch.inputs[0])

    #original_oe_bloom_high.Image -> ob_switch.On
    oe_bloom.links.new(original_oe_bloom_high.outputs[0], ob_switch.inputs[1])

    #original_oe_bloom_low.Image -> ob_switch.Off
    oe_bloom.links.new(original_oe_bloom_low.outputs[0], ob_switch.inputs[0])

    #group_input_04.Blur Mix -> blur.Size
    oe_bloom.links.new(group_input_04.outputs[6], blur.inputs[1])

    #kb_switch.Image -> reroute_00.Input
    oe_bloom.links.new(kb_switch.outputs[0], reroute_00.inputs[0])

    #group_input_00.Image -> original_oe_bloom_low.Image
    oe_bloom.links.new(group_input_00.outputs[0], original_oe_bloom_low.inputs[0])

    #reroute_00.Output -> reroute_01.Input
    oe_bloom.links.new(reroute_00.outputs[0], reroute_01.inputs[0])

    #reroute_01.Output -> knee_mix.Image
    oe_bloom.links.new(reroute_01.outputs[0], knee_mix.inputs[2])

    #clamp.Image -> intensity.Image
    oe_bloom.links.new(clamp.outputs[0], intensity.inputs[2])

    #color.Image -> clamp.Image
    oe_bloom.links.new(color.outputs[0], clamp.inputs[1])

    return oe_bloom

class NODE_OT_BLOOM(bpy.types.Operator):
    bl_label = OE_Bloom_Names.OE_Bloom
    bl_idname = "node.oe_bloom_operator"
    bl_description = "Replication of the legacy eevee bloom option, but can be used in cycles as well"

    def execute(shelf, context):
        # Get the compositor node tree
        node_tree = context.scene.node_tree
        nodes = node_tree.nodes
        links = node_tree.links

        # Check if nodes exist, otherwise create them
        render_layer_node = nodes.get("Render Layers") or nodes.new(type="CompositorNodeRLayers")
        render_layer_node.location = (-300, 0)

        composite_node = nodes.get("Composite") or nodes.new(type="CompositorNodeComposite")
        composite_node.location = (300, 86)

        viewer_node = nodes.get("Viewer") or nodes.new(type="CompositorNodeViewer")
        viewer_node.location = (300, -24)

        custom_oe_bloom_node_name = OE_Bloom_Names.OE_Bloom
        oe_bloom_group = oe_bloom_node_group(shelf, context, custom_oe_bloom_node_name)
        oe_bloom_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        oe_bloom_node.name = OE_Bloom_Names.OE_Bloom
        oe_bloom_node.label = OE_Bloom_Names.OE_Bloom
        oe_bloom_node.width = 149
        oe_bloom_node.node_tree = bpy.data.node_groups[oe_bloom_group.name]
        oe_bloom_node.use_custom_color = True
        oe_bloom_node.color = Color.DARK_PURPLE
        oe_bloom_node.select = True

        def add_driver_var(socket, data_path, name="default_value", id_type="SCENE", id=bpy.context.scene):
            """
            Adds a variable to a given socket.

            Parameters
            ----------
            socket : bpy.types.NodeSocket
                The socket to add the variable to.
            data_path : str
                The data path for the variable.
            name : str, optional
                The name of the variable. Defaults to "default_value".
            id_type : str, optional
                The type of ID for the variable. Defaults to "SCENE".
            id : bpy.types.ID, optional
                The ID for the variable. Defaults to bpy.context.scene.

            Returns
            -------
            driver_var : bpy.types.DriverVariable
                The added variable.
            """

            driver_var = socket.variables.new()
            driver_var.name = name
            driver_var.targets[0].id_type = id_type
            driver_var.targets[0].id = id
            driver_var.targets[0].data_path = data_path
            return driver_var

        """
        * The ability to add drivers to nodes is made possible by Victor Stepanov
        * (https://www.skool.com/cgpython/how-to-add-drivers-to-node-group-sockets-using-python?p=0be0f439)
        * (https://www.skool.com/cgpython/how-do-i-add-the-drivers-to-a-node-group-every-time?p=4220eddf)
        * His youtube channel (https://www.youtube.com/@CGPython)
        """

        # Original Bloom Switch
        oe_bloom_obs_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.OB_Switch].driver_add('check').driver
        oe_bloom_obs_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obs_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[2].default_value'
        )

        # Knee Bloom Switch
        oe_bloom_kbs_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.KB_Switch].driver_add('check').driver
        oe_bloom_kbs_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_kbs_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[2].default_value'
        )

        # Original Bloom High
        oe_bloom_obh_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Original_Bloom_High].driver_add('threshold').driver
        oe_bloom_obh_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obh_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[4].default_value'
        )

        # Original Bloom Low
        oe_bloom_obl_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Original_Bloom_Low].driver_add('threshold').driver
        oe_bloom_obl_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obl_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[4].default_value'
        )

        # Original Bloom High Size
        oe_bloom_obhs_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Original_Bloom_High].driver_add('size').driver
        oe_bloom_obhs_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obhs_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[8].default_value'
        )

        # Original Bloom Low Size
        oe_bloom_obls_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Original_Bloom_Low].driver_add('size').driver
        oe_bloom_obls_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obls_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[8].default_value'
        )

        # Radius X
        oe_bloom_arx_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Blur].driver_add('size_x').driver
        oe_bloom_arx_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_arx_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[5].default_value'
        )

        # Radius Y
        oe_bloom_ary_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Blur].driver_add('size_y').driver
        oe_bloom_ary_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_ary_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[5].default_value'
        )

        # Ensure all connections exist
        def ensure_connection(output_node, output_socket_name, input_node, input_socket_name):
            """
            Ensures that a connection exists between two nodes

            Args:
                output_node (bpy.types.Node): The node that the connection comes from
                output_socket_name (str): The name of the output socket
                input_node (bpy.types.Node): The node that the connection goes to
                input_socket_name (str): The name of the input socket

            Returns:
                None
            """
            # Check if a link already exists
            for link in links:
                if (
                    link.from_node == output_node
                    and link.to_node == input_node
                    and link.from_socket.name == output_socket_name
                    and link.to_socket.name == input_socket_name
                ):
                    return  # Connection already exists

            # Create the link if not found
            links.new(output_node.outputs[output_socket_name], input_node.inputs[input_socket_name])

        # Connect the nodes
        ensure_connection(render_layer_node, "Image", oe_bloom_node, "Image")
        ensure_connection(oe_bloom_node, "Image", composite_node, "Image")
        ensure_connection(oe_bloom_node, "Image", viewer_node, "Image")

        return {"FINISHED"}

class PROP_PT_BLOOM(bpy.types.Panel):
    bl_label = 'Bloom'
    bl_idname = 'PROP_PT_BLOOM'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_description = 'Old Eevee Bloom In Both Eevee And Cycles'
    bl_order = 3
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True  # Always display the panel

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        node_tree = bpy.context.scene.node_tree  # Access the Compositor node tree

        if node_tree:
            # Check if the OE_Bloom node group exists
            bloom_node = next((node for node in node_tree.nodes if node.type == 'GROUP' and node.name == OE_Bloom_Names.OE_Bloom), None)
            if bloom_node:
                # Add Mute/Unmute property
                layout.prop(scene, "bloom_mute_unmute_bool", text="Mute/Unmute", icon='CHECKBOX_HLT' if scene.bloom_mute_unmute_bool else 'CANCEL')
                
                # Display properties of the active node
                box = layout.box()
                box.label(text="Properties", icon="PROPERTIES")

                for input in bloom_node.inputs:
                    # Skip the "Image" input
                    if input.name == OE_Bloom_Names.Image:
                        continue
                    box.prop(input, "default_value", text=input.name)
            else:
                layout.operator("node.oe_bloom_operator", text="Create OE_Bloom", icon='NODE_MATERIAL')

# Register and unregister
classes = [PROP_PT_BLOOM, NODE_OT_BLOOM]

def register():
    bpy.types.Scene.bloom_mute_unmute_bool = BoolProperty(
        name="Bloom Mute/Unmute",
        description="Mute or unmute the OE_Bloom node group in the Compositor",
        default=False,
        update=toggle_bloom_mute  # Attach the callback function
    )
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    del bpy.types.Scene.bloom_mute_unmute_bool
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()