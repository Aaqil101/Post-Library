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
path_to_nodes_folder = script_dir / "nodes"
path_to_helpers_folder = script_dir / "helpers"
path_to_core_folder = script_dir / "core"

# List of paths
paths = [
    script_dir, path_to_nodes_folder,
    path_to_helpers_folder
]

# Add directories to sys.path
for path in paths:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.append(path_str)
        print(f"Added {path_str} to sys.path")
    else:
        print(f"{path_str} already in sys.path")

from helpers import (
    # For adding drivers to sockets
    add_driver_var, 

    # Color references
    Color,

    # Names and descriptions
    CompositorNodeNames,
    OldEevee_Bloom_Names,
    UpdateRTCompositingNames,
    OldEevee_Bloom_Descr,

    # Functions
    ensure_connection,
    poll_view_3d,
    update_real_time_compositing,
    toggle_oe_bloom,
    is_compositor_enabled
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

#initialize OE_Bloom node group
def oe_bloom_node_group(context, operator, group_name):
    oe_bloom = bpy.data.node_groups.new(group_name, CompositorNodeNames.TREE)

    oe_bloom.color_tag = 'FILTER'
    oe_bloom.description = OldEevee_Bloom_Descr.oe_bloom
    oe_bloom.default_group_node_width = 149

    #oe_bloom interface
    #Socket Image
    image_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Image, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket_1 = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Image, in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.description = OldEevee_Bloom_Descr.image

    #Socket Quality
    quality_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Quality, in_out='INPUT', socket_type = 'NodeSocketFloat')
    quality_socket.default_value = 0.0
    quality_socket.min_value = 0.0
    quality_socket.max_value = 1.0
    quality_socket.subtype = 'FACTOR'
    quality_socket.attribute_domain = 'POINT'
    quality_socket.description = OldEevee_Bloom_Descr.quality

    #Socket Threshold
    threshold_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Threshold, in_out='INPUT', socket_type = 'NodeSocketFloat')
    threshold_socket.default_value = 1.0
    threshold_socket.min_value = 0.0
    threshold_socket.max_value = 1000.0
    threshold_socket.subtype = 'NONE'
    threshold_socket.attribute_domain = 'POINT'
    threshold_socket.description = OldEevee_Bloom_Descr.threshold

    #Socket Knee
    knee_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Knee, in_out='INPUT', socket_type = 'NodeSocketFloat')
    knee_socket.default_value = 0.0
    knee_socket.min_value = 0.0
    knee_socket.max_value = 1.0
    knee_socket.subtype = 'FACTOR'
    knee_socket.attribute_domain = 'POINT'
    knee_socket.description = OldEevee_Bloom_Descr.knee

    #Socket Radius
    radius_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Radius, in_out='INPUT', socket_type = 'NodeSocketFloat')
    radius_socket.default_value = 0.0
    radius_socket.min_value = 0.0
    radius_socket.max_value = 2048.0
    radius_socket.subtype = 'NONE'
    radius_socket.attribute_domain = 'POINT'
    radius_socket.description = OldEevee_Bloom_Descr.radius

    #Socket Color
    color_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Color, in_out='INPUT', socket_type = 'NodeSocketColor')
    color_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.description = OldEevee_Bloom_Descr.color

    #Socket Intensity
    intensity_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Intensity, in_out='INPUT', socket_type = 'NodeSocketFloat')
    intensity_socket.default_value = 1.0
    intensity_socket.min_value = 0.0
    intensity_socket.max_value = 1.0
    intensity_socket.subtype = 'FACTOR'
    intensity_socket.attribute_domain = 'POINT'
    intensity_socket.description = OldEevee_Bloom_Descr.intensity

    #Socket Clamp
    clamp_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat')
    clamp_socket.default_value = 1.0
    clamp_socket.min_value = 0.0
    clamp_socket.max_value = 2.0
    clamp_socket.subtype = 'FACTOR'
    clamp_socket.attribute_domain = 'POINT'
    clamp_socket.description = OldEevee_Bloom_Descr.clamp

    #Panel Clamp Mix
    clamp_mix_panel = oe_bloom.interface.new_panel(OldEevee_Bloom_Names.Clamp_Mix, default_closed=True)
    clamp_mix_panel.description = OldEevee_Bloom_Descr.clamp_mix

    #Socket BM Clamp
    bm_clamp_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.BM_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    bm_clamp_socket.default_value = 1.0
    bm_clamp_socket.min_value = 0.0
    bm_clamp_socket.max_value = 1.0
    bm_clamp_socket.subtype = 'FACTOR'
    bm_clamp_socket.attribute_domain = 'POINT'
    bm_clamp_socket.description = OldEevee_Bloom_Descr.bm_clamp

    #Socket KM Clamp
    km_clamp_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.KM_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    km_clamp_socket.default_value = 0.0
    km_clamp_socket.min_value = 0.0
    km_clamp_socket.max_value = 1.0
    km_clamp_socket.subtype = 'FACTOR'
    km_clamp_socket.attribute_domain = 'POINT'
    km_clamp_socket.description = OldEevee_Bloom_Descr.km_clamp

    #Socket CR Clamp
    cr_clamp_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.CR_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    cr_clamp_socket.default_value = 0.0
    cr_clamp_socket.min_value = 0.0
    cr_clamp_socket.max_value = 1.0
    cr_clamp_socket.subtype = 'FACTOR'
    cr_clamp_socket.attribute_domain = 'POINT'
    cr_clamp_socket.description = OldEevee_Bloom_Descr.cr_clamp

    #Socket IY Clamp
    iy_clamp_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.IY_Clamp, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = clamp_mix_panel)
    iy_clamp_socket.default_value = 0.0
    iy_clamp_socket.min_value = 0.0
    iy_clamp_socket.max_value = 1.0
    iy_clamp_socket.subtype = 'FACTOR'
    iy_clamp_socket.attribute_domain = 'POINT'
    iy_clamp_socket.description = OldEevee_Bloom_Descr.iy_clamp

    #Panel Other
    other_panel = oe_bloom.interface.new_panel(OldEevee_Bloom_Names.Other, default_closed=True)
    other_panel.description = OldEevee_Bloom_Descr.other

    #Socket Hue
    hue_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Hue, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    hue_socket.default_value = 0.5
    hue_socket.min_value = 0.0
    hue_socket.max_value = 1.0
    hue_socket.subtype = 'FACTOR'
    hue_socket.attribute_domain = 'POINT'
    hue_socket.description = OldEevee_Bloom_Descr.hue

    #Socket Saturation
    saturation_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Saturation, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    saturation_socket.default_value = 1.0
    saturation_socket.min_value = 0.0
    saturation_socket.max_value = 2.0
    saturation_socket.subtype = 'FACTOR'
    saturation_socket.attribute_domain = 'POINT'
    saturation_socket.description = OldEevee_Bloom_Descr.saturation

    #Socket Fac
    fac_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Fac, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    fac_socket.default_value = 1.0
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = 'FACTOR'
    fac_socket.attribute_domain = 'POINT'
    fac_socket.description = OldEevee_Bloom_Descr.fac

    #Socket Blur Mix
    blur_mix_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Blur_Mix, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    blur_mix_socket.default_value = 1.0
    blur_mix_socket.min_value = 0.0
    blur_mix_socket.max_value = 1.0
    blur_mix_socket.subtype = 'NONE'
    blur_mix_socket.attribute_domain = 'POINT'
    blur_mix_socket.description = OldEevee_Bloom_Descr.blur_mix

    #Socket Bloom Size
    bloom_size_socket = oe_bloom.interface.new_socket(name = OldEevee_Bloom_Names.Bloom_Size, in_out='INPUT', socket_type = 'NodeSocketFloat', parent = other_panel)
    bloom_size_socket.default_value = 9.0
    bloom_size_socket.min_value = 1.0
    bloom_size_socket.max_value = 9.0
    bloom_size_socket.subtype = 'NONE'
    bloom_size_socket.attribute_domain = 'POINT'
    bloom_size_socket.description = OldEevee_Bloom_Descr.bloom_size

    # Initialize oe_bloom nodes
    # Initialize node managers with the oe_bloom node group and custom settings
    FNM = FilterNodeManager(node_group=oe_bloom, use_custom_color=True)
    CNM = ColorNodeManager(node_group=oe_bloom, use_custom_color=True)
    LNM = LayoutNodeManager(node_group=oe_bloom, node_color=["77535F", "3C3937"], use_custom_color=True)
    UNM = UtilitiesNodeManager(node_group=oe_bloom, use_custom_color=True)
    INM = InputNodeManager(node_group=oe_bloom, use_custom_color=True)
    ONM = OutputNodeManager(node_group=oe_bloom, use_custom_color=True)

    #node Group Output
    group_output = ONM.create_group_output_node(
        group_output_name=OldEevee_Bloom_Names.Group_Output,
        group_output_label=OldEevee_Bloom_Names.Group_Output,
        settings=GroupOutputSettings(
            outputs_to_hide=[1],
            is_active_output=True
        )
    )

    #node Original Bloom High
    original_bloom_high = FNM.create_glare_node(
        glare_name=OldEevee_Bloom_Names.Original_Bloom_High,
        glare_label=OldEevee_Bloom_Names.Original_Bloom_High,
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
        glare_name=OldEevee_Bloom_Names.Original_Bloom_Low,
        glare_label=OldEevee_Bloom_Names.Original_Bloom_Low,
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
        glare_name=OldEevee_Bloom_Names.Knee_Bloom_High,
        glare_label=OldEevee_Bloom_Names.Knee_Bloom_High,
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
        glare_name=OldEevee_Bloom_Names.Knee_Bloom_Low,
        glare_label=OldEevee_Bloom_Names.Knee_Bloom_Low,
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
        blur_name=OldEevee_Bloom_Names.Blur,
        blur_label=OldEevee_Bloom_Names.Blur,
        settings=BlurSettings(filter_type=BlurFilterType.FAST_GAUSS)
    )


    #node Color
    color = CNM.create_mixcolor_node(
        mixcolor_name=OldEevee_Bloom_Names.Color,
        mixcolor_label=OldEevee_Bloom_Names.Color,
        settings=MixColorSettings(
            blend_type=BlendType.COLOR,
            fac_default_value=1.0,
            hide_fac=True
        )
    )

    #node Blur Mix
    blur_mix = CNM.create_mixcolor_node(
        mixcolor_name=OldEevee_Bloom_Names.Blur_Mix,
        mixcolor_label=OldEevee_Bloom_Names.Blur_Mix,
        settings=MixColorSettings(
            blend_type=BlendType.SCREEN,
            use_clamp=True,
            fac_default_value=1.0,
            hide_fac=True
        )
    )

    #node Intensity
    intensity = CNM.create_mixcolor_node(
        mixcolor_name=OldEevee_Bloom_Names.Intensity,
        mixcolor_label=OldEevee_Bloom_Names.Intensity,
        settings=MixColorSettings(blend_type=BlendType.ADD)
    )

    #node Knee Mix
    knee_mix = CNM.create_mixcolor_node(
        mixcolor_name=OldEevee_Bloom_Names.Knee_Mix,
        mixcolor_label=OldEevee_Bloom_Names.Knee_Mix,
        settings=MixColorSettings(blend_type=BlendType.ADD)
    )

    #node Clamp
    clamp = CNM.create_huesat_node(huesat_name=OldEevee_Bloom_Names.Clamp, huesat_label=OldEevee_Bloom_Names.Clamp)


    #node Bloom High && Low
    bloom_high____low = LNM.create_frame_node(
        frame_name=OldEevee_Bloom_Names.Bloom_High_Low,
        frame_label=OldEevee_Bloom_Names.Bloom_High_Low,
        settings=FrameSettings(
            label_size=32,
            shrink=True
        )
    )

    #node Reroute_00
    reroute_00 = LNM.create_reroute_node(reroute_name=OldEevee_Bloom_Names.Reroute_00, reroute_label=OldEevee_Bloom_Names.KB_Switch)

    #node Reroute_01
    reroute_01 = LNM.create_reroute_node(reroute_name=OldEevee_Bloom_Names.Reroute_01, reroute_label=OldEevee_Bloom_Names.KB_Switch)

    #node KB Switch
    kb_switch = UNM.create_switch_node(switch_name=OldEevee_Bloom_Names.KB_Switch, switch_label=OldEevee_Bloom_Names.KB_Switch)

    #node OB Switch
    ob_switch = UNM.create_switch_node(switch_name=OldEevee_Bloom_Names.OB_Switch, switch_label=OldEevee_Bloom_Names.OB_Switch)


    #node Group Input 00
    group_input_00 = INM.create_group_input_node(
        group_input_name=OldEevee_Bloom_Names.Group_Input_00,
        group_input_label=OldEevee_Bloom_Names.Group_Input_00,
        settings=GroupInputSettings(
            outputs_to_hide=list(range(1, 18)) # Hide outputs 1 to 17
        )
    )

    #node Group Input 01
    group_input_01 = INM.create_group_input_node(
        group_input_name=OldEevee_Bloom_Names.Group_Input_01,
        group_input_label=OldEevee_Bloom_Names.Group_Input_01,
        settings=GroupInputSettings(
            outputs_to_hide=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17]  # Outputs to hide
        )
    )

    #node Group Input 02
    group_input_02 = INM.create_group_input_node(
        group_input_name=OldEevee_Bloom_Names.Group_Input_02,
        group_input_label=OldEevee_Bloom_Names.Group_Input_02,
        settings=GroupInputSettings(
            outputs_to_hide=[0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  # Outputs to hide
        )
    )

    #node Group Input 03
    group_input_03 = INM.create_group_input_node(
        group_input_name=OldEevee_Bloom_Names.Group_Input_03,
        group_input_label=OldEevee_Bloom_Names.Group_Input_03,
        settings=GroupInputSettings(
            outputs_to_hide=[0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  # Outputs to hide
        )
    )

    #node Group Input 04
    group_input_04 = INM.create_group_input_node(
        group_input_name=OldEevee_Bloom_Names.Group_Input_04,
        group_input_label=OldEevee_Bloom_Names.Group_Input_04,
        settings=GroupInputSettings(
            outputs_to_hide=[0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 15, 16, 17]  # Outputs to hide
        )
    )

    #node Group Input 05
    group_input_05 = INM.create_group_input_node(
        group_input_name=OldEevee_Bloom_Names.Group_Input_05,
        group_input_label=OldEevee_Bloom_Names.Group_Input_05,
        settings=GroupInputSettings(
            outputs_to_hide=[1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  # Outputs to hide
        )
    )

    """
    ! Old method to create the Group Output Node
    group_output = oe_bloom.nodes.new("NodeGroupOutput")
    group_output.label = OldEevee_Bloom_Names.Group_Output
    group_output.name = OldEevee_Bloom_Names.Group_Output
    group_output.use_custom_color = True
    group_output.color = Color.DARK_GRAY
    group_output.inputs[1].hide = True
    group_output.is_active_output = True

    ! Old method to create the Original Bloom High node
    original_bloom_high = oe_bloom.nodes.new("CompositorNodeGlare")
    original_bloom_high.label = OldEevee_Bloom_Names.Original_Bloom_High
    original_bloom_high.name = OldEevee_Bloom_Names.Original_Bloom_High
    original_bloom_high.use_custom_color = True
    original_bloom_high.color = Color.DARK_PURPLE
    original_bloom_high.glare_type = 'BLOOM'
    original_bloom_high.quality = 'HIGH'
    original_bloom_high.mix = 1.0
    original_bloom_high.threshold = 1.0
    original_bloom_high.size = 9

    ! Old method to create the Original Bloom Low node
    original_bloom_low = oe_bloom.nodes.new("CompositorNodeGlare")
    original_bloom_low.label = OldEevee_Bloom_Names.Original_Bloom_Low
    original_bloom_low.name = OldEevee_Bloom_Names.Original_Bloom_Low
    original_bloom_low.use_custom_color = True
    original_bloom_low.color = Color.DARK_PURPLE
    original_bloom_low.glare_type = 'BLOOM'
    original_bloom_low.quality = 'LOW'
    original_bloom_low.mix = 1.0
    original_bloom_low.threshold = 1.0
    original_bloom_low.size = 9

    ! Old method to create the Knee Bloom High node
    knee_bloom_high = oe_bloom.nodes.new("CompositorNodeGlare")
    knee_bloom_high.label = OldEevee_Bloom_Names.Knee_Bloom_High
    knee_bloom_high.name = OldEevee_Bloom_Names.Knee_Bloom_High
    knee_bloom_high.use_custom_color = True
    knee_bloom_high.color = Color.DARK_PURPLE
    knee_bloom_high.glare_type = 'BLOOM'
    knee_bloom_high.quality = 'HIGH'
    knee_bloom_high.mix = 1.0
    knee_bloom_high.threshold = 0.0
    knee_bloom_high.size = 9

    ! Old method to create the Knee Bloom Low node
    knee_bloom_low = oe_bloom.nodes.new("CompositorNodeGlare")
    knee_bloom_low.label = OldEevee_Bloom_Names.Knee_Bloom_Low
    knee_bloom_low.name = OldEevee_Bloom_Names.Knee_Bloom_Low
    knee_bloom_low.use_custom_color = True
    knee_bloom_low.color = Color.DARK_PURPLE
    knee_bloom_low.glare_type = 'BLOOM'
    knee_bloom_low.quality = 'LOW'
    knee_bloom_low.mix = 1.0
    knee_bloom_low.threshold = 0.0
    knee_bloom_low.size = 9

    ! Old method to create the Blur node
    blur = oe_bloom.nodes.new("CompositorNodeBlur")
    blur.label = OldEevee_Bloom_Names.Blur
    blur.name = OldEevee_Bloom_Names.Blur
    blur.use_custom_color = True
    blur.color = Color.DARK_PURPLE
    blur.filter_type = 'FAST_GAUSS'
    blur.use_relative = False
    blur.use_extended_bounds = False

    ! Old method to create the Mix Color node
    color = oe_bloom.nodes.new("CompositorNodeMixRGB")
    color.label = OldEevee_Bloom_Names.Color
    color.name = OldEevee_Bloom_Names.Color
    color.use_custom_color = True
    color.color = Color.BROWN
    color.blend_type = 'COLOR'
    color.use_alpha = False
    color.use_clamp = False
    color.inputs[0].hide = True
    #Fac
    color.inputs[0].default_value = 1.0

    ! Old method to create the Blur Mix node
    blur_mix = oe_bloom.nodes.new("CompositorNodeMixRGB")
    blur_mix.label = OldEevee_Bloom_Names.Blur_Mix
    blur_mix.name = OldEevee_Bloom_Names.Blur_Mix
    blur_mix.use_custom_color = True
    blur_mix.color = Color.BROWN
    blur_mix.blend_type = 'SCREEN'
    blur_mix.use_alpha = False
    blur_mix.use_clamp = True
    blur_mix.inputs[0].hide = True
    #Fac
    blur_mix.inputs[0].default_value = 1.0

    ! Old method to create the Intensity node
    intensity = oe_bloom.nodes.new("CompositorNodeMixRGB")
    intensity.label = OldEevee_Bloom_Names.Intensity
    intensity.name = OldEevee_Bloom_Names.Intensity
    intensity.use_custom_color = True
    intensity.color = Color.BROWN
    intensity.blend_type = 'ADD'
    intensity.use_alpha = False
    intensity.use_clamp = False
    
    ! Old method to create the Knee Mix node
    knee_mix = oe_bloom.nodes.new("CompositorNodeMixRGB")
    knee_mix.label = OldEevee_Bloom_Names.Knee_Mix
    knee_mix.name = OldEevee_Bloom_Names.Knee_Mix
    knee_mix.use_custom_color = True
    knee_mix.color = Color.BROWN
    knee_mix.blend_type = 'ADD'
    knee_mix.use_alpha = False
    knee_mix.use_clamp = False
    
    ! Old method to create the Clamp node
    clamp = oe_bloom.nodes.new("CompositorNodeHueSat")
    clamp.label = OldEevee_Bloom_Names.Clamp
    clamp.name = OldEevee_Bloom_Names.Clamp
    clamp.use_custom_color = True
    clamp.color = Color.BROWN

    ! Old method to create the Bloom High && Low Frame
    bloom_high____low = oe_bloom.nodes.new("NodeFrame")
    bloom_high____low.label = OldEevee_Bloom_Names.Bloom_High_Low
    bloom_high____low.name = OldEevee_Bloom_Names.Bloom_High_Low
    bloom_high____low.use_custom_color = True

    # Combine two hex colors into a single hex color code
    bloom_high_low_color = hex_color_add("77535F", "3C3937")
    
    # Convert the combined hex color code to Linear RGB
    bloom_high_low_color = hexcode_to_rgb(bloom_high_low_color)

    bloom_high____low.color = bloom_high_low_color
    bloom_high____low.label_size = 32
    bloom_high____low.shrink = True

    ! Old method to create the Reroute_00 node
    reroute_00 = oe_bloom.nodes.new("NodeReroute")
    reroute_00.label = OldEevee_Bloom_Names.KB_Switch
    reroute_00.name = OldEevee_Bloom_Names.Reroute_00
    reroute_00.socket_idname = "NodeSocketColor"

    ! Old method to create the Reroute_01 node
    reroute_01 = oe_bloom.nodes.new("NodeReroute")
    reroute_01.label = OldEevee_Bloom_Names.KB_Switch
    reroute_01.name = OldEevee_Bloom_Names.Reroute_01
    reroute_01.socket_idname = "NodeSocketColor"

    ! Old method to create the kb_switch node
    kb_switch = oe_bloom.nodes.new("CompositorNodeSwitch")
    kb_switch.label = OldEevee_Bloom_Names.KB_Switch
    kb_switch.name = OldEevee_Bloom_Names.KB_Switch
    kb_switch.use_custom_color = True
    kb_switch.color = Color.LIGHT_GRAY
    kb_switch.check = False

    ! Old method to create the ob_switch node
    ob_switch = oe_bloom.nodes.new("CompositorNodeSwitch")
    ob_switch.label = OldEevee_Bloom_Names.OB_Switch
    ob_switch.name = OldEevee_Bloom_Names.OB_Switch
    ob_switch.use_custom_color = True
    ob_switch.color = Color.LIGHT_GRAY
    ob_switch.check = False

    ! Old method to create the group_input_00 node
    group_input_00 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_00.label = OldEevee_Bloom_Names.Group_Input_00
    group_input_00.name = OldEevee_Bloom_Names.Group_Input_00
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
    group_input_00.outputs[17].hide = True

    ! Old method to create the group_input_01 node
    group_input_01 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_01.label = OldEevee_Bloom_Names.Group_Input_01
    group_input_01.name = OldEevee_Bloom_Names.Group_Input_01
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
    group_input_01.outputs[14].hide = True
    group_input_01.outputs[16].hide = True
    group_input_01.outputs[17].hide = True

    ! Old method to create the group_input_02 node
    group_input_02 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_02.label = OldEevee_Bloom_Names.Group_Input_02
    group_input_02.name = OldEevee_Bloom_Names.Group_Input_02
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
    group_input_02.outputs[17].hide = True

    ! Old method to create the group_input_03 node
    group_input_03 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_03.label = OldEevee_Bloom_Names.Group_Input_03
    group_input_03.name = OldEevee_Bloom_Names.Group_Input_03
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
    group_input_03.outputs[17].hide = True

    ! Old method to create the group_input_04 node
    group_input_04 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_04.label = OldEevee_Bloom_Names.Group_Input_04
    group_input_04.name = OldEevee_Bloom_Names.Group_Input_04
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
    group_input_04.outputs[11].hide = True
    group_input_04.outputs[15].hide = True
    group_input_04.outputs[16].hide = True
    group_input_04.outputs[17].hide = True

    ! Old method to create the group_input_05 node
    group_input_05 = oe_bloom.nodes.new("NodeGroupInput")
    group_input_05.label = OldEevee_Bloom_Names.Group_Input_05
    group_input_05.name = OldEevee_Bloom_Names.Group_Input_05
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
    group_input_05.outputs[17].hide = True
    """

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

    #intensity.Image -> group_output.Image
    oe_bloom.links.new(intensity.outputs[0], group_output.inputs[0])

    #knee_bloom_high.Image -> kb_switch.On
    oe_bloom.links.new(knee_bloom_high.outputs[0], kb_switch.inputs[1])

    #knee_bloom_low.Image -> kb_switch.Off
    oe_bloom.links.new(knee_bloom_low.outputs[0], kb_switch.inputs[0])

    #original_bloom_high.Image -> ob_switch.On
    oe_bloom.links.new(original_bloom_high.outputs[0], ob_switch.inputs[1])

    #original_bloom_low.Image -> ob_switch.Off
    oe_bloom.links.new(original_bloom_low.outputs[0], ob_switch.inputs[0])

    #kb_switch.Image -> reroute_00.Input
    oe_bloom.links.new(kb_switch.outputs[0], reroute_00.inputs[0])

    #reroute_00.Output -> reroute_01.Input
    oe_bloom.links.new(reroute_00.outputs[0], reroute_01.inputs[0])

    #reroute_01.Output -> knee_mix.Image
    oe_bloom.links.new(reroute_01.outputs[0], knee_mix.inputs[2])

    #color.Image -> clamp.Image
    oe_bloom.links.new(color.outputs[0], clamp.inputs[0])

    #clamp.Image -> intensity.Image
    oe_bloom.links.new(clamp.outputs[0], intensity.inputs[2])

    #group_input_05.Image -> intensity.Image
    oe_bloom.links.new(group_input_05.outputs[0], intensity.inputs[1])

    #group_input_00.Image -> original_bloom_high.Image
    oe_bloom.links.new(group_input_00.outputs[0], original_bloom_high.inputs[0])

    #group_input_00.Image -> knee_bloom_high.Image
    oe_bloom.links.new(group_input_00.outputs[0], knee_bloom_high.inputs[0])

    #group_input_00.Image -> knee_bloom_low.Image
    oe_bloom.links.new(group_input_00.outputs[0], knee_bloom_low.inputs[0])

    #group_input_00.Image -> original_bloom_low.Image
    oe_bloom.links.new(group_input_00.outputs[0], original_bloom_low.inputs[0])

    #group_input_02.Knee -> knee_mix.Fac
    oe_bloom.links.new(group_input_02.outputs[3], knee_mix.inputs[0])

    #group_input_03.Color -> color.Image
    oe_bloom.links.new(group_input_03.outputs[5], color.inputs[2])

    #group_input_05.Intensity -> intensity.Fac
    oe_bloom.links.new(group_input_05.outputs[6], intensity.inputs[0])

    #group_input_04.Clamp -> clamp.Value
    oe_bloom.links.new(group_input_04.outputs[7], clamp.inputs[3])

    #group_input_04.Hue -> clamp.Hue
    oe_bloom.links.new(group_input_04.outputs[12], clamp.inputs[1])

    #group_input_04.Saturation -> clamp.Saturation
    oe_bloom.links.new(group_input_04.outputs[13], clamp.inputs[2])

    #group_input_04.Fac -> clamp.Fac
    oe_bloom.links.new(group_input_04.outputs[14], clamp.inputs[4])

    #group_input_01.Blur Mix -> blur.Size
    oe_bloom.links.new(group_input_01.outputs[15], blur.inputs[1])
    
    return oe_bloom

class NODE_OT_BLOOM(bpy.types.Operator):
    bl_label = OldEevee_Bloom_Names.OE_Bloom
    bl_idname = "node.oe_bloom_operator"
    bl_description = OldEevee_Bloom_Descr.node_ot_bloom

    def execute(shelf, context):
        # Get the compositor node tree
        node_tree = context.scene.node_tree
        nodes = node_tree.nodes

        # Check if nodes exist, otherwise create them
        render_layer_node = nodes.get(OldEevee_Bloom_Names.Render_Layers) or nodes.new(type=CompositorNodeNames.RENDER_LAYERS)
        render_layer_node.location = (-300, 0)

        composite_node = nodes.get(OldEevee_Bloom_Names.Composite) or nodes.new(type=CompositorNodeNames.COMPOSITE)
        composite_node.location = (300, 86)

        viewer_node = nodes.get(OldEevee_Bloom_Names.Viewer) or nodes.new(type=CompositorNodeNames.VIEWER)
        viewer_node.location = (300, -24)

        custom_oe_bloom_node_name = OldEevee_Bloom_Names.OE_Bloom
        oe_bloom_group = oe_bloom_node_group(shelf, context, custom_oe_bloom_node_name)
        oe_bloom_node = context.scene.node_tree.nodes.new(CompositorNodeNames.GROUP)
        oe_bloom_node.name = OldEevee_Bloom_Names.OE_Bloom
        oe_bloom_node.label = OldEevee_Bloom_Names.OE_Bloom
        oe_bloom_node.width = 149
        oe_bloom_node.node_tree = bpy.data.node_groups[oe_bloom_group.name]
        oe_bloom_node.use_custom_color = True
        oe_bloom_node.color = Color.DARK_PURPLE
        oe_bloom_node.select = True

        # Original Bloom Switch
        oe_bloom_obs_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.OB_Switch].driver_add('check').driver
        oe_bloom_obs_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obs_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[1].default_value'
        )

        # Knee Bloom Switch
        oe_bloom_kbs_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.KB_Switch].driver_add('check').driver
        oe_bloom_kbs_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_kbs_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[1].default_value'
        )

        # Original Bloom High
        oe_bloom_obh_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.Original_Bloom_High].driver_add('threshold').driver
        oe_bloom_obh_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obh_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[2].default_value'
        )

        # Original Bloom Low
        oe_bloom_obl_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.Original_Bloom_Low].driver_add('threshold').driver
        oe_bloom_obl_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obl_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[2].default_value'
        )

        # Original Bloom High Size
        oe_bloom_obhs_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.Original_Bloom_High].driver_add('size').driver
        oe_bloom_obhs_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obhs_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[16].default_value'
        )

        # Original Bloom Low Size
        oe_bloom_obls_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.Original_Bloom_Low].driver_add('size').driver
        oe_bloom_obls_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_obls_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[16].default_value'
        )

        # Radius X
        oe_bloom_rx_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.Blur].driver_add('size_x').driver
        oe_bloom_rx_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_rx_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[4].default_value'
        )

        # Radius Y
        oe_bloom_ry_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.Blur].driver_add('size_y').driver
        oe_bloom_ry_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_ry_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[4].default_value'
        )

        # Blur Mix Clamp
        oe_bloom_bxc_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.Blur_Mix].driver_add('use_clamp').driver
        oe_bloom_bxc_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_bxc_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[8].default_value'
        )

        # Knee Mix Clamp
        oe_bloom_kxc_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.Knee_Mix].driver_add('use_clamp').driver
        oe_bloom_kxc_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_kxc_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[9].default_value'
        )

        # Color Clamp
        oe_bloom_cc_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.Color].driver_add('use_clamp').driver
        oe_bloom_cc_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_cc_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[10].default_value'
        )

        # Intensity Clamp
        oe_bloom_ic_driver = oe_bloom_node.node_tree.nodes[OldEevee_Bloom_Names.Intensity].driver_add('use_clamp').driver
        oe_bloom_ic_driver.type = "AVERAGE"
        add_driver_var(
            oe_bloom_ic_driver,
            f'node_tree.nodes["{oe_bloom_node.name}"].inputs[11].default_value'
        )

        # Connect the nodes
        ensure_connection(render_layer_node, OldEevee_Bloom_Names.Image, oe_bloom_node, OldEevee_Bloom_Names.Image)
        ensure_connection(oe_bloom_node, OldEevee_Bloom_Names.Image, composite_node, OldEevee_Bloom_Names.Image)
        ensure_connection(oe_bloom_node, OldEevee_Bloom_Names.Image, viewer_node, OldEevee_Bloom_Names.Image)

        return {"FINISHED"}

