import bpy

class COMP_PT_MAINPANEL(bpy.types.Panel):
    bl_label = "test"
    bl_idname = "COMP_PT_MAINPANEL"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "T"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("node.bloom_operator", icon="IMAGE_RGB")

from typing import Tuple

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

COLORS_DICT = {
        "LIGHT_RED": hexcode_to_rgb("#94493E"),
        "DARK_RED": hexcode_to_rgb("#823A35"),
        "LIGHT_BLUE": hexcode_to_rgb("#646E66"),
        "DARK_BLUE": hexcode_to_rgb("#4C6160"),
        "LIGHT_PURPLE": hexcode_to_rgb("#846167"),
        "DARK_PURPLE": hexcode_to_rgb("#77535F"),
        "BROWN": hexcode_to_rgb("#866937"),
        "DARK_GRAY": hexcode_to_rgb("#3C3937"),
        "LIGHT_GRAY": hexcode_to_rgb("#59514B"),
    }

#initialize Bloom node group
def bloom_node_group(context, operator, group_name):

    #enable use nodes
    bpy.context.scene.use_nodes = True

    bloom = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    bloom.color_tag = 'FILTER'
    bloom.description = "Replication Of The Legacy Eevee Bloom Option"
    bloom.default_group_node_width = 160
        
    #bloom interface
    #Socket Image
    image_socket = bloom.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket_1 = bloom.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.description = "Standard color output"

    #Socket Color
    color_socket = bloom.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
    color_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.description = "Bloom Color"

    #Socket Quality
    quality_socket = bloom.interface.new_socket(name = "Quality", in_out='INPUT', socket_type = 'NodeSocketFloat')
    quality_socket.default_value = 0.0
    quality_socket.min_value = 0.0
    quality_socket.max_value = 1.0
    quality_socket.subtype = 'FACTOR'
    quality_socket.attribute_domain = 'POINT'
    quality_socket.description = "If not set to something other the High, then the glare effect will only be applied to a low resolution copy of the image. This can be helpful to save render times while only doing preview renders"

    #Socket Knee
    knee_socket = bloom.interface.new_socket(name = "Knee", in_out='INPUT', socket_type = 'NodeSocketFloat')
    knee_socket.default_value = 0.0
    knee_socket.min_value = 0.0
    knee_socket.max_value = 1.0
    knee_socket.subtype = 'FACTOR'
    knee_socket.attribute_domain = 'POINT'

    #Socket Threshold
    threshold_socket = bloom.interface.new_socket(name = "Threshold", in_out='INPUT', socket_type = 'NodeSocketFloat')
    threshold_socket.default_value = 1.0
    threshold_socket.min_value = 0.0
    threshold_socket.max_value = 1000.0
    threshold_socket.subtype = 'NONE'
    threshold_socket.attribute_domain = 'POINT'

    #Socket Added Radius
    added_radius_socket = bloom.interface.new_socket(name = "Added Radius", in_out='INPUT', socket_type = 'NodeSocketFloat')
    added_radius_socket.default_value = 0.0
    added_radius_socket.min_value = 0.0
    added_radius_socket.max_value = 2048
    added_radius_socket.subtype = 'NONE'
    added_radius_socket.attribute_domain = 'POINT'

    #Socket Blur Mix
    blur_mix_socket = bloom.interface.new_socket(name = "Blur Mix", in_out='INPUT', socket_type = 'NodeSocketFloat')
    blur_mix_socket.default_value = 1.0
    blur_mix_socket.min_value = 0.0
    blur_mix_socket.max_value = 1.0
    blur_mix_socket.subtype = 'NONE'
    blur_mix_socket.attribute_domain = 'POINT'

    #Socket Intensity
    intensity_socket = bloom.interface.new_socket(name = "Intensity", in_out='INPUT', socket_type = 'NodeSocketFloat')
    intensity_socket.default_value = 1.0
    intensity_socket.min_value = 0.0
    intensity_socket.max_value = 1.0
    intensity_socket.subtype = 'FACTOR'
    intensity_socket.attribute_domain = 'POINT'

    #Socket Bloom Size
    bloom_size_socket = bloom.interface.new_socket(name = "Bloom Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
    bloom_size_socket.default_value = 9.0
    bloom_size_socket.min_value = 1.0
    bloom_size_socket.max_value = 9.0
    bloom_size_socket.subtype = 'NONE'
    bloom_size_socket.attribute_domain = 'POINT'
    bloom_size_socket.description = "Scale of the glow relative to the size of the image. 9 means the glow can cover the entire image, 8 means it can only cover half the image, 7 means it can only cover quarter of the image, and so on."


    #initialize bloom nodes
    #node Group Output
    group_output = bloom.nodes.new("NodeGroupOutput")
    group_output.label = "Group Output"
    group_output.name = "Group Output"
    group_output.use_custom_color = True
    group_output.color = COLORS_DICT["DARK_GRAY"]
    group_output.is_active_output = True

    #node Group Input 00
    group_input_00 = bloom.nodes.new("NodeGroupInput")
    group_input_00.label = "Group Input 00"
    group_input_00.name = "Group Input 00"
    group_input_00.use_custom_color = True
    group_input_00.color = COLORS_DICT["DARK_GRAY"]
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
    original_bloom_high = bloom.nodes.new("CompositorNodeGlare")
    original_bloom_high.label = "Original Bloom High"
    original_bloom_high.name = "Original Bloom High"
    original_bloom_high.use_custom_color = True
    original_bloom_high.color = COLORS_DICT["DARK_PURPLE"]
    original_bloom_high.glare_type = 'BLOOM'
    original_bloom_high.mix = 1.0
    original_bloom_high.quality = 'HIGH'
    original_bloom_high.size = 9
    original_bloom_high.threshold = 1.0

    #node Color
    color = bloom.nodes.new("CompositorNodeMixRGB")
    color.label = "Color"
    color.name = "Color"
    color.use_custom_color = True
    color.color = COLORS_DICT["BROWN"]
    color.blend_type = 'COLOR'
    color.use_alpha = False
    color.use_clamp = False
    color.inputs[0].hide = True
    #Fac
    color.inputs[0].default_value = 1.0

    #node Blur
    blur = bloom.nodes.new("CompositorNodeBlur")
    blur.label = "Blur"
    blur.name = "Blur"
    blur.use_custom_color = True
    blur.color = COLORS_DICT["DARK_PURPLE"]
    blur.aspect_correction = 'NONE'
    blur.filter_type = 'FAST_GAUSS'
    blur.size_x = 0
    blur.size_y = 0
    blur.use_extended_bounds = False
    blur.use_relative = False

    #node Blur Mix
    blur_mix = bloom.nodes.new("CompositorNodeMixRGB")
    blur_mix.label = "Blur Mix"
    blur_mix.name = "Blur Mix"
    blur_mix.use_custom_color = True
    blur_mix.color = COLORS_DICT["BROWN"]
    blur_mix.blend_type = 'SCREEN'
    blur_mix.use_alpha = False
    blur_mix.use_clamp = True
    blur_mix.inputs[0].hide = True
    #Fac
    blur_mix.inputs[0].default_value = 1.0

    #node Intensity
    intensity = bloom.nodes.new("CompositorNodeMixRGB")
    intensity.label = "Intensity"
    intensity.name = "Intensity"
    intensity.use_custom_color = True
    intensity.color = COLORS_DICT["BROWN"]
    intensity.blend_type = 'ADD'
    intensity.use_alpha = False
    intensity.use_clamp = False

    #node Knee Bloom High
    knee_bloom_high = bloom.nodes.new("CompositorNodeGlare")
    knee_bloom_high.label = "Knee Bloom High"
    knee_bloom_high.name = "Knee Bloom High"
    knee_bloom_high.use_custom_color = True
    knee_bloom_high.color = COLORS_DICT["DARK_PURPLE"]
    knee_bloom_high.angle_offset = 0.0
    knee_bloom_high.color_modulation = 0.25
    knee_bloom_high.fade = 0.8999999761581421
    knee_bloom_high.glare_type = 'BLOOM'
    knee_bloom_high.mix = 1.0
    knee_bloom_high.quality = 'HIGH'
    knee_bloom_high.size = 9
    knee_bloom_high.threshold = 0.0

    #node Knee Mix
    knee_mix = bloom.nodes.new("CompositorNodeMixRGB")
    knee_mix.label = "Knee Mix"
    knee_mix.name = "Knee Mix"
    knee_mix.use_custom_color = True
    knee_mix.color = COLORS_DICT["BROWN"]
    knee_mix.blend_type = 'ADD'
    knee_mix.use_alpha = False
    knee_mix.use_clamp = False

    #node Group Input 01
    group_input_01 = bloom.nodes.new("NodeGroupInput")
    group_input_01.label = "Group Input 01"
    group_input_01.name = "Group Input 01"
    group_input_01.use_custom_color = True
    group_input_01.color = COLORS_DICT["DARK_GRAY"]
    group_input_01.outputs[1].hide = True
    group_input_01.outputs[2].hide = True
    group_input_01.outputs[3].hide = True
    group_input_01.outputs[4].hide = True
    group_input_01.outputs[5].hide = True
    group_input_01.outputs[6].hide = True
    group_input_01.outputs[8].hide = True
    group_input_01.outputs[9].hide = True

    #node Group Input 02
    group_input_02 = bloom.nodes.new("NodeGroupInput")
    group_input_02.label = "Group Input 02"
    group_input_02.name = "Group Input 02"
    group_input_02.use_custom_color = True
    group_input_02.color = COLORS_DICT["DARK_GRAY"]
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
    group_input_03 = bloom.nodes.new("NodeGroupInput")
    group_input_03.label = "Group Input 03"
    group_input_03.name = "Group Input 03"
    group_input_03.use_custom_color = True
    group_input_03.color = COLORS_DICT["DARK_GRAY"]
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
    bloom_high____low = bloom.nodes.new("NodeFrame")
    bloom_high____low.label = "Bloom High && Low"
    bloom_high____low.name = "Bloom High && Low"
    bloom_high____low.use_custom_color = True
    bloom_high____low.color = (0.27887165546417236, 0.4313916563987732, 0.31700167059898376)
    bloom_high____low.label_size = 32
    bloom_high____low.shrink = True

    #node Knee Bloom Low
    knee_bloom_low = bloom.nodes.new("CompositorNodeGlare")
    knee_bloom_low.label = "Knee Bloom Low"
    knee_bloom_low.name = "Knee Bloom Low"
    knee_bloom_low.use_custom_color = True
    knee_bloom_low.color = COLORS_DICT["DARK_PURPLE"]
    knee_bloom_low.glare_type = 'BLOOM'
    knee_bloom_low.mix = 1.0
    knee_bloom_low.quality = 'LOW'
    knee_bloom_low.size = 9
    knee_bloom_low.threshold = 0.0

    #node KB Switch
    kb_switch = bloom.nodes.new("CompositorNodeSwitch")
    kb_switch.label = "KB Switch"
    kb_switch.name = "KB Switch"
    kb_switch.use_custom_color = True
    kb_switch.color = COLORS_DICT["LIGHT_GRAY"]
    kb_switch.check = False

    #node OB Switch
    ob_switch = bloom.nodes.new("CompositorNodeSwitch")
    ob_switch.label = "OB Switch"
    ob_switch.name = "OB Switch"
    ob_switch.use_custom_color = True
    ob_switch.color = COLORS_DICT["LIGHT_GRAY"]
    ob_switch.check = False

    #node Original Bloom Low
    original_bloom_low = bloom.nodes.new("CompositorNodeGlare")
    original_bloom_low.label = "Original Bloom Low"
    original_bloom_low.name = "Original Bloom Low"
    original_bloom_low.use_custom_color = True
    original_bloom_low.color = COLORS_DICT["DARK_PURPLE"]
    original_bloom_low.glare_type = 'BLOOM'
    original_bloom_low.mix = 1.0
    original_bloom_low.quality = 'LOW'
    original_bloom_low.threshold = 1.0
    original_bloom_low.size = 9

    #node Group Input 04
    group_input_04 = bloom.nodes.new("NodeGroupInput")
    group_input_04.label = "Group Input 04"
    group_input_04.name = "Group Input 04"
    group_input_04.use_custom_color = True
    group_input_04.color = COLORS_DICT["DARK_GRAY"]
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
    reroute_00 = bloom.nodes.new("NodeReroute")
    reroute_00.name = "Reroute_00"
    reroute_00.socket_idname = "NodeSocketColor"

    #node Reroute_01
    reroute_01 = bloom.nodes.new("NodeReroute")
    reroute_01.name = "Reroute_01"
    reroute_01.socket_idname = "NodeSocketColor"

    #node Clamp
    clamp = bloom.nodes.new("CompositorNodeCurveRGB")
    clamp.label = "Clamp"
    clamp.name = "Clamp"
    clamp.use_custom_color = True
    clamp.color = COLORS_DICT["BROWN"]

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
    original_bloom_high.parent = bloom_high____low
    knee_bloom_high.parent = bloom_high____low
    knee_bloom_low.parent = bloom_high____low
    kb_switch.parent = bloom_high____low
    ob_switch.parent = bloom_high____low
    original_bloom_low.parent = bloom_high____low

    #Set locations
    group_output.location = (820.0, 120.0)
    group_input_00.location = (-1040.0, -300.0)
    original_bloom_high.location = (53.0, -48.0)
    color.location = (220.0, -40.0)
    blur.location = (-320.0, -40.0)
    blur_mix.location = (-140.0, -40.0)
    intensity.location = (640.0, 120.0)
    knee_bloom_high.location = (53.0, -488.0)
    knee_mix.location = (40.0, -40.0)
    group_input_01.location = (640.0, 220.0)
    group_input_02.location = (220.0, -200.0)
    group_input_03.location = (40.0, -220.0)
    bloom_high____low.location = (-833.0, -52.0)
    knee_bloom_low.location = (53.0, -268.0)
    kb_switch.location = (273.0, -328.0)
    ob_switch.location = (273.0, 112.0)
    original_bloom_low.location = (53.0, 172.0)
    group_input_04.location = (-320.0, -260.0)
    reroute_00.location = (-180.0, -340.0)
    reroute_01.location = (0.0, -220.0)
    clamp.location = (400.0, -40.0)

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
    group_input_01.width, group_input_01.height = 140.0, 100.0
    group_input_02.width, group_input_02.height = 140.0, 100.0
    group_input_03.width, group_input_03.height = 140.0, 100.0
    bloom_high____low.width, bloom_high____low.height = 420.0, 944.0
    knee_bloom_low.width, knee_bloom_low.height = 153.29302978515625, 100.0
    kb_switch.width, kb_switch.height = 140.0, 100.0
    ob_switch.width, ob_switch.height = 140.0, 100.0
    original_bloom_low.width, original_bloom_low.height = 154.0098876953125, 100.0
    group_input_04.width, group_input_04.height = 150.76458740234375, 100.0
    reroute_00.width, reroute_00.height = 16.0, 100.0
    reroute_01.width, reroute_01.height = 16.0, 100.0
    clamp.width, clamp.height = 200.0, 100.0

    #initialize bloom links
    #ob_switch.Image -> blur_mix.Image
    bloom.links.new(ob_switch.outputs[0], blur_mix.inputs[2])

    #blur_mix.Image -> knee_mix.Image
    bloom.links.new(blur_mix.outputs[0], knee_mix.inputs[1])

    #blur.Image -> blur_mix.Image
    bloom.links.new(blur.outputs[0], blur_mix.inputs[1])

    #knee_mix.Image -> color.Image
    bloom.links.new(knee_mix.outputs[0], color.inputs[1])

    #ob_switch.Image -> blur.Image
    bloom.links.new(ob_switch.outputs[0], blur.inputs[0])

    #group_input_00.Image -> original_bloom_high.Image
    bloom.links.new(group_input_00.outputs[0], original_bloom_high.inputs[0])

    #group_input_00.Image -> knee_bloom_high.Image
    bloom.links.new(group_input_00.outputs[0], knee_bloom_high.inputs[0])

    #intensity.Image -> group_output.Image
    bloom.links.new(intensity.outputs[0], group_output.inputs[0])

    #group_input_01.Image -> intensity.Image
    bloom.links.new(group_input_01.outputs[0], intensity.inputs[1])

    #group_input_01.Intensity -> intensity.Fac
    bloom.links.new(group_input_01.outputs[7], intensity.inputs[0])

    #group_input_02.Color -> color.Image
    bloom.links.new(group_input_02.outputs[1], color.inputs[2])

    #group_input_03.Knee -> knee_mix.Fac
    bloom.links.new(group_input_03.outputs[3], knee_mix.inputs[0])

    #group_input_00.Image -> knee_bloom_low.Image
    bloom.links.new(group_input_00.outputs[0], knee_bloom_low.inputs[0])
    
    #knee_bloom_high.Image -> kb_switch.On
    bloom.links.new(knee_bloom_high.outputs[0], kb_switch.inputs[1])

    #knee_bloom_low.Image -> kb_switch.Off
    bloom.links.new(knee_bloom_low.outputs[0], kb_switch.inputs[0])

    #original_bloom_high.Image -> ob_switch.On
    bloom.links.new(original_bloom_high.outputs[0], ob_switch.inputs[1])

    #original_bloom_low.Image -> ob_switch.Off
    bloom.links.new(original_bloom_low.outputs[0], ob_switch.inputs[0])

    #group_input_04.Blur Mix -> blur.Size
    bloom.links.new(group_input_04.outputs[6], blur.inputs[1])

    #kb_switch.Image -> reroute_00.Input
    bloom.links.new(kb_switch.outputs[0], reroute_00.inputs[0])

    #group_input_00.Image -> original_bloom_low.Image
    bloom.links.new(group_input_00.outputs[0], original_bloom_low.inputs[0])

    #reroute_00.Output -> reroute_01.Input
    bloom.links.new(reroute_00.outputs[0], reroute_01.inputs[0])

    #reroute_01.Output -> knee_mix.Image
    bloom.links.new(reroute_01.outputs[0], knee_mix.inputs[2])

    #clamp.Image -> intensity.Image
    bloom.links.new(clamp.outputs[0], intensity.inputs[2])

    #color.Image -> clamp.Image
    bloom.links.new(color.outputs[0], clamp.inputs[1])

    return bloom


class NODE_OT_BLOOM(bpy.types.Operator):
    bl_label = "Bloom"
    bl_idname = "node.bloom_operator"

    def execute(shelf, context):

        custom_bloom_node_name = "Bloom"
        bloom_group = bloom_node_group(shelf, context, custom_bloom_node_name)
        bloom_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        bloom_node.node_tree = bpy.data.node_groups[bloom_group.name]
        bloom_node.use_custom_color = True
        bloom_node.color = COLORS_DICT["DARK_PURPLE"]
        bloom_node.select = False

        """
        * Adding drivers to nodes is possible by Victor Stepanov
        * (https://www.skool.com/cgpython/how-to-add-drivers-to-node-group-sockets-using-python?p=0be0f439)
        * His youtube channel (https://www.youtube.com/@CGPython)
        """
        bloom_tree = bpy.context.scene.node_tree

        def add_var(socket, data_path, name="default_value", id_type="SCENE", id=bpy.context.scene):
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

        # Original Bloom Switch
        bloom_obs_driver = bloom_tree.nodes['Group'].node_tree.nodes['OB Switch'].driver_add('check').driver
        bloom_obs_driver.type = "AVERAGE"
        add_var(
            bloom_obs_driver,
            'node_tree.nodes["Group"].inputs[2].default_value'
        )

        # Knee Bloom Switch
        bloom_kbs_driver = bloom_tree.nodes['Group'].node_tree.nodes['KB Switch'].driver_add('check').driver
        bloom_kbs_driver.type = "AVERAGE"
        add_var(
            bloom_kbs_driver,
            'node_tree.nodes["Group"].inputs[2].default_value'
        )

        # Original Bloom High
        bloom_obh_driver = bloom_tree.nodes['Group'].node_tree.nodes['Original Bloom High'].driver_add('threshold').driver
        bloom_obh_driver.type = "AVERAGE"
        add_var(
            bloom_obh_driver,
            'node_tree.nodes["Group"].inputs[4].default_value'
        )

        # Original Bloom Low
        bloom_obl_driver = bloom_tree.nodes['Group'].node_tree.nodes['Original Bloom Low'].driver_add('threshold').driver
        bloom_obl_driver.type = "AVERAGE"
        add_var(
            bloom_obl_driver,
            'node_tree.nodes["Group"].inputs[4].default_value'
        )

        # Original Bloom High Size
        bloom_obhs_driver = bloom_tree.nodes['Group'].node_tree.nodes['Original Bloom High'].driver_add('size').driver
        bloom_obhs_driver.type = "AVERAGE"
        add_var(
            bloom_obhs_driver,
            'node_tree.nodes["Group"].inputs[8].default_value'
        )

        # Original Bloom Low Size
        bloom_obls_driver = bloom_tree.nodes['Group'].node_tree.nodes['Original Bloom Low'].driver_add('size').driver
        bloom_obls_driver.type = "AVERAGE"
        add_var(
            bloom_obls_driver,
            'node_tree.nodes["Group"].inputs[8].default_value'
        )

        # Added Radius X
        bloom_arx_driver = bloom_tree.nodes['Group'].node_tree.nodes['Blur'].driver_add('size_x').driver
        bloom_arx_driver.type = "AVERAGE"
        add_var(
            bloom_arx_driver,
            'node_tree.nodes["Group"].inputs[5].default_value'
        )

        # Added Radius Y
        bloom_ary_driver = bloom_tree.nodes['Group'].node_tree.nodes['Blur'].driver_add('size_y').driver
        bloom_ary_driver.type = "AVERAGE"
        add_var(
            bloom_ary_driver,
            'node_tree.nodes["Group"].inputs[5].default_value'
        )


        return {"FINISHED"}
    
# Register and unregister list variable
classes = [COMP_PT_MAINPANEL, NODE_OT_BLOOM]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()