from helpers.add_driver_manager import NodeDriverManager
from helpers.color_utils import Color, hex_color_add, hexcode_to_rgb
from helpers.compositor_node_names import CompositorNodeNames
from helpers.oldeevee_bloom_prop_utilities import (
    Descriptions,
    Names,
    SocketNames,
    ensure_connection,
    is_compositor_enabled,
    poll_view_3d,
    setup_bloom,
    toggle_oldeevee_bloom,
    update_real_time_compositing,
)

# Proper __all__ definition as strings
__all__ = [
    "NodeDriverManager",
    "CompositorNodeNames",
    "hexcode_to_rgb",
    "hex_color_add",
    "Color",
    "Names",
    "Descriptions",
    "SocketNames",
    "setup_bloom",
    "ensure_connection",
    "poll_view_3d",
    "update_real_time_compositing",
    "toggle_oldeevee_bloom",
    "is_compositor_enabled",
]
