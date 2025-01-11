from dataclasses import dataclass, field

@dataclass
class ToggleOeBloomNames:
    OE_Bloom: str = "OE_Bloom"
    GROUP = 'GROUP'
    COMPOSITING = 'COMPOSITING'

def toggle_oe_bloom(self, context):
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

    if node_tree and node_tree.type == ToggleOeBloomNames.COMPOSITING:
        found_node = None
        for node in node_tree.nodes:
            if node.type == ToggleOeBloomNames.GROUP and node.name == ToggleOeBloomNames.OE_Bloom:
                found_node = node
                break

        if found_node:
            found_node.mute = scene.bloom_mute_unmute_bool
            print(f"Node group 'OE_Bloom' is now {'muted' if found_node.mute else 'unmuted'}.")
        else:
            print("Node group 'OE_Bloom' not found in the Compositor node tree.")
    else:
        print("Compositor node tree is not active.")