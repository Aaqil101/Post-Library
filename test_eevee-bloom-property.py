import bpy
import sys
from pathlib import Path
from bpy.props import BoolProperty, EnumProperty

# Determine script path
try:
    script_path = (
        bpy.context.space_data.text.filepath
        if bpy.context.space_data and bpy.context.space_data.type == "TEXT_EDITOR"
        else __file__
    )
except NameError:
    raise RuntimeError("Unable to determine script path. Are you running this in Blender?")

if not script_path:
    raise RuntimeError("The script must be saved to disk before running!")

# Resolve directories
script_dir = Path(script_path).resolve().parent
path_to_helpers_folder = script_dir / "helpers"
path_to_core_folder = script_dir / "core"

"""
TODO: When it's time to relese the addon, remove the {# Determine script path} and enable this one
try:
    # Determine script path
    script_path = Path(__file__).resolve()
except NameError:
    raise RuntimeError("The script must be saved to disk before running!")

# Resolve directories
script_dir = script_path.parent
path_to_helpers_folder = script_dir / "helpers"
path_to_core_folder = script_dir / "core"
"""

# List of paths
paths = [
    script_dir, path_to_helpers_folder
]


# Add directories to sys.path
for path in paths:
    if path.exists():
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.append(path_str)
            print(f"Added {path_str} to sys.path")
        else:
            print(f"{path_str} already in sys.path")
    else:
        print(f"Warning: {path} does not exist.")

from helpers import (
    # For adding drivers to sockets
    NodeDriverManager,

    # Color references
    Color,

    # Names and descriptions
    CompositorNodeNames,
    Names,
    Descriptions,
    SocketNames,

    # Functions
    ensure_connection,
    is_compositor_enabled,
    poll_view_3d,
    update_real_time_compositing,
    toggle_oldeevee_bloom
)
from core import (
    # Import all classes used by the Filter Node Manager
    FilterNodeManager,
    GlareSettings,
    GlareType,
    GlareQuality,
    BlurSettings,
    BlurFilterType,

    # Import all classes used by the Color Node Manager
    ColorNodeManager,
    MixColorSettings,
    BlendType,

    # Import all classes used by the Layout Node Manager
    LayoutNodeManager,
    FrameSettings,

    # Import UtilitiesNodeManager
    UtilitiesNodeManager,

    # Import all classes used by the Input Node Manager
    InputNodeManager,
    GroupInputSettings,

    # Import all classes used by the Output Node Manager
    OutputNodeManager,
    GroupOutputSettings,
)

