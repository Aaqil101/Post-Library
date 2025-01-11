from dataclasses import dataclass, field

@dataclass
class UpdateRTCompositingNames:
    """
    Class containing constants used for real-time compositing settings
    """
    DISABLED: str = "DISABLED"
    CAMERA: str = "CAMERA"
    ALWAYS: str = "ALWAYS"
    VIEW_3D: str = 'VIEW_3D'
    USE_COMPOSITOR: str = 'use_compositor'

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
    for area in context.screen.areas:  # Iterate through all areas
        if area.type == UpdateRTCompositingNames.VIEW_3D:  # Find the 3D Viewport
            for space in area.spaces:
                if space.type == UpdateRTCompositingNames.VIEW_3D:  # Confirm it's a 3D View space
                    if hasattr(space.shading, UpdateRTCompositingNames.USE_COMPOSITOR):  # Ensure shading property exists
                        if self.real_time_compositing_enum == UpdateRTCompositingNames.DISABLED:
                            space.shading.use_compositor = UpdateRTCompositingNames.DISABLED
                        elif self.real_time_compositing_enum == UpdateRTCompositingNames.CAMERA:
                            space.shading.use_compositor = UpdateRTCompositingNames.CAMERA
                        elif self.real_time_compositing_enum == UpdateRTCompositingNames.ALWAYS:
                            space.shading.use_compositor = UpdateRTCompositingNames.ALWAYS
            break
    else:
        # self.report({'WARNING'}, "No 3D Viewport available to update the shading property.")
        print("No 3D Viewport available to update the shading property.")