class SCENE_OT_ENABLE_COMPOSITOR(bpy.types.Operator):
    bl_label = OldEevee_Bloom_Names.Enable_Compositor
    bl_description = OldEevee_Bloom_Descr.scene_ot_enable_compositor
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
    bl_description = OldEevee_Bloom_Descr.prop_pt_bloom
    bl_order = 3
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True  # Always display the panel

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        node_tree = bpy.context.scene.node_tree  # Access the Compositor node tree

        if not is_compositor_enabled(scene):
            # If compositor is disabled, show the operator to enable it
            layout.operator("scene.enable_compositor_operator", text="Enable Compositor", icon='NODE_COMPOSITING')
        else:
            # Once the compositor is enabled, check for the OE_Bloom node
            if node_tree:
                oe_bloom_node = next(
                    (
                        node for node in node_tree.nodes
                        if node.type == 'GROUP' and node.name == OldEevee_Bloom_Names.OE_Bloom
                    ),
                    None
                )
                if oe_bloom_node:
                    # Add Real-Time Compositing property
                    # Conditionally display the enum property based on the presence of a VIEW_3D area
                    if poll_view_3d(self, context):
                        layout.alignment = 'RIGHT'
                        layout.prop(
                            scene,
                            "real_time_compositing_enum",
                        ) # Show the enum property
                    # else:
                        # layout.label(text="No 3D View found. The enum property will not be shown.")

                    # Show Mute/Unmute property
                    layout.prop(
                        scene,
                        "bloom_mute_unmute_bool",
                        text="Mute" if scene.bloom_mute_unmute_bool else "Unmute",
                        icon='MUTE_IPO_ON' if scene.bloom_mute_unmute_bool else 'MUTE_IPO_OFF'
                    )

                    # Organize inputs into panels (same logic as before)
                    image_inputs = []
                    clamp_mix_inputs = []
                    other_inputs = []

                    for input in oe_bloom_node.inputs:
                        if input.name == OldEevee_Bloom_Names.Image:
                            continue
                        elif input.name in [
                            OldEevee_Bloom_Names.Quality, OldEevee_Bloom_Names.Threshold,
                            OldEevee_Bloom_Names.Knee, OldEevee_Bloom_Names.Radius,
                            OldEevee_Bloom_Names.Color, OldEevee_Bloom_Names.Intensity,
                            OldEevee_Bloom_Names.Clamp
                        ]:
                            image_inputs.append(input)
                        elif OldEevee_Bloom_Names.Clamp in input.name:
                            clamp_mix_inputs.append(input)
                        else:
                            other_inputs.append(input)

                    # Image Panel
                    if image_inputs:
                        for input in image_inputs:
                            layout.prop(input, "default_value", text=input.name)

                    # Clamp Panel
                    row = layout.row()
                    row.prop(scene, "bloom_clamp_mix_bool", icon="RESTRICT_RENDER_OFF", emboss=False)
                    if scene.bloom_clamp_mix_bool:
                        clamp_mix_box = layout.box()
                        for input in clamp_mix_inputs:
                            clamp_mix_box.prop(input, "default_value", text=input.name)

                    # Other Panel
                    row = layout.row()
                    row.prop(scene, "bloom_other_bool", icon="MODIFIER", emboss=False)
                    if scene.bloom_other_bool:
                        other_box = layout.box()
                        for input in other_inputs:
                            other_box.prop(input, "default_value", text=input.name)
                else:
                    # If OE_Bloom node doesn't exist, show the operator to create it
                    layout.operator("node.oe_bloom_operator", text="Create OE_Bloom", icon='NODE_MATERIAL')

