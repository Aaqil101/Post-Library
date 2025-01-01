import bpy
from typing import Tuple
from bpy.props import BoolProperty

def toggle_oe_bloom_mute(self, context):
    """
    Callback function to mute or unmute the OE_Bloom node group in the Compositor node tree.

    Args:
        self: The current context owner (usually the scene).
        context: The Blender context.
    """
    scene = context.scene
    node_tree = context.scene.node_tree  # Access the active Compositor node tree

    if node_tree:  # Ensure the node tree exists
        for node in node_tree.nodes: 
            if node.type == 'GROUP' and node.name == OE_Bloom_Names.OE_Bloom:  # Check for the specific node group
                node.mute = scene.bloom_mute_unmute_bool  # Set the mute property
                print(f"Node group 'OE_Bloom' is now {'muted' if node.mute else 'unmuted'}.")
                return
        print("Node group 'OE_Bloom' not found in the Compositor node tree.")
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

def hex_color_add(color1, color2):
    """
    This function takes two hex color codes, adds their RGB components, and clamps each component to a maximum of 255.
    The resulting RGB components are then combined back into a hex color code.
    """
    # Split the hex codes into RGB components
    r1, g1, b1 = int(color1[:2], 16), int(color1[2:4], 16), int(color1[4:], 16)
    r2, g2, b2 = int(color2[:2], 16), int(color2[2:4], 16), int(color2[4:], 16)
    
    # Add the components and clamp each to a maximum of 255
    r = min(r1 + r2, 255)
    g = min(g1 + g2, 255)
    b = min(b1 + b2, 255)
    
    # Combine the components back into a hex color
    return f"{r:02X}{g:02X}{b:02X}"

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
    Intensity = "Intensity"
    Clamp = "Clamp"
    Other = "Other"
    Hue = "Hue"
    Saturation = "Saturation"
    Fac = "Fac"
    Composite = "Composite"
    Viewer = "Viewer"
    BM_Clamp = "BM Clamp"
    KM_Clamp = "KM Clamp"
    CR_Clamp = "CR Clamp"
    IY_Clamp = "IY Clamp"
    Clamp_Mix = "Clamp Mix"
    Blur_Mix = "Blur Mix"
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
    Group_Input_05 = "Group Input 05"
    Bloom_High_Low = "Bloom High && Low"
    Knee_Bloom_Low = "Knee Bloom Low"
    KB_Switch = "KB Switch"
    OB_Switch = "OB Switch"
    Original_Bloom_Low = "Original Bloom Low"
    Reroute_00 = "Reroute_00"
    Reroute_01 = "Reroute_01"
    Render_Layers = "Render Layers"

# Class to store all the descriptions of the Bloom properties
class OE_Bloom_Descr:
    image = "Standard color output"
    quality = "If the value is set to 0 then the bloom effect will be applied to the low resolution copy of the image. If the value is set to 1 then the bloom effect will be applied to the high resolution copy of the image. This can be helpful to save render times while only doing preview renders"
    threshold = "Filters out pixels under this level of brightness"
    knee = "Makes transition between under/over-threshold gradual"
    radius = "Bloom spread distance"
    color = "Color applied to the bloom effect"
    intensity = "Blend factor"
    clamp = "Maximum intensity a bloom pixel can have"
    other = "Additional options for customizing the bloom effect"
    hue = "The hue rotation offset, from 0 (-180°) to 1 (+180°). Note that 0 and 1 have the same result"
    saturation = "A value of 0 removes color from the image, making it black-and-white. A value greater than 1.0 increases saturation"
    fac = "The amount of influence the node exerts on the image"
    node_ot_bloom = "Replication of the legacy eevee bloom option, but can be used in cycles as well"
    prop_pt_bloom = "Old Eevee Bloom In Both Eevee And Cycles"
    blur_mix = "The optional Size input will be multiplied with the X and Y blur radius values. It also accepts a value image, to control the blur radius with a mask. The values should be mapped between (0 to 1) for an optimal effect"
    bloom_size = "Scale of the glow relative to the size of the image. 9 means the glow can cover the entire image, 8 means it can only cover half the image, 7 means it can only cover quarter of the image, and so on."
    bloom_mute_unmute_bool = "Toggle the bloom effect on or off"
    oe_bloom = "Replication of the legacy eevee bloom option"
    clamp_mix = "Clamps of each mix nodes in the oe_bloom node group"
    bm_clamp = "Blur Mix Clamp"
    km_clamp = "Knee Mix Clamp"
    cr_clamp = "Color Clamp"
    iy_clamp = "Intensity Clamp"