#initialize OldEevee_Bloom node group
def oldeevee_bloom_node_group(context, operator, group_name):
    oldeevee_bloom = bpy.data.node_groups.new(group_name, CompositorNodeNames.TREE)

    oldeevee_bloom.color_tag = 'FILTER'
    oldeevee_bloom.description = Descriptions.oldeevee_bloom
    oldeevee_bloom.default_group_node_width = 174

    #oldeevee_bloom interface
    #Socket Image
    image_socket = oldeevee_bloom.interface.new_socket(name = Names.Image, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket_1 = oldeevee_bloom.interface.new_socket(name = Names.Image, in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.description = Descriptions.image

    #Socket Quality
    quality_socket = oldeevee_bloom.interface.new_socket(name = Names.Quality, in_out='INPUT', socket_type = 'NodeSocketFloat')
    quality_socket.default_value = 0.0
    quality_socket.min_value = 0.0
    quality_socket.max_value = 1.0
    quality_socket.subtype = 'FACTOR'
    quality_socket.attribute_domain = 'POINT'
    quality_socket.description = Descriptions.quality

    #Socket Threshold
    threshold_socket = oldeevee_bloom.interface.new_socket(name = Names.Threshold, in_out='INPUT', socket_type = 'NodeSocketFloat')
    threshold_socket.default_value = 1.0
    threshold_socket.min_value = 0.0
    threshold_socket.max_value = 1000.0
    threshold_socket.subtype = 'NONE'
    threshold_socket.attribute_domain = 'POINT'
    threshold_socket.description = Descriptions.threshold

    #Socket Knee
    knee_socket = oldeevee_bloom.interface.new_socket(name = Names.Knee, in_out='INPUT', socket_type = 'NodeSocketFloat')
    knee_socket.default_value = 0.0
    knee_socket.min_value = 0.0
    knee_socket.max_value = 1.0
    knee_socket.subtype = 'FACTOR'
    knee_socket.attribute_domain = 'POINT'
    knee_socket.description = Descriptions.knee

    #Socket Radius
    radius_socket = oldeevee_bloom.interface.new_socket(name = Names.Radius, in_out='INPUT', socket_type = 'NodeSocketFloat')
    radius_socket.default_value = 0.0
    radius_socket.min_value = 0.0
    radius_socket.max_value = 2048.0
    radius_socket.subtype = 'NONE'
    radius_socket.attribute_domain = 'POINT'
    radius_socket.description = Descriptions.radius

    #Socket Color
    color_socket = oldeevee_bloom.interface.new_socket(name = Names.Color, in_out='INPUT', socket_type = 'NodeSocketColor')
    color_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.description = Descriptions.color

    #Socket Intensity
    intensity_socket = oldeevee_bloom.interface.new_socket(name = Names.Intensity, in_out='INPUT', socket_type = 'NodeSocketFloat')
    intensity_socket.default_value = 1.0
    intensity_socket.min_value = 0.0
    intensity_socket.max_value = 1.0
    intensity_socket.subtype = 'FACTOR'
    intensity_socket.attribute_domain = 'POINT'
    intensity_socket.description = Descriptions.intensity

    #Socket Clamp
    clamp_socket = oldeevee_bloom.interface.new_socket(name = Names.Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat')
    clamp_socket.default_value = 1.0
    clamp_socket.min_value = 0.0
    clamp_socket.max_value = 2.0
    clamp_socket.subtype = 'FACTOR'
    clamp_socket.attribute_domain = 'POINT'
    clamp_socket.description = Descriptions.clamp

    #Panel Clamp Mix
    clamp_mix_panel = oldeevee_bloom.interface.new_panel(Names.Clamp_Mix, default_closed=True)
    clamp_mix_panel.description = Descriptions.clamp_mix

    #Socket BM Clamp
    bm_clamp_socket = oldeevee_bloom.interface.new_socket(name = Names.BM_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    bm_clamp_socket.default_value = 1.0
    bm_clamp_socket.min_value = 0.0
    bm_clamp_socket.max_value = 1.0
    bm_clamp_socket.subtype = 'FACTOR'
    bm_clamp_socket.attribute_domain = 'POINT'
    bm_clamp_socket.description = Descriptions.bm_clamp

    #Socket KM Clamp
    km_clamp_socket = oldeevee_bloom.interface.new_socket(name = Names.KM_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    km_clamp_socket.default_value = 0.0
    km_clamp_socket.min_value = 0.0
    km_clamp_socket.max_value = 1.0
    km_clamp_socket.subtype = 'FACTOR'
    km_clamp_socket.attribute_domain = 'POINT'
    km_clamp_socket.description = Descriptions.km_clamp

    #Socket CR Clamp
    cr_clamp_socket = oldeevee_bloom.interface.new_socket(name = Names.CR_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    cr_clamp_socket.default_value = 0.0
    cr_clamp_socket.min_value = 0.0
    cr_clamp_socket.max_value = 1.0
    cr_clamp_socket.subtype = 'FACTOR'
    cr_clamp_socket.attribute_domain = 'POINT'
    cr_clamp_socket.description = Descriptions.cr_clamp

    #Socket IY Clamp
    iy_clamp_socket = oldeevee_bloom.interface.new_socket(name = Names.IY_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    iy_clamp_socket.default_value = 0.0
    iy_clamp_socket.min_value = 0.0
    iy_clamp_socket.max_value = 1.0
    iy_clamp_socket.subtype = 'FACTOR'
    iy_clamp_socket.attribute_domain = 'POINT'
    iy_clamp_socket.description = Descriptions.iy_clamp

    #Panel Other
    other_panel = oldeevee_bloom.interface.new_panel(Names.Other, default_closed=True)
    other_panel.description = Descriptions.other

    #Socket Hue
    hue_socket = oldeevee_bloom.interface.new_socket(name = Names.Hue, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    hue_socket.default_value = 0.5
    hue_socket.min_value = 0.0
    hue_socket.max_value = 1.0
    hue_socket.subtype = 'FACTOR'
    hue_socket.attribute_domain = 'POINT'
    hue_socket.description = Descriptions.hue

    #Socket Saturation
    saturation_socket = oldeevee_bloom.interface.new_socket(name = Names.Saturation, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    saturation_socket.default_value = 1.0
    saturation_socket.min_value = 0.0
    saturation_socket.max_value = 2.0
    saturation_socket.subtype = 'FACTOR'
    saturation_socket.attribute_domain = 'POINT'
    saturation_socket.description = Descriptions.saturation

    #Socket Fac
    fac_socket = oldeevee_bloom.interface.new_socket(name = Names.Fac, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    fac_socket.default_value = 1.0
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = 'FACTOR'
    fac_socket.attribute_domain = 'POINT'
    fac_socket.description = Descriptions.fac

    #Socket Blur Mix
    blur_mix_socket = oldeevee_bloom.interface.new_socket(name = Names.Blur_Mix, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    blur_mix_socket.default_value = 1.0
    blur_mix_socket.min_value = 0.0
    blur_mix_socket.max_value = 1.0
    blur_mix_socket.subtype = 'NONE'
    blur_mix_socket.attribute_domain = 'POINT'
    blur_mix_socket.description = Descriptions.blur_mix

    #Socket Bloom Size
    bloom_size_socket = oldeevee_bloom.interface.new_socket(name = Names.Bloom_Size, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    bloom_size_socket.default_value = 9.0
    bloom_size_socket.min_value = 1.0
    bloom_size_socket.max_value = 9.0
    bloom_size_socket.subtype = 'NONE'
    bloom_size_socket.attribute_domain = 'POINT'
    bloom_size_socket.description = Descriptions.bloom_size

    # Initialize oldeevee_bloom nodes
    # Initialize node managers with the oldeevee_bloom node group and custom settings
    FNM = FilterNodeManager(node_group=oldeevee_bloom, use_custom_color=True)
    CNM = ColorNodeManager(node_group=oldeevee_bloom, use_custom_color=True)
    LNM = LayoutNodeManager(node_group=oldeevee_bloom, node_color=["77535F", "3C3937"], use_custom_color=True)
    UNM = UtilitiesNodeManager(node_group=oldeevee_bloom, use_custom_color=True)
    INM = InputNodeManager(node_group=oldeevee_bloom, use_custom_color=True)
    ONM = OutputNodeManager(node_group=oldeevee_bloom, use_custom_color=True)

    #node Group Output
    group_output = ONM.create_group_output_node(
        group_output_name=Names.Group_Output,
        group_output_label=Names.Group_Output,
        settings=GroupOutputSettings(
            outputs_to_hide=[1],
            is_active_output=True
        )
    )

    #node Original Bloom High
    original_bloom_high = FNM.create_glare_node(
        glare_name=Names.Original_Bloom_High,
        glare_label=Names.Original_Bloom_High,
        settings=GlareSettings(
            glare_type=GlareType.BLOOM,
            quality=GlareQuality.HIGH,
            mix=1.0,
            threshold=1.0,
            size=9
        )
    )

    #node Original Bloom Low
    original_bloom_low = FNM.create_glare_node(
        glare_name=Names.Original_Bloom_Low,
        glare_label=Names.Original_Bloom_Low,
        settings=GlareSettings(
            glare_type=GlareType.BLOOM,
            quality=GlareQuality.LOW,
            mix=1.0,
            threshold=1.0,
            size=9
        )
    )

    #node Knee Bloom High
    knee_bloom_high = FNM.create_glare_node(
        glare_name=Names.Knee_Bloom_High,
        glare_label=Names.Knee_Bloom_High,
        settings=GlareSettings(
            glare_type=GlareType.BLOOM,
            quality=GlareQuality.HIGH,
            mix=1.0,
            threshold=0.0,
            size=9
        )
    )
    
    #node Knee Bloom Low
    knee_bloom_low = FNM.create_glare_node(
        glare_name=Names.Knee_Bloom_Low,
        glare_label=Names.Knee_Bloom_Low,
        settings=GlareSettings(
            glare_type=GlareType.BLOOM,
            quality=GlareQuality.LOW,
            mix=1.0,
            threshold=0.0,
            size=9
        )
    )

    #node Blur
    blur = FNM.create_blur_node(
        blur_name=Names.Blur,
        blur_label=Names.Blur,
        settings=BlurSettings(filter_type=BlurFilterType.FAST_GAUSS)
    )


    #node Color
    color = CNM.create_mixcolor_node(
        mixcolor_name=Names.Color,
        mixcolor_label=Names.Color,
        settings=MixColorSettings(
            blend_type=BlendType.COLOR,
            fac_default_value=1.0,
            hide_fac=True
        )
    )

    #node Blur Mix
    blur_mix = CNM.create_mixcolor_node(
        mixcolor_name=Names.Blur_Mix,
        mixcolor_label=Names.Blur_Mix,
        settings=MixColorSettings(
            blend_type=BlendType.SCREEN,
            use_clamp=True,
            fac_default_value=1.0,
            hide_fac=True
        )
    )

    #node Intensity
    intensity = CNM.create_mixcolor_node(
        mixcolor_name=Names.Intensity,
        mixcolor_label=Names.Intensity,
        settings=MixColorSettings(blend_type=BlendType.ADD)
    )

    #node Knee Mix
    knee_mix = CNM.create_mixcolor_node(
        mixcolor_name=Names.Knee_Mix,
        mixcolor_label=Names.Knee_Mix,
        settings=MixColorSettings(blend_type=BlendType.ADD)
    )

    #node Clamp
    clamp = CNM.create_huesat_node(huesat_name=Names.Clamp, huesat_label=Names.Clamp)


    #node Bloom High && Low
    bloom_high____low = LNM.create_frame_node(
        frame_name=Names.Bloom_High_Low,
        frame_label=Names.Bloom_High_Low,
        settings=FrameSettings(
            label_size=32,
            shrink=True
        )
    )

    #node Reroute_00
    reroute_00 = LNM.create_reroute_node(reroute_name=Names.Reroute_00, reroute_label=Names.KB_Switch)

    #node Reroute_01
    reroute_01 = LNM.create_reroute_node(reroute_name=Names.Reroute_01, reroute_label=Names.KB_Switch)

    #node KB Switch
    kb_switch = UNM.create_switch_node(switch_name=Names.KB_Switch, switch_label=Names.KB_Switch)

    #node OB Switch
    ob_switch = UNM.create_switch_node(switch_name=Names.OB_Switch, switch_label=Names.OB_Switch)


    #node Group Input 00
    group_input_00 = INM.create_group_input_node(
        group_input_name=Names.Group_Input_00,
        group_input_label=Names.Group_Input_00,
        settings=GroupInputSettings(
            outputs_to_hide=list(range(1, 18)) # Hide outputs 1 to 17
        )
    )

    #node Group Input 01
    group_input_01 = INM.create_group_input_node(
        group_input_name=Names.Group_Input_01,
        group_input_label=Names.Group_Input_01,
        settings=GroupInputSettings(
            outputs_to_hide=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17]  # Outputs to hide
        )
    )

    #node Group Input 02
    group_input_02 = INM.create_group_input_node(
        group_input_name=Names.Group_Input_02,
        group_input_label=Names.Group_Input_02,
        settings=GroupInputSettings(
            outputs_to_hide=[0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  # Outputs to hide
        )
    )

    #node Group Input 03
    group_input_03 = INM.create_group_input_node(
        group_input_name=Names.Group_Input_03,
        group_input_label=Names.Group_Input_03,
        settings=GroupInputSettings(
            outputs_to_hide=[0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  # Outputs to hide
        )
    )

    #node Group Input 04
    group_input_04 = INM.create_group_input_node(
        group_input_name=Names.Group_Input_04,
        group_input_label=Names.Group_Input_04,
        settings=GroupInputSettings(
            outputs_to_hide=[0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 15, 16, 17]  # Outputs to hide
        )
    )

    #node Group Input 05
    group_input_05 = INM.create_group_input_node(
        group_input_name=Names.Group_Input_05,
        group_input_label=Names.Group_Input_05,
        settings=GroupInputSettings(
            outputs_to_hide=[1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  # Outputs to hide
        )
    )

    #Set parents
    original_bloom_high.parent = bloom_high____low
    knee_bloom_high.parent = bloom_high____low
    knee_bloom_low.parent = bloom_high____low
    kb_switch.parent = bloom_high____low
    ob_switch.parent = bloom_high____low
    original_bloom_low.parent = bloom_high____low

    #Set locations
    group_output.location = (800.0, 120.0)
    original_bloom_high.location = (53.0, -48.0)
    color.location = (220.0, -40.0)
    blur.location = (-320.0, -40.0)
    blur_mix.location = (-140.0, -40.0)
    intensity.location = (620.0, 120.0)
    knee_bloom_high.location = (53.0, -488.0)
    knee_mix.location = (40.0, -40.0)
    bloom_high____low.location = (-833.0, -52.0)
    knee_bloom_low.location = (53.0, -268.0)
    kb_switch.location = (273.0, -328.0)
    ob_switch.location = (273.0, 112.0)
    original_bloom_low.location = (53.0, 172.0)
    reroute_00.location = (-180.0, -369.0)
    reroute_01.location = (0.0, -220.0)
    clamp.location = (400.0, -40.0)
    group_input_00.location = (-1077.6015625, -314.0210266113281)
    group_input_02.location = (40.0, -220.0)
    group_input_03.location = (220.0, -198.0)
    group_input_05.location = (620.0, 209.0)
    group_input_04.location = (400.0, -218.0)
    group_input_01.location = (-320.0, -263.0)

    #Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    original_bloom_high.width, original_bloom_high.height = 154.0098876953125, 100.0
    color.width, color.height = 140.0, 100.0
    blur.width, blur.height = 151.06350708007812, 100.0
    blur_mix.width, blur_mix.height = 140.0, 100.0
    intensity.width, intensity.height = 140.0, 100.0
    knee_bloom_high.width, knee_bloom_high.height = 152.26959228515625, 100.0
    knee_mix.width, knee_mix.height = 140.0, 100.0
    bloom_high____low.width, bloom_high____low.height = 420.0, 944.0
    knee_bloom_low.width, knee_bloom_low.height = 153.29302978515625, 100.0
    kb_switch.width, kb_switch.height = 140.0, 100.0
    ob_switch.width, ob_switch.height = 140.0, 100.0
    original_bloom_low.width, original_bloom_low.height = 154.0098876953125, 100.0
    reroute_00.width, reroute_00.height = 16.0, 100.0
    reroute_01.width, reroute_01.height = 16.0, 100.0
    clamp.width, clamp.height = 152.98968505859375, 100.0
    group_input_00.width, group_input_00.height = 149.76272583007812, 100.0
    group_input_02.width, group_input_02.height = 138.52658081054688, 100.0
    group_input_03.width, group_input_03.height = 140.50942993164062, 100.0
    group_input_05.width, group_input_05.height = 139.75918579101562, 100.0
    group_input_04.width, group_input_04.height = 153.06747436523438, 100.0
    group_input_01.width, group_input_01.height = 149.76272583007812, 100.0

    #initialize oldeevee_bloom links
    #ob_switch.Image -> blur_mix.Image
    oldeevee_bloom.links.new(ob_switch.outputs[0], blur_mix.inputs[2])

    #blur_mix.Image -> knee_mix.Image
    oldeevee_bloom.links.new(blur_mix.outputs[0], knee_mix.inputs[1])

    #blur.Image -> blur_mix.Image
    oldeevee_bloom.links.new(blur.outputs[0], blur_mix.inputs[1])

    #knee_mix.Image -> color.Image
    oldeevee_bloom.links.new(knee_mix.outputs[0], color.inputs[1])

    #ob_switch.Image -> blur.Image
    oldeevee_bloom.links.new(ob_switch.outputs[0], blur.inputs[0])

    #intensity.Image -> group_output.Image
    oldeevee_bloom.links.new(intensity.outputs[0], group_output.inputs[0])

    #knee_bloom_high.Image -> kb_switch.On
    oldeevee_bloom.links.new(knee_bloom_high.outputs[0], kb_switch.inputs[1])

    #knee_bloom_low.Image -> kb_switch.Off
    oldeevee_bloom.links.new(knee_bloom_low.outputs[0], kb_switch.inputs[0])

    #original_bloom_high.Image -> ob_switch.On
    oldeevee_bloom.links.new(original_bloom_high.outputs[0], ob_switch.inputs[1])

    #original_bloom_low.Image -> ob_switch.Off
    oldeevee_bloom.links.new(original_bloom_low.outputs[0], ob_switch.inputs[0])

    #kb_switch.Image -> reroute_00.Input
    oldeevee_bloom.links.new(kb_switch.outputs[0], reroute_00.inputs[0])

    #reroute_00.Output -> reroute_01.Input
    oldeevee_bloom.links.new(reroute_00.outputs[0], reroute_01.inputs[0])

    #reroute_01.Output -> knee_mix.Image
    oldeevee_bloom.links.new(reroute_01.outputs[0], knee_mix.inputs[2])

    #color.Image -> clamp.Image
    oldeevee_bloom.links.new(color.outputs[0], clamp.inputs[0])

    #clamp.Image -> intensity.Image
    oldeevee_bloom.links.new(clamp.outputs[0], intensity.inputs[2])

    #group_input_05.Image -> intensity.Image
    oldeevee_bloom.links.new(group_input_05.outputs[0], intensity.inputs[1])

    #group_input_00.Image -> original_bloom_high.Image
    oldeevee_bloom.links.new(group_input_00.outputs[0], original_bloom_high.inputs[0])

    #group_input_00.Image -> knee_bloom_high.Image
    oldeevee_bloom.links.new(group_input_00.outputs[0], knee_bloom_high.inputs[0])

    #group_input_00.Image -> knee_bloom_low.Image
    oldeevee_bloom.links.new(group_input_00.outputs[0], knee_bloom_low.inputs[0])

    #group_input_00.Image -> original_bloom_low.Image
    oldeevee_bloom.links.new(group_input_00.outputs[0], original_bloom_low.inputs[0])

    #group_input_02.Knee -> knee_mix.Fac
    oldeevee_bloom.links.new(group_input_02.outputs[3], knee_mix.inputs[0])

    #group_input_03.Color -> color.Image
    oldeevee_bloom.links.new(group_input_03.outputs[5], color.inputs[2])

    #group_input_05.Intensity -> intensity.Fac
    oldeevee_bloom.links.new(group_input_05.outputs[6], intensity.inputs[0])

    #group_input_04.Clamp -> clamp.Value
    oldeevee_bloom.links.new(group_input_04.outputs[7], clamp.inputs[3])

    #group_input_04.Hue -> clamp.Hue
    oldeevee_bloom.links.new(group_input_04.outputs[12], clamp.inputs[1])

    #group_input_04.Saturation -> clamp.Saturation
    oldeevee_bloom.links.new(group_input_04.outputs[13], clamp.inputs[2])

    #group_input_04.Fac -> clamp.Fac
    oldeevee_bloom.links.new(group_input_04.outputs[14], clamp.inputs[4])

    #group_input_01.Blur Mix -> blur.Size
    oldeevee_bloom.links.new(group_input_01.outputs[15], blur.inputs[1])
    
    return oldeevee_bloom

class NODE_OT_BLOOM(bpy.types.Operator):
    bl_label = Names.OldEevee_Bloom
    bl_idname = "node.oldeevee_bloom_operator"
    bl_description = Descriptions.node_ot_bloom

    def execute(shelf, context):
        # Get the compositor node tree
        node_tree = context.scene.node_tree
        nodes = node_tree.nodes

        # Check if nodes exist, otherwise create them
        render_layer_node = nodes.get(Names.Render_Layers) or nodes.new(type=CompositorNodeNames.RENDER_LAYERS)
        render_layer_node.location = (-300, 0)

        composite_node = nodes.get(Names.Composite) or nodes.new(type=CompositorNodeNames.COMPOSITE)
        composite_node.location = (300, 86)

        viewer_node = nodes.get(Names.Viewer) or nodes.new(type=CompositorNodeNames.VIEWER)
        viewer_node.location = (300, -24)

        custom_oldeevee_bloom_node_name = Names.OldEevee_Bloom
        oldeevee_bloom_group = oldeevee_bloom_node_group(shelf, context, custom_oldeevee_bloom_node_name)
        oldeevee_bloom_node = context.scene.node_tree.nodes.new(CompositorNodeNames.GROUP)
        oldeevee_bloom_node.name = Names.OldEevee_Bloom
        oldeevee_bloom_node.label = Names.OldEevee_Bloom
        oldeevee_bloom_node.width = 174
        oldeevee_bloom_node.node_tree = bpy.data.node_groups[oldeevee_bloom_group.name]
        oldeevee_bloom_node.use_custom_color = True
        oldeevee_bloom_node.color = Color.DARK_PURPLE
        oldeevee_bloom_node.select = True

        # Initialize NodeDriverManager to manage drivers for the node group
        drivers = NodeDriverManager(node_group=oldeevee_bloom_node, id_type="SCENE", id=bpy.context.scene)

        # Original Bloom Switch
        drivers.add_driver(node_name=Names.OB_Switch, socket_name=SocketNames.check)
        drivers.add_driver_var(1)

        # Knee Bloom Switch
        drivers.add_driver(node_name=Names.KB_Switch, socket_name=SocketNames.check)
        drivers.add_driver_var(1)

        # Original Bloom High
        drivers.add_driver(node_name=Names.Original_Bloom_High, socket_name=SocketNames.threshold)
        drivers.add_driver_var(2)

        # Original Bloom Low
        drivers.add_driver(node_name=Names.Original_Bloom_Low, socket_name=SocketNames.threshold)
        drivers.add_driver_var(2)

        # Original Bloom High Size
        drivers.add_driver(node_name=Names.Original_Bloom_High, socket_name=SocketNames.size)
        drivers.add_driver_var(16)

        # Original Bloom Low Size
        drivers.add_driver(node_name=Names.Original_Bloom_Low, socket_name=SocketNames.size)
        drivers.add_driver_var(16)

        # Radius X
        drivers.add_driver(node_name=Names.Blur, socket_name=SocketNames.size_x)
        drivers.add_driver_var(4)

        # Radius Y
        drivers.add_driver(node_name=Names.Blur, socket_name=SocketNames.size_y)
        drivers.add_driver_var(4)

        # Blur Mix Clamp
        drivers.add_driver(node_name=Names.Blur_Mix, socket_name=SocketNames.use_clamp)
        drivers.add_driver_var(8)

        # Knee Mix Clamp
        drivers.add_driver(node_name=Names.Knee_Mix, socket_name=SocketNames.use_clamp)
        drivers.add_driver_var(9)

        # Color Clamp
        drivers.add_driver(node_name=Names.Color, socket_name=SocketNames.use_clamp)
        drivers.add_driver_var(10)

        # Intensity Clamp
        drivers.add_driver(node_name=Names.Intensity, socket_name=SocketNames.use_clamp)
        drivers.add_driver_var(11)

        # Connect the nodes
        ensure_connection(render_layer_node, Names.Image, oldeevee_bloom_node, Names.Image)
        ensure_connection(oldeevee_bloom_node, Names.Image, composite_node, Names.Image)
        ensure_connection(oldeevee_bloom_node, Names.Image, viewer_node, Names.Image)

        return {"FINISHED"}

class SCENE_OT_ENABLE_COMPOSITOR(bpy.types.Operator):
    bl_label = Names.Enable_Compositor
    bl_description = Descriptions.scene_ot_enable_compositor
    bl_idname = "scene.enable_compositor_operator"

    def execute(self, context):
        context.scene.use_nodes = True  # Enable compositor
        self.report({'INFO'}, "Compositor enabled.")
        return {'FINISHED'}

class PROP_PT_BLOOM(bpy.types.Panel):
    bl_label = 'Bloom'
    bl_idname = 'PROP_PT_BLOOM'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_description = Descriptions.prop_pt_bloom
    bl_order = 3
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True  # Always display the panel

    def draw_header(self, context):
        scene = context.scene
        self.layout.prop(scene, "bloom_mute_unmute_bool", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.enabled = context.scene.bloom_mute_unmute_bool
        
        scene = context.scene
        node_tree = bpy.context.scene.node_tree  # Access the Compositor node tree

            
        if not is_compositor_enabled(scene):
            # If compositor is disabled, show the operator to enable it
            layout.operator("scene.enable_compositor_operator", text="Enable Compositor", icon='NODE_COMPOSITING')
        else:
            # Once the compositor is enabled, check for the oldeevee_bloom node
            if node_tree:
                oldeevee_bloom_node = next(
                    (
                        node for node in node_tree.nodes
                        if node.type == 'GROUP' and node.name == Names.OldEevee_Bloom
                    ),
                    None
                )
                if oldeevee_bloom_node:
                    # Add Real-Time Compositing property
                    # Conditionally display the enum property based on the presence of a VIEW_3D area
                    if poll_view_3d(context):
                        layout.alignment = 'RIGHT'
                        layout.prop(
                            scene,
                            "real_time_compositing_enum",
                        ) # Show the enum property
                    # else:
                        # layout.label(text="No 3D View found. The enum property will not be shown.")

                    # Organize inputs into panels (same logic as before)
                    image_inputs = []
                    clamp_mix_inputs = []
                    other_inputs = []

                    for input in oldeevee_bloom_node.inputs:
                        if input.name == Names.Image:
                            continue
                        elif input.name in [
                            Names.Quality, Names.Threshold,
                            Names.Knee, Names.Radius,
                            Names.Color, Names.Intensity,
                            Names.Clamp
                        ]:
                            image_inputs.append(input)
                        elif Names.Clamp in input.name:
                            clamp_mix_inputs.append(input)
                        else:
                            other_inputs.append(input)

                    # Image Panel
                    if image_inputs:
                        image_box = layout.box()
                        image_col = image_box.column()
                        for input in image_inputs:
                            image_col.separator(factor=0.1)
                            image_col.prop(input, "default_value", text=input.name)

                    # Clamp Panel
                    row = layout.row()
                    row.prop(scene, "bloom_clamp_mix_bool", icon="RESTRICT_RENDER_OFF", emboss=False)
                    if scene.bloom_clamp_mix_bool:
                        clamp_mix_box = layout.box()
                        clamp_mix_col = clamp_mix_box.column()
                        for input in clamp_mix_inputs:
                            clamp_mix_col.separator(factor=0.1)
                            clamp_mix_col.prop(input, "default_value", text=input.name)

                    # Other Panel
                    row = layout.row()
                    row.prop(scene, "bloom_other_bool", icon="MODIFIER", emboss=False)
                    if scene.bloom_other_bool:
                        other_box = layout.box()
                        other_col = other_box.column()
                        for input in other_inputs:
                            other_col.separator(factor=0.1)
                            other_col.prop(input, "default_value", text=input.name)

                else:
                    # If oldeevee_bloom node doesn't exist, show the operator to create it
                    layout.operator("node.oldeevee_bloom_operator", text="Create OldEevee Bloom", icon='NODE_MATERIAL')

                    """
                    split = layout.split(factor=0.7)    # Adjust the split factor for a smaller gap

                    col_left = split.column()       # Left column
                    col_left.alignment = 'RIGHT'    # Align text to the right
                    col_right = split.column()      # Right column

                    col_left.label(text="Create OldEevee Bloom")    # Add text to the left column
                    col_right.operator("node.oldeevee_bloom_operator", text="", icon='NODE_MATERIAL')   # Add button to the right column
                    """

# Scene property reference
prop_scene = bpy.types.Scene

# Classes to Register/Unregister
classes = [PROP_PT_BLOOM, NODE_OT_BLOOM, SCENE_OT_ENABLE_COMPOSITOR]

# Register and unregister
def register():
    # Register properties
    prop_scene.bloom_mute_unmute_bool = BoolProperty(
        name=Names.Bloom_Mute_Unmute,
        description=Descriptions.bloom_mute_unmute_bool,
        default=False,
        update=toggle_oldeevee_bloom  # Attach the callback function
    )
    prop_scene.real_time_compositing_enum = EnumProperty(
        name=Names.Real_Time_Compositing,
        description=Descriptions.real_time_compositing,
        items=[
            (
                Names.Disabled.upper(), Names.Disabled, Descriptions.disabled, "CANCEL", 0
            ),
            (
                Names.Camera.upper(), Names.Camera, Descriptions.camera, "CAMERA_DATA", 1
            ),
            (
                Names.Always.upper(), Names.Always, Descriptions.always, "CHECKMARK", 2
            )
        ],
        default=Names.Disabled.upper(),
        update=update_real_time_compositing  # Attach the callback function here
    )
    prop_scene.bloom_clamp_mix_bool = BoolProperty(
        name=Names.Clamp_Mix,
        description=Descriptions.clamp_mix,
        default=False
    )
    prop_scene.bloom_other_bool = BoolProperty(
        name=Names.Other,
        description=Descriptions.other,
        default=False
    )

    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # Unregister properties
    del prop_scene.bloom_mute_unmute_bool
    del prop_scene.real_time_compositing_enum
    del prop_scene.bloom_clamp_mix_bool
    del prop_scene.bloom_other_bool

    # Unregister classes
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
