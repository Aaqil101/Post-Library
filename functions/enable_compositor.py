import bpy


def enable_compositor(scene=None):
    """
    Enables the compositor for the given Blender scene or the current scene if None.

    Args:
        scene: The Blender scene to enable the compositor for. If None, the current scene is used.
    """
    if scene is None:
        scene = bpy.context.scene
    
    # Enable the compositor
    if not scene.use_nodes:
        scene.use_nodes = True