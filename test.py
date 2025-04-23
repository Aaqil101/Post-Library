from typing import Tuple

import bpy
from bpy.types import NodeTree


class COMP_PT_MAINPANEL(bpy.types.Panel):
    bl_label = "test"
    bl_idname = "COMP_PT_MAINPANEL"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "T"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("node.bloom_operator", text="Test", icon="IMAGE_RGB")


def hexcode_to_rgb(hexcode: str) -> Tuple[float]:
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB

    Supports: "#RRGGBB" or "RRGGBB"

    Note: We are converting into Linear RGB since Blender uses a Linear Color Space internally
    https://docs.blender.org/manual/en/latest/render/color_management.html
    """
    # remove the leading '#' symbol if present
    if hexcode.startswith("#"):
        hexcode = hexcode[1:]

    assert len(hexcode) == 6, f"RRGGBB is the supported hex color format: {hexcode}"

    # extracting the Red color component - RRxxxx
    red = int(hexcode[:2], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_red: float = red / 255

    # extracting the Green color component - xxGGxx
    green = int(hexcode[2:4], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_green: float = green / 255

    # extracting the Blue color component - xxxxBB
    blue = int(hexcode[4:6], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_blue: float = blue / 255

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
    r: int = min(r1 + r2, 255)
    g: int = min(g1 + g2, 255)
    b: int = min(b1 + b2, 255)

    # Combine the components back into a hex color
    return f"{r:02X}{g:02X}{b:02X}"


class Color:
    """
    Class to store color values converted from hex codes to RGB

    Example:
        Import the Color class

        Color.LIGHT_RED
    """

    LIGHT_RED: Tuple[float] = hexcode_to_rgb("#94493E")
    DARK_RED: Tuple[float] = hexcode_to_rgb("#823A35")
    LIGHT_BLUE: Tuple[float] = hexcode_to_rgb("#646E66")
    DARK_BLUE: Tuple[float] = hexcode_to_rgb("#4C6160")
    LIGHT_PURPLE: Tuple[float] = hexcode_to_rgb("#846167")
    DARK_PURPLE: Tuple[float] = hexcode_to_rgb("#77535F")
    BROWN: Tuple[float] = hexcode_to_rgb("#866937")
    DARK_GRAY: Tuple[float] = hexcode_to_rgb("#3C3937")
    LIGHT_GRAY: Tuple[float] = hexcode_to_rgb("#59514B")


# initialize Bloom node group
def bloom_node_group(context, operator, group_name) -> NodeTree:
    # enable use nodes
    bpy.context.scene.use_nodes = True

    bloom = bpy.data.node_groups.new(group_name, "CompositorNodeTree")

    bloom.color_tag = "FILTER"
    bloom.description = "Simulates the soft glow around bright areas due to light scattering in eyes and camera lenses"
    bloom.default_group_node_width = 168

    # bloom interface
    # Socket Image
    image_socket = bloom.interface.new_socket(
        name="Image", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    image_socket.default_value = (
        0.8,
        0.8,
        0.8,
        1.0,
    )
    image_socket.attribute_domain = "POINT"
    image_socket.description = "Standard color output"

    # Socket Image
    image_socket_1 = bloom.interface.new_socket(
        name="Image", in_out="INPUT", socket_type="NodeSocketColor"
    )
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = "POINT"
    image_socket_1.description = "Standard color input"

    # Socket Quality
    quality_socket = bloom.interface.new_socket(
        name="Quality", in_out="INPUT", socket_type="NodeSocketInt"
    )
    quality_socket.default_value = 2
    quality_socket.min_value = 0
    quality_socket.max_value = 2
    quality_socket.subtype = "NONE"
    quality_socket.attribute_domain = "POINT"
    quality_socket.description = (
        "Controls the resolution at which the bloom effect is processed. "
        "This can help save render times during preview renders.\n\n"
        "Quality levels:\n"
        "   0 - High\n"
        "   1 - Medium\n"
        "   2 - Low"
    )

    # Socket Threshold
    threshold_socket = bloom.interface.new_socket(
        name="Threshold", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    threshold_socket.default_value = 1.0
    threshold_socket.min_value = 0.0
    threshold_socket.max_value = 3.4
    threshold_socket.subtype = "NONE"
    threshold_socket.attribute_domain = "POINT"
    threshold_socket.description = "Defines the minimum luminance required for an area to contribute to the glare effect. Lower values include more areas, while higher values restrict glare to the brightest regions"

    # Socket Knee
    knee_socket = bloom.interface.new_socket(
        name="Knee", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    knee_socket.default_value = 0.0
    knee_socket.min_value = 0.0
    knee_socket.max_value = 1.0
    knee_socket.subtype = "FACTOR"
    knee_socket.attribute_domain = "POINT"
    knee_socket.description = "Makes transition between under/over-threshold gradual"

    # Socket Radius
    radius_socket = bloom.interface.new_socket(
        name="Radius", in_out="INPUT", socket_type="NodeSocketInt"
    )
    radius_socket.default_value = 0
    radius_socket.min_value = 0
    radius_socket.max_value = 2048
    radius_socket.subtype = "NONE"
    radius_socket.attribute_domain = "POINT"
    radius_socket.description = "Bloom spread distance"

    # Socket Color
    color_socket = bloom.interface.new_socket(
        name="Color", in_out="INPUT", socket_type="NodeSocketColor"
    )
    color_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    color_socket.attribute_domain = "POINT"
    color_socket.description = "Color applied to the bloom effect"

    # Socket Intensity
    intensity_socket = bloom.interface.new_socket(
        name="Intensity", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    intensity_socket.default_value = 1.0
    intensity_socket.min_value = 0.0
    intensity_socket.max_value = 1.0
    intensity_socket.subtype = "FACTOR"
    intensity_socket.attribute_domain = "POINT"
    intensity_socket.description = "Blend factor"

    # Socket Clamp
    clamp_socket = bloom.interface.new_socket(
        name="Clamp", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    clamp_socket.default_value = 0.0
    clamp_socket.min_value = 0.0
    clamp_socket.max_value = 10.0
    clamp_socket.subtype = "FACTOR"
    clamp_socket.attribute_domain = "POINT"
    clamp_socket.description = "Maximum intensity a bloom pixel can have"

    # Socket Size
    size_socket = bloom.interface.new_socket(
        name="Size", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    size_socket.default_value = 0.5
    size_socket.min_value = 0.0
    size_socket.max_value = 1.0
    size_socket.subtype = "FACTOR"
    size_socket.attribute_domain = "POINT"
    size_socket.description = "Defines the relative spread of the glare across the image. A value of 1 makes the glare cover the full image, while 0.5 restricts it to half, and so on"

    # initialize bloom nodes
    # node Group Output
    group_output = bloom.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.use_custom_color = True
    group_output.color = Color.DARK_GRAY

    # Group Output settings
    group_output.is_active_output = True
    group_output.inputs[1].hide = True

    # node Main Bloom
    main_bloom = bloom.nodes.new("CompositorNodeGlare")
    main_bloom.label = "Main Bloom"
    main_bloom.name = "Main Bloom"

    # Bloom settings
    main_bloom.glare_type = "BLOOM"
    main_bloom.quality = "LOW"
    main_bloom.inputs[1].default_value = 1.0  # Highlights Threshold
    main_bloom.inputs[2].default_value = 0.1  # Highlights Smoothness
    main_bloom.inputs[3].default_value = 0.0  # Maximum Highlights
    main_bloom.inputs[4].default_value = 1.0  # Strength
    main_bloom.inputs[5].default_value = 1.0  # Saturation
    main_bloom.inputs[6].default_value = (1.0, 1.0, 1.0, 1.0)  # Tint
    main_bloom.inputs[7].default_value = 0.5  # Size

    main_bloom.use_custom_color = True
    main_bloom.color = Color.DARK_PURPLE
    main_bloom.inputs[2].hide = True
    main_bloom.inputs[3].hide = True
    main_bloom.inputs[4].hide = True
    main_bloom.inputs[5].hide = True
    main_bloom.inputs[6].hide = True
    main_bloom.inputs[8].hide = True
    main_bloom.inputs[9].hide = True
    main_bloom.inputs[10].hide = True
    main_bloom.inputs[11].hide = True
    main_bloom.inputs[12].hide = True
    main_bloom.outputs[0].hide = True
    main_bloom.outputs[2].hide = True

    # node Color
    color = bloom.nodes.new("CompositorNodeMixRGB")
    color.label = "Color"
    color.name = "Color"
    color.use_custom_color = True
    color.color = Color.BROWN

    # Color settings
    color.blend_type = "COLOR"
    color.use_alpha = False
    color.use_clamp = False
    color.inputs[0].hide = True
    color.inputs[0].default_value = 1.0  # Fac

    # node Blur
    blur = bloom.nodes.new("CompositorNodeBlur")
    blur.label = "Blur"
    blur.name = "Blur"
    blur.use_custom_color = True
    blur.color = Color.DARK_PURPLE

    # Blur settings
    blur.filter_type = "FAST_GAUSS"
    blur.size_x = 0
    blur.size_y = 0
    blur.use_extended_bounds = False
    blur.use_relative = False
    blur.inputs[1].hide = True
    blur.inputs[1].default_value = 1.0  # Size

    # node Blur Mix
    blur_mix = bloom.nodes.new("CompositorNodeMixRGB")
    blur_mix.label = "Blur Mix"
    blur_mix.name = "Blur Mix"
    blur_mix.use_custom_color = True
    blur_mix.color = Color.BROWN

    # Blur Mix settings
    blur_mix.blend_type = "SCREEN"
    blur_mix.use_alpha = False
    blur_mix.use_clamp = False
    blur_mix.inputs[0].hide = True
    blur_mix.inputs[0].default_value = 1.0  # Fac

    # node Intensity
    intensity = bloom.nodes.new("CompositorNodeMixRGB")
    intensity.label = "Intensity"
    intensity.name = "Intensity"
    intensity.use_custom_color = True
    intensity.color = Color.BROWN

    # Intensity settings
    intensity.blend_type = "ADD"
    intensity.use_alpha = False
    intensity.use_clamp = False

    # node Knee Bloom
    knee_bloom = bloom.nodes.new("CompositorNodeGlare")
    knee_bloom.label = "Knee Bloom"
    knee_bloom.name = "Knee Bloom"
    knee_bloom.use_custom_color = True
    knee_bloom.color = Color.DARK_PURPLE

    # Knee Bloom settings
    knee_bloom.glare_type = "BLOOM"
    knee_bloom.quality = "LOW"
    knee_bloom.inputs[1].default_value = 0.0  # Highlights Threshold
    knee_bloom.inputs[2].default_value = 0.1  # Highlights Smoothness
    knee_bloom.inputs[3].default_value = 0.0  # Maximum Highlights
    knee_bloom.inputs[4].default_value = 8.0  # Strength
    knee_bloom.inputs[5].default_value = 1.0  # Saturation
    knee_bloom.inputs[6].default_value = (1.0, 1.0, 1.0, 1.0)  # Tint
    knee_bloom.inputs[7].default_value = 1.0  # Size

    knee_bloom.inputs[1].hide = True
    knee_bloom.inputs[2].hide = True
    knee_bloom.inputs[3].hide = True
    knee_bloom.inputs[4].hide = True
    knee_bloom.inputs[5].hide = True
    knee_bloom.inputs[6].hide = True
    knee_bloom.inputs[7].hide = True
    knee_bloom.inputs[8].hide = True
    knee_bloom.inputs[9].hide = True
    knee_bloom.inputs[10].hide = True
    knee_bloom.inputs[11].hide = True
    knee_bloom.inputs[12].hide = True
    knee_bloom.outputs[0].hide = True
    knee_bloom.outputs[2].hide = True

    # node Knee Mix
    knee_mix = bloom.nodes.new("CompositorNodeMixRGB")
    knee_mix.label = "Knee Mix"
    knee_mix.name = "Knee Mix"
    knee_mix.use_custom_color = True
    knee_mix.color = Color.BROWN

    # Knee Mix settings
    knee_mix.blend_type = "ADD"
    knee_mix.use_alpha = False
    knee_mix.use_clamp = False

    # node Group Input 001
    group_input_001 = bloom.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input 001"
    group_input_001.use_custom_color = True
    group_input_001.color = Color.DARK_GRAY
    group_input_001.outputs[0].hide = True
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[3].hide = True
    group_input_001.outputs[4].hide = True
    group_input_001.outputs[5].hide = True
    group_input_001.outputs[6].hide = True
    group_input_001.outputs[8].hide = True
    group_input_001.outputs[9].hide = True

    # node Clamp
    clamp = bloom.nodes.new("CompositorNodeExposure")
    clamp.label = "Clamp"
    clamp.name = "Clamp"
    clamp.use_custom_color = True
    clamp.color = Color.BROWN

    # node Invert Color
    invert_color = bloom.nodes.new("CompositorNodeInvert")
    invert_color.label = "Invert Color"
    invert_color.name = "Invert Color"
    invert_color.use_custom_color = True
    invert_color.color = Color.BROWN

    # Invert Color settings
    invert_color.invert_alpha = False
    invert_color.invert_rgb = True
    invert_color.inputs[0].hide = True
    invert_color.inputs[0].default_value = 1.0  # Fac

    # node Group Input 002
    group_input_002 = bloom.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input 002"
    group_input_002.use_custom_color = True
    group_input_002.color = Color.DARK_GRAY
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[3].hide = True
    group_input_002.outputs[4].hide = True
    group_input_002.outputs[5].hide = True
    group_input_002.outputs[6].hide = True
    group_input_002.outputs[7].hide = True
    group_input_002.outputs[9].hide = True

    # node Group Input 003
    group_input_003 = bloom.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input 003"
    group_input_003.use_custom_color = True
    group_input_003.color = Color.DARK_GRAY
    group_input_003.outputs[1].hide = True
    group_input_003.outputs[2].hide = True
    group_input_003.outputs[3].hide = True
    group_input_003.outputs[4].hide = True
    group_input_003.outputs[5].hide = True
    group_input_003.outputs[6].hide = True
    group_input_003.outputs[7].hide = True
    group_input_003.outputs[8].hide = True
    group_input_003.outputs[9].hide = True

    # node Group Input 004
    group_input_004 = bloom.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input 004"
    group_input_004.use_custom_color = True
    group_input_004.color = Color.DARK_GRAY
    group_input_004.outputs[0].hide = True
    group_input_004.outputs[1].hide = True
    group_input_004.outputs[2].hide = True
    group_input_004.outputs[4].hide = True
    group_input_004.outputs[5].hide = True
    group_input_004.outputs[6].hide = True
    group_input_004.outputs[7].hide = True
    group_input_004.outputs[8].hide = True
    group_input_004.outputs[9].hide = True

    # node Group Input 05
    group_input_005 = bloom.nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input 005"
    group_input_005.use_custom_color = True
    group_input_005.color = Color.DARK_GRAY
    group_input_005.outputs[0].hide = True
    group_input_005.outputs[1].hide = True
    group_input_005.outputs[2].hide = True
    group_input_005.outputs[3].hide = True
    group_input_005.outputs[4].hide = True
    group_input_005.outputs[6].hide = True
    group_input_005.outputs[7].hide = True
    group_input_005.outputs[8].hide = True
    group_input_005.outputs[9].hide = True

    # node Group Input 006
    group_input_006 = bloom.nodes.new("NodeGroupInput")
    group_input_006.name = "Group Input 006"
    group_input_006.use_custom_color = True
    group_input_006.color = Color.DARK_GRAY
    group_input_006.outputs[1].hide = True
    group_input_006.outputs[2].hide = True
    group_input_006.outputs[3].hide = True
    group_input_006.outputs[4].hide = True
    group_input_006.outputs[5].hide = True
    group_input_006.outputs[7].hide = True
    group_input_006.outputs[8].hide = True
    group_input_006.outputs[9].hide = True

    # node Image
    image = bloom.nodes.new("NodeReroute")
    image.label = "Image"
    image.name = "Image"
    image.socket_idname = "NodeSocketColor"

    # node Blurring
    blurring = bloom.nodes.new("NodeReroute")
    blurring.label = "Blurring"
    blurring.name = "Blurring"
    blurring.socket_idname = "NodeSocketColor"

    # Set locations
    group_output.location = (650.0, -16.0)
    main_bloom.location = (-760.0, -100.0)
    color.location = (110.0, 73.0)
    blur.location = (-540.0, 40.0)
    blur_mix.location = (-300.0, 20.0)
    intensity.location = (490.0, -16.0)
    knee_bloom.location = (-540.0, 176.0)
    knee_mix.location = (-80.0, 73.0)
    group_input_001.location = (290.0, -175.0)
    clamp.location = (290.0, 73.0)
    invert_color.location = (290.0, -39.0)
    group_input_002.location = (-960.0, -200.0)
    group_input_003.location = (-540.0, 243.0)
    group_input_004.location = (-80.0, 140.0)
    group_input_005.location = (110.0, -85.0)
    group_input_006.location = (490.0, 73.0)
    image.location = (-540.0, -180.0)
    blurring.location = (-380.0, -180.0)

    # Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    main_bloom.width, main_bloom.height = 160.0, 100.0
    color.width, color.height = 140.0, 100.0
    blur.width, blur.height = 140.0, 100.0
    blur_mix.width, blur_mix.height = 140.0, 100.0
    intensity.width, intensity.height = 140.0, 100.0
    knee_bloom.width, knee_bloom.height = 140.0, 100.0
    knee_mix.width, knee_mix.height = 140.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    clamp.width, clamp.height = 140.0, 100.0
    invert_color.width, invert_color.height = 140.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0
    group_input_003.width, group_input_003.height = 140.0, 100.0
    group_input_004.width, group_input_004.height = 140.0, 100.0
    group_input_005.width, group_input_005.height = 140.0, 100.0
    group_input_006.width, group_input_006.height = 140.0, 100.0
    image.width, image.height = 10.0, 100.0
    blurring.width, blurring.height = 10.0, 100.0

    # initialize bloom links
    # knee_mix.Image -> color.Image
    bloom.links.new(knee_mix.outputs[0], color.inputs[1])

    # blur_mix.Image -> knee_mix.Image
    bloom.links.new(blur_mix.outputs[0], knee_mix.inputs[1])

    # clamp.Image -> intensity.Image
    bloom.links.new(clamp.outputs[0], intensity.inputs[2])

    # main_bloom.Glare -> blur.Image
    bloom.links.new(main_bloom.outputs[1], blur.inputs[0])

    # intensity.Image -> group_output.Image
    bloom.links.new(intensity.outputs[0], group_output.inputs[0])

    # blurring.Output -> blur_mix.Image
    bloom.links.new(blurring.outputs[0], blur_mix.inputs[2])

    # blur.Image -> blur_mix.Image
    bloom.links.new(blur.outputs[0], blur_mix.inputs[1])

    # color.Image -> clamp.Image
    bloom.links.new(color.outputs[0], clamp.inputs[0])

    # invert_color.Color -> clamp.Exposure
    bloom.links.new(invert_color.outputs[0], clamp.inputs[1])

    # group_input_001.Clamp -> invert_color.Color
    bloom.links.new(group_input_001.outputs[7], invert_color.inputs[1])

    # knee_bloom.Glare -> knee_mix.Image
    bloom.links.new(knee_bloom.outputs[1], knee_mix.inputs[2])

    # group_input_002.Image -> main_bloom.Image
    bloom.links.new(group_input_002.outputs[0], main_bloom.inputs[0])

    # group_input_002.Threshold -> main_bloom.Threshold
    bloom.links.new(group_input_002.outputs[2], main_bloom.inputs[1])

    # group_input_002.Size -> main_bloom.Size
    bloom.links.new(group_input_002.outputs[8], main_bloom.inputs[7])

    # group_input_003.Image -> knee_bloom.Image
    bloom.links.new(group_input_003.outputs[0], knee_bloom.inputs[0])

    # group_input_004.Knee -> knee_mix.Fac
    bloom.links.new(group_input_004.outputs[3], knee_mix.inputs[0])

    # group_input_005.Color -> color.Image
    bloom.links.new(group_input_005.outputs[5], color.inputs[2])

    # group_input_006.Image -> intensity.Image
    bloom.links.new(group_input_006.outputs[0], intensity.inputs[1])

    # group_input_006.Intensity -> intensity.Fac
    bloom.links.new(group_input_006.outputs[6], intensity.inputs[0])

    # main_bloom.Glare -> image.Input
    bloom.links.new(main_bloom.outputs[1], image.inputs[0])

    # image.Output -> blurring.Input
    bloom.links.new(image.outputs[0], blurring.inputs[0])

    return bloom


class NodeDriverManager:
    """
    Class to manage drivers on a node group.

    Can be used to create drivers on a node group and link them to a specific
    ID type and path.

    :param node_group: The node group to modify
    :type node_group: bpy.types.NodeGroup

    :param id_type: The type of object to link to
    :type id_type: str

    :param id: The object to link to
    :type id: bpy.types.ID

    :param var_name: The name of the variable to create
    :type var_name: str

    :param driver_type: The type of driver to create
    :type driver_type: str
    """

    def __init__(
        self,
        *,
        node_group: str,
        id_type: str,
        id: bpy.types.ID,
        var_name="default_value",
        driver_type="AVERAGE",
    ):
        """
        Constructor for NodeDriverManager

        :param node_group: The node group to modify
        :type node_group: bpy.types.NodeGroup

        :param id_type: The type of object to link to
        :type id_type: str

        :param id: The object to link to
        :type id: bpy.types.ID

        :param var_name: The name of the variable to create
        :type var_name: str

        :param driver_type: The type of driver to create
        :type driver_type: str
        """
        if not isinstance(id, bpy.types.ID):
            raise TypeError("The 'id' must be of type 'bpy.types.ID'")
        self.node_group = node_group
        self.var_name = var_name
        self.driver_type = driver_type
        self.id_type = id_type
        self.id = id
        self.driver = None

    def add_driver(self, *, node_name: str, socket_name: str):
        """
        Adds a driver to a specified node and socket within the node group.

        :param node_name: The name of the node to which the driver will be added.
        :type node_name: str

        :param socket_name: The name of the socket on the node where the driver will be added.
        :type socket_name: str

        :raises ValueError: If the node with the specified name is not found.

        :return: The created driver.
        :rtype: bpy.types.Driver
        """
        node = self.node_group.node_tree.nodes.get(node_name)
        if node is None:
            raise ValueError(f"Node with name {node_name} not found.")
        else:
            self.driver = node.driver_add(socket_name).driver
            self.driver.type = self.driver_type
            return self.driver

    def add_driver_var(self, number: int):
        """
        Adds a variable to the driver associated with the node group.

        This function creates a new variable in the driver and sets its data path
        to point to the default value of the specified input number in the node group.

        Args:
            number (int): The index of the input in the node group whose default value
            will be linked to the driver variable.

        Raises:
            ValueError: If the driver is not initialized or if the input number is out of range.

        Returns:
            bpy.types.DriverVariable: The created driver variable.
        """
        if self.driver is None:
            raise ValueError("Driver not initialized. Call add_driver first.")
        if number < 0 or number >= len(self.node_group.inputs):
            raise ValueError(f"Input number {number} is out of range.")
        driver_var = self.driver.variables.new()
        driver_var.name = self.var_name
        driver_var.targets[0].id_type = self.id_type
        driver_var.targets[0].id = self.id
        driver_var.targets[0].data_path = (
            f'node_tree.nodes["{self.node_group.name}"].inputs[{number}].default_value'
        )
        return driver_var


class NODE_OT_BLOOM(bpy.types.Operator):
    bl_label = "Bloom"
    bl_idname = "node.bloom_operator"
    bl_description = "Replication of the legacy eevee bloom option, but can be used in cycles as well"

    def execute(shelf, context) -> set[str]:

        custom_bloom_node_name = "Bloom"
        bloom_group = bloom_node_group(shelf, context, custom_bloom_node_name)
        bloom_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        bloom_node.name = "Bloom"
        bloom_node.label = "Bloom"
        bloom_node.width = 168
        bloom_node.node_tree = bpy.data.node_groups[bloom_group.name]
        bloom_node.use_custom_color = True
        bloom_node.color = Color.DARK_PURPLE
        bloom_node.select = False

        """
        * The ability to add drivers to nodes is made possible by Victor Stepanov
        * (https://www.skool.com/cgpython/how-to-add-drivers-to-node-group-sockets-using-python?p=0be0f439)
        * (https://www.skool.com/cgpython/how-do-i-add-the-drivers-to-a-node-group-every-time?p=4220eddf)
        * His youtube channel (https://www.youtube.com/@CGPython)
        """

        # Initialize NodeDriverManager to manage drivers for the node group
        drivers = NodeDriverManager(
            node_group=bloom_node, id_type="SCENE", id=bpy.context.scene
        )

        # Radius X
        drivers.add_driver(node_name="Blur", socket_name="size_x")
        drivers.add_driver_var(4)

        # Radius Y
        drivers.add_driver(node_name="Blur", socket_name="size_y")
        drivers.add_driver_var(4)

        # Main Bloom
        drivers.add_driver(node_name="Main Bloom", socket_name="quality")
        drivers.add_driver_var(1)

        # Knee Bloom
        drivers.add_driver(node_name="Knee Bloom", socket_name="quality")
        drivers.add_driver_var(1)

        return {"FINISHED"}


# Register and Unregister
classes = [COMP_PT_MAINPANEL, NODE_OT_BLOOM]


def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
