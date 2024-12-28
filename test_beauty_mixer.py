import bpy
from typing import Tuple
from bpy.props import BoolProperty, EnumProperty

class COMP_PT_MAINPANEL(bpy.types.Panel):
    bl_label = "test"
    bl_idname = "COMP_PT_MAINPANEL"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "T"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("node.beautymixer_operator", text=Names.BeautyMixer, icon="IMAGE_RGB")

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

# Class to store color values converted from hex codes to RGB
class Color:
    LIGHT_RED = hexcode_to_rgb("#94493E")
    DARK_RED = hexcode_to_rgb("#823A35")
    LIGHT_BLUE = hexcode_to_rgb("#646E66")
    DARK_BLUE = hexcode_to_rgb("#4C6160")
    LIGHT_PURPLE = hexcode_to_rgb("#846167")
    DARK_PURPLE = hexcode_to_rgb("#77535F")
    BROWN = hexcode_to_rgb("#866937")
    DARK_GRAY = hexcode_to_rgb("#3C3937")
    LIGHT_GRAY = hexcode_to_rgb("#59514B")

# Class to store the names of various passes and sockets
class Names:
    BeautyMixer = "BeautyMixer"
    Diffuse = "Diffuse"
    Glossy = "Glossy"
    Transmission = "Transmission"
    Volume = "Volume"
    Diff = "Diff"
    Gloss = "Gloss"
    Trans = "Trans"
    Vol = "Vol"
    DiffDir = "DiffDir"
    DiffInd = "DiffInd"
    DiffCol = "DiffCol"
    GlossDir = "GlossDir"
    GlossInd = "GlossInd"
    GlossCol = "GlossCol"
    TransDir = "TransDir"
    TransInd = "TransInd"
    TransCol = "TransCol"
    VolumeDir = "VolumeDir"
    VolumeInd = "VolumeInd"

#initialize Diffuse node group
def diffuse_node_group():
    diffuse = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = Names.Diff)

    diffuse.color_tag = "CONVERTER"
    diffuse.description = "A node group for mixing diffuse passes together."
    diffuse.default_group_node_width = 163

    #diffuse interface
    #Socket Diff
    diff_socket = diffuse.interface.new_socket(name = Names.Diff, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    diff_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    diff_socket.attribute_domain = 'POINT'

    #Socket DiffDir
    diffdir_socket = diffuse.interface.new_socket(name = Names.DiffDir, in_out='INPUT', socket_type = 'NodeSocketColor')
    diffdir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    diffdir_socket.attribute_domain = 'POINT'
    diffdir_socket.hide_value = True

    #Socket DiffInd
    diffind_socket = diffuse.interface.new_socket(name = Names.DiffInd, in_out='INPUT', socket_type = 'NodeSocketColor')
    diffind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    diffind_socket.attribute_domain = 'POINT'
    diffind_socket.hide_value = True

    #Socket DiffCol
    diffcol_socket = diffuse.interface.new_socket(name = Names.DiffCol, in_out='INPUT', socket_type = 'NodeSocketColor')
    diffcol_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    diffcol_socket.attribute_domain = 'POINT'
    diffcol_socket.hide_value = True

    #initialize diffuse nodes
    #node Diffuse Group Output
    diffuse_group_output = diffuse.nodes.new("NodeGroupOutput")
    diffuse_group_output.label = "Diffuse Group Output"
    diffuse_group_output.name = "Diffuse Group Output"
    diffuse_group_output.use_custom_color = True
    diffuse_group_output.color = Color.DARK_GRAY
    diffuse_group_output.is_active_output = True
    diffuse_group_output.inputs[1].hide = True

    #node Diffuse Group Input
    diffuse_group_input = diffuse.nodes.new("NodeGroupInput")
    diffuse_group_input.label = "Diffuse Group Input"
    diffuse_group_input.name = "Diffuse Group Input"
    diffuse_group_input.use_custom_color = True
    diffuse_group_input.color = Color.DARK_GRAY
    diffuse_group_input.outputs[3].hide = True

    #node add_diffuse
    add_diffuse = diffuse.nodes.new("CompositorNodeMixRGB")
    add_diffuse.label = "Add_Diffuse"
    add_diffuse.name = "add_diffuse"
    add_diffuse.use_custom_color = True
    add_diffuse.color = Color.BROWN
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
    multiply_diffuse.color = Color.BROWN
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
    glossy = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = Names.Gloss)

    glossy.color_tag = "CONVERTER"
    glossy.description = "A node group for mixing glossy passes together."
    glossy.default_group_node_width = 163     

    #glossy interface
    #Socket Gloss
    gloss_socket = glossy.interface.new_socket(name = Names.Gloss, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    gloss_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    gloss_socket.attribute_domain = 'POINT'

    #Socket GlossDir
    glossdir_socket = glossy.interface.new_socket(name = Names.GlossDir, in_out='INPUT', socket_type = 'NodeSocketColor')
    glossdir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    glossdir_socket.attribute_domain = 'POINT'
    glossdir_socket.hide_value = True

    #Socket GlossInd
    glossind_socket = glossy.interface.new_socket(name = Names.GlossInd, in_out='INPUT', socket_type = 'NodeSocketColor')
    glossind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    glossind_socket.attribute_domain = 'POINT'
    glossind_socket.hide_value = True

    #Socket GlossCol
    glosscol_socket = glossy.interface.new_socket(name = Names.GlossCol, in_out='INPUT', socket_type = 'NodeSocketColor')
    glosscol_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    glosscol_socket.attribute_domain = 'POINT'
    glosscol_socket.hide_value = True

    #initialize glossy nodes
    #node Glossy Group Output
    glossy_group_output = glossy.nodes.new("NodeGroupOutput")
    glossy_group_output.label = "Glossy Group Output"
    glossy_group_output.name = "Glossy Group Output"
    glossy_group_output.use_custom_color = True
    glossy_group_output.color = Color.DARK_GRAY
    glossy_group_output.is_active_output = True
    glossy_group_output.inputs[1].hide = True

    #node Glossy Group Input
    glossy_group_input = glossy.nodes.new("NodeGroupInput")
    glossy_group_input.label = "Glossy Group Input"
    glossy_group_input.name = "Glossy Group Input"
    glossy_group_input.use_custom_color = True
    glossy_group_input.color = Color.DARK_GRAY
    glossy_group_input.outputs[3].hide = True

    #node add_glossy
    add_glossy = glossy.nodes.new("CompositorNodeMixRGB")
    add_glossy.label = "Add_Glossy"
    add_glossy.name = "add_glossy"
    add_glossy.use_custom_color = True
    add_glossy.color = Color.BROWN
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
    multiply_glossy.color = Color.BROWN
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
    transmission = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = Names.Trans)

    transmission.color_tag = "CONVERTER"
    transmission.description = "A node group for mixing transmission passes together."
    transmission.default_group_node_width = 163

    #transmission interface
    #Socket Trans
    trans_socket = transmission.interface.new_socket(name = Names.Trans, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    trans_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    trans_socket.attribute_domain = 'POINT'

    #Socket TransDir
    transdir_socket = transmission.interface.new_socket(name = Names.TransDir, in_out='INPUT', socket_type = 'NodeSocketColor')
    transdir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    transdir_socket.attribute_domain = 'POINT'
    transdir_socket.hide_value = True

    #Socket TransInd
    transind_socket = transmission.interface.new_socket(name = Names.TransInd, in_out='INPUT', socket_type = 'NodeSocketColor')
    transind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    transind_socket.attribute_domain = 'POINT'
    transind_socket.hide_value = True

    #Socket TransCol
    transcol_socket = transmission.interface.new_socket(name = Names.TransCol, in_out='INPUT', socket_type = 'NodeSocketColor')
    transcol_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    transcol_socket.attribute_domain = 'POINT'
    transcol_socket.hide_value = True

    #initialize transmission nodes
    #node Transmission Group Output
    transmission_group_output = transmission.nodes.new("NodeGroupOutput")
    transmission_group_output.label = "Transmission Group Output"
    transmission_group_output.name = "Transmission Group Output"
    transmission_group_output.use_custom_color = True
    transmission_group_output.color = Color.DARK_GRAY
    transmission_group_output.is_active_output = True
    transmission_group_output.inputs[1].hide = True

    #node Transmission Group Input
    transmission_group_input = transmission.nodes.new("NodeGroupInput")
    transmission_group_input.label = "Transmission Group Input"
    transmission_group_input.name = "Transmission Group Input"
    transmission_group_input.use_custom_color = True
    transmission_group_input.color = Color.DARK_GRAY
    transmission_group_input.outputs[3].hide = True

    #node add_transmission
    add_transmission = transmission.nodes.new("CompositorNodeMixRGB")
    add_transmission.label = "Add_Transmission"
    add_transmission.name = "add_transmission"
    add_transmission.use_custom_color = True
    add_transmission.color = Color.BROWN
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
    multiply_transmission.color = Color.BROWN
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
    volume = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = Names.Vol)

    volume.color_tag = "CONVERTER"
    volume.description = "A node group for mixing volume passes together."
    volume.default_group_node_width = 163

    #volume interface
    #Socket Volume
    volume_socket = volume.interface.new_socket(name = Names.Volume, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    volume_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    volume_socket.attribute_domain = 'POINT'

    #Socket VolumeDir
    volumedir_socket = volume.interface.new_socket(name = Names.VolumeDir, in_out='INPUT', socket_type = 'NodeSocketColor')
    volumedir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    volumedir_socket.attribute_domain = 'POINT'
    volumedir_socket.hide_value = True

    #Socket VolumeInd
    volumeind_socket = volume.interface.new_socket(name = Names.VolumeInd, in_out='INPUT', socket_type = 'NodeSocketColor')
    volumeind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    volumeind_socket.attribute_domain = 'POINT'
    volumeind_socket.hide_value = True

    #initialize volume nodes
    #node Volume Group Output
    volume_group_output = volume.nodes.new("NodeGroupOutput")
    volume_group_output.label = "Volume Group Output"
    volume_group_output.name = "Volume Group Output"
    volume_group_output.use_custom_color = True
    volume_group_output.color = Color.DARK_GRAY
    volume_group_output.is_active_output = True
    volume_group_output.inputs[1].hide = True

    #node Volume Group Input
    volume_group_input = volume.nodes.new("NodeGroupInput")
    volume_group_input.label = "Volume Group Input"
    volume_group_input.name = "Volume Group Input"
    volume_group_input.use_custom_color = True
    volume_group_input.color = Color.DARK_GRAY
    volume_group_input.outputs[2].hide = True

    #node add_volume
    add_volume = volume.nodes.new("CompositorNodeMixRGB")
    add_volume.label = "Add_Volume"
    add_volume.name = "add_volume"
    add_volume.use_custom_color = True
    add_volume.color = Color.BROWN
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
    multiply_volume.color = Color.BROWN
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
    diff_socket_1 = beautymixer.interface.new_socket(name = Names.Diff, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    diff_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    diff_socket_1.attribute_domain = 'POINT'

    #Socket Gloss
    gloss_socket_1 = beautymixer.interface.new_socket(name = Names.Gloss, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    gloss_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    gloss_socket_1.attribute_domain = 'POINT'

    #Socket Trans
    trans_socket_1 = beautymixer.interface.new_socket(name = Names.Trans, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    trans_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    trans_socket_1.attribute_domain = 'POINT'

    #Socket Volume
    volume_socket_1 = beautymixer.interface.new_socket(name = Names.Vol, in_out='OUTPUT', socket_type = 'NodeSocketColor')
    volume_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    volume_socket_1.attribute_domain = 'POINT'

    #Panel Diffuse
    diffuse_panel = beautymixer.interface.new_panel(Names.Diffuse, default_closed=False)
    diffuse_panel.description = "For mixing diffuse pass"

    #Socket DiffDir
    diffdir_socket_1 = beautymixer.interface.new_socket(name = Names.DiffDir, in_out='INPUT', socket_type = 'NodeSocketColor', parent = diffuse_panel)
    diffdir_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    diffdir_socket_1.attribute_domain = 'POINT'
    diffdir_socket_1.hide_value = True

    #Socket DiffInd
    diffind_socket_1 = beautymixer.interface.new_socket(name = Names.DiffInd, in_out='INPUT', socket_type = 'NodeSocketColor', parent = diffuse_panel)
    diffind_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    diffind_socket_1.attribute_domain = 'POINT'
    diffind_socket_1.hide_value = True

    #Socket DiffCol
    diffcol_socket_1 = beautymixer.interface.new_socket(name = Names.DiffCol, in_out='INPUT', socket_type = 'NodeSocketColor', parent = diffuse_panel)
    diffcol_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    diffcol_socket_1.attribute_domain = 'POINT'
    diffcol_socket_1.hide_value = True

    #Panel Glossy
    glossy_panel = beautymixer.interface.new_panel(Names.Glossy, default_closed=False)
    glossy_panel.description = "For mixing glossy pass"
    
    #Socket GlossDir
    glossdir_socket_1 = beautymixer.interface.new_socket(name = Names.GlossDir, in_out='INPUT', socket_type = 'NodeSocketColor', parent = glossy_panel)
    glossdir_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    glossdir_socket_1.attribute_domain = 'POINT'
    glossdir_socket_1.hide_value = True

    #Socket GlossInd
    glossind_socket_1 = beautymixer.interface.new_socket(name = Names.GlossInd, in_out='INPUT', socket_type = 'NodeSocketColor', parent = glossy_panel)
    glossind_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    glossind_socket_1.attribute_domain = 'POINT'
    glossind_socket_1.hide_value = True

    #Socket GlossCol
    glosscol_socket_1 = beautymixer.interface.new_socket(name = Names.GlossCol, in_out='INPUT', socket_type = 'NodeSocketColor', parent = glossy_panel)
    glosscol_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    glosscol_socket_1.attribute_domain = 'POINT'
    glosscol_socket_1.hide_value = True

    #Panel Transmission
    transmission_panel = beautymixer.interface.new_panel(Names.Transmission, default_closed=False)
    transmission_panel.description = "For mixing transmission pass"

    #Socket TransDir
    transdir_socket_1 = beautymixer.interface.new_socket(name = Names.TransDir, in_out='INPUT', socket_type = 'NodeSocketColor', parent = transmission_panel)
    transdir_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    transdir_socket_1.attribute_domain = 'POINT'
    transdir_socket_1.hide_value = True

    #Socket TransInd
    transind_socket_1 = beautymixer.interface.new_socket(name = Names.TransInd, in_out='INPUT', socket_type = 'NodeSocketColor', parent = transmission_panel)
    transind_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    transind_socket_1.attribute_domain = 'POINT'
    transind_socket_1.hide_value = True

    #Socket TransCol
    transcol_socket_1 = beautymixer.interface.new_socket(name = Names.TransCol, in_out='INPUT', socket_type = 'NodeSocketColor', parent = transmission_panel)
    transcol_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    transcol_socket_1.attribute_domain = 'POINT'
    transcol_socket_1.hide_value = True

    #Panel Volume
    volume_panel = beautymixer.interface.new_panel(Names.Volume, default_closed=False)
    volume_panel.description = "For mixing volume pass"

    #Socket VolumeDir
    volumedir_socket_1 = beautymixer.interface.new_socket(name = Names.VolumeDir, in_out='INPUT', socket_type = 'NodeSocketColor', parent = volume_panel)
    volumedir_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    volumedir_socket_1.attribute_domain = 'POINT'
    volumedir_socket_1.hide_value = True

    #Socket VolumeInd
    volumeind_socket_1 = beautymixer.interface.new_socket(name = Names.VolumeInd, in_out='INPUT', socket_type = 'NodeSocketColor', parent = volume_panel)
    volumeind_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    volumeind_socket_1.attribute_domain = 'POINT'
    volumeind_socket_1.hide_value = True

    #initialize beautymixer nodes
    #node BM Group Output
    bm_group_output = beautymixer.nodes.new("NodeGroupOutput")
    bm_group_output.label = "BM Group Output"
    bm_group_output.name = "BM Group Output"
    bm_group_output.use_custom_color = True
    bm_group_output.color = Color.DARK_GRAY
    bm_group_output.is_active_output = True
    bm_group_output.inputs[4].hide = True

    #node BM Group Input
    bm_group_input = beautymixer.nodes.new("NodeGroupInput")
    bm_group_input.label = "BM Group Input"
    bm_group_input.name = "BM Group Input"
    bm_group_input.use_custom_color = True
    bm_group_input.color = Color.DARK_GRAY
    bm_group_input.outputs[11].hide = True

    #node Diffuse
    diffuse_1 = beautymixer.nodes.new("CompositorNodeGroup")
    diffuse_1.label = Names.Diff
    diffuse_1.name = Names.Diff
    diffuse_1.use_custom_color = True
    diffuse_1.color = Color.DARK_BLUE
    diffuse_1.node_tree = diffuse_node_group()

    #node Glossy
    glossy_1 = beautymixer.nodes.new("CompositorNodeGroup")
    glossy_1.label = Names.Gloss
    glossy_1.name = Names.Gloss
    glossy_1.use_custom_color = True
    glossy_1.color = Color.DARK_BLUE
    glossy_1.node_tree = glossy_node_group()

    #node Transmission
    transmission_1 = beautymixer.nodes.new("CompositorNodeGroup")
    transmission_1.label = Names.Trans
    transmission_1.name = Names.Trans
    transmission_1.use_custom_color = True
    transmission_1.color = Color.DARK_BLUE
    transmission_1.node_tree = transmission_node_group()

    #node Volume
    volume_1 = beautymixer.nodes.new("CompositorNodeGroup")
    volume_1.label = Names.Vol
    volume_1.name = Names.Vol
    volume_1.use_custom_color = True
    volume_1.color = Color.DARK_BLUE
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
    bl_label = Names.BeautyMixer
    bl_idname = "node.beautymixer_operator"

    def execute(shelf, context):

        # Deselect all selected nodes
        for node in context.scene.node_tree.nodes:
            node.select = False

        # Create a new node group for the BeautyMixer
        custom_beautymixer_node_name = Names.BeautyMixer
        beautymixer_group = beautymixer_node_group(shelf, context, custom_beautymixer_node_name)
        beautymixer_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        beautymixer_node.name = Names.BeautyMixer
        beautymixer_node.label = Names.BeautyMixer
        beautymixer_node.width = 162
        beautymixer_node.node_tree = bpy.data.node_groups[beautymixer_group.name]
        beautymixer_node.use_custom_color = True
        beautymixer_node.color = Color.DARK_BLUE
        beautymixer_node.select = True

        # Invoking WM_OT_SELECT_PASSES operator to let the user select the passes
        # The 'INVOKE_DEFAULT' argument is used to show the dialog box
        # https://docs.blender.org/api/blender_python_api_current/bpy.ops.html
        bpy.ops.wm.select_passes('INVOKE_DEFAULT')

        return {'FINISHED'}

class WM_OT_SELECT_PASSES(bpy.types.Operator):
    bl_idname = "wm.select_passes"
    bl_label = "Pass/Passes Selector"

    diffuse_bool: BoolProperty(name=Names.Diffuse, default=False) # type: ignore
    glossy_bool: BoolProperty(name=Names.Glossy, default=False) # type: ignore
    transmission_bool: BoolProperty(name=Names.Transmission, default=False) # type: ignore
    volume_bool: BoolProperty(name=Names.Volume, default=False) # type: ignore

    group_ungroup_enum: EnumProperty(
        name="Group/Ungroup",
        description="Choose whether to group or ungroup selected nodes",
        items=[
            ("GROUP", "Group", "Combine selected nodes into a node group", "NODETREE", 0),
            ("UNGROUP", "Ungroup", "Break apart the node group into individual nodes", "X", 1)
        ],
        default="GROUP"
    ) # type: ignore
    
    def invoke(self, context, event):

        node_tree = bpy.context.scene.node_tree

        # find the selected mixer node
        self.beauty_mixer_node = None
        for node in node_tree.nodes:
            if Names.BeautyMixer in node.name and node.select:
                self.beauty_mixer_node = node
                break
            
        if self.beauty_mixer_node is None:
            self.report({'WARNING'}, "Please select a BeautyMixer node!")
            return {'CANCELLED'}

        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        layout.label(text= "Choose the pass or passes that you want to keep:")

        row = layout.row()
        row.prop(self, "diffuse_bool", text=Names.Diffuse, icon='MATERIAL')
        row.prop(self, "glossy_bool", text=Names.Glossy, icon='SHADING_RENDERED')

        row = layout.row()
        row.prop(self, "transmission_bool", text=Names.Transmission, icon='OUTLINER_OB_LIGHT')
        row.prop(self, "volume_bool", text=Names.Volume, icon='MOD_FLUID')

        if sum([self.diffuse_bool, self.glossy_bool, self.transmission_bool, self.volume_bool]) >= 2:
            layout.alignment = 'RIGHT'
            layout.prop(self, "group_ungroup_enum")

    def execute(self, context):
        # Retrieve the boolean values for each pass and the enum property
        db = self.diffuse_bool
        gb = self.glossy_bool
        tb = self.transmission_bool
        vb = self.volume_bool
        enum = self.group_ungroup_enum
        
        # Get the current node tree
        node_tree = bpy.context.scene.node_tree
        node_selected = bpy.context.selected_nodes

        def rm_nodes_from_group(parent_node_group, node_names_to_remove):
            """
            Removes nodes from a node group that have names matching any of the ones in node_names_to_remove.

            Args:
                parent_node_group (bpy.types.NodeTree): The node group to remove nodes from.
                node_names_to_remove (list of str): A list of node group names to remove from the parent node group.

            Returns:
                None
            """
            if not parent_node_group:
                print(f"Parent node group not provided or not found.")
                return
    
            nodes_to_remove = []

            # Iterate through nodes in the parent node group
            for node in parent_node_group.node_tree.nodes:
                if node.type == 'GROUP' and any(name in node.node_tree.name for name in node_names_to_remove):
                    # Add nodes to the list to remove
                    nodes_to_remove.append(node)

            # Remove nodes from the parent node group
            for node in nodes_to_remove:
                parent_node_group.node_tree.nodes.remove(node)

            # Remove the node groups from the data
            removed_count = 0
            for name in node_names_to_remove:
                node_group = bpy.data.node_groups.get(name)
                if node_group: # Check if the node group exists
                    print(f"Removing node group: {name}")
                    bpy.data.node_groups.remove(node_group)
                    removed_count += 1
                else:
                    print(f"Node group '{name}' not found.")

            # Final Summary
            self.report({'INFO'}, f"Removed {removed_count} node group(s) out of {len(node_names_to_remove)} requested.")
            # print(f"Removed {removed_count} node group(s) out of {len(node_names_to_remove)} requested.")

        def rm_ngs_from_data(ngs_names_to_rm):
            """
            Removes specified node groups from the Blender data.

            Args:
                ngs_names_to_rm (list of str): List of node group names to remove.

            Returns:
                dict: A dictionary with counts and details:
                      {'removed': int, 'not_found': int, 'errors': list}
            """
            if not isinstance(ngs_names_to_rm, (list, tuple)):
                raise ValueError("Expected a list or tuple of node group names.")

            results = {
                'removed': 0,
                'not_found': 0,
                'errors': []
            }

            for name in ngs_names_to_rm:
                node_group = bpy.data.node_groups.get(name)
                if node_group:  # Check if the node group exists
                    try:
                        print(f"Removing node group: {name}")
                        bpy.data.node_groups.remove(node_group)
                        results['removed'] += 1
                    except Exception as e:
                        print(f"Error removing node group '{name}': {e}")
                        results['errors'].append((name, str(e)))
                else:
                    print(f"Node group '{name}' not found.")
                    results['not_found'] += 1

            return results

        def rm_sockets_and_panels(parent_node_group, socket_names, panels_names):
            """
            Removes sockets and panels from a parent node group in Blender.

            Args:
                parent_node_group (bpy.types.NodeTree): The parent node group to remove sockets and panels from.
                socket_names (list of str): A list of socket names to remove from the group.
                panels_names (list of str): A list of panel names to remove from the group.

            Returns:
                None
            """
            for socket_name in socket_names:
                socket = parent_node_group.node_tree.interface.items_tree[socket_name]
                parent_node_group.node_tree.interface.remove(socket)
            
            for panel_name in panels_names:
                panel = parent_node_group.node_tree.interface.items_tree[panel_name]
                parent_node_group.node_tree.interface.remove(panel)

        def rename_and_label_nodes(node_data):
            """
            Renames multiple nodes and assigns labels to them. If a node is a group type, it also renames the node tree.
            If width is provided, it will also set the width of the node.

            Args:
                node_data (list of tuple): A list of tuples, each containing:
                    - node (bpy.types.Node): The node to rename and label.
                    - name (str): The new name and label for the node.
                    - width (int, optional): The new width of the node. Defaults to None.
            """
            for node, name, *optional_width in node_data:
                if node:
                    node.name = name
                    node.label = name
                    if hasattr(node, "node_tree") and node.node_tree:
                        node.node_tree.name = name
                    if optional_width:
                        node.width = optional_width[0]

        def get_nodes(names, tree=None):
            """
            Gets multiple nodes from a node tree by their names.

            Args:
                names (list of str): A list of node names to get.
                tree (bpy.types.NodeTree, optional): The node tree to get nodes from. Defaults to None.

            Returns:
                dict: A dictionary with node names and indices as keys, and the corresponding nodes as values.
            """
            if tree is None:
                tree = node_tree
            
            nodes = {}
            for i, name in enumerate(names):
                nodes[i] = tree.nodes.get(name)  # Access by index
                nodes[name] = tree.nodes.get(name)  # Access by name
            return nodes
        
        def group_ungroup_node(parent_node_group):
            """
            Groups or ungroups nodes within a parent node group in Blender's compositor.

            If nodes are selected, this function will ungroup them. If not, it checks if the 
            specified node group exists in the compositor's node tree. If it exists, it purges 
            orphaned data. If not, it attempts to remove the node group from Blender's data and 
            reports the results.

            Args:
                parent_node_group (str): The name of the parent node group to be processed.

            Returns:
                None
            """
            # Ensure the correct context before ungrouping
            if node_selected:
                bpy.ops.node.group_ungroup()

            group_name = parent_node_group

            # Check if the node group already exists in the compositor's node tree
            group_found = any(
                node.type == 'GROUP' and getattr(node, "node_tree", None) and node.node_tree.name == group_name
                for node in node_tree.nodes
            )

            if group_found:
                bpy.ops.outliner.orphans_purge(
                    do_local_ids=True,
                    do_linked_ids=True,
                    do_recursive=True
                )
            else:
                # Attempt to remove the node group from Blender's data
                try:
                    rm_ngs_result = rm_ngs_from_data([parent_node_group])
                    # Report the results of the removal operation
                    self.report({'INFO'}, f"Removed: {rm_ngs_result['removed']}, Not Found: {rm_ngs_result['not_found']}, Errors: {rm_ngs_result['errors']}")
                except Exception as e:
                    self.report({'ERROR'}, f"Failed to remove node group: {str(e)}")

        # Retrieve the nodes for each pass from the beauty mixer node tree
        default_nodes = get_nodes(
            names=[Names.Diff, Names.Gloss, Names.Trans, Names.Vol],
            tree=self.beauty_mixer_node.node_tree
        )
        diffuse_node = default_nodes[0]
        glossy_node = default_nodes[1]
        transmission_node = default_nodes[2]
        volume_node = default_nodes[3]

        # 15 If all passes are selected
        if all([db, gb, tb, vb]):
            DGTV_node_data = [
                (diffuse_node, "DGTV_Diff_Mixer", 186),
                (glossy_node, "DGTV_Gloss_Mixer", 186),
                (transmission_node, "DGTV_Trans_Mixer", 186),
                (volume_node, "DGTV_Vol_Mixer", 186)
            ]

            rename_and_label_nodes(DGTV_node_data)

            if enum == "UNGROUP":
                group_ungroup_node(Names.BeautyMixer)

                DGTV_NODES = get_nodes(names=["DGTV_Diff_Mixer", "DGTV_Gloss_Mixer", "DGTV_Trans_Mixer", "DGTV_Vol_Mixer"])
                DGTV_NLW_node_data = [
                    (DGTV_NODES[0], Names.Diffuse, 155),
                    (DGTV_NODES[1], Names.Glossy, 155),
                    (DGTV_NODES[2], Names.Transmission, 155),
                    (DGTV_NODES[3], Names.Volume, 155)
                ]

                rename_and_label_nodes(DGTV_NLW_node_data)
            elif enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass

        # 14 If glossy, transmission and volume passes are selected
        elif gb and tb and vb:
            gb_tb_vb_rm_node_groups = [Names.Diff]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                gb_tb_vb_rm_node_groups
            )

            gb_tb_vb_rm_sockets = [Names.Diff, Names.DiffDir, Names.DiffInd, Names.DiffCol]
            gb_tb_vb_rm_panels = [Names.Diffuse]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                gb_tb_vb_rm_sockets,
                gb_tb_vb_rm_panels
            )

            GTV_node_data = [
                (glossy_node, "GTV_Gloss_Mixer", 178),
                (transmission_node, "GTV_Trans_Mixer", 178),
                (volume_node, "GTV_Vol_Mixer", 178)
            ]
            
            rename_and_label_nodes(GTV_node_data)

            self.beauty_mixer_node.name = "Gloss&Trans&Vol"
            self.beauty_mixer_node.label = "Gloss&Trans&Vol"
            self.beauty_mixer_node.node_tree.name = "Gloss&Trans&Vol"
            self.beauty_mixer_node.width = 178

            if enum == "UNGROUP":
                group_ungroup_node("Gloss&Trans&Vol")

                GTV_NODES = get_nodes(names=["GTV_Gloss_Mixer", "GTV_Trans_Mixer", "GTV_Vol_Mixer"])
                GTV_NLW_node_data = [
                    (GTV_NODES[0], Names.Glossy, 155),
                    (GTV_NODES[1], Names.Transmission, 155),
                    (GTV_NODES[2], Names.Volume, 155)
                ]

                rename_and_label_nodes(GTV_NLW_node_data)
            elif enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass

        # 13 If diffuse, transmission and volume passes are selected
        elif db and tb and vb:
            db_tb_vb_rm_node_groups = [Names.Gloss]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                db_tb_vb_rm_node_groups
            )

            db_tb_vb_rm_sockets = [Names.Gloss, Names.GlossDir, Names.GlossInd, Names.GlossCol]
            db_tb_vb_rm_panels = [Names.Glossy]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                db_tb_vb_rm_sockets,
                db_tb_vb_rm_panels
            )

            DTV_node_data = [
                (diffuse_node, "DTV_Diff_Mixer", 178),
                (transmission_node, "DTV_Trans_Mixer", 178),
                (volume_node, "DTV_Vol_Mixer", 178)
            ]
            
            rename_and_label_nodes(DTV_node_data)

            self.beauty_mixer_node.name = "Diff&Trans&Vol"
            self.beauty_mixer_node.label = "Diff&Trans&Vol"
            self.beauty_mixer_node.node_tree.name = "Diff&Trans&Vol"
            self.beauty_mixer_node.width = 166

            if enum == "UNGROUP":
                group_ungroup_node("Diff&Trans&Vol")

                DTV_NODES = get_nodes(names=["DTV_Diff_Mixer", "DTV_Trans_Mixer", "DTV_Vol_Mixer"])
                DTV_NLW_node_data = [
                    (DTV_NODES[0], Names.Diffuse, 155),
                    (DTV_NODES[1], Names.Transmission, 155),
                    (DTV_NODES[2], Names.Volume, 155)
                ]

                rename_and_label_nodes(DTV_NLW_node_data)
            if enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass

        # 12 If diffuse, glossy and volume passes are selected
        elif db and gb and vb:
            db_gb_vb_rm_node_groups = [Names.Trans]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                db_gb_vb_rm_node_groups
            )
            
            db_gb_vb_rm_sockets = [Names.Trans, Names.TransDir, Names.TransInd, Names.TransCol]
            db_gb_vb_rm_panels = [Names.Transmission]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                db_gb_vb_rm_sockets,
                db_gb_vb_rm_panels
            )

            DGV_node_data = [
                (diffuse_node, "DGV_Diff_Mixer", 178),
                (glossy_node, "DGV_Gloss_Mixer", 178),
                (volume_node, "DGV_Vol_Mixer", 178)
            ]
            
            rename_and_label_nodes(DGV_node_data)

            self.beauty_mixer_node.name = "Diff&Gloss&Vol"
            self.beauty_mixer_node.label = "Diff&Gloss&Vol"
            self.beauty_mixer_node.node_tree.name = "Diff&Gloss&Vol"
            self.beauty_mixer_node.width = 166

            if enum == "UNGROUP":
                group_ungroup_node("Diff&Gloss&Vol")

                DGV_NODES = get_nodes(names=["DGV_Diff_Mixer", "DGV_Gloss_Mixer", "DGV_Vol_Mixer"])
                DGV_NLW_node_data = [
                    (DGV_NODES[0], Names.Diffuse, 155),
                    (DGV_NODES[1], Names.Glossy, 155),
                    (DGV_NODES[2], Names.Volume, 155)
                ]

                rename_and_label_nodes(DGV_NLW_node_data)
            if enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass

        # 11 If diffuse, glossy and transmission passes are selected
        elif db and gb and tb:
            db_gb_tb_rm_node_groups = [Names.Vol]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                db_gb_tb_rm_node_groups
            )
            
            db_gb_tb_rm_sockets = [Names.Vol, Names.VolumeDir, Names.VolumeInd]
            db_gb_tb_rm_panels = [Names.Volume]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                db_gb_tb_rm_sockets,
                db_gb_tb_rm_panels
            )

            DGT_node_data = [
                (diffuse_node, "DGT_Diff_Mixer", 178),
                (glossy_node, "DGT_Gloss_Mixer", 178),
                (transmission_node, "DGT_Trans_Mixer", 178)
            ]
            
            rename_and_label_nodes(DGT_node_data)

            self.beauty_mixer_node.name = "Diff&Gloss&Trans"
            self.beauty_mixer_node.label = "Diff&Gloss&Trans"
            self.beauty_mixer_node.node_tree.name = "Diff&Gloss&Trans"
            self.beauty_mixer_node.width = 178

            if enum == "UNGROUP":
                group_ungroup_node("Diff&Gloss&Trans")

                DGT_NODES = get_nodes(names=["DGT_Diff_Mixer", "DGT_Gloss_Mixer", "DGT_Trans_Mixer"])
                DGT_NLW_node_data = [
                    (DGT_NODES[0], Names.Diffuse, 155),
                    (DGT_NODES[1], Names.Glossy, 155),
                    (DGT_NODES[2], Names.Transmission, 155)
                ]

                rename_and_label_nodes(DGT_NLW_node_data)
            elif enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass

        # 10 If transmission and volume passes are selected
        elif tb and vb:
            tb_vb_rm_node_groups = [Names.Diff, Names.Gloss]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                tb_vb_rm_node_groups
            )

            tb_vb_rm_sockets = [Names.Diff, Names.Gloss, Names.DiffDir, Names.DiffInd, Names.DiffCol, Names.GlossDir, Names.GlossInd, Names.GlossCol]
            tb_vb_rm_panels = [Names.Diffuse, Names.Glossy]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                tb_vb_rm_sockets,
                tb_vb_rm_panels
            )

            TV_node_data = [
                (transmission_node, "TV_Trans_Mixer", 170),
                (volume_node, "TV_Vol_Mixer", 170)
            ]

            rename_and_label_nodes(TV_node_data)

            self.beauty_mixer_node.name = "Trans&Volume"
            self.beauty_mixer_node.label = "Trans&Volume"
            self.beauty_mixer_node.node_tree.name = "Trans&Volume"

            if enum == "UNGROUP":
                group_ungroup_node("Trans&Volume")

                TV_NODES = get_nodes(names=["TV_Trans_Mixer", "TV_Vol_Mixer"])
                TV_NLW_node_data = [
                    (TV_NODES[0], Names.Transmission, 155),
                    (TV_NODES[1], Names.Volume, 155)
                ]

                rename_and_label_nodes(TV_NLW_node_data)
            elif enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass

        # 9 If glossy and volume passes are selected
        elif gb and vb:
            gb_vb_rm_node_groups = [Names.Diff, Names.Trans]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                gb_vb_rm_node_groups
            )

            gb_vb_rm_sockets = [Names.Diff, Names.Trans, Names.DiffDir, Names.DiffInd, Names.DiffCol, Names.TransDir, Names.TransInd, Names.TransCol]
            gb_vb_rm_panels = [Names.Diffuse, Names.Transmission]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                gb_vb_rm_sockets,
                gb_vb_rm_panels
            )

            GV_node_data = [
                (glossy_node, "GV_Gloss_Mixer", 174),
                (volume_node, "GV_Vol_Mixer", 174)
            ]

            rename_and_label_nodes(GV_node_data)

            self.beauty_mixer_node.name = "Gloss&Volume"
            self.beauty_mixer_node.label = "Gloss&Volume"
            self.beauty_mixer_node.node_tree.name = "Gloss&Volume"

            if enum == "UNGROUP":
                group_ungroup_node("Gloss&Volume")

                GV_NODES = get_nodes(names=["GV_Gloss_Mixer", "GV_Vol_Mixer"])
                GV_NLW_node_data = [
                    (GV_NODES[0], Names.Glossy, 155),
                    (GV_NODES[1], Names.Volume, 155)
                ]

                rename_and_label_nodes(GV_NLW_node_data)
            elif enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass

        # 8 If glossy and transmission passes are selected
        elif gb and tb:
            gb_tb_rm_node_groups = [Names.Diff, Names.Vol]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                gb_tb_rm_node_groups
            )

            gb_tb_rm_sockets = [Names.Diff, Names.Vol, Names.DiffDir, Names.DiffInd, Names.DiffCol, Names.VolumeDir, Names.VolumeInd]
            gb_tb_rm_panels = [Names.Diffuse, Names.Volume]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                gb_tb_rm_sockets,
                gb_tb_rm_panels
            )

            GT_node_data = [
                (glossy_node, "GT_Gloss_Mixer", 174),
                (transmission_node, "GT_Trans_Mixer", 174)
            ]

            rename_and_label_nodes(GT_node_data)

            self.beauty_mixer_node.name = "Gloss&Trans"
            self.beauty_mixer_node.label = "Gloss&Trans"
            self.beauty_mixer_node.node_tree.name = "Gloss&Trans"

            if enum == "UNGROUP":
                group_ungroup_node("Gloss&Trans")

                GT_NODES = get_nodes(names=["GT_Gloss_Mixer", "GT_Trans_Mixer"])
                GT_NLW_node_data = [
                    (GT_NODES[0], Names.Glossy, 155),
                    (GT_NODES[1], Names.Transmission, 155)
                ]

                rename_and_label_nodes(GT_NLW_node_data)
            elif enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass

        # 7 If diffuse and volume passes are selected
        elif db and vb:
            db_vb_rm_node_groups = [Names.Gloss, Names.Trans]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                db_vb_rm_node_groups
            )
            
            db_vb_rm_sockets = [Names.Gloss, Names.Trans, Names.GlossDir, Names.GlossInd, Names.GlossCol, Names.TransDir, Names.TransInd, Names.TransCol]
            db_vb_rm_panels = [Names.Glossy, Names.Transmission]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                db_vb_rm_sockets,
                db_vb_rm_panels
            )

            DV_node_data = [
                (diffuse_node, "DV_Diff_Mixer"),
                (volume_node, "DV_Vol_Mixer")
            ]

            rename_and_label_nodes(DV_node_data)

            self.beauty_mixer_node.name = "Diff&Volume"
            self.beauty_mixer_node.label = "Diff&Volume"
            self.beauty_mixer_node.node_tree.name = "Diff&Volume"

            if enum == "UNGROUP":
                group_ungroup_node("Diff&Volume")

                DV_NODES = get_nodes(names=["DV_Diff_Mixer", "DV_Vol_Mixer"])
                DV_NLW_node_data = [
                    (DV_NODES[0], Names.Diffuse, 155),
                    (DV_NODES[1], Names.Volume, 155)
                ]

                rename_and_label_nodes(DV_NLW_node_data)
            elif enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass

        # 6 If diffuse and transmission passes are selected
        elif db and tb:
            db_tb_rm_node_groups = [Names.Gloss, Names.Vol]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                db_tb_rm_node_groups
            )

            db_tb_rm_sockets = [Names.Gloss, Names.Vol, Names.GlossDir, Names.GlossInd, Names.GlossCol, Names.VolumeDir, Names.VolumeInd]
            db_tb_rm_panels = [Names.Glossy, Names.Volume]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                db_tb_rm_sockets,
                db_tb_rm_panels
            )

            DT_node_data = [
                (diffuse_node, "DT_Diff_Mixer", 172),
                (transmission_node, "DT_Trans_Mixer", 172)
            ]

            rename_and_label_nodes(DT_node_data)

            self.beauty_mixer_node.name = "Diff&Trans"
            self.beauty_mixer_node.label = "Diff&Trans"
            self.beauty_mixer_node.node_tree.name = "Diff&Trans"

            if enum == "UNGROUP":
                group_ungroup_node("Diff&Trans")

                DT_NODES = get_nodes(names=["DT_Diff_Mixer", "DT_Trans_Mixer"])
                DT_NLW_node_data = [
                    (DT_NODES[0], Names.Diffuse, 155),
                    (DT_NODES[1], Names.Transmission, 155),
                ]

                rename_and_label_nodes(DT_NLW_node_data)
            elif enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass

        # 5 If diffuse and glossy passes are selected
        elif db and gb:
            db_gb_rm_node_groups = [Names.Trans, Names.Vol]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                db_gb_rm_node_groups
            )

            db_gb_rm_sockets = [Names.Trans, Names.Vol, Names.TransDir, Names.TransInd, Names.TransCol, Names.VolumeDir, Names.VolumeInd]
            db_gb_rm_panels = [Names.Transmission, Names.Volume]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                db_gb_rm_sockets,
                db_gb_rm_panels
            )

            DG_node_data = [
                (diffuse_node, "DG_Diff_Mixer", 174),
                (glossy_node, "DG_Gloss_Mixer", 174)
            ]

            rename_and_label_nodes(DG_node_data)

            self.beauty_mixer_node.name = "Diff&Gloss"
            self.beauty_mixer_node.label = "Diff&Gloss"
            self.beauty_mixer_node.node_tree.name = "Diff&Gloss"

            if enum == "UNGROUP":
                group_ungroup_node("Diff&Gloss")

                DG_NODES = get_nodes(names=["DG_Diff_Mixer", "DG_Gloss_Mixer"])
                DG_NLW_node_data = [
                    (DG_NODES[0], Names.Diffuse, 155),
                    (DG_NODES[1], Names.Glossy, 155),
                ]

                rename_and_label_nodes(DG_NLW_node_data)
            elif enum == "GROUP":
                # Intentionally does nothing, as this case is not implemented by design.
                pass
        
        # 4 If volume pass is selected
        elif vb:
            vb_rm_node_groups = [Names.Diff, Names.Gloss, Names.Trans]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                vb_rm_node_groups
            )

            vb_rm_sockets = [Names.Diff, Names.Gloss, Names.Trans, Names.DiffDir, Names.DiffInd, Names.DiffCol, Names.GlossDir, Names.GlossInd, Names.GlossCol, Names.TransDir, Names.TransInd, Names.TransCol]
            vb_rm_panels = [Names.Diffuse, Names.Glossy, Names.Transmission, Names.Volume]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                vb_rm_sockets,
                vb_rm_panels
            )

            V_node_data = [
                (volume_node, "Vol_Mixer")
            ]

            rename_and_label_nodes(V_node_data)

            self.beauty_mixer_node.name = Names.Volume
            self.beauty_mixer_node.label = Names.Volume
            self.beauty_mixer_node.node_tree.name = Names.Volume
        
        # 3 If transmission pass is selected
        elif tb:
            tb_rm_node_groups = [Names.Diff, Names.Gloss, Names.Vol]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                tb_rm_node_groups
            )

            tb_rm_sockets = [Names.Diff, Names.Gloss, Names.Vol, Names.DiffDir, Names.DiffInd, Names.DiffCol, Names.GlossDir, Names.GlossInd, Names.GlossCol, Names.VolumeDir, Names.VolumeInd]
            tb_rm_panels = [Names.Diffuse, Names.Glossy, Names.Transmission, Names.Volume]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                tb_rm_sockets,
                tb_rm_panels
            )

            T_node_data = [
                (transmission_node, "Trans_Mixer")
            ]

            rename_and_label_nodes(T_node_data)
                
            self.beauty_mixer_node.name = Names.Transmission
            self.beauty_mixer_node.label = Names.Transmission
            self.beauty_mixer_node.node_tree.name = Names.Transmission

        # 2 If glossy pass is selected
        elif gb:
            gb_rm_node_groups = [Names.Diff, Names.Trans, Names.Vol]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                gb_rm_node_groups
            )

            gb_rm_sockets = [Names.Diff, Names.Trans, Names.Vol, Names.DiffDir, Names.DiffInd, Names.DiffCol, Names.TransDir, Names.TransInd, Names.TransCol, Names.VolumeDir, Names.VolumeInd]
            gb_rm_panels = [Names.Diffuse, Names.Glossy, Names.Transmission, Names.Volume]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                gb_rm_sockets,
                gb_rm_panels
            )

            G_node_data = [
                (glossy_node, "Gloss_Mixer")
            ]

            rename_and_label_nodes(G_node_data)

            self.beauty_mixer_node.name = Names.Glossy
            self.beauty_mixer_node.label = Names.Glossy
            self.beauty_mixer_node.node_tree.name = Names.Glossy

        # 1 If diffuse pass is selected
        elif db:
            db_rm_node_groups = [Names.Gloss, Names.Trans, Names.Vol]
            rm_nodes_from_group(
                self.beauty_mixer_node,
                db_rm_node_groups
            )

            db_rm_sockets = [Names.Gloss, Names.Trans, Names.Vol, Names.GlossDir, Names.GlossInd, Names.GlossCol, Names.TransDir, Names.TransInd, Names.TransCol, Names.VolumeDir, Names.VolumeInd]
            db_rm_panels = [Names.Diffuse, Names.Glossy, Names.Transmission, Names.Volume]
            rm_sockets_and_panels(
                self.beauty_mixer_node,
                db_rm_sockets,
                db_rm_panels
            )

            D_node_data = [
                (diffuse_node, "Diff_Mixer")
            ]

            rename_and_label_nodes(D_node_data)
                
            self.beauty_mixer_node.name = Names.Diffuse
            self.beauty_mixer_node.label = Names.Diffuse
            self.beauty_mixer_node.node_tree.name = Names.Diffuse

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