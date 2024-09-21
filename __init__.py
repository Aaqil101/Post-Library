# ##### BEGIN LICENSE BLOCK #####
#
#  Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) 
#
#  This work is licensed under the Creative Commons
#  Attribution-NonCommercial-NoDerivatives 4.0 International License. 
#
#  To view a copy of this license,
#  visit http://creativecommons.org/licenses/by-nc-nd/4.0/.
#
# ##### END LICENSE BLOCK #####

bl_info = {
    "name": "Post Library",
    "author": "Aaqil",
    "version": (1, 0),
    "blender": (4, 2, 1),
    "location": "Compositor > Toolshelf",
    "description": "Boost your Blender workflow with essential tools for efficient VFX and post-processing. Simplify compositing, and finishing touches with this powerful addon.",
    "warning": "",
    "doc_url": "",
    "category": "Nodes",
}

import bpy
import bpy, mathutils
import sys

sys.path.append(r"C:\Users\User\Documents\PY - Scripting\Blender\PostLibrary")

from dictionaries import COLORS_DICT

from functions import (
    multidenoiser_node_group,
    passmixer_node_group,
    lensdistortion_node,
    film_grain_node_group,
    vignette_node_group,
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
        row.operator('node.multidenoiser_operator', icon= 'RENDER_RESULT')
        row.operator('node.passmixer_operator', icon= 'STICKY_UVS_DISABLE')
        row = layout.row()
        row.operator('node.lensdistortion_operator', icon= 'DRIVER_DISTANCE')
        row.operator('node.filmgrain_operator', icon= 'FILE_MOVIE')
        row = layout.row()
        row.operator('node.vignette_operator', icon= 'IMAGE_RGB')

class NODE_OT_MULTIDENOISER(bpy.types.Operator):
    bl_label = "MultiDenoiser"
    bl_idname = 'node.multidenoiser_operator'

    def execute(shelf, context):

        custom_multidenoiser_node_name = 'MultiDenoiser'
        multidenoiser_group = multidenoiser_node_group(shelf, context, custom_multidenoiser_node_name)
        multidenoiser_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        multidenoiser_node.node_tree = bpy.data.node_groups[multidenoiser_group.name]
        multidenoiser_node.use_custom_color = True
        bpy.data.node_groups["MultiDenoiser"].color_tag = 'FILTER'
        multidenoiser_node.color = COLORS_DICT["LIGHT_PURPLE"]
        multidenoiser_node.select = False

        return {'FINISHED'}

class NODE_OT_PASSMIXER(bpy.types.Operator):
    bl_label = "PassMixer"
    bl_idname = 'node.passmixer_operator'

    def execute(shelf, context):

        custom_passmixer_node_name = 'PassMixer'
        passmixer_group = passmixer_node_group(shelf, context, custom_passmixer_node_name)
        passmixer_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
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

def register():
    bpy.utils.register_class(COMP_PT_MAINPANEL)
    bpy.utils.register_class(NODE_OT_MULTIDENOISER)
    bpy.utils.register_class(NODE_OT_PASSMIXER)
    bpy.utils.register_class(NODE_OT_LENSDISTORTION)
    bpy.utils.register_class(NODE_OT_FILMGRAIN)
    bpy.utils.register_class(NODE_OT_VIGNETTE)

def unregister():
    bpy.utils.unregister_class(COMP_PT_MAINPANEL)
    bpy.utils.unregister_class(NODE_OT_MULTIDENOISER)
    bpy.utils.unregister_class(NODE_OT_PASSMIXER)
    bpy.utils.unregister_class(NODE_OT_LENSDISTORTION)
    bpy.utils.unregister_class(NODE_OT_FILMGRAIN)
    bpy.utils.unregister_class(NODE_OT_VIGNETTE)

if __name__ == "__main__":
    register()