#initialize OE_Bloom node group
def oe_bloom_node_group(context, operator, group_name):
    scene = bpy.context.scene
    oe_bloom = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    #enable use nodes
    if scene.use_nodes == False:
        scene.use_nodes = True

    oe_bloom.color_tag = 'FILTER'
    oe_bloom.description = OE_Bloom_Descr.oe_bloom
    oe_bloom.default_group_node_width = 149

    #oe_bloom interface
    #Socket Image
    image_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Image, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket_1 = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Image, in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.description = OE_Bloom_Descr.image

    #Socket Quality
    quality_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Quality, in_out='INPUT', socket_type = 'NodeSocketFloat')
    quality_socket.default_value = 0.0
    quality_socket.min_value = 0.0
    quality_socket.max_value = 1.0
    quality_socket.subtype = 'FACTOR'
    quality_socket.attribute_domain = 'POINT'
    quality_socket.description = OE_Bloom_Descr.quality

    #Socket Threshold
    threshold_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Threshold, in_out='INPUT', socket_type = 'NodeSocketFloat')
    threshold_socket.default_value = 1.0
    threshold_socket.min_value = 0.0
    threshold_socket.max_value = 1000.0
    threshold_socket.subtype = 'NONE'
    threshold_socket.attribute_domain = 'POINT'
    threshold_socket.description = OE_Bloom_Descr.threshold

    #Socket Knee
    knee_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Knee, in_out='INPUT', socket_type = 'NodeSocketFloat')
    knee_socket.default_value = 0.0
    knee_socket.min_value = 0.0
    knee_socket.max_value = 1.0
    knee_socket.subtype = 'FACTOR'
    knee_socket.attribute_domain = 'POINT'
    knee_socket.description = OE_Bloom_Descr.knee

    #Socket Radius
    radius_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Radius, in_out='INPUT', socket_type = 'NodeSocketFloat')
    radius_socket.default_value = 0.0
    radius_socket.min_value = 0.0
    radius_socket.max_value = 2048.0
    radius_socket.subtype = 'NONE'
    radius_socket.attribute_domain = 'POINT'
    radius_socket.description = OE_Bloom_Descr.radius

    #Socket Color
    color_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Color, in_out='INPUT', socket_type = 'NodeSocketColor')
    color_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.description = OE_Bloom_Descr.color

    #Socket Intensity
    intensity_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Intensity, in_out='INPUT', socket_type = 'NodeSocketFloat')
    intensity_socket.default_value = 1.0
    intensity_socket.min_value = 0.0
    intensity_socket.max_value = 1.0
    intensity_socket.subtype = 'FACTOR'
    intensity_socket.attribute_domain = 'POINT'
    intensity_socket.description = OE_Bloom_Descr.intensity

    #Panel Clamp Mix
    clamp_mix_panel = oe_bloom.interface.new_panel(
        OE_Bloom_Names.Clamp_Mix,
        description=OE_Bloom_Descr.clamp_mix,
        default_closed=True
    )

    #Socket Clamp
    clamp_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat')
    clamp_socket.default_value = 1.0
    clamp_socket.min_value = 0.0
    clamp_socket.max_value = 2.0
    clamp_socket.subtype = 'FACTOR'
    clamp_socket.attribute_domain = 'POINT'
    clamp_socket.description = OE_Bloom_Descr.clamp

    #Socket BM Clamp
    bm_clamp_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.BM_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    bm_clamp_socket.default_value = 1.0
    bm_clamp_socket.min_value = 0.0
    bm_clamp_socket.max_value = 1.0
    bm_clamp_socket.subtype = 'FACTOR'
    bm_clamp_socket.attribute_domain = 'POINT'
    bm_clamp_socket.description = OE_Bloom_Descr.bm_clamp

    #Socket KM Clamp
    km_clamp_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.KM_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    km_clamp_socket.default_value = 0.0
    km_clamp_socket.min_value = 0.0
    km_clamp_socket.max_value = 1.0
    km_clamp_socket.subtype = 'FACTOR'
    km_clamp_socket.attribute_domain = 'POINT'
    km_clamp_socket.description = OE_Bloom_Descr.km_clamp

    #Socket CR Clamp
    cr_clamp_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.CR_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    cr_clamp_socket.default_value = 0.0
    cr_clamp_socket.min_value = 0.0
    cr_clamp_socket.max_value = 1.0
    cr_clamp_socket.subtype = 'FACTOR'
    cr_clamp_socket.attribute_domain = 'POINT'
    cr_clamp_socket.description = OE_Bloom_Descr.cr_clamp

    #Socket IY Clamp
    cr_clamp_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.IY_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    cr_clamp_socket.default_value = 0.0
    cr_clamp_socket.min_value = 0.0
    cr_clamp_socket.max_value = 1.0
    cr_clamp_socket.subtype = 'FACTOR'
    cr_clamp_socket.attribute_domain = 'POINT'
    cr_clamp_socket.description = OE_Bloom_Descr.iy_clamp

    #Panel Other
    other_panel = oe_bloom.interface.new_panel(
        OE_Bloom_Names.Other,
        description=OE_Bloom_Descr.other,
        default_closed=True
    )

    #Socket Hue
    hue_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Hue, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    hue_socket.default_value = 0.5
    hue_socket.min_value = 0.0
    hue_socket.max_value = 1.0
    hue_socket.subtype = 'FACTOR'
    hue_socket.attribute_domain = 'POINT'
    hue_socket.description = OE_Bloom_Descr.hue

    #Socket Saturation
    saturation_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Saturation, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    saturation_socket.default_value = 1.0
    saturation_socket.min_value = 0.0
    saturation_socket.max_value = 2.0
    saturation_socket.subtype = 'FACTOR'
    saturation_socket.attribute_domain = 'POINT'
    saturation_socket.description = OE_Bloom_Descr.saturation

    #Socket Fac
    fac_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Fac, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    fac_socket.default_value = 1.0
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = 'FACTOR'
    fac_socket.attribute_domain = 'POINT'
    fac_socket.description = OE_Bloom_Descr.fac

    #Socket Blur Mix
    blur_mix_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Blur_Mix, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    blur_mix_socket.default_value = 1.0
    blur_mix_socket.min_value = 0.0
    blur_mix_socket.max_value = 1.0
    blur_mix_socket.subtype = 'NONE'
    blur_mix_socket.attribute_domain = 'POINT'
    blur_mix_socket.description = OE_Bloom_Descr.blur_mix

    #Socket Bloom Size
    bloom_size_socket = oe_bloom.interface.new_socket(name = OE_Bloom_Names.Bloom_Size, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    bloom_size_socket.default_value = 9.0
    bloom_size_socket.min_value = 1.0
    bloom_size_socket.max_value = 9.0
    bloom_size_socket.subtype = 'NONE'
    bloom_size_socket.attribute_domain = 'POINT'
    bloom_size_socket.description = OE_Bloom_Descr.bloom_size

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
    group_input_00.outputs[10].hide = True
    group_input_00.outputs[11].hide = True
    group_input_00.outputs[12].hide = True
    group_input_00.outputs[13].hide = True
    group_input_00.outputs[14].hide = True
    group_input_00.outputs[15].hide = True
    group_input_00.outputs[16].hide = True

    #node Original Bloom High
    original_bloom_high = oe_bloom.nodes.new("CompositorNodeGlare")
    original_bloom_high.label = OE_Bloom_Names.Original_Bloom_High
    original_bloom_high.name = OE_Bloom_Names.Original_Bloom_High
    original_bloom_high.use_custom_color = True
    original_bloom_high.color = Color.DARK_PURPLE
    original_bloom_high.angle_offset = 0.0
    original_bloom_high.color_modulation = 0.25
    original_bloom_high.fade = 0.9
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
    knee_bloom_high = oe_bloom.nodes.new("CompositorNodeGlare")
    knee_bloom_high.label = OE_Bloom_Names.Knee_Bloom_High
    knee_bloom_high.name = OE_Bloom_Names.Knee_Bloom_High
    knee_bloom_high.use_custom_color = True
    knee_bloom_high.color = Color.DARK_PURPLE
    knee_bloom_high.angle_offset = 0.0
    knee_bloom_high.color_modulation = 0.25
    knee_bloom_high.fade = 0.9
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
    knee_mix.label = OE_Bloom_Names.Knee_Mix
    knee_mix.name = OE_Bloom_Names.Knee_Mix
    knee_mix.use_custom_color = True
    knee_mix.color = Color.BROWN
    knee_mix.blend_type = 'ADD'
    knee_mix.use_alpha = False
    knee_mix.use_clamp = False

    #node Group Input 05
    group_input_05 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_05.label = OE_Bloom_Names.Group_Input_05
    group_input_05.name = OE_Bloom_Names.Group_Input_05
    group_input_05.use_custom_color = True
    group_input_05.color = Color.DARK_GRAY
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
    group_input_03.label = OE_Bloom_Names.Group_Input_03
    group_input_03.name = OE_Bloom_Names.Group_Input_03
    group_input_03.use_custom_color = True
    group_input_03.color = Color.DARK_GRAY
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
    group_input_02.label = OE_Bloom_Names.Group_Input_02
    group_input_02.name = OE_Bloom_Names.Group_Input_02
    group_input_02.use_custom_color = True
    group_input_02.color = Color.DARK_GRAY
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
    bloom_high____low.label = OE_Bloom_Names.Bloom_High_Low
    bloom_high____low.name = OE_Bloom_Names.Bloom_High_Low
    bloom_high____low.use_custom_color = True
    
    # Combine two hex colors into a single hex color code
    bloom_high_low_color = hex_color_add("77535F", "3C3937")
    
    # Convert the combined hex color code to Linear RGB
    bloom_high_low_color = hexcode_to_rgb(bloom_high_low_color)

    bloom_high____low.color = bloom_high_low_color
    bloom_high____low.label_size = 32
    bloom_high____low.shrink = True

    #node Knee Bloom Low
    knee_bloom_low = oe_bloom.nodes.new("CompositorNodeGlare")
    knee_bloom_low.label = OE_Bloom_Names.Knee_Bloom_Low
    knee_bloom_low.name = OE_Bloom_Names.Knee_Bloom_Low
    knee_bloom_low.use_custom_color = True
    knee_bloom_low.color = Color.DARK_PURPLE
    knee_bloom_low.angle_offset = 0.0
    knee_bloom_low.color_modulation = 0.25
    knee_bloom_low.fade = 0.9
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
    kb_switch.label = OE_Bloom_Names.KB_Switch
    kb_switch.name = OE_Bloom_Names.KB_Switch
    kb_switch.use_custom_color = True
    kb_switch.color = Color.LIGHT_GRAY
    kb_switch.check = True

    #node OB Switch
    ob_switch = oe_bloom.nodes.new("CompositorNodeSwitch")
    ob_switch.label = OE_Bloom_Names.OB_Switch
    ob_switch.name = OE_Bloom_Names.OB_Switch
    ob_switch.use_custom_color = True
    ob_switch.color = Color.LIGHT_GRAY
    ob_switch.check = True

    #node Original Bloom Low
    original_bloom_low = oe_bloom.nodes.new("CompositorNodeGlare")
    original_bloom_low.label = OE_Bloom_Names.Original_Bloom_Low
    original_bloom_low.name = OE_Bloom_Names.Original_Bloom_Low
    original_bloom_low.use_custom_color = True
    original_bloom_low.color = Color.DARK_PURPLE
    original_bloom_low.angle_offset = 0.0
    original_bloom_low.color_modulation = 0.25
    original_bloom_low.fade = 0.9
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
    group_input_01.label = OE_Bloom_Names.Group_Input_01
    group_input_01.name = OE_Bloom_Names.Group_Input_01
    group_input_01.use_custom_color = True
    group_input_01.color = Color.DARK_GRAY
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
    reroute_00.name = OE_Bloom_Names.Reroute_00
    reroute_00.label = OE_Bloom_Names.KB_Switch
    reroute_00.socket_idname = "NodeSocketColor"
    #node Reroute_01
    reroute_01 = oe_bloom.nodes.new("NodeReroute")
    reroute_01.name = OE_Bloom_Names.Reroute_01
    reroute_01.label = OE_Bloom_Names.KB_Switch
    reroute_01.socket_idname = "NodeSocketColor"
    #node Clamp
    clamp = oe_bloom.nodes.new("CompositorNodeHueSat")
    clamp.label = OE_Bloom_Names.Clamp
    clamp.name = OE_Bloom_Names.Clamp
    clamp.use_custom_color = True
    clamp.color = Color.BROWN

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
    reroute_00.location = (-180.0, -369.0)
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

class NODE_OT_BLOOM(bpy.types.Operator):
    bl_label = OE_Bloom_Names.OE_Bloom
    bl_idname = "node.oe_bloom_operator"
    bl_description = OE_Bloom_Descr.node_ot_bloom

    def execute(shelf, context):
        # Get the compositor node tree
        node_tree = context.scene.node_tree
        nodes = node_tree.nodes
        links = node_tree.links

        # Check if nodes exist, otherwise create them
        render_layer_node = nodes.get(OE_Bloom_Names.Render_Layers) or nodes.new(type="CompositorNodeRLayers")
        render_layer_node.location = (-300, 0)

        composite_node = nodes.get(OE_Bloom_Names.Composite) or nodes.new(type="CompositorNodeComposite")
        composite_node.location = (300, 86)

        viewer_node = nodes.get(OE_Bloom_Names.Viewer) or nodes.new(type="CompositorNodeViewer")
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
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[1].default_value'
        )

        # Knee Bloom Switch
        oe_bloom_kbs_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.KB_Switch].driver_add('check').driver
        oe_bloom_kbs_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_kbs_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[1].default_value'
        )

        # Original Bloom High
        oe_bloom_obh_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Original_Bloom_High].driver_add('threshold').driver
        oe_bloom_obh_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obh_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[2].default_value'
        )

        # Original Bloom Low
        oe_bloom_obl_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Original_Bloom_Low].driver_add('threshold').driver
        oe_bloom_obl_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obl_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[2].default_value'
        )

        # Original Bloom High Size
        oe_bloom_obhs_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Original_Bloom_High].driver_add('size').driver
        oe_bloom_obhs_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obhs_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[16].default_value'
        )

        # Original Bloom Low Size
        oe_bloom_obls_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Original_Bloom_Low].driver_add('size').driver
        oe_bloom_obls_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obls_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[16].default_value'
        )

        # Radius X
        oe_bloom_rx_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Blur].driver_add('size_x').driver
        oe_bloom_rx_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_rx_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[4].default_value'
        )

        # Radius Y
        oe_bloom_ry_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Blur].driver_add('size_y').driver
        oe_bloom_ry_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_ry_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[4].default_value'
        )

        # Blur Mix Clamp
        oe_bloom_bxc_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Blur_Mix].driver_add('use_clamp').driver
        oe_bloom_bxc_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_bxc_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[8].default_value'
        )

        # Knee Mix Clamp
        oe_bloom_kxc_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Knee_Mix].driver_add('use_clamp').driver
        oe_bloom_kxc_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_kxc_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[9].default_value'
        )

        # Color Clamp
        oe_bloom_cc_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Color].driver_add('use_clamp').driver
        oe_bloom_cc_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_cc_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[10].default_value'
        )

        # Intensity Clamp
        oe_bloom_ic_driver = oe_bloom_node.node_tree.nodes[OE_Bloom_Names.Intensity].driver_add('use_clamp').driver
        oe_bloom_ic_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_ic_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[11].default_value'
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
        ensure_connection(render_layer_node, OE_Bloom_Names.Image, oe_bloom_node, OE_Bloom_Names.Image)
        ensure_connection(oe_bloom_node, OE_Bloom_Names.Image, composite_node, OE_Bloom_Names.Image)
        ensure_connection(oe_bloom_node, OE_Bloom_Names.Image, viewer_node, OE_Bloom_Names.Image)

        return {"FINISHED"}

