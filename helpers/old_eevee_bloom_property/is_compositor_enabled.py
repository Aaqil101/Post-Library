def is_compositor_enabled(scene):
    """
    Check if the compositor is enabled for the given scene.

    Args:
        scene: The Blender scene to check.

    Returns:
        bool: True if the compositor is enabled, otherwise False.
    """
    return scene.use_nodes  # 'use_nodes' tells if the compositor is enabled