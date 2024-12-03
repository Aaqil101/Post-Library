import bpy, mathutils

class COMP_PT_MAINPANEL(bpy.types.Panel):
    bl_label = "test"
    bl_idname = "COMP_PT_MAINPANEL"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "T"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("node.halation_operator", icon="IMAGE_RGB")

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
        "LIGHT_GRAY": hexcode_to_rgb("#59514B")
    }

#initialize Halation node group
def halation_node_group(context, operator, group_name):
    #enable use nodes
    bpy.context.scene.use_nodes = True

    halation = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    halation.color_tag = 'FILTER'
    halation.description = "Halation is a color grading filter that adds a warm glow around the edges of the frame, giving it a retro look."
    halation.default_group_node_width = 151

    #halation interface
    #Socket Image
    image_socket = halation.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'
    image_socket.hide_value = True

    #Socket Image
    image_socket_1 = halation.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'

    #Socket Size X
    size_x_socket = halation.interface.new_socket(name = "Size X", in_out='INPUT', socket_type = 'NodeSocketFloat')
    size_x_socket.default_value = 20.0
    size_x_socket.min_value = 0.0
    size_x_socket.max_value = 2048.0
    size_x_socket.subtype = 'NONE'
    size_x_socket.attribute_domain = 'POINT'

    #Socket Size Y
    size_y_socket = halation.interface.new_socket(name = "Size Y", in_out='INPUT', socket_type = 'NodeSocketFloat')
    size_y_socket.default_value = 20.0
    size_y_socket.min_value = 0.0
    size_y_socket.max_value = 2048.0
    size_y_socket.subtype = 'NONE'
    size_y_socket.attribute_domain = 'POINT'

    #Socket Fac
    fac_socket = halation.interface.new_socket(name = "Fac", in_out='INPUT', socket_type = 'NodeSocketFloat')
    fac_socket.default_value = 1.0
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = 'FACTOR'
    fac_socket.attribute_domain = 'POINT'
    fac_socket.description = "Color Balance Factor"

    #initialize halation nodes
    #node H Group Output
    h_group_output = halation.nodes.new("NodeGroupOutput")
    h_group_output.label = "H Group Output"
    h_group_output.name = "H Group Output"
    h_group_output.use_custom_color = True
    h_group_output.color = COLORS_DICT["DARK_GRAY"]
    h_group_output.is_active_output = True
    h_group_output.inputs[1].hide = True

    #node H Group Input
    h_group_input = halation.nodes.new("NodeGroupInput")
    h_group_input.label = "H Group Input"
    h_group_input.name = "H Group Input"
    h_group_input.use_custom_color = True
    h_group_input.color = COLORS_DICT["DARK_GRAY"]
    h_group_input.outputs[1].hide = True
    h_group_input.outputs[2].hide = True
    h_group_input.outputs[4].hide = True

    #node H Blur
    h_blur = halation.nodes.new("CompositorNodeBlur")
    h_blur.label = "H Blur"
    h_blur.name = "H Blur"
    h_blur.use_custom_color = True
    h_blur.color = COLORS_DICT["DARK_PURPLE"]
    h_blur.aspect_correction = 'NONE'
    h_blur.factor = 0.0
    h_blur.factor_x = 0.0
    h_blur.factor_y = 0.0
    h_blur.filter_type = 'GAUSS'
    h_blur.size_x = 20
    h_blur.size_y = 20
    h_blur.use_bokeh = False
    h_blur.use_extended_bounds = False
    h_blur.use_gamma_correction = False
    h_blur.use_relative = False
    h_blur.use_variable_size = True

    #node H Combine Color
    h_combine_color = halation.nodes.new("CompositorNodeCombineColor")
    h_combine_color.label = "H Combine Color"
    h_combine_color.name = "H Combine Color"
    h_combine_color.use_custom_color = True
    h_combine_color.color = COLORS_DICT["DARK_BLUE"]
    h_combine_color.mode = 'RGB'
    h_combine_color.ycc_mode = 'ITUBT709'
    #Alpha
    h_combine_color.inputs[3].default_value = 1.0

    #node H Separate Color
    h_separate_color = halation.nodes.new("CompositorNodeSeparateColor")
    h_separate_color.label = "H Separate Color"
    h_separate_color.name = "H Separate Color"
    h_separate_color.use_custom_color = True
    h_separate_color.color = COLORS_DICT["DARK_BLUE"]
    h_separate_color.mode = 'RGB'
    h_separate_color.ycc_mode = 'ITUBT709'

    #node H Color Ramp
    h_color_ramp = halation.nodes.new("CompositorNodeValToRGB")
    h_color_ramp.label = "H Color Ramp"
    h_color_ramp.name = "H Color Ramp"
    h_color_ramp.use_custom_color = True
    h_color_ramp.color = COLORS_DICT["DARK_BLUE"]
    h_color_ramp.color_ramp.color_mode = 'RGB'
    h_color_ramp.color_ramp.hue_interpolation = 'NEAR'
    h_color_ramp.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    h_color_ramp.color_ramp.elements.remove(h_color_ramp.color_ramp.elements[0])
    h_color_ramp_cre_0 = h_color_ramp.color_ramp.elements[0]
    h_color_ramp_cre_0.position = 0.0
    h_color_ramp_cre_0.alpha = 1.0
    h_color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    h_color_ramp_cre_1 = h_color_ramp.color_ramp.elements.new(1.0)
    h_color_ramp_cre_1.alpha = 1.0
    h_color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    #node H Color Balance
    h_color_balance = halation.nodes.new("CompositorNodeColorBalance")
    h_color_balance.label = "H Color Balance"
    h_color_balance.name = "H Color Balance"
    h_color_balance.use_custom_color = True
    h_color_balance.color = COLORS_DICT["BROWN"]
    h_color_balance.correction_method = 'LIFT_GAMMA_GAIN'
    h_color_balance.gain = mathutils.Color((1.0625041723251343, 0.9746971726417542, 0.9597135186195374))
    h_color_balance.gamma = mathutils.Color((1.0547555685043335, 0.9844463467597961, 0.95830899477005))
    h_color_balance.lift = mathutils.Color((1.0, 1.0, 1.0))

    #Set locations
    h_group_output.location = (1060.0, -120.0)
    h_group_input.location = (-820.0, -240.0)
    h_blur.location = (90.0, 120.0)
    h_combine_color.location = (430.0, -120.0)
    h_separate_color.location = (-630.0, -120.0)
    h_color_ramp.location = (-250.0, 120.0)
    h_color_balance.location = (630.0, -120.0)

    #Set dimensions
    h_group_output.width, h_group_output.height = 140.0, 100.0
    h_group_input.width, h_group_input.height = 140.0, 100.0
    h_blur.width, h_blur.height = 140.0, 100.0
    h_combine_color.width, h_combine_color.height = 140.0, 100.0
    h_separate_color.width, h_separate_color.height = 140.0, 100.0
    h_color_ramp.width, h_color_ramp.height = 240.0, 100.0
    h_color_balance.width, h_color_balance.height = 400.0, 100.0

    #initialize halation links
    #h_separate_color.Red -> h_color_ramp.Fac
    halation.links.new(h_separate_color.outputs[0], h_color_ramp.inputs[0])

    #h_separate_color.Red -> h_blur.Image
    halation.links.new(h_separate_color.outputs[0], h_blur.inputs[0])

    #h_combine_color.Image -> h_color_balance.Image
    halation.links.new(h_combine_color.outputs[0], h_color_balance.inputs[1])

    #h_separate_color.Blue -> h_combine_color.Blue
    halation.links.new(h_separate_color.outputs[2], h_combine_color.inputs[2])

    #h_separate_color.Green -> h_combine_color.Green
    halation.links.new(h_separate_color.outputs[1], h_combine_color.inputs[1])

    #h_blur.Image -> h_combine_color.Red
    halation.links.new(h_blur.outputs[0], h_combine_color.inputs[0])

    #h_color_balance.Image -> h_group_output.Image
    halation.links.new(h_color_balance.outputs[0], h_group_output.inputs[0])

    #h_group_input.Image -> h_separate_color.Image
    halation.links.new(h_group_input.outputs[0], h_separate_color.inputs[0])

    #h_color_ramp.Image -> h_blur.Size
    halation.links.new(h_color_ramp.outputs[0], h_blur.inputs[1])

    #h_group_input.Fac -> h_color_balance.Fac
    halation.links.new(h_group_input.outputs[3], h_color_balance.inputs[0])

    return halation