class PROP_PT_BLOOM(bpy.types.Panel):
    bl_label = 'Bloom'
    bl_idname = 'PROP_PT_BLOOM'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_description = OE_Bloom_Descr.prop_pt_bloom
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
            oe_bloom_node = next(
                (
                    node for node in node_tree.nodes
                    if node.type == 'GROUP' and node.name == OE_Bloom_Names.OE_Bloom
                ),
                None
            )
            if oe_bloom_node:
                # Add Mute/Unmute property
                layout.prop(
                    scene,
                    "bloom_mute_unmute_bool",
                    text="Mute" if scene.bloom_mute_unmute_bool else "Unmute",
                    icon='CHECKBOX_HLT' if scene.bloom_mute_unmute_bool else 'CANCEL'
                )

                # Organize inputs into panels
                image_inputs = []
                clamp_mix_inputs = []
                other_inputs = []

                for input in oe_bloom_node.inputs:
                    # Skip the "Image" input
                    if input.name == OE_Bloom_Names.Image:
                        continue
                    elif input.name in [
                        OE_Bloom_Names.Quality, OE_Bloom_Names.Threshold,
                        OE_Bloom_Names.Knee, OE_Bloom_Names.Radius,
                        OE_Bloom_Names.Color, OE_Bloom_Names.Intensity,
                        OE_Bloom_Names.Clamp
                    ]:
                        image_inputs.append(input)
                    elif OE_Bloom_Names.Clamp in input.name:
                        clamp_mix_inputs.append(input)
                    else:
                        other_inputs.append(input)

                # Draw Image Panel
                if image_inputs:
                    # layout.label(text="Image", icon="IMAGE_DATA")
                    for input in image_inputs:
                        layout.prop(
                            input,
                            "default_value",
                            text=input.name
                        )

                # Clamp Panel (Collapsible)
                row = layout.row()
                row.prop(
                    scene,
                    "bloom_clamp_mix_bool",
                    icon="RESTRICT_RENDER_OFF",
                    emboss=False
                )
                if scene.bloom_clamp_mix_bool:
                    clamp_mix_box = layout.box()
                    for input in clamp_mix_inputs:
                        clamp_mix_box.prop(input, "default_value", text=input.name)
    
                # Other Panel (Collapsible)
                row = layout.row()
                row.prop(
                    scene,
                    "bloom_other_bool",
                    icon="MODIFIER",
                    emboss=False
                )
                if scene.bloom_other_bool:
                    other_box = layout.box()
                    for input in other_inputs:
                        other_box.prop(input, "default_value", text=input.name)
            else:
                # If the node group doesn't exist, show the operator to create it
                layout.operator(
                    "node.oe_bloom_operator",
                    text="Create OE_Bloom",
                    icon='NODE_MATERIAL'
                )

# Register and unregister
classes = [PROP_PT_BLOOM, NODE_OT_BLOOM]

prop_scene = bpy.types.Scene

def register():
    prop_scene.bloom_mute_unmute_bool = BoolProperty(
        name="Bloom Mute/Unmute",
        description=OE_Bloom_Descr.bloom_mute_unmute_bool,
        default=False,
        update=toggle_oe_bloom_mute  # Attach the callback function
    )
    prop_scene.bloom_clamp_mix_bool = bpy.props.BoolProperty(
        name=OE_Bloom_Names.Clamp_Mix, 
        description=OE_Bloom_Descr.clamp_mix,
        default=False
    )
    prop_scene.bloom_other_bool = bpy.props.BoolProperty(
        name=OE_Bloom_Names.Other,
        description=OE_Bloom_Descr.other,
        default=False
    )
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    del prop_scene.bloom_mute_unmute_bool
    del prop_scene.bloom_clamp_mix_bool
    del prop_scene.bloom_other_bool
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()