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