# Scene property reference
prop_scene = bpy.types.Scene

# Classes to Register/Unregister
classes = [PROP_PT_BLOOM, NODE_OT_BLOOM, SCENE_OT_ENABLE_COMPOSITOR]

# Register and unregister
def register():
    # Register properties
    prop_scene.bloom_mute_unmute_bool = BoolProperty(
        name=OldEevee_Bloom_Names.Bloom_Mute_Unmute,
        description=OldEevee_Bloom_Descr.bloom_mute_unmute_bool,
        default=False,
        update=toggle_oe_bloom  # Attach the callback function
    )
    prop_scene.real_time_compositing_enum = EnumProperty(
        name=OldEevee_Bloom_Names.Real_Time_Compositing,
        description=OldEevee_Bloom_Descr.real_time_compositing,
        items=[
            (
                UpdateRTCompositingNames.DISABLED, UpdateRTCompositingNames.DISABLED.title(), OldEevee_Bloom_Descr.disabled, "CANCEL", 0
            ),
            (
                UpdateRTCompositingNames.CAMERA, UpdateRTCompositingNames.CAMERA.title(), OldEevee_Bloom_Descr.camera, "CAMERA_DATA", 1
            ),
            (
                UpdateRTCompositingNames.ALWAYS, UpdateRTCompositingNames.ALWAYS.title(), OldEevee_Bloom_Descr.always, "CHECKMARK", 2
            )
        ],
        default=UpdateRTCompositingNames.DISABLED,
        update=update_real_time_compositing  # Attach the callback function here
    )
    prop_scene.bloom_clamp_mix_bool = BoolProperty(
        name=OldEevee_Bloom_Names.Clamp_Mix,
        description=OldEevee_Bloom_Descr.clamp_mix,
        default=False
    )
    prop_scene.bloom_other_bool = BoolProperty(
        name=OldEevee_Bloom_Names.Other,
        description=OldEevee_Bloom_Descr.other,
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