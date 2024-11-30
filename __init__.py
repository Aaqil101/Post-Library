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

# Get the path to the lib directory
lib_path = (r"C:\Users\User\Documents\GitHub\Post-Library")

# Add the module path to sys.path
if lib_path not in sys.path:
    sys.path.append(lib_path)

from dictionaries import COLORS_DICT
from var_func import add_var
from pass_mixer import passmixer_node_group
from lens_distortion import lensdistortion_node
from bloom import bloom_node_group
from file_film_grain import file_film_grain_node_group
from vignette import vignette_node_group
from vignette_basic import vignette_basic_node_group

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


class COMP_PT_RENDER(bpy.types.Panel):
    bl_label = "Render"
    bl_parent_id = 'COMP_PT_MAINPANEL'
    bl_idname = "COMP_PT_RENDER"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'PLib'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator('node.passmixer_operator', icon= 'STICKY_UVS_DISABLE')


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
        row.operator('node.lensdistortion_operator', icon= 'DRIVER_DISTANCE')
        row.operator('node.filmgrain_operator', icon= 'FILE_MOVIE')
        row = layout.row()
        row.operator('node.vignette_operator', icon= 'IMAGE_RGB')
        row.operator('node.vignette_basic_operator', icon= 'IMAGE_RGB')

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
        vignette_node.color = COLORS_DICT["LIGHT_PURPLE"]
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
        vignette_basic_node.color = COLORS_DICT["LIGHT_PURPLE"]
        vignette_basic_node.select = False

        return {'FINISHED'}

class NODE_OT_BLOOM(bpy.types.Operator):
    bl_label = "Bloom"
    bl_idname = "node.bloom_operator"


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
        add_var(
            bloom_obs_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[2].default_value'
        )

        # Knee Bloom Switch
        bloom_kbs_driver = bloom_node.node_tree.nodes['KB Switch'].driver_add('check').driver
        bloom_kbs_driver.type = "AVERAGE"
        add_var(
            bloom_kbs_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[2].default_value'
        )

        # Original Bloom High
        bloom_obh_driver = bloom_node.node_tree.nodes['Original Bloom High'].driver_add('threshold').driver
        bloom_obh_driver.type = "AVERAGE"
        add_var(
            bloom_obh_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[4].default_value'
        )

        # Original Bloom Low
        bloom_obl_driver = bloom_node.node_tree.nodes['Original Bloom Low'].driver_add('threshold').driver
        bloom_obl_driver.type = "AVERAGE"
        add_var(
            bloom_obl_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[4].default_value'
        )

        # Original Bloom High Size
        bloom_obhs_driver = bloom_node.node_tree.nodes['Original Bloom High'].driver_add('size').driver
        bloom_obhs_driver.type = "AVERAGE"
        add_var(
            bloom_obhs_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[8].default_value'
        )

        # Original Bloom Low Size
        bloom_obls_driver = bloom_node.node_tree.nodes['Original Bloom Low'].driver_add('size').driver
        bloom_obls_driver.type = "AVERAGE"
        add_var(
            bloom_obls_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[8].default_value'
        )

        # Added Radius X
        bloom_arx_driver = bloom_node.node_tree.nodes['Blur'].driver_add('size_x').driver
        bloom_arx_driver.type = "AVERAGE"
        add_var(
            bloom_arx_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[5].default_value'
        )

        # Added Radius Y
        bloom_ary_driver = bloom_node.node_tree.nodes['Blur'].driver_add('size_y').driver
        bloom_ary_driver.type = "AVERAGE"
        add_var(
            bloom_ary_driver,
            f'node_tree.nodes["{bloom_node.name}"].inputs[5].default_value'
        )

        return {"FINISHED"}

# Register and unregister list variable
classes = [
    # Panels
    COMP_PT_MAINPANEL,
    COMP_PT_RENDER,
    COMP_PT_FINALTOUCHES,

    # Node Groups
    NODE_OT_PASSMIXER,
    NODE_OT_LENSDISTORTION,
    NODE_OT_FFGRAIN,
    NODE_OT_VIGNETTE,
    NODE_OT_BASICVIGNETTE,
    NODE_OT_BLOOM
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