bl_info = {
    "name": "Post Library",
    "author": "Aaqil",
    "version": (2, 0, 0),
    "blender": (4, 4, 0),
    "location": "Compositor > Toolshelf",
    "description": "Boost your Blender workflow with essential tools for efficient VFX and post-processing. Simplify compositing, and finishing touches with this powerful addon.",
    "warning": "",
    "doc_url": "https://github.com/Aaqil101/Post-Library",
    "category": "Nodes",
}

# Build-in Modules
import sys
from pathlib import Path

# Blender Modules
import bpy
from bpy.types import UILayout

"""
INFO: I used the [node to python add-on](https://extensions.blender.org/add-ons/node-to-python/) to convert the node groups into a Python script.
"""

# Determine script path
try:
    script_path = (
        bpy.context.space_data.text.filepath
        if bpy.context.space_data and bpy.context.space_data.type == "TEXT_EDITOR"
        else __file__
    )
except NameError:
    raise RuntimeError(
        "Unable to determine script path. Are you running this in Blender?"
    )

if not script_path:
    raise RuntimeError("The script must be saved to disk before running!")

# Resolve directories
script_dir: Path = Path(script_path).resolve().parent
path_to_nodes_folder: Path = script_dir / "nodes"
path_to_helpers_folder: Path = script_dir / "helpers"
path_to_core_folder: Path = script_dir / "core"

