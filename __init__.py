bl_info = {
    "name": "Post Library",
    "author": "Aaqil",
    "version": (1, 3, 0),
    "blender": (4, 3, 0),
    "location": "Compositor > Toolshelf",
    "description": "Boost your Blender workflow with essential tools for efficient VFX and post-processing. Simplify compositing, and finishing touches with this powerful addon.",
    "warning": "",
    "doc_url": "https://github.com/Aaqil101/Post-Library",
    "category": "Nodes",
}

import bpy
import sys
import pathlib

"""
* I used the [node to python add-on](https://extensions.blender.org/add-ons/node-to-python/) to convert the node groups into a Python script.
"""

# Check if the script is run from Blender's Text Editor
if bpy.context.space_data is not None and bpy.context.space_data.type == "TEXT_EDITOR":
    print("Running from Blender Text Editor")
    script_path = bpy.context.space_data.text.filepath
else:
    try:
        print("Running from external Python environment")
        script_path = __file__
    except NameError:
        raise RuntimeError("Unable to determine script path. Are you running this in Blender?")

if not script_path:
    raise RuntimeError("The script needs to be saved to disk before running!")

print(f"script_path -> {script_path}")

# Resolve the directory of the script
script_dir = pathlib.Path(script_path).resolve().parent
print(f"[pathlib] script_dir -> {script_dir}")

# get the path to the nodes folder
path_to_nodes_folder = str(script_dir / "nodes")
print(f"path_to_nodes_folder -> {path_to_nodes_folder}")

# get the path to the functions folder
path_to_functions_folder = str(script_dir / "functions")
print(f"path_to_functions_folder -> {path_to_functions_folder}")

# Add the script's directory to sys.path if not already there
if str(script_dir) not in sys.path:
    sys.path.append(str(script_dir))
    print(f"Added {script_dir} to sys.path")
else:
    print(f"{script_dir} already in sys.path")

# Add the path to the nodes folder to sys.path
if path_to_nodes_folder not in sys.path:
    sys.path.append(path_to_nodes_folder)
    print(f"Added {path_to_nodes_folder} to sys.path")
else:
    print(f"{path_to_nodes_folder} already in sys.path")

# Add the path to the functions folder to sys.path
if path_to_functions_folder not in sys.path:
    sys.path.append(path_to_functions_folder)
    print(f"Added {path_to_functions_folder} to sys.path")
else:
    print(f"{path_to_functions_folder} already in sys.path")


from functions import(
    COLORS_DICT, add_driver_var
)

from nodes import(
    passmixer_node_group, lensdistortion_node, bloom_node_group, file_film_grain_node_group,
    vignette_node_group, vignette_basic_node_group, beautymixer_node_group, chromatic_aberration_node_group,
    contrast_node_group, exponential_glare_node_group, glow_node_group, halation_node_group
)

class COMP_PT_MAINPANEL(bpy.types.Panel):
    bl_label = "Post Library"
    bl_idname = "COMP_PT_MAINPANEL"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'PLib'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="Welcome to Post Library!", icon="INFO")

class COMP_PT_FINALTOUCHES(bpy.types.Panel):
    bl_label = "Final Touches"
    bl_parent_id = 'COMP_PT_MAINPANEL'
    bl_idname = "COMP_PT_FINALTOUCHES"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'PLib'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator('node.passmixer_operator', icon= 'STICKY_UVS_DISABLE')
        row = layout.row()

        row.operator('node.lensdistortion_operator', icon= 'DRIVER_DISTANCE')
        row.operator('node.filmgrain_operator', icon= 'FILE_MOVIE')
        row = layout.row()
        row.operator('node.vignette_operator', icon= 'IMAGE_RGB')
        row.operator('node.vignette_basic_operator', icon= 'IMAGE_RGB')

        row = layout.row()
        row.operator('node.chromatic_aberration_operator', icon= 'IMAGE_RGB')
        row = layout.row()

        row.operator('node.bloom_operator', icon= 'LIGHT_SUN')
        row.operator('node.beautymixer_operator', icon= 'RENDERLAYERS')
        row = layout.row()
        row.operator('node.exponential_glare_operator', icon= 'FREEZE')
        row = layout.row()
        row.operator('node.contrast_operator', icon= 'IMAGE_RGB')
        row.operator('node.glow_operator', icon= 'LIGHT_SUN')
        row = layout.row()
        row.operator('node.halation_operator', icon= 'IMAGE_RGB')

