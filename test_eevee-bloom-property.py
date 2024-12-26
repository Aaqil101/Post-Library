import bpy
from bpy.props import BoolProperty

class PROP_PT_BLOOM(bpy.types.Panel):
    bl_label = 'Bloom'
    bl_idname = 'PROP_PT_BLOOM'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_description = 'Old Eevee Bloom In Both Eevee And Cycles'
    bl_category = ""
    bl_order = 3
    bl_ui_units_x = 0

    @classmethod
    def poll(cls, context):
        """
        Determines whether the panel should be displayed in the UI.

        Args:
            context (bpy.types.Context): The current Blender context.

        Returns:
            bool: True if the panel should be displayed, False otherwise.
        """
        return True  # Always display the panel

    def draw_header(self, context):
        layout = self.layout
        scene = context.scene  # Use a property attached to the scene
        layout.prop(scene, "bloom_bool", text="")  # Add the checkbox in the header

    def draw(self, context):
        layout = self.layout
        scene = context.scene  # Use a property attached to the scene

        if scene.bloom_bool:  # Display extra content if bloom_bool is enabled
            layout.label(text="Bloom is enabled")
        else:
            layout.label(text="Bloom is disabled")


# Register and unregister
classes = [PROP_PT_BLOOM]

def register():
    bpy.types.Scene.bloom_bool = BoolProperty(
        name="Bloom",
        description="Enable or disable Bloom",
        default=False
    )
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    del bpy.types.Scene.bloom_bool  # Unregister the property
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()