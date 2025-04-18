# Blender Modules
import bpy
from bpy.types import NodeTree

# Helper Modules
from helpers import Color


# initialize FilmGrain node group
def file_film_grain_node_group(
    context, operator, group_name, image_path
) -> None | NodeTree:
    # enable use nodes
    bpy.context.scene.use_nodes = True

    file_film_grain = bpy.data.node_groups.new(group_name, "CompositorNodeTree")

    file_film_grain.color_tag = "FILTER"
    file_film_grain.default_group_node_width = 140
    file_film_grain.description = "A custom node group for film grain effect"

    # file_film_grain interface
    # Socket image
    image_socket = file_film_grain.interface.new_socket(
        name="image", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = "POINT"

    # Socket Image
    image_socket = file_film_grain.interface.new_socket(
        name="Image", in_out="INPUT", socket_type="NodeSocketColor"
    )
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = "POINT"

    # Socket Fac
    fac_socket = file_film_grain.interface.new_socket(
        name="Fac", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    fac_socket.default_value = 0.0
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = "FACTOR"
    fac_socket.attribute_domain = "POINT"

    # initialize file_film_grain nodes
    # node FG Group Output
    fg_group_output = file_film_grain.nodes.new("NodeGroupOutput")
    fg_group_output.label = "FG Group Output"
    fg_group_output.name = "FG Group Output"
    fg_group_output.use_custom_color = True
    fg_group_output.color = Color.DARK_GRAY
    fg_group_output.is_active_output = True
    fg_group_output.inputs[1].hide = True

    # node FG Group Input
    fg_group_input = file_film_grain.nodes.new("NodeGroupInput")
    fg_group_input.label = "FG Group Input"
    fg_group_input.name = "FG Group Input"
    fg_group_input.use_custom_color = True
    fg_group_input.color = Color.DARK_GRAY
    fg_group_input.outputs[2].hide = True

    # node image_file_film_grain
    image_file_film_grain = file_film_grain.nodes.new("CompositorNodeImage")
    image_file_film_grain.label = "FG Image"
    image_file_film_grain.name = "image_ff_grain"
    image_file_film_grain.use_custom_color = True
    image_file_film_grain.color = Color.LIGHT_RED
    image_file_film_grain.frame_duration = 1
    image_file_film_grain.frame_offset = -1
    image_file_film_grain.frame_start = 1
    image_file_film_grain.use_auto_refresh = True
    image_file_film_grain.use_cyclic = False
    image_file_film_grain.use_straight_alpha_output = False
    image_file_film_grain.outputs[1].hide = True

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

    image_file_film_grain.image = image

    # node overlay_file_film_grain
    overlay_file_film_grain = file_film_grain.nodes.new("CompositorNodeMixRGB")
    overlay_file_film_grain.label = "FG Overlay"
    overlay_file_film_grain.name = "overlay_ff_grain"
    overlay_file_film_grain.use_custom_color = True
    overlay_file_film_grain.color = Color.BROWN
    overlay_file_film_grain.blend_type = "OVERLAY"
    overlay_file_film_grain.use_alpha = False
    overlay_file_film_grain.use_clamp = False

    if image_file_film_grain is None:
        print("Error: image_file_film_grain is null")
        return None

    if fg_group_input is None:
        print("Error: group_input is null")
        return None

    if fg_group_output is None:
        print("Error: group_output is null")
        return None

    if overlay_file_film_grain is None:
        print("Error: overlay_file_film_grain is null")
        return None

    # Set locations
    fg_group_output.location = (238.55990600585938, 67.29718780517578)
    fg_group_input.location = (-142.61561584472656, 19.61834716796875)
    image_file_film_grain.location = (-304.08319091796875, -69.38165283203125)
    overlay_file_film_grain.location = (54.53009033203125, 67.29718780517578)

    # Set dimensions
    fg_group_output.width, fg_group_output.height = 140.0, 100.0
    fg_group_input.width, fg_group_input.height = 140.0, 100.0
    image_file_film_grain.width, image_file_film_grain.height = 300.8544921875, 100.0
    overlay_file_film_grain.width, overlay_file_film_grain.height = 140.0, 100.0

    # initialize file_film_grain links
    # image_file_film_grain.Image -> overlay_file_film_grain.Image
    try:
        file_film_grain.links.new(
            image_file_film_grain.outputs[0], overlay_file_film_grain.inputs[2]
        )
    except Exception as e:
        print(
            "Error: unable to create link between image_file_film_grain and overlay_file_film_grain"
        )
        print(e)

    # fg_group_input.Image -> overlay_file_film_grain.Image
    try:
        file_film_grain.links.new(
            fg_group_input.outputs[0], overlay_file_film_grain.inputs[1]
        )
    except Exception as e:
        print(
            "Error: unable to create link between fg_group_input and overlay_file_film_grain"
        )
        print(e)

    # overlay_file_film_grain.Image -> fg_group_output.image
    try:
        file_film_grain.links.new(
            overlay_file_film_grain.outputs[0], fg_group_output.inputs[0]
        )
    except Exception as e:
        print(
            "Error: unable to create link between overlay_file_film_grain and group_output"
        )
        print(e)

    # fg_group_input.Fac -> overlay_file_film_grain.Fac
    try:
        file_film_grain.links.new(
            fg_group_input.outputs[1], overlay_file_film_grain.inputs[0]
        )
    except Exception as e:
        print(
            "Error: unable to create link between fg_group_input and overlay_file_film_grain"
        )
        print(e)

    return file_film_grain