"""
TODO: When it's time to release the addon, remove the {# Determine script path} and enable this one
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
paths: list[Path] = [script_dir, path_to_nodes_folder, path_to_helpers_folder]

# Add directories to sys.path
for path in paths:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.append(path_str)
        print(f"Added {path_str} to sys.path")
    else:
        print(f"{path_str} already in sys.path")

from helpers import Color, NodeDriverManager
from nodes import (
    beautymixer_node_group,
    bloom_node_group,
    chromatic_aberration_node_group,
    contrast_node_group,
    exponential_glare_node_group,
    file_film_grain_node_group,
    glow_node_group,
    halation_node_group,
    lensdistortion_node,
    passmixer_node_group,
    vignette_basic_node_group,
    vignette_node_group,
)


class COMP_PT_MAINPANEL(bpy.types.Panel):
    bl_label = "Post Library"
    bl_idname = "COMP_PT_MAINPANEL"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "PLib"

    def draw(self, context) -> None:
        layout = self.layout

        row: UILayout = layout.row()
        row.label(text="Welcome to Post Library!", icon="INFO")


class COMP_PT_FINALTOUCHES(bpy.types.Panel):
    bl_label = "Final Touches"
    bl_parent_id = "COMP_PT_MAINPANEL"
    bl_idname = "COMP_PT_FINALTOUCHES"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "PLib"

    def draw(self, context) -> None:
        layout = self.layout

        row = layout.row()
        row.operator("node.passmixer_operator", icon="STICKY_UVS_DISABLE")
        row = layout.row()

        row.operator("node.lensdistortion_operator", icon="DRIVER_DISTANCE")
        row.operator("node.filmgrain_operator", icon="FILE_MOVIE")
        row = layout.row()
        row.operator("node.vignette_operator", icon="IMAGE_RGB")
        row.operator("node.vignette_basic_operator", icon="IMAGE_RGB")

        row = layout.row()
        row.operator("node.chromatic_aberration_operator", icon="IMAGE_RGB")
        row = layout.row()

        row.operator("node.bloom_operator", icon="LIGHT_SUN")
        row.operator("node.beautymixer_operator", icon="RENDERLAYERS")
        row = layout.row()
        row.operator("node.exponential_glare_operator", icon="FREEZE")
        row = layout.row()
        row.operator("node.contrast_operator", icon="IMAGE_RGB")
        row.operator("node.glow_operator", icon="LIGHT_SUN")
        row = layout.row()
        row.operator("node.halation_operator", icon="IMAGE_RGB")


class NODE_OT_PASSMIXER(bpy.types.Operator):
    bl_label = "PassMixer"
    bl_idname = "node.passmixer_operator"

    def execute(shelf, context) -> set[str]:

        custom_passmixer_node_name = "PassMixer"
        passmixer_group = passmixer_node_group(
            shelf, context, custom_passmixer_node_name
        )
        passmixer_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        passmixer_node.name = "PassMixer"
        passmixer_node.width = 160
        passmixer_node.node_tree = bpy.data.node_groups[passmixer_group.name]
        passmixer_node.use_custom_color = True
        passmixer_node.color = Color.DARK_BLUE
        passmixer_node.select = False

        return {"FINISHED"}


class NODE_OT_LENSDISTORTION(bpy.types.Operator):
    bl_label = "Lens Distortion"
    bl_idname = "node.lensdistortion_operator"

    def execute(shelf, context) -> set[str]:

        lensdistortion_node(context, shelf)

        return {"FINISHED"}


class NODE_OT_FFGRAIN(bpy.types.Operator):
    bl_label = "FF Grain"
    bl_idname = "node.filmgrain_operator"

    # I don't know why it says like this but it works so i am might not worry about it for know
    # and I did search for a solution but I didn't find any. (https://youtu.be/P8w-tswp0JI?list=PLB8-FQgROBmlqzZ4HBzIAGpho-xp0Bn_h)
    # Error: Call expression not allowed in type expression

    filepath: bpy.props.StringProperty(
        name="Image Path",
        description="The path to the image used for the film grain effect",
        subtype="FILE_PATH",
        default="",
        options={"HIDDEN"},
    )  # type: ignore

    def execute(self, context) -> set[str]:

        custom_ff_grain_node_name = "FF Grain"
        image_path = self.filepath
        ff_grain_group = file_film_grain_node_group(
            context, self, custom_ff_grain_node_name, image_path
        )
        ff_grain_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        ff_grain_node.name = "FF Grain"
        ff_grain_node.label = "FF Grain"
        ff_grain_node.width = 140
        ff_grain_node.node_tree = bpy.data.node_groups[ff_grain_group.name]
        ff_grain_node.use_custom_color = True
        ff_grain_node.color = Color.LIGHT_PURPLE
        ff_grain_node.select = False

        return {"FINISHED"}

    def invoke(self, context, event) -> set[str]:
        # Open the file browser to select an image
        context.window_manager.fileselect_add(self)

        return {"RUNNING_MODAL"}


class NODE_OT_VIGNETTE(bpy.types.Operator):
    bl_label = "Vignette"
    bl_idname = "node.vignette_operator"

    # I don't know why it says like this but it works so i am might not worry about it for know
    # and I did search for a solution but I didn't find any. (https://youtu.be/P8w-tswp0JI?list=PLB8-FQgROBmlqzZ4HBzIAGpho-xp0Bn_h)
    # Error: Call expression not allowed in type expression

    filepath: bpy.props.StringProperty(
        name="Image Path",
        description="The path to the image used for the vignette effect",
        subtype="FILE_PATH",
        default="",
        options={"HIDDEN"},
    )  # type: ignore

    def execute(self, context) -> set[str]:

        custom_vignette_node_name = "Vignette"
        image_path = self.filepath
        vignette_group = vignette_node_group(
            context, self, custom_vignette_node_name, image_path
        )
        vignette_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        vignette_node.name = "Vignette"
        vignette_node.label = "Vignette"
        vignette_node.width = 140
        vignette_node.node_tree = bpy.data.node_groups[vignette_group.name]
        vignette_node.use_custom_color = True
        vignette_node.color = Color.DARK_PURPLE
        vignette_node.select = False

        return {"FINISHED"}

    def invoke(self, context, event) -> set[str]:
        # Open the file browser to select an image

        context.window_manager.fileselect_add(self)

        return {"RUNNING_MODAL"}


class NODE_OT_BASICVIGNETTE(bpy.types.Operator):
    bl_label = "Vignette-Basic"
    bl_idname = "node.vignette_basic_operator"
    bl_description = "A basic node group for vignette effect"

    def execute(shelf, context) -> set[str]:

        custom_vignette_basic_node_name = "Vignette-Basic"
        vignette_basic_group = vignette_basic_node_group(
            shelf, context, custom_vignette_basic_node_name
        )
        vignette_basic_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        vignette_basic_node.name = "Vignette-Basic"
        vignette_basic_node.label = "Vignette-Basic"
        vignette_basic_node.width = 165
        vignette_basic_node.node_tree = bpy.data.node_groups[vignette_basic_group.name]
        vignette_basic_node.use_custom_color = True
        vignette_basic_node.color = Color.DARK_PURPLE
        vignette_basic_node.select = False

        return {"FINISHED"}


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


class NODE_OT_BEAUTYMIXER(bpy.types.Operator):
    bl_label = "BeautyMixer"
    bl_idname = "node.beautymixer_operator"
    bl_description = "To mix all the beauty passes"

    def execute(shelf, context) -> set[str]:

        custom_beautymixer_node_name = "BeautyMixer"
        beautymixer_group = beautymixer_node_group(
            shelf, context, custom_beautymixer_node_name
        )
        beautymixer_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        beautymixer_node.name = "BeautyMixer"
        beautymixer_node.label = "BeautyMixer"
        beautymixer_node.width = 162
        beautymixer_node.node_tree = bpy.data.node_groups[beautymixer_group.name]
        beautymixer_node.use_custom_color = True
        beautymixer_node.color = Color.DARK_BLUE
        beautymixer_node.select = False

        return {"FINISHED"}


class NODE_OT_CHROMATICABERRATION(bpy.types.Operator):
    bl_label = "Chromatic Aberration"
    bl_idname = "node.chromatic_aberration_operator"
    bl_description = "This node group is used to create a chromatic aberration effect."

    def execute(shelf, context) -> set[str]:

        custom_chromatic_aberration_node_name = "Chromatic Aberration"
        chromatic_aberration_group = chromatic_aberration_node_group(
            shelf, context, custom_chromatic_aberration_node_name
        )
        chromatic_aberration_node = context.scene.node_tree.nodes.new(
            "CompositorNodeGroup"
        )
        chromatic_aberration_node.name = "Chromatic Aberration"
        chromatic_aberration_node.label = "Chromatic Aberration"
        chromatic_aberration_node.width = 197
        chromatic_aberration_node.node_tree = bpy.data.node_groups[
            chromatic_aberration_group.name
        ]
        chromatic_aberration_node.use_custom_color = True
        chromatic_aberration_node.color = Color.DARK_PURPLE
        chromatic_aberration_node.select = False

        return {"FINISHED"}


class NODE_OT_CONTRAST(bpy.types.Operator):
    bl_label = "Contrast"
    bl_idname = "node.contrast_operator"
    bl_description = "This node group is used to add contrast to an image."

    def execute(shelf, context) -> set[str]:

        custom_contrast_node_name = "Contrast"
        contrast_group = contrast_node_group(shelf, context, custom_contrast_node_name)
        contrast_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        contrast_node.name = "Contrast"
        contrast_node.label = "Contrast"
        contrast_node.width = 149
        contrast_node.node_tree = bpy.data.node_groups[contrast_group.name]
        contrast_node.use_custom_color = True
        contrast_node.color = Color.BROWN
        contrast_node.select = False

        # Initialize NodeDriverManager to manage drivers for the node group
        drivers = NodeDriverManager(
            node_group=contrast_group, id_type="SCENE", id=bpy.context.scene
        )

        # Blur Size X
        drivers.add_driver(node_name="C Blur", socket_name="size_x")
        drivers.add_driver_var(2)

        # Blur Size Y
        drivers.add_driver(node_name="C Blur", socket_name="size_y")
        drivers.add_driver_var(3)

        return {"FINISHED"}


class NODE_OT_EXPONENTIALGLARE(bpy.types.Operator):
    bl_label = "Exponential Glare"
    bl_idname = "node.exponential_glare_operator"
    bl_description = "This node group is used to add exponential glare to an image."

    def execute(shelf, context) -> set[str]:

        custom_exponential_glare_node_name = "Exponential Glare"
        exponential_glare_group = exponential_glare_node_group(
            shelf, context, custom_exponential_glare_node_name
        )
        exponential_glare_node = context.scene.node_tree.nodes.new(
            "CompositorNodeGroup"
        )
        exponential_glare_node.name = "Exponential Glare"
        exponential_glare_node.label = "Exponential Glare"
        exponential_glare_node.width = 194
        exponential_glare_node.node_tree = bpy.data.node_groups[
            exponential_glare_group.name
        ]
        exponential_glare_node.use_custom_color = True
        exponential_glare_node.color = Color.DARK_PURPLE
        exponential_glare_node.select = False

        return {"FINISHED"}


class NODE_OT_GLOW(bpy.types.Operator):
    bl_label = "Glow"
    bl_idname = "node.glow_operator"
    bl_description = "This node group is used to add glow to an image."

    def execute(shelf, context) -> set[str]:

        custom_glow_node_name = "Glow"
        glow_group = glow_node_group(shelf, context, custom_glow_node_name)
        glow_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        glow_node.name = "Glow"
        glow_node.width = 197
        glow_node.node_tree = bpy.data.node_groups[glow_group.name]
        glow_node.use_custom_color = True
        glow_node.color = Color.DARK_PURPLE
        glow_node.select = False

        # Initialize NodeDriverManager to manage drivers for the node group
        drivers = NodeDriverManager(
            node_group=glow_group, id_type="SCENE", id=bpy.context.scene
        )

        # G Switch 01
        drivers.add_driver(node_name="G Switch 01", socket_name="check")
        drivers.add_driver_var(1)

        # G Switch 00
        drivers.add_driver(node_name="G Switch 00", socket_name="check")
        drivers.add_driver_var(1)

        # G Bloom Low Threshold
        drivers.add_driver(node_name="G Bloom Low", socket_name="threshold")
        drivers.add_driver_var(4)

        # G Bloom High Threshold
        drivers.add_driver(node_name="G Bloom High", socket_name="threshold")
        drivers.add_driver_var(4)

        # G Bloom Low Size
        drivers.add_driver(node_name="G Bloom Low", socket_name="size")
        drivers.add_driver_var(5)

        # G Bloom High Size
        drivers.add_driver(node_name="G Bloom High", socket_name="size")
        drivers.add_driver_var(5)

        # G Streaks Low Iterations
        drivers.add_driver(node_name="G Streaks Low", socket_name="iterations")
        drivers.add_driver_var(7)

        # G Streaks High Iterations
        drivers.add_driver(node_name="G Streaks High", socket_name="iterations")
        drivers.add_driver_var(7)

        # G Streaks Low Color Modulation
        drivers.add_driver(node_name="G Streaks Low", socket_name="color_modulation")
        drivers.add_driver_var(8)

        # G Streaks High Color Modulation
        drivers.add_driver(node_name="G Streaks High", socket_name="color_modulation")
        drivers.add_driver_var(8)

        # G Streaks Low Threshold
        drivers.add_driver(node_name="G Streaks Low", socket_name="threshold")
        drivers.add_driver_var(9)

        # G Streaks High Threshold
        drivers.add_driver(node_name="G Streaks High", socket_name="threshold")
        drivers.add_driver_var(9)

        # G Streaks Low Streaks
        drivers.add_driver(node_name="G Streaks Low", socket_name="streaks")
        drivers.add_driver_var(10)

        # G Streaks High Streaks
        drivers.add_driver(node_name="G Streaks High", socket_name="streaks")
        drivers.add_driver_var(10)

        # G Streaks Low Angle Offset
        drivers.add_driver(node_name="G Streaks Low", socket_name="angle_offset")
        drivers.add_driver_var(11)

        # G Streaks High Angle Offset
        drivers.add_driver(node_name="G Streaks High", socket_name="angle_offset")
        drivers.add_driver_var(11)

        # G Streaks Low Fade
        drivers.add_driver(node_name="G Streaks Low", socket_name="fade")
        drivers.add_driver_var(12)

        # G Streaks High Fade
        drivers.add_driver(node_name="G Streaks High", socket_name="fade")
        drivers.add_driver_var(12)

        return {"FINISHED"}


class NODE_OT_HALATION(bpy.types.Operator):
    bl_label = "Halation"
    bl_idname = "node.halation_operator"
    bl_description = "This node group is used to add halation to an image."

    def execute(shelf, context) -> set[str]:

        custom_halation_node_name = "Halation"
        halation_group = halation_node_group(shelf, context, custom_halation_node_name)
        halation_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        halation_node.name = "Halation"
        halation_node.width = 151
        halation_node.node_tree = bpy.data.node_groups[halation_group.name]
        halation_node.use_custom_color = True
        halation_node.color = Color.DARK_PURPLE
        halation_node.select = False

        # Initialize NodeDriverManager to manage drivers for the node group
        drivers = NodeDriverManager(
            node_group=halation_group, id_type="SCENE", id=bpy.context.scene
        )

        # H Blur Size X
        drivers.add_driver(node_name="H Blur", socket_name="size_x")
        drivers.add_driver_var(1)

        # H Blur Size Y
        drivers.add_driver(node_name="H Blur", socket_name="size_y")
        drivers.add_driver_var(2)

        return {"FINISHED"}


# Register and Unregister
classes = [
    # Panels
    COMP_PT_MAINPANEL,
    COMP_PT_FINALTOUCHES,
    # Node Groups
    NODE_OT_PASSMIXER,
    NODE_OT_LENSDISTORTION,
    NODE_OT_FFGRAIN,
    NODE_OT_VIGNETTE,
    NODE_OT_BASICVIGNETTE,
    NODE_OT_BLOOM,
    NODE_OT_BEAUTYMIXER,
    NODE_OT_EXPONENTIALGLARE,
    NODE_OT_CHROMATICABERRATION,
    NODE_OT_CONTRAST,
    NODE_OT_GLOW,
    NODE_OT_HALATION,
]


def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