class NODE_OT_PASSMIXER(bpy.types.Operator):
    bl_label = "PassMixer"
    bl_idname = "node.passmixer_operator"

    def execute(shelf, context):

        custom_passmixer_node_name = "PassMixer"
        passmixer_group = passmixer_node_group(shelf, context, custom_passmixer_node_name)
        passmixer_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        passmixer_node.name = "PassMixer"
        passmixer_node.width = 160
        passmixer_node.node_tree = bpy.data.node_groups[passmixer_group.name]
        passmixer_node.use_custom_color = True
        passmixer_node.color = COLORS_DICT["DARK_BLUE"]
        passmixer_node.select = False

        return {'FINISHED'}

class NODE_OT_LENSDISTORTION(bpy.types.Operator):
    bl_label = "Lens Distortion"
    bl_idname = 'node.lensdistortion_operator'

    def execute(shelf, context):

        lensdistortion_node(context, shelf)

        return {'FINISHED'}

class NODE_OT_FFGRAIN(bpy.types.Operator):
    bl_label = "FF Grain"
    bl_idname = "node.filmgrain_operator"

    # I don't know why it says like this but it works so i am might not worie about it for know
    # and I did search for a solution but I didn't find any. (https://youtu.be/P8w-tswp0JI?list=PLB8-FQgROBmlqzZ4HBzIAGpho-xp0Bn_h)
    # Error: Call expression not allowed in type expression

    filepath: bpy.props.StringProperty(
        name="Image Path",
        description="The path to the image used for the film grain effect",
        subtype="FILE_PATH",
        default="",
        options={'HIDDEN'},
    ) # type: ignore

    def execute(self, context):

        custom_ff_grain_node_name = "FF Grain"
        image_path = self.filepath
        ff_grain_group = file_film_grain_node_group(context, self, custom_ff_grain_node_name, image_path)
        ff_grain_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        ff_grain_node.name = "FF Grain"
        ff_grain_node.label = "FF Grain"
        ff_grain_node.width = 140
        ff_grain_node.node_tree = bpy.data.node_groups[ff_grain_group.name]
        ff_grain_node.use_custom_color = True
        ff_grain_node.color = COLORS_DICT["LIGHT_PURPLE"]
        ff_grain_node.select = False

        return {'FINISHED'}
    
    def invoke(self, context, event):
        # Open the file browser to select an image
        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}

class NODE_OT_VIGNETTE(bpy.types.Operator):
    bl_label = "Vignette"
    bl_idname = 'node.vignette_operator'

    # I don't know why it says like this but it works so i am might not worie about it for know
    # and I did search for a solution but I didn't find any. (https://youtu.be/P8w-tswp0JI?list=PLB8-FQgROBmlqzZ4HBzIAGpho-xp0Bn_h)
    # Error: Call expression not allowed in type expression

    filepath: bpy.props.StringProperty(
        name="Image Path",
        description="The path to the image used for the vignette effect",
        subtype="FILE_PATH",
        default="",
        options={'HIDDEN'},
    ) # type: ignore

    def execute(self, context):

        custom_vignette_node_name = "Vignette"
        image_path = self.filepath
        vignette_group = vignette_node_group(context, self, custom_vignette_node_name, image_path)
        vignette_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        vignette_node.name = "Vignette"
        vignette_node.label = "Vignette"
        vignette_node.width = 140
        vignette_node.node_tree = bpy.data.node_groups[vignette_group.name]
        vignette_node.use_custom_color = True
        vignette_node.color = COLORS_DICT["DARK_PURPLE"]
        vignette_node.select = False

        return {'FINISHED'}
    
    def invoke(self, context, event):
        # Open the file browser to select an image

        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}
    
