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
        row.operator("node.multiexposure_operator", icon="IMAGE_RGB")

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

class NODE_OT_MULTIEXPOSURE(bpy.types.Operator):
    bl_label = "MultiExposure"
    bl_idname = "node.multiexposure_operator"
    bl_description = "This node group is used to create a multiexposure."

    def execute(shelf, context):

        custom_multiexposure_node_name = "MultiExposure"
        multiexposure_group = multiexposure_node_group(shelf, context, custom_multiexposure_node_name)
        multiexposure_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        multiexposure_node.name = "MultiExposure"
        multiexposure_node.width = 151
        multiexposure_node.node_tree = bpy.data.node_groups[multiexposure_group.name]
        multiexposure_node.use_custom_color = True
        multiexposure_node.color = COLORS_DICT["DARK_PURPLE"]
        multiexposure_node.select = False

        return {'FINISHED'}
    
# Register and unregister
classes = [COMP_PT_MAINPANEL, NODE_OT_MULTIEXPOSURE]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()