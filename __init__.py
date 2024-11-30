bl_info = {
    "name": "Post Library",
    "author": "Aaqil",
    "version": (1, 0),
    "blender": (4, 2, 1),
    "location": "Compositor > Toolshelf",
    "description": "Boost your Blender workflow with essential tools for efficient VFX and post-processing. Simplify compositing, and finishing touches with this powerful addon.",
    "warning": "",
    "doc_url": "https://github.com/Aaqil101/Post-Library",
    "category": "Nodes",
}

import bpy
from pathlib import Path
import sys

# Get the path to the lib directory
lib_path = (r"C:\Users\User\Documents\GitHub\Post-Library\lib")

# Add the module path to sys.path
if lib_path not in sys.path:
    sys.path.append(lib_path)

from dictionaries import (COLORS_DICT)
from pass_mixer import (passmixer_node_group)
from lens_distortion import (lensdistortion_node)

from functions import (
    film_grain_node_group,
    vignette_node_group,
    vignette_basic_node_group,
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

class NODE_OT_FILMGRAIN(bpy.types.Operator):
    bl_label = "Film Grain"
    bl_idname = 'node.filmgrain_operator'

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

        custom_film_grain_node_name = 'Film Grain'
        image_path = self.filepath
        film_grain_group = film_grain_node_group(context, self, custom_film_grain_node_name, image_path)
        film_grain_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        film_grain_node.name = "Film Grain"
        film_grain_node.label = "Film Grain"
        film_grain_node.node_tree = bpy.data.node_groups[film_grain_group.name]
        film_grain_node.use_custom_color = True
        film_grain_node.color = COLORS_DICT["LIGHT_PURPLE"]
        film_grain_node.select = False

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

        custom_vignette_node_name = 'Vignette'
        image_path = self.filepath
        vignette_group = vignette_node_group(context, self, custom_vignette_node_name, image_path)
        vignette_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        vignette_node.name = "Vignette"
        vignette_node.label = "Vignette"
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

    def execute(shelf, context):

        custom_vignette_basic_node_name = 'Vignette-Basic'
        vignette_basic_group = vignette_basic_node_group(shelf, context, custom_vignette_basic_node_name)
        vignette_basic_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        vignette_basic_node.node_tree = bpy.data.node_groups[vignette_basic_group.name]
        vignette_basic_node.use_custom_color = True
        vignette_basic_node.color = COLORS_DICT["LIGHT_PURPLE"]
        vignette_basic_node.select = False

        return {'FINISHED'}

# Register and unregister list variable
classes = [
    # Panels
    COMP_PT_MAINPANEL,
    COMP_PT_RENDER,
    COMP_PT_FINALTOUCHES,

    # Node Groups
    NODE_OT_PASSMIXER,
    NODE_OT_LENSDISTORTION,
    NODE_OT_FILMGRAIN,
    NODE_OT_VIGNETTE,
    NODE_OT_BASICVIGNETTE
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