class NODE_OT_BASICVIGNETTE(bpy.types.Operator):
    bl_label = "Vignette-Basic"
    bl_idname = 'node.vignette_basic_operator'
    bl_description = "A basic node group for vignette effect"

    def execute(shelf, context):

        custom_vignette_basic_node_name = "Vignette-Basic"
        vignette_basic_group = vignette_basic_node_group(shelf, context, custom_vignette_basic_node_name)
        vignette_basic_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        vignette_basic_node.name = "Vignette-Basic"
        vignette_basic_node.label = "Vignette-Basic"
        vignette_basic_node.width = 165
        vignette_basic_node.node_tree = bpy.data.node_groups[vignette_basic_group.name]
        vignette_basic_node.use_custom_color = True
        vignette_basic_node.color = COLORS_DICT["DARK_PURPLE"]
        vignette_basic_node.select = False

        return {'FINISHED'}

class NODE_OT_BLOOM(bpy.types.Operator):
    bl_label = "Bloom"
    bl_idname = "node.bloom_operator"
    bl_description = "Replication of the legacy eevee bloom option, but can be used in cycles as well"


    def execute(shelf, context):

        custom_bloom_node_name = "Bloom"
        bloom_group = bloom_node_group(shelf, context, custom_bloom_node_name)
        bloom_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
        bloom_node.name = "Bloom"
        bloom_node.width = 168
        bloom_node.node_tree = bpy.data.node_groups[bloom_group.name]
        bloom_node.use_custom_color = True
        bloom_node.color = COLORS_DICT["DARK_PURPLE"]
        bloom_node.select = False

        """
        * The ability to add drivers to nodes is made possible by Victor Stepanov
        * (https://www.skool.com/cgpython/how-to-add-drivers-to-node-group-sockets-using-python?p=0be0f439)
        * (https://www.skool.com/cgpython/how-do-i-add-the-drivers-to-a-node-group-every-time?p=4220eddf)
        * His youtube channel (https://www.youtube.com/@CGPython)
        """

        # Original Bloom Switch
        bloom_obs_driver = bloom_node.node_tree.nodes['OB Switch'].driver_add('check').driver
        bloom_obs_driver.type = "AVERAGE"
        add_driver_var(
            bloom_obs_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[2].default_value'
        )

        # Knee Bloom Switch
        bloom_kbs_driver = bloom_node.node_tree.nodes['KB Switch'].driver_add('check').driver
        bloom_kbs_driver.type = "AVERAGE"
        add_driver_var(
            bloom_kbs_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[2].default_value'
        )

        # Original Bloom High
        bloom_obh_driver = bloom_node.node_tree.nodes['Original Bloom High'].driver_add('threshold').driver
        bloom_obh_driver.type = "AVERAGE"
        add_driver_var(
            bloom_obh_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[4].default_value'
        )

        # Original Bloom Low
        bloom_obl_driver = bloom_node.node_tree.nodes['Original Bloom Low'].driver_add('threshold').driver
        bloom_obl_driver.type = "AVERAGE"
        add_driver_var(
            bloom_obl_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[4].default_value'
        )

        # Original Bloom High Size
        bloom_obhs_driver = bloom_node.node_tree.nodes['Original Bloom High'].driver_add('size').driver
        bloom_obhs_driver.type = "AVERAGE"
        add_driver_var(
            bloom_obhs_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[8].default_value'
        )

        # Original Bloom Low Size
        bloom_obls_driver = bloom_node.node_tree.nodes['Original Bloom Low'].driver_add('size').driver
        bloom_obls_driver.type = "AVERAGE"
        add_driver_var(
            bloom_obls_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[8].default_value'
        )

        # Added Radius X
        bloom_arx_driver = bloom_node.node_tree.nodes['Blur'].driver_add('size_x').driver
        bloom_arx_driver.type = "AVERAGE"
        add_driver_var(
            bloom_arx_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[5].default_value'
        )

        # Added Radius Y
        bloom_ary_driver = bloom_node.node_tree.nodes['Blur'].driver_add('size_y').driver
        bloom_ary_driver.type = "AVERAGE"
        add_driver_var(
            bloom_ary_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[5].default_value'
        )

        return {"FINISHED"}