class NODE_OT_HALATION(bpy.types.Operator):
    bl_label = "Halation"
    bl_idname = "node.halation_operator"
    bl_description = "This node group is used to add halation to an image."

    def execute(shelf, context):

        custom_halation_node_name = "Halation"
        halation_group = halation_node_group(shelf, context, custom_halation_node_name)
        halation_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        halation_node.name = "Halation"
        halation_node.width = 151
        halation_node.node_tree = bpy.data.node_groups[halation_group.name]
        halation_node.use_custom_color = True
        halation_node.color = COLORS_DICT["DARK_PURPLE"]
        halation_node.select = False
        
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
        
        # H Blur Size X
        h_blur_size_x_driver = halation_node.node_tree.nodes['H Blur'].driver_add('size_x').driver
        h_blur_size_x_driver.type = "AVERAGE"
        add_driver_var(
            h_blur_size_x_driver,
            f'node_tree.nodes["{halation_node.name}"].inputs[1].default_value'
        )

        # H Blur Size Y
        h_blur_size_y_driver = halation_node.node_tree.nodes['H Blur'].driver_add('size_y').driver
        h_blur_size_y_driver.type = "AVERAGE"
        add_driver_var(
            h_blur_size_y_driver,
            f'node_tree.nodes["{halation_node.name}"].inputs[2].default_value'
        )

        return {'FINISHED'}
    
# Register and unregister
classes = [COMP_PT_MAINPANEL, NODE_OT_HALATION]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()