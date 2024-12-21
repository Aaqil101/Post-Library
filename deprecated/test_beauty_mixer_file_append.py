import bpy
import pathlib

class COMP_PT_MAINPANEL(bpy.types.Panel):
    bl_label = "test"
    bl_idname = "COMP_PT_MAINPANEL"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "T"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("wm.select_passes", text= "BeautyMixer", icon="IMAGE_RGB")

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

class WM_OT_SELECT_PASSES(bpy.types.Operator):
    bl_idname = "wm.select_passes"
    bl_label = "Passes Selection"

    diffuse_bool: bpy.props.BoolProperty(name="Diffuse", default=False) # type: ignore
    glossy_bool: bpy.props.BoolProperty(name="Glossy", default=False) # type: ignore
    transmission_bool: bpy.props.BoolProperty(name="Transmission", default=False) # type: ignore
    volume_bool: bpy.props.BoolProperty(name="Volume", default=False) # type: ignore
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        # Get boolean values for passes
        db = self.diffuse_bool
        gb = self.glossy_bool
        tb = self.transmission_bool
        vb = self.volume_bool

        def remove_libraries(libraries_to_remove):
            """
            Removes libraries from bpy.data.libraries.

            Args:
                libraries_to_remove (list of str): A list of library names to remove from bpy.data.libraries.
            """
            for lib in libraries_to_remove:
                if lib in bpy.data.libraries:
                    bpy.data.libraries.remove(bpy.data.libraries[lib])

        def link_blend_file_node_groups(blend_file_path, link=False):
            """
            Links a blend file with node groups to the current blend file.

            If link is False, the node groups are appended to the current blend file.
            If link is True, the node groups are linked to the current blend file.

            Args:
                blend_file_path (str): The path to the blend file to link.
                link (bool, optional): Whether to link or append the node groups. Defaults to False.
            """
            with bpy.data.libraries.load(blend_file_path, link=link) as (data_from, data_to):
                for node_group_name in data_from.node_groups:
                    if "Diffuse" in node_group_name:
                        data_to.node_groups.append(node_group_name)

        def add_node_group_to_compositor(node_group_name, node_color):
            """
            Adds a node group to the compositor and assigns it to a GROUP node.

            Args:
                node_group_name (str): The name of the node group to add.
                node_color (tuple of float): The color of the node group in the compositor.

            Returns:
                None
            """
            # Ensure the compositor is enabled
            bpy.context.scene.use_nodes = True

            # Get the compositor node tree
            node_tree = bpy.context.scene.node_tree

            # Find the node group by name
            node_group = bpy.data.node_groups.get(node_group_name)
            if not node_group:
                print(f"Node group '{node_group_name}' not found.")
                return
            
            # Add a GROUP node to the compositor
            group_node = node_tree.nodes.new(type="CompositorNodeGroup")
            
            # Assign the existing node group to the new node
            group_node.node_tree = node_group

            # Set the label and name
            group_node.label = "BeautyMixer"
            group_node.name = node_group_name

            # Set the Color
            group_node.use_custom_color = True
            group_node.color = node_color


        if db == True:
            remove_libraries(["diffuse.blend"])

            # check if we are running from the Text Editor
            if bpy.context.space_data != None and bpy.context.space_data.type == "TEXT_EDITOR":
                # get the path to the SAVED TO DISK script when running from blender
                print("bpy.context.space_data script_path")
                script_path = bpy.context.space_data.text.filepath
            else:
                print("__file__ script_path")
                # __file__ is built-in Python variable that represents the path to the script
                script_path = __file__

            print(f"script_path -> {script_path}")

            script_dir = pathlib.Path(script_path).resolve().parent
            print(f"[pathlib] script_dir -> {script_dir}")

            # get a path to a file that is next to the script
            blend_file_path = str(script_dir / "beauty_mixer" / "diff.blend")
            print(f"path_to_file -> {blend_file_path}")

            link_blend_file_node_groups(blend_file_path)

            add_node_group_to_compositor("Diffuse", COLORS_DICT["DARK_BLUE"])

            remove_libraries(["diffuse.blend"])

        return {'FINISHED'}
    
# Register and unregister
classes = [COMP_PT_MAINPANEL, WM_OT_SELECT_PASSES]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()