class NODE_OT_BEAUTYMIXER(bpy.types.Operator):
    bl_label = "BeautyMixer"
    bl_idname = "node.beautymixer_operator"
    bl_description = "To mix all the beauty passes"

    def execute(shelf, context):

        custom_beautymixer_node_name = "BeautyMixer"
        beautymixer_group = beautymixer_node_group(shelf, context, custom_beautymixer_node_name)
        beautymixer_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        beautymixer_node.name = "BeautyMixer"
        beautymixer_node.label = "BeautyMixer"
        beautymixer_node.width = 162
        beautymixer_node.node_tree = bpy.data.node_groups[beautymixer_group.name]
        beautymixer_node.use_custom_color = True
        beautymixer_node.color = COLORS_DICT["DARK_BLUE"]
        beautymixer_node.select = False

        return {'FINISHED'}

class NODE_OT_CHROMATICABERRATION(bpy.types.Operator):
    bl_label = "Chromatic Aberration"
    bl_idname = "node.chromatic_aberration_operator"
    bl_description = "This node group is used to create a chromatic aberration effect."

    def execute(shelf, context):

        custom_chromatic_aberration_node_name = "Chromatic Aberration"
        chromatic_aberration_group = chromatic_aberration_node_group(shelf, context, custom_chromatic_aberration_node_name)
        chromatic_aberration_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        chromatic_aberration_node.name = "Chromatic Aberration"
        chromatic_aberration_node.label = "Chromatic Aberration"
        chromatic_aberration_node.width = 197
        chromatic_aberration_node.node_tree = bpy.data.node_groups[chromatic_aberration_group.name]
        chromatic_aberration_node.use_custom_color = True
        chromatic_aberration_node.color = COLORS_DICT["DARK_PURPLE"]
        chromatic_aberration_node.select = False

        return {'FINISHED'}

class NODE_OT_CONTRAST(bpy.types.Operator):
    bl_label = "Contrast"
    bl_idname = "node.contrast_operator"
    bl_description = "This node group is used to add contrast to an image."

    def execute(shelf, context):

        custom_contrast_node_name = "Contrast"
        contrast_group = contrast_node_group(shelf, context, custom_contrast_node_name)
        contrast_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        contrast_node.name = "Contrast"
        contrast_node.label = "Contrast"
        contrast_node.width = 149
        contrast_node.node_tree = bpy.data.node_groups[contrast_group.name]
        contrast_node.use_custom_color = True
        contrast_node.color = COLORS_DICT["BROWN"]
        contrast_node.select = False
        
        # Blur Size X
        contrast_bsx_driver = contrast_node.node_tree.nodes['C Blur'].driver_add('size_x').driver
        contrast_bsx_driver.type = "AVERAGE"
        add_driver_var(
            contrast_bsx_driver,
            f'node_tree.nodes["{contrast_node.name}"].inputs[2].default_value'
        )

        # Blur Size Y
        contrast_bsy_driver = contrast_node.node_tree.nodes['C Blur'].driver_add('size_y').driver
        contrast_bsy_driver.type = "AVERAGE"
        add_driver_var(
            contrast_bsy_driver,
            f'node_tree.nodes["{contrast_node.name}"].inputs[3].default_value'
        )

        return {'FINISHED'}

class NODE_OT_EXPONENTIALGLARE(bpy.types.Operator):
    bl_label = "Exponential Glare"
    bl_idname = "node.exponential_glare_operator"
    bl_description = "This node group is used to add exponential glare to an image."

    def execute(shelf, context):

        custom_exponential_glare_node_name = "Exponential Glare"
        exponential_glare_group = exponential_glare_node_group(shelf, context, custom_exponential_glare_node_name)
        exponential_glare_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        exponential_glare_node.name = "Exponential Glare"
        exponential_glare_node.label = "Exponential Glare"
        exponential_glare_node.width = 194
        exponential_glare_node.node_tree = bpy.data.node_groups[exponential_glare_group.name]
        exponential_glare_node.use_custom_color = True
        exponential_glare_node.color = COLORS_DICT["DARK_PURPLE"]
        exponential_glare_node.select = False

        return {'FINISHED'}

class NODE_OT_GLOW(bpy.types.Operator):
    bl_label = "Glow"
    bl_idname = "node.glow_operator"
    bl_description = "This node group is used to add glow to an image."

    def execute(shelf, context):

        custom_glow_node_name = "Glow"
        glow_group = glow_node_group(shelf, context, custom_glow_node_name)
        glow_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        glow_node.name = "Glow"
        glow_node.width = 197
        glow_node.node_tree = bpy.data.node_groups[glow_group.name]
        glow_node.use_custom_color = True
        glow_node.color = COLORS_DICT["DARK_PURPLE"]
        glow_node.select = False
        
        # G Switch 01
        g_switch_01_driver = glow_node.node_tree.nodes['G Switch 01'].driver_add('check').driver
        g_switch_01_driver.type = "AVERAGE"
        add_driver_var(
            g_switch_01_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[1].default_value'
        )

        # G Switch 00
        g_switch_00_driver = glow_node.node_tree.nodes['G Switch 00'].driver_add('check').driver
        g_switch_00_driver.type = "AVERAGE"
        add_driver_var(
            g_switch_00_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[1].default_value'
        )

        # G Bloom Low Threshold
        g_bloom_low_threshold_driver = glow_node.node_tree.nodes['G Bloom Low'].driver_add('threshold').driver
        g_bloom_low_threshold_driver.type = "AVERAGE"
        add_driver_var(
            g_bloom_low_threshold_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[4].default_value'
        )

        # G Bloom High Threshold
        g_bloom_high_threshold_driver = glow_node.node_tree.nodes['G Bloom High'].driver_add('threshold').driver
        g_bloom_high_threshold_driver.type = "AVERAGE"
        add_driver_var(
            g_bloom_high_threshold_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[4].default_value'
        )

        # G Bloom Low Size
        g_bloom_low_size_driver = glow_node.node_tree.nodes['G Bloom Low'].driver_add('size').driver
        g_bloom_low_size_driver.type = "AVERAGE"
        add_driver_var(
            g_bloom_low_size_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[5].default_value'
        )

        # G Bloom High Size
        g_bloom_high_size_driver = glow_node.node_tree.nodes['G Bloom High'].driver_add('size').driver
        g_bloom_high_size_driver.type = "AVERAGE"
        add_driver_var(
            g_bloom_high_size_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[5].default_value'
        )

        # G Streaks Low Iterations
        g_streaks_low_iterations_driver = glow_node.node_tree.nodes['G Streaks Low'].driver_add('iterations').driver
        g_streaks_low_iterations_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_low_iterations_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[7].default_value'
        )

        # G Streaks High Iterations
        g_streaks_high_iterations_driver = glow_node.node_tree.nodes['G Streaks High'].driver_add('iterations').driver
        g_streaks_high_iterations_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_high_iterations_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[7].default_value'
        )

        # G Streaks Low Color Modulation
        g_streaks_low_color_modulation_driver = glow_node.node_tree.nodes['G Streaks Low'].driver_add('color_modulation').driver
        g_streaks_low_color_modulation_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_low_color_modulation_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[8].default_value'
        )

        # G Streaks High Color Modulation
        g_streaks_high_color_modulation_driver = glow_node.node_tree.nodes['G Streaks High'].driver_add('color_modulation').driver
        g_streaks_high_color_modulation_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_high_color_modulation_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[8].default_value'
        )

        # G Streaks Low Threshold
        g_streaks_low_threshold_driver = glow_node.node_tree.nodes['G Streaks Low'].driver_add('threshold').driver
        g_streaks_low_threshold_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_low_threshold_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[9].default_value'
        )

        # G Streaks High Threshold
        g_streaks_high_threshold_driver = glow_node.node_tree.nodes['G Streaks High'].driver_add('threshold').driver
        g_streaks_high_threshold_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_high_threshold_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[9].default_value'  
        )

        # G Streaks Low Streaks
        g_streaks_low_streaks_driver = glow_node.node_tree.nodes['G Streaks Low'].driver_add('streaks').driver
        g_streaks_low_streaks_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_low_streaks_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[10].default_value'
        )

        # G Streaks High Streaks
        g_streaks_high_streaks_driver = glow_node.node_tree.nodes['G Streaks High'].driver_add('streaks').driver
        g_streaks_high_streaks_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_high_streaks_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[10].default_value'
        )

        # G Streaks Low Angle Offset
        g_streaks_low_angle_offset_driver = glow_node.node_tree.nodes['G Streaks Low'].driver_add('angle_offset').driver
        g_streaks_low_angle_offset_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_low_angle_offset_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[11].default_value'
        )

        # G Streaks High Angle Offset
        g_streaks_high_angle_offset_driver = glow_node.node_tree.nodes['G Streaks High'].driver_add('angle_offset').driver
        g_streaks_high_angle_offset_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_high_angle_offset_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[11].default_value'
        )

        # G Streaks Low Fade
        g_streaks_low_fade_driver = glow_node.node_tree.nodes['G Streaks Low'].driver_add('fade').driver
        g_streaks_low_fade_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_low_fade_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[12].default_value'
        )

        # G Streaks High Fade
        g_streaks_high_fade_driver = glow_node.node_tree.nodes['G Streaks High'].driver_add('fade').driver
        g_streaks_high_fade_driver.type = "AVERAGE"
        add_driver_var(
            g_streaks_high_fade_driver,
            f'node_tree.nodes["{glow_node.name}"].inputs[12].default_value'
        )
        
        return {'FINISHED'}

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

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

"""
!Old register and unregister method
!def register():
!    bpy.utils.register_class(COMP_PT_MAINPANEL)
!    bpy.utils.register_class(COMP_PT_RENDER)
!    bpy.utils.register_class(COMP_PT_FINALTOUCHES)
!    bpy.utils.register_class(NODE_OT_MULTIDENOISER)
!    bpy.utils.register_class(NODE_OT_PASSMIXER)
!    bpy.utils.register_class(NODE_OT_LENSDISTORTION)
!    bpy.utils.register_class(NODE_OT_FILMGRAIN)
!    bpy.utils.register_class(NODE_OT_VIGNETTE)
!
!def unregister():
!    bpy.utils.unregister_class(COMP_PT_MAINPANEL)
!    bpy.utils.unregister_class(COMP_PT_RENDER)
!    bpy.utils.unregister_class(COMP_PT_FINALTOUCHES)
!    bpy.utils.unregister_class(NODE_OT_MULTIDENOISER)
!    bpy.utils.unregister_class(NODE_OT_PASSMIXER)
!    bpy.utils.unregister_class(NODE_OT_LENSDISTORTION)
!    bpy.utils.unregister_class(NODE_OT_FILMGRAIN)
!    bpy.utils.unregister_class(NODE_OT_VIGNETTE)
"""

if __name__ == "__main__":
    register()