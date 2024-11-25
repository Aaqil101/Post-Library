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
        "GRAY": hexcode_to_rgb("#3C3937"),
    }

#initialize test node group
def test_node_group(context, operator, group_name):
    
    #enable use nodes
    bpy.context.scene.use_nodes = True

    test = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    test.color_tag = 'FILTER'
    test.description = ""
    test.default_group_node_width = 160
    

    #test interface
    #Socket Image
    image_socket = test.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket_1 = test.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'

    #Socket Socket
    socket_socket = test.interface.new_socket(name = "Socket", in_out='INPUT', socket_type = 'NodeSocketFloat')
    socket_socket.default_value = 0.0
    socket_socket.min_value = 0.0
    socket_socket.max_value = 1000.0
    socket_socket.subtype = 'NONE'
    socket_socket.attribute_domain = 'POINT'


    #initialize test nodes
    #node Group Output
    group_output = test.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.use_custom_color = True
    group_output.color = (0.23529097437858582, 0.2235269844532013, 0.21568608283996582)
    group_output.is_active_output = True

    #node Group Input
    group_input = test.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.use_custom_color = True
    group_input.color = (0.23529097437858582, 0.2235269844532013, 0.21568608283996582)

    #node Glare
    glare = test.nodes.new("CompositorNodeGlare")
    glare.name = "Glare"
    glare.use_custom_color = True
    glare.color = (0.4666634798049927, 0.32548609375953674, 0.37254956364631653)
    glare.angle_offset = 0.0
    glare.color_modulation = 0.25
    glare.fade = 0.8999999761581421
    glare.glare_type = 'BLOOM'
    glare.iterations = 3
    glare.mix = 0.0
    glare.quality = 'HIGH'
    glare.size = 8
    glare.streaks = 4
    glare.threshold = 1.0
    glare.use_rotate_45 = True


    #Set locations
    group_output.location = (180.0, 0.0)
    group_input.location = (-180.0, 0.0)
    glare.location = (0.0, 0.0)

    #Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    glare.width, glare.height = 149.0894775390625, 100.0

    #initialize test links
    #glare.Image -> group_output.Image
    test.links.new(glare.outputs[0], group_output.inputs[0])
    #group_input.Image -> glare.Image
    test.links.new(group_input.outputs[0], glare.inputs[0])
    return test

class NODE_OT_BLOOM(bpy.types.Operator):
    bl_label = "Bloom"
    bl_idname = "node.bloom_operator"

    def execute(shelf, context):

        custom_bloom_node_name = "Bloom"
        bloom_group = test_node_group(shelf, context, custom_bloom_node_name)
        bloom_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        bloom_node.node_tree = bpy.data.node_groups[bloom_group.name]
        bloom_node.use_custom_color = True
        bloom_node.color = COLORS_DICT["LIGHT_PURPLE"]
        bloom_node.select = False
        """ bpy.data.node_groups["Bloom"] = 'AVERAGE'
        bpy.data.node_groups["Bloom"] = "default_value"
        bpy.data.node_groups["Bloom"] = 'SCENE'
        bpy.data.node_groups["Bloom"] = bpy.data.scenes["Scene"]
        bpy.data.node_groups["Bloom"] = "node_tree.nodes[\"Group\"].inputs[2].default_value" """

        return {"FINISHED"}
    
# Register and unregister list variable
classes = [
    COMP_PT_MAINPANEL, NODE_OT_BLOOM
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()