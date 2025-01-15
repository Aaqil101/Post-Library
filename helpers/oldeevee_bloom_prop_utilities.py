import bpy
from dataclasses import dataclass, field

@dataclass
class OldEevee_Bloom_Names:
    """
    Class to store the names of various nodes and sockets used in the bloom node group
    """
    OldEevee_Bloom: str = "OldEevee_Bloom"
    Image: str = "Image"
    Color: str = "Color"
    Quality: str = "Quality"
    Knee: str = "Knee"
    Threshold: str = "Threshold"
    Radius: str = "Radius"
    Blur: str = "Blur"
    Intensity: str = "Intensity"
    Clamp: str = "Clamp"
    Other: str = "Other"
    Hue: str = "Hue"
    Saturation: str = "Saturation"
    Fac: str = "Fac"
    Composite: str = "Composite"
    Viewer: str = "Viewer"
    Disabled: str = "Disabled"
    Camera: str = "Camera"
    Always: str = "Always"
    BM_Clamp: str = "BM Clamp"
    KM_Clamp: str = "KM Clamp"
    CR_Clamp: str = "CR Clamp"
    IY_Clamp: str = "IY Clamp"
    Clamp_Mix: str = "Clamp Mix"
    Blur_Mix: str = "Blur Mix"
    Bloom_Size: str = "Bloom Size"
    Group_Output: str = "Group Output"
    Group_Input_00: str = "Group Input 00"
    Original_Bloom_High: str = "Original Bloom High"
    Knee_Bloom_High: str = "Knee Bloom High"
    Knee_Mix: str = "Knee Mix"
    Group_Input_01: str = "Group Input 01"
    Group_Input_02: str = "Group Input 02"
    Group_Input_03: str = "Group Input 03"
    Group_Input_04: str = "Group Input 04"
    Group_Input_05: str = "Group Input 05"
    Bloom_High_Low: str = "Bloom High && Low"
    Knee_Bloom_Low: str = "Knee Bloom Low"
    KB_Switch: str = "KB Switch"
    OB_Switch: str = "OB Switch"
    Original_Bloom_Low: str = "Original Bloom Low"
    Reroute_00: str = "Reroute_00"
    Reroute_01: str = "Reroute_01"
    Render_Layers: str = "Render Layers"
    Bloom_Mute_Unmute: str = "Bloom Mute/Unmute"
    Real_Time_Compositing: str = "Real-Time Compositor"
    Enable_Compositor: str = "Enable Compositor"

@dataclass
class OldEevee_Bloom_Descr:
    """
    Class to store all the descriptions of the Bloom properties
    """
    image: str = "Standard color output"
    quality: str = "If the value is set to 0 then the bloom effect will be applied to the low resolution copy of the image. If the value is set to 1 then the bloom effect will be applied to the high resolution copy of the image. This can be helpful to save render times while only doing preview renders"
    threshold: str = "Filters out pixels under this level of brightness"
    knee: str = "Makes transition between under/over-threshold gradual"
    radius: str = "Bloom spread distance"
    color: str = "Color applied to the bloom effect"
    intensity: str = "Blend factor"
    clamp: str = "Maximum intensity a bloom pixel can have"
    other: str = "Additional options for customizing the bloom effect"
    hue: str = "The hue rotation offset, from 0 (-180°) to 1 (+180°). Note that 0 and 1 have the same result"
    saturation: str = "A value of 0 removes color from the image, making it black-and-white. A value greater than 1.0 increases saturation"
    fac: str = "The amount of influence the node exerts on the image"
    disabled: str = "The compositor is disabled"
    camera: str = "The compositor is enabled only in camera view"
    always: str = "The compositor is always enabled regardless of the view"
    node_ot_bloom: str = "Replication of the legacy eevee bloom option, but can be used in cycles as well"
    prop_pt_bloom: str = "Old Eevee Bloom In Both Eevee And Cycles"
    scene_ot_enable_compositor: str = "Enable the compositing node tree"
    blur_mix: str = "The optional Size input will be multiplied with the X and Y blur radius values. It also accepts a value image, to control the blur radius with a mask. The values should be mapped between (0 to 1) for an optimal effect"
    bloom_size: str = "Scale of the glow relative to the size of the image. 9 means the glow can cover the entire image, 8 means it can only cover half the image, 7 means it can only cover quarter of the image, and so on."
    bloom_mute_unmute_bool: str = "Toggle the bloom effect on or off"
    oldeevee_bloom: str = "Replication of the legacy eevee bloom option"
    clamp_mix: str = "Clamps of each mix nodes in the OldEevee_Bloom node group"
    bm_clamp: str = "Blur Mix Clamp"
    km_clamp: str = "Knee Mix Clamp"
    cr_clamp: str = "Color Clamp"
    iy_clamp: str = "Intensity Clamp"
    real_time_compositing: str = "When to preview the compositor output inside the viewport"

def toggle_oldeevee_bloom(self, context):
    """
    Toggle the mute property of the 'OE_Bloom' node group in the Compositor.

    Args:
        self: The instance of the class.
        context: The Blender context.

    Returns:
        None
    """
    scene = context.scene
    node_tree = context.scene.node_tree  # Access the active node tree

    if node_tree and node_tree.type == 'COMPOSITING':
        found_node = None
        for node in node_tree.nodes:
            if node.type == 'GROUP' and node.name == OldEevee_Bloom_Names.OE_Bloom:
                found_node = node
                break

        if found_node:
            found_node.mute = not scene.bloom_mute_unmute_bool
            print(f"Node group 'OE_Bloom' is now {'muted' if found_node.mute else 'unmuted'}.")
        else:
            print("Node group 'OE_Bloom' not found in the Compositor node tree.")
    else:
        print("Compositor node tree is not active.")

def update_real_time_compositing(self, context):
    """
    Update the real-time compositing settings for 3D Viewport areas based on the 
    'real_time_compositing_enum' attribute.

    This function iterates through all screen areas in the current context and checks 
    for 3D Viewport areas. If found, it updates the 'use_compositor' attribute of the 
    shading settings for the 3D View space based on the value of 'real_time_compositing_enum', 
    which can be 'DISABLED', 'CAMERA', or 'ALWAYS'.

    Args:
        self: The instance of the class containing the 'real_time_compositing_enum' attribute.
        context: The Blender context, providing access to the current screen and its areas.

    Returns:
        None
    """
    for workspace in bpy.data.workspaces:
        for screen in workspace.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    view_3d = area.spaces[0]
                    with context.temp_override(space=view_3d):
                        view_3d.shading.use_compositor = self.real_time_compositing_enum

def poll_view_3d(self, context):
    """
    Check if a 3D Viewport area exists in the current screen layout.

    Args:
        self: The current context owner (typically a UI panel or operator).
        context: The Blender context containing information about the current state.

    Returns:
        bool: True if a 3D Viewport area is found, otherwise False.
    """
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':  # Check if VIEW_3D area exists
            return True
    return False

# Ensure all connections exist
def ensure_connection(output_node, output_socket_name, input_node, input_socket_name):
    """
    Ensures that a connection exists between two nodes

    Args:
        output_node (bpy.types.Node): The node that the connection comes from
        output_socket_name (str): The name of the output socket
        input_node (bpy.types.Node): The node that the connection goes to
        input_socket_name (str): The name of the input socket

    Returns:
        None
    """
    # Get the compositor node tree
    node_tree = bpy.context.scene.node_tree
    links = node_tree.links

    # Check if a link already exists
    for link in links:
        if (
            link.from_node == output_node
            and link.to_node == input_node
            and link.from_socket.name == output_socket_name
            and link.to_socket.name == input_socket_name
        ):
            return  # Connection already exists

    # Create the link if not found
    links.new(output_node.outputs[output_socket_name], input_node.inputs[input_socket_name])