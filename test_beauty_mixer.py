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
        row.operator("wm.select_passes", icon="IMAGE_RGB")

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

#initialize Diffuse node group
def diffuse_node_group():
    diffuse = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = "Diffuse")

    diffuse.color_tag = "CONVERTER"
    diffuse.description = ""
    diffuse.default_group_node_width = 163

    #diffuse interface
    #Socket Diff
    diff_socket = diffuse.interface.new_socket(name = "Diff", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    diff_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    diff_socket.attribute_domain = 'POINT'

    #Socket DiffDir
    diffdir_socket = diffuse.interface.new_socket(name = "DiffDir", in_out='INPUT', socket_type = 'NodeSocketColor')
    diffdir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    diffdir_socket.attribute_domain = 'POINT'
    diffdir_socket.hide_value = True

    #Socket DiffInd
    diffind_socket = diffuse.interface.new_socket(name = "DiffInd", in_out='INPUT', socket_type = 'NodeSocketColor')
    diffind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    diffind_socket.attribute_domain = 'POINT'
    diffind_socket.hide_value = True

    #Socket DiffCol
    diffcol_socket = diffuse.interface.new_socket(name = "DiffCol", in_out='INPUT', socket_type = 'NodeSocketColor')
    diffcol_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    diffcol_socket.attribute_domain = 'POINT'
    diffcol_socket.hide_value = True

    #initialize diffuse nodes
    #node Diffuse Group Output
    diffuse_group_output = diffuse.nodes.new("NodeGroupOutput")
    diffuse_group_output.label = "Diffuse Group Output"
    diffuse_group_output.name = "Diffuse Group Output"
    diffuse_group_output.use_custom_color = True
    diffuse_group_output.color = COLORS_DICT["DARK_GRAY"]
    diffuse_group_output.is_active_output = True
    diffuse_group_output.inputs[1].hide = True

    #node Diffuse Group Input
    diffuse_group_input = diffuse.nodes.new("NodeGroupInput")
    diffuse_group_input.label = "Diffuse Group Input"
    diffuse_group_input.name = "Diffuse Group Input"
    diffuse_group_input.use_custom_color = True
    diffuse_group_input.color = COLORS_DICT["DARK_GRAY"]
    diffuse_group_input.outputs[3].hide = True

    #node add_diffuse
    add_diffuse = diffuse.nodes.new("CompositorNodeMixRGB")
    add_diffuse.label = "Add_Diffuse"
    add_diffuse.name = "add_diffuse"
    add_diffuse.use_custom_color = True
    add_diffuse.color = COLORS_DICT["BROWN"]
    add_diffuse.blend_type = 'ADD'
    add_diffuse.use_alpha = False
    add_diffuse.use_clamp = False
    add_diffuse.inputs[0].hide = True
    #Fac
    add_diffuse.inputs[0].default_value = 1.0

    #node multiply_diffuse
    multiply_diffuse = diffuse.nodes.new("CompositorNodeMixRGB")
    multiply_diffuse.label = "Multiply_Diffuse"
    multiply_diffuse.name = "multiply_diffuse"
    multiply_diffuse.use_custom_color = True
    multiply_diffuse.color = COLORS_DICT["BROWN"]
    multiply_diffuse.blend_type = 'MULTIPLY'
    multiply_diffuse.use_alpha = False
    multiply_diffuse.use_clamp = False
    multiply_diffuse.inputs[0].hide = True
    #Fac
    multiply_diffuse.inputs[0].default_value = 1.0

    #Set locations
    diffuse_group_output.location = (300.0, 0.0)
    diffuse_group_input.location = (-280.0, 0.0)
    add_diffuse.location = (-87.60699462890625, 0.0)
    multiply_diffuse.location = (100.0, 0.0)

    #Set dimensions
    diffuse_group_output.width, diffuse_group_output.height = 144.14923095703125, 100.0
    diffuse_group_input.width, diffuse_group_input.height = 140.0, 100.0
    add_diffuse.width, add_diffuse.height = 147.60699462890625, 100.0
    multiply_diffuse.width, multiply_diffuse.height = 163.0916748046875, 100.0

    #initialize diffuse links
    #add_diffuse.Image -> multiply_diffuse.Image
    diffuse.links.new(add_diffuse.outputs[0], multiply_diffuse.inputs[1])

    #diffuse_group_input.DiffCol -> multiply_diffuse.Image
    diffuse.links.new(diffuse_group_input.outputs[2], multiply_diffuse.inputs[2])

    #diffuse_group_input.DiffInd -> add_diffuse.Image
    diffuse.links.new(diffuse_group_input.outputs[1], add_diffuse.inputs[2])

    #diffuse_group_input.DiffDir -> add_diffuse.Image
    diffuse.links.new(diffuse_group_input.outputs[0], add_diffuse.inputs[1])

    #multiply_diffuse.Image -> diffuse_group_output.Diff
    diffuse.links.new(multiply_diffuse.outputs[0], diffuse_group_output.inputs[0])

    return diffuse

#initialize Glossy node group
def glossy_node_group():
    glossy = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = "Glossy")

    glossy.color_tag = "CONVERTER"
    glossy.description = ""
    glossy.default_group_node_width = 163
        

    #glossy interface
    #Socket Gloss
    gloss_socket = glossy.interface.new_socket(name = "Gloss", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    gloss_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    gloss_socket.attribute_domain = 'POINT'

    #Socket GlossDir
    glossdir_socket = glossy.interface.new_socket(name = "GlossDir", in_out='INPUT', socket_type = 'NodeSocketColor')
    glossdir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    glossdir_socket.attribute_domain = 'POINT'
    glossdir_socket.hide_value = True

    #Socket GlossInd
    glossind_socket = glossy.interface.new_socket(name = "GlossInd", in_out='INPUT', socket_type = 'NodeSocketColor')
    glossind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    glossind_socket.attribute_domain = 'POINT'
    glossind_socket.hide_value = True

    #Socket GlossCol
    glosscol_socket = glossy.interface.new_socket(name = "GlossCol", in_out='INPUT', socket_type = 'NodeSocketColor')
    glosscol_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    glosscol_socket.attribute_domain = 'POINT'
    glosscol_socket.hide_value = True

    #initialize glossy nodes
    #node Glossy Group Output
    glossy_group_output = glossy.nodes.new("NodeGroupOutput")
    glossy_group_output.label = "Glossy Group Output"
    glossy_group_output.name = "Glossy Group Output"
    glossy_group_output.use_custom_color = True
    glossy_group_output.color = COLORS_DICT["DARK_GRAY"]
    glossy_group_output.is_active_output = True
    glossy_group_output.inputs[1].hide = True

    #node Glossy Group Input
    glossy_group_input = glossy.nodes.new("NodeGroupInput")
    glossy_group_input.label = "Glossy Group Input"
    glossy_group_input.name = "Glossy Group Input"
    glossy_group_input.use_custom_color = True
    glossy_group_input.color = COLORS_DICT["DARK_GRAY"]
    glossy_group_input.outputs[3].hide = True

    #node add_glossy
    add_glossy = glossy.nodes.new("CompositorNodeMixRGB")
    add_glossy.label = "Add_Glossy"
    add_glossy.name = "add_glossy"
    add_glossy.use_custom_color = True
    add_glossy.color = COLORS_DICT["BROWN"]
    add_glossy.blend_type = 'ADD'
    add_glossy.use_alpha = False
    add_glossy.use_clamp = False
    add_glossy.inputs[0].hide = True
    #Fac
    add_glossy.inputs[0].default_value = 1.0

    #node multiply_glossy
    multiply_glossy = glossy.nodes.new("CompositorNodeMixRGB")
    multiply_glossy.label = "Multiply_Glossy"
    multiply_glossy.name = "multiply_glossy"
    multiply_glossy.use_custom_color = True
    multiply_glossy.color = COLORS_DICT["BROWN"]
    multiply_glossy.blend_type = 'MULTIPLY'
    multiply_glossy.use_alpha = False
    multiply_glossy.use_clamp = False
    multiply_glossy.inputs[0].hide = True
    #Fac
    multiply_glossy.inputs[0].default_value = 1.0

    #Set locations
    glossy_group_output.location = (300.0, 0.0)
    glossy_group_input.location = (-280.0, 0.0)
    add_glossy.location = (-87.60699462890625, 0.0)
    multiply_glossy.location = (100.0, 0.0)

    #Set dimensions
    glossy_group_output.width, glossy_group_output.height = 147.60699462890625, 100.0
    glossy_group_input.width, glossy_group_input.height = 140.0, 100.0
    add_glossy.width, add_glossy.height = 147.60699462890625, 100.0
    multiply_glossy.width, multiply_glossy.height = 163.0916748046875, 100.0

    #initialize glossy links
    #add_glossy.Image -> multiply_glossy.Image
    glossy.links.new(add_glossy.outputs[0], multiply_glossy.inputs[1])

    #glossy_group_input.GlossCol -> multiply_glossy.Image
    glossy.links.new(glossy_group_input.outputs[2], multiply_glossy.inputs[2])

    #glossy_group_input.GlossInd -> add_glossy.Image
    glossy.links.new(glossy_group_input.outputs[1], add_glossy.inputs[2])

    #glossy_group_input.GlossDir -> add_glossy.Image
    glossy.links.new(glossy_group_input.outputs[0], add_glossy.inputs[1])

    #multiply_glossy.Image -> glossy_group_output.Gloss
    glossy.links.new(multiply_glossy.outputs[0], glossy_group_output.inputs[0])

    return glossy

#initialize Transmission node group
def transmission_node_group():
    transmission = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = "Transmission")

    transmission.color_tag = "CONVERTER"
    transmission.description = ""
    transmission.default_group_node_width = 163

    #transmission interface
    #Socket Trans
    trans_socket = transmission.interface.new_socket(name = "Trans", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    trans_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    trans_socket.attribute_domain = 'POINT'

    #Socket TransDir
    transdir_socket = transmission.interface.new_socket(name = "TransDir", in_out='INPUT', socket_type = 'NodeSocketColor')
    transdir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    transdir_socket.attribute_domain = 'POINT'
    transdir_socket.hide_value = True

    #Socket TransInd
    transind_socket = transmission.interface.new_socket(name = "TransInd", in_out='INPUT', socket_type = 'NodeSocketColor')
    transind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    transind_socket.attribute_domain = 'POINT'
    transind_socket.hide_value = True

    #Socket TransCol
    transcol_socket = transmission.interface.new_socket(name = "TransCol", in_out='INPUT', socket_type = 'NodeSocketColor')
    transcol_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    transcol_socket.attribute_domain = 'POINT'
    transcol_socket.hide_value = True

    #initialize transmission nodes
    #node Transmission Group Output
    transmission_group_output = transmission.nodes.new("NodeGroupOutput")
    transmission_group_output.label = "Transmission Group Output"
    transmission_group_output.name = "Transmission Group Output"
    transmission_group_output.use_custom_color = True
    transmission_group_output.color = COLORS_DICT["DARK_GRAY"]
    transmission_group_output.is_active_output = True
    transmission_group_output.inputs[1].hide = True

    #node Transmission Group Input
    transmission_group_input = transmission.nodes.new("NodeGroupInput")
    transmission_group_input.label = "Transmission Group Input"
    transmission_group_input.name = "Transmission Group Input"
    transmission_group_input.use_custom_color = True
    transmission_group_input.color = COLORS_DICT["DARK_GRAY"]
    transmission_group_input.outputs[3].hide = True

    #node add_transmission
    add_transmission = transmission.nodes.new("CompositorNodeMixRGB")
    add_transmission.label = "Add_Transmission"
    add_transmission.name = "add_transmission"
    add_transmission.use_custom_color = True
    add_transmission.color = COLORS_DICT["BROWN"]
    add_transmission.blend_type = 'ADD'
    add_transmission.use_alpha = False
    add_transmission.use_clamp = False
    add_transmission.inputs[0].hide = True
    #Fac
    add_transmission.inputs[0].default_value = 1.0

    #node multiply_transmission
    multiply_transmission = transmission.nodes.new("CompositorNodeMixRGB")
    multiply_transmission.label = "Multiply_Transmission"
    multiply_transmission.name = "multiply_transmission"
    multiply_transmission.use_custom_color = True
    multiply_transmission.color = COLORS_DICT["BROWN"]
    multiply_transmission.blend_type = 'MULTIPLY'
    multiply_transmission.use_alpha = False
    multiply_transmission.use_clamp = False
    multiply_transmission.inputs[0].hide = True
    #Fac
    multiply_transmission.inputs[0].default_value = 1.0

    #Set locations
    transmission_group_output.location = (300.0, 0.0)
    transmission_group_input.location = (-310.42803955078125, 0.0)
    add_transmission.location = (-87.60699462890625, 0.0)
    multiply_transmission.location = (100.0, 0.0)

    #Set dimensions
    transmission_group_output.width, transmission_group_output.height = 174.54278564453125, 100.0
    transmission_group_input.width, transmission_group_input.height = 170.42803955078125, 100.0
    add_transmission.width, add_transmission.height = 147.60699462890625, 100.0
    multiply_transmission.width, multiply_transmission.height = 163.0916748046875, 100.0

    #initialize transmission links
    #add_transmission.Image -> multiply_transmission.Image
    transmission.links.new(add_transmission.outputs[0], multiply_transmission.inputs[1])

    #transmission_group_input.TransCol -> multiply_transmission.Image
    transmission.links.new(transmission_group_input.outputs[2], multiply_transmission.inputs[2])

    #transmission_group_input.TransInd -> add_transmission.Image
    transmission.links.new(transmission_group_input.outputs[1], add_transmission.inputs[2])

    #transmission_group_input.TransDir -> add_transmission.Image
    transmission.links.new(transmission_group_input.outputs[0], add_transmission.inputs[1])

    #multiply_transmission.Image -> transmission_group_output.Trans
    transmission.links.new(multiply_transmission.outputs[0], transmission_group_output.inputs[0])

    return transmission

#initialize Volume node group
def volume_node_group():
    volume = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = "Volume")

    volume.color_tag = "CONVERTER"
    volume.description = ""
    volume.default_group_node_width = 163

    #volume interface
    #Socket Volume
    volume_socket = volume.interface.new_socket(name = "Volume", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    volume_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    volume_socket.attribute_domain = 'POINT'

    #Socket VolumeDir
    volumedir_socket = volume.interface.new_socket(name = "VolumeDir", in_out='INPUT', socket_type = 'NodeSocketColor')
    volumedir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    volumedir_socket.attribute_domain = 'POINT'
    volumedir_socket.hide_value = True

    #Socket VolumeInd
    volumeind_socket = volume.interface.new_socket(name = "VolumeInd", in_out='INPUT', socket_type = 'NodeSocketColor')
    volumeind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    volumeind_socket.attribute_domain = 'POINT'
    volumeind_socket.hide_value = True

    #initialize volume nodes
    #node Volume Group Output
    volume_group_output = volume.nodes.new("NodeGroupOutput")
    volume_group_output.label = "Volume Group Output"
    volume_group_output.name = "Volume Group Output"
    volume_group_output.use_custom_color = True
    volume_group_output.color = COLORS_DICT["DARK_GRAY"]
    volume_group_output.is_active_output = True
    volume_group_output.inputs[1].hide = True

    #node Volume Group Input
    volume_group_input = volume.nodes.new("NodeGroupInput")
    volume_group_input.label = "Volume Group Input"
    volume_group_input.name = "Volume Group Input"
    volume_group_input.use_custom_color = True
    volume_group_input.color = COLORS_DICT["DARK_GRAY"]
    volume_group_input.outputs[2].hide = True

    #node add_volume
    add_volume = volume.nodes.new("CompositorNodeMixRGB")
    add_volume.label = "Add_Volume"
    add_volume.name = "add_volume"
    add_volume.use_custom_color = True
    add_volume.color = COLORS_DICT["BROWN"]
    add_volume.blend_type = 'ADD'
    add_volume.use_alpha = False
    add_volume.use_clamp = False
    add_volume.inputs[0].hide = True
    #Fac
    add_volume.inputs[0].default_value = 1.0

    #node multiply_volume
    multiply_volume = volume.nodes.new("CompositorNodeMixRGB")
    multiply_volume.label = "Multiply_Volume"
    multiply_volume.name = "multiply_volume"
    multiply_volume.use_custom_color = True
    multiply_volume.color = COLORS_DICT["BROWN"]
    multiply_volume.blend_type = 'MULTIPLY'
    multiply_volume.use_alpha = False
    multiply_volume.use_clamp = False
    multiply_volume.inputs[0].hide = True
    #Fac
    multiply_volume.inputs[0].default_value = 1.0
    #Image_001
    multiply_volume.inputs[2].default_value = (1.0, 1.0, 1.0, 1.0)

    #Set locations
    volume_group_output.location = (300.0, 0.0)
    volume_group_input.location = (-240.69866943359375, 0.0)
    add_volume.location = (-70.69866943359375, 0.0)
    multiply_volume.location = (106.9083251953125, 0.0)

    #Set dimensions
    volume_group_output.width, volume_group_output.height = 145.36395263671875, 100.0
    volume_group_input.width, volume_group_input.height = 140.0, 100.0
    add_volume.width, add_volume.height = 147.60699462890625, 100.0
    multiply_volume.width, multiply_volume.height = 163.0916748046875, 100.0

    #initialize volume links
    #add_volume.Image -> multiply_volume.Image
    volume.links.new(add_volume.outputs[0], multiply_volume.inputs[1])
        
    #volume_group_input.VolumeInd -> add_volume.Image
    volume.links.new(volume_group_input.outputs[1], add_volume.inputs[2])

    #volume_group_input.VolumeDir -> add_volume.Image
    volume.links.new(volume_group_input.outputs[0], add_volume.inputs[1])

    #multiply_volume.Image -> volume_group_output.Volume
    volume.links.new(multiply_volume.outputs[0], volume_group_output.inputs[0])

    return volume

#initialize BeautyMixer node group
def beautymixer_node_group(context, operator, group_name):

    #enable use nodes
    bpy.context.scene.use_nodes = True

    beautymixer = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
        
    beautymixer.color_tag = "CONVERTER"
    beautymixer.description = "Mix all the beauty passes"
    beautymixer.default_group_node_width = 162

    #beautymixer interface
    #Socket Diff
    diff_socket_1 = beautymixer.interface.new_socket(name = "Diff", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    diff_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    diff_socket_1.attribute_domain = 'POINT'

    #Socket Gloss
    gloss_socket_1 = beautymixer.interface.new_socket(name = "Gloss", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    gloss_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    gloss_socket_1.attribute_domain = 'POINT'

    #Socket Trans
    trans_socket_1 = beautymixer.interface.new_socket(name = "Trans", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    trans_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    trans_socket_1.attribute_domain = 'POINT'

    #Socket Volume
    volume_socket_1 = beautymixer.interface.new_socket(name = "Volume", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    volume_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    volume_socket_1.attribute_domain = 'POINT'

    #Panel Diffuse
    diffuse_panel = beautymixer.interface.new_panel("Diffuse", default_closed=True)
    diffuse_panel.description = "For mixing diffuse pass"

    #Socket DiffDir
    diffdir_socket_1 = beautymixer.interface.new_socket(name = "DiffDir", in_out='INPUT', socket_type = 'NodeSocketColor', parent = diffuse_panel)
    diffdir_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    diffdir_socket_1.attribute_domain = 'POINT'
    diffdir_socket_1.hide_value = True

    #Socket DiffInd
    diffind_socket_1 = beautymixer.interface.new_socket(name = "DiffInd", in_out='INPUT', socket_type = 'NodeSocketColor', parent = diffuse_panel)
    diffind_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    diffind_socket_1.attribute_domain = 'POINT'
    diffind_socket_1.hide_value = True

    #Socket DiffCol
    diffcol_socket_1 = beautymixer.interface.new_socket(name = "DiffCol", in_out='INPUT', socket_type = 'NodeSocketColor', parent = diffuse_panel)
    diffcol_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    diffcol_socket_1.attribute_domain = 'POINT'
    diffcol_socket_1.hide_value = True

    #Panel Glossy
    glossy_panel = beautymixer.interface.new_panel("Glossy", default_closed=True)
    glossy_panel.description = "For mixing glossy pass"
    
    #Socket GlossDir
    glossdir_socket_1 = beautymixer.interface.new_socket(name = "GlossDir", in_out='INPUT', socket_type = 'NodeSocketColor', parent = glossy_panel)
    glossdir_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    glossdir_socket_1.attribute_domain = 'POINT'
    glossdir_socket_1.hide_value = True

    #Socket GlossInd
    glossind_socket_1 = beautymixer.interface.new_socket(name = "GlossInd", in_out='INPUT', socket_type = 'NodeSocketColor', parent = glossy_panel)
    glossind_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    glossind_socket_1.attribute_domain = 'POINT'
    glossind_socket_1.hide_value = True

    #Socket GlossCol
    glosscol_socket_1 = beautymixer.interface.new_socket(name = "GlossCol", in_out='INPUT', socket_type = 'NodeSocketColor', parent = glossy_panel)
    glosscol_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    glosscol_socket_1.attribute_domain = 'POINT'
    glosscol_socket_1.hide_value = True

    #Panel Transmission
    transmission_panel = beautymixer.interface.new_panel("Transmission", default_closed=True)
    transmission_panel.description = "For mixing transmission pass"

    #Socket TransDir
    transdir_socket_1 = beautymixer.interface.new_socket(name = "TransDir", in_out='INPUT', socket_type = 'NodeSocketColor', parent = transmission_panel)
    transdir_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    transdir_socket_1.attribute_domain = 'POINT'
    transdir_socket_1.hide_value = True

    #Socket TransInd
    transind_socket_1 = beautymixer.interface.new_socket(name = "TransInd", in_out='INPUT', socket_type = 'NodeSocketColor', parent = transmission_panel)
    transind_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    transind_socket_1.attribute_domain = 'POINT'
    transind_socket_1.hide_value = True

    #Socket TransCol
    transcol_socket_1 = beautymixer.interface.new_socket(name = "TransCol", in_out='INPUT', socket_type = 'NodeSocketColor', parent = transmission_panel)
    transcol_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    transcol_socket_1.attribute_domain = 'POINT'
    transcol_socket_1.hide_value = True

    #Panel Volume
    volume_panel = beautymixer.interface.new_panel("Volume", default_closed=True)
    volume_panel.description = "For mixing volume pass"

    #Socket VolumeDir
    volumedir_socket_1 = beautymixer.interface.new_socket(name = "VolumeDir", in_out='INPUT', socket_type = 'NodeSocketColor', parent = volume_panel)
    volumedir_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    volumedir_socket_1.attribute_domain = 'POINT'
    volumedir_socket_1.hide_value = True

    #Socket VolumeInd
    volumeind_socket_1 = beautymixer.interface.new_socket(name = "VolumeInd", in_out='INPUT', socket_type = 'NodeSocketColor', parent = volume_panel)
    volumeind_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    volumeind_socket_1.attribute_domain = 'POINT'
    volumeind_socket_1.hide_value = True

    #initialize beautymixer nodes
    #node BM Group Output
    bm_group_output = beautymixer.nodes.new("NodeGroupOutput")
    bm_group_output.label = "BM Group Output"
    bm_group_output.name = "BM Group Output"
    bm_group_output.use_custom_color = True
    bm_group_output.color = COLORS_DICT["DARK_GRAY"]
    bm_group_output.is_active_output = True
    bm_group_output.inputs[4].hide = True

    #node BM Group Input
    bm_group_input = beautymixer.nodes.new("NodeGroupInput")
    bm_group_input.label = "BM Group Input"
    bm_group_input.name = "BM Group Input"
    bm_group_input.use_custom_color = True
    bm_group_input.color = COLORS_DICT["DARK_GRAY"]
    bm_group_input.outputs[11].hide = True

    #node Diffuse
    diffuse_1 = beautymixer.nodes.new("CompositorNodeGroup")
    diffuse_1.label = "Diffuse"
    diffuse_1.name = "Diffuse"
    diffuse_1.use_custom_color = True
    diffuse_1.color = COLORS_DICT["DARK_BLUE"]
    diffuse_1.node_tree = diffuse_node_group()

    #node Glossy
    glossy_1 = beautymixer.nodes.new("CompositorNodeGroup")
    glossy_1.label = "Glossy"
    glossy_1.name = "Glossy"
    glossy_1.use_custom_color = True
    glossy_1.color = COLORS_DICT["DARK_BLUE"]
    glossy_1.node_tree = glossy_node_group()

    #node Transmission
    transmission_1 = beautymixer.nodes.new("CompositorNodeGroup")
    transmission_1.label = "Transmission"
    transmission_1.name = "Transmission"
    transmission_1.use_custom_color = True
    transmission_1.color = COLORS_DICT["DARK_BLUE"]
    transmission_1.node_tree = transmission_node_group()

    #node Volume
    volume_1 = beautymixer.nodes.new("CompositorNodeGroup")
    volume_1.label = "Volume"
    volume_1.name = "Volume"
    volume_1.use_custom_color = True
    volume_1.color = COLORS_DICT["DARK_BLUE"]
    volume_1.node_tree = volume_node_group()

    #Set locations
    bm_group_output.location = (560.0, -100.0)
    bm_group_input.location = (-300.0, -20.0)
    diffuse_1.location = (120.0, 157.1907958984375)
    glossy_1.location = (120.0, -23.603065490722656)
    transmission_1.location = (120.0, -204.39694213867188)
    volume_1.location = (120.0, -385.1907958984375)

    #Set dimensions
    bm_group_output.width, bm_group_output.height = 140.0, 100.0
    bm_group_input.width, bm_group_input.height = 140.0, 100.0
    diffuse_1.width, diffuse_1.height = 163.51251220703125, 100.0
    glossy_1.width, glossy_1.height = 163.51251220703125, 100.0
    transmission_1.width, transmission_1.height = 163.51251220703125, 100.0
    volume_1.width, volume_1.height = 163.51251220703125, 100.0

    #initialize beautymixer links
    #diffuse_1.Diff -> bm_group_output.Diff
    beautymixer.links.new(diffuse_1.outputs[0], bm_group_output.inputs[0])

    #glossy_1.Gloss -> bm_group_output.Gloss
    beautymixer.links.new(glossy_1.outputs[0], bm_group_output.inputs[1])

    #transmission_1.Trans -> bm_group_output.Trans
    beautymixer.links.new(transmission_1.outputs[0], bm_group_output.inputs[2])

    #volume_1.Volume -> bm_group_output.Volume
    beautymixer.links.new(volume_1.outputs[0], bm_group_output.inputs[3])

    #bm_group_input.DiffDir -> diffuse_1.DiffDir
    beautymixer.links.new(bm_group_input.outputs[0], diffuse_1.inputs[0])

    #bm_group_input.DiffInd -> diffuse_1.DiffInd
    beautymixer.links.new(bm_group_input.outputs[1], diffuse_1.inputs[1])

    #bm_group_input.DiffCol -> diffuse_1.DiffCol
    beautymixer.links.new(bm_group_input.outputs[2], diffuse_1.inputs[2])

    #bm_group_input.GlossDir -> glossy_1.GlossDir
    beautymixer.links.new(bm_group_input.outputs[3], glossy_1.inputs[0])

    #bm_group_input.GlossInd -> glossy_1.GlossInd
    beautymixer.links.new(bm_group_input.outputs[4], glossy_1.inputs[1])

    #bm_group_input.GlossCol -> glossy_1.GlossCol
    beautymixer.links.new(bm_group_input.outputs[5], glossy_1.inputs[2])

    #bm_group_input.TransDir -> transmission_1.TransDir
    beautymixer.links.new(bm_group_input.outputs[6], transmission_1.inputs[0])

    #bm_group_input.TransInd -> transmission_1.TransInd
    beautymixer.links.new(bm_group_input.outputs[7], transmission_1.inputs[1])

    #bm_group_input.TransCol -> transmission_1.TransCol
    beautymixer.links.new(bm_group_input.outputs[8], transmission_1.inputs[2])

    #bm_group_input.VolumeDir -> volume_1.VolumeDir
    beautymixer.links.new(bm_group_input.outputs[9], volume_1.inputs[0])

    #bm_group_input.VolumeInd -> volume_1.VolumeInd
    beautymixer.links.new(bm_group_input.outputs[10], volume_1.inputs[1])

    return beautymixer

class NODE_OT_BEAUTYMIXER(bpy.types.Operator):
    """To mix all the beauty passes"""
    bl_label = "BeautyMixer"
    bl_idname = "node.beautymixer_operator"

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


class WM_OT_SELECT_PASSES(bpy.types.Operator):
    bl_idname = "wm.select_passes"
    bl_label = "Passes Selection"

    diffuse_bool: bpy.props.BoolProperty(name="Diffuse", default=False)
    glossy_bool: bpy.props.BoolProperty(name="Glossy", default=False)
    transmission_bool: bpy.props.BoolProperty(name="Transmission", default=False)
    volume_bool: bpy.props.BoolProperty(name="Volume", default=False)
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
 
    def execute(self, context):
 
        return {'FINISHED'}
    
# Register and unregister
classes = [COMP_PT_MAINPANEL, NODE_OT_BEAUTYMIXER, WM_OT_SELECT_PASSES]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()