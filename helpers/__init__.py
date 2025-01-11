"""
Functions and Classes

This module contains functions and classes that are used throughout the add-on.

"""
from .driver_var_func import add_driver_var
from .compositor_node_names import CompositorNodeNames
from .color_utils import (hexcode_to_rgb, hex_color_add, Color)

# Proper __all__ definition as strings
__all__ = [
    "add_driver_var", "CompositorNodeNames", "hexcode_to_rgb",
    "hex_color_add", "Color"
]

# Reload modules if needed (this is optional and mainly useful for development)
from . import (driver_var_func, compositor_node_names, color_utils)
from importlib import reload
reload(driver_var_func)
reload(compositor_node_names)
reload(color_utils)