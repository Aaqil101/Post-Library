# Blender Modules
import bpy
from bpy.types import NodeTree

# Helper Modules
from helpers import Color


# initialize Vignette node group
def vignette_node_group(context, operator, group_name, image_path) -> None | NodeTree:
    # enable use nodes
    bpy.context.scene.use_nodes = True

    vignette = bpy.data.node_groups.new(group_name, "CompositorNodeTree")

    vignette.color_tag = "FILTER"
    vignette.default_group_node_width = 140
    vignette.description = "A custom node group for vignette effect"

    # vignette interface
    # Socket image
    image_socket = vignette.interface.new_socket(
        name="image", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = "POINT"

    # Socket Image
    image_socket = vignette.interface.new_socket(
        name="Image", in_out="INPUT", socket_type="NodeSocketColor"
    )
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = "POINT"

    # Socket Fac
    fac_socket = vignette.interface.new_socket(
        name="Fac", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    fac_socket.default_value = 0.0
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = "FACTOR"
    fac_socket.attribute_domain = "POINT"

    # initialize vignette nodes
    # node VIG Group Output
    vig_group_output = vignette.nodes.new("NodeGroupOutput")
    vig_group_output.label = "VIG Group Output"
    vig_group_output.name = "VIG Group Output"
    vig_group_output.use_custom_color = True
    vig_group_output.color = Color.DARK_GRAY
    vig_group_output.is_active_output = True
    vig_group_output.inputs[1].hide = True

    # node VIG Group Input
    vig_group_input = vignette.nodes.new("NodeGroupInput")
    vig_group_input.label = "VIG Group Input"
    vig_group_input.name = "VIG Group Input"
    vig_group_input.use_custom_color = True
    vig_group_input.color = Color.DARK_GRAY
    vig_group_input.outputs[2].hide = True

    # node image_vignette
    image_vignette = vignette.nodes.new("CompositorNodeImage")
    image_vignette.label = "VIG Image"
    image_vignette.name = "Image Vignette"
    image_vignette.use_custom_color = True
    image_vignette.color = Color.LIGHT_RED
    image_vignette.frame_duration = 1
    image_vignette.frame_offset = 39
    image_vignette.frame_start = 1
    image_vignette.use_auto_refresh = True
    image_vignette.use_cyclic = False
    image_vignette.use_straight_alpha_output = False
    image_vignette.outputs[1].hide = True

    # Load the selected image and assign it to the image node
    try:
        image = bpy.data.images.load(image_path)
        # image.colorspace_settings.name = "ACEScg"
    except Exception as e:
        print("Error: unable to load image")
        print(e)

    if image is None:
        print("Error: image is null")
        return None

    image_vignette.image = image

    # node multiply_vignette
    multiply_vignette = vignette.nodes.new("CompositorNodeMixRGB")
    multiply_vignette.label = "VIG Multiply"
    multiply_vignette.name = "Multiply Vignette"
    multiply_vignette.use_custom_color = True
    multiply_vignette.color = Color.BROWN
    multiply_vignette.blend_type = "MULTIPLY"
    multiply_vignette.use_alpha = False
    multiply_vignette.use_clamp = False

    if image_vignette is None:
        print("Error: image_vignette is null")
        return None

    if vig_group_input is None:
        print("Error: group_input is null")
        return None

    if vig_group_output is None:
        print("Error: group_output is null")
        return None

    if multiply_vignette is None:
        print("Error: multiply_vignette is null")
        return None

    # Set locations
    vig_group_output.location = (77.98977661132812, 6.222320556640625)
    vig_group_input.location = (-291.3733215332031, -39.500518798828125)
    image_vignette.location = (-420.0, -128.50051879882812)
    multiply_vignette.location = (-94.09931945800781, 6.222320556640625)

    # Set dimensions
    vig_group_output.width, vig_group_output.height = 140.0, 100.0
    vig_group_input.width, vig_group_input.height = 140.0, 100.0
    image_vignette.width, image_vignette.height = 268.69482421875, 100.0
    multiply_vignette.width, multiply_vignette.height = 140.0, 100.0

    # initialize vignette links
    # image_vignette.Image -> multiply_vignette.Image
    try:
        vignette.links.new(image_vignette.outputs[0], multiply_vignette.inputs[2])
    except Exception as e:
        print(
            "Error: unable to create link between image_vignette and multiply_vignette"
        )
        print(e)

    # vig_group_input.Image -> multiply_vignette.Image
    try:
        vignette.links.new(vig_group_input.outputs[0], multiply_vignette.inputs[1])
    except Exception as e:
        print(
            "Error: unable to create link between vig_group_input and multiply_vignette"
        )
        print(e)

    # multiply_vignette.Image -> vig_group_output.image
    try:
        vignette.links.new(multiply_vignette.outputs[0], vig_group_output.inputs[0])
    except Exception as e:
        print(
            "Error: unable to create link between multiply_vignette and vig_group_output"
        )
        print(e)

    # vig_group_input.Fac -> multiply_vignette.Fac
    try:
        vignette.links.new(vig_group_input.outputs[1], multiply_vignette.inputs[0])
    except Exception as e:
        print(
            "Error: unable to create link between vig_group_input and multiply_vignette"
        )
        print(e)

    return vignette
