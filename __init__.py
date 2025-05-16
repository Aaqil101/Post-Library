bl_info = {
    "name": "Post Library",
    "author": "Aaqil",
    "version": (2, 0, 0),
    "location": "Compositor > Toolshelf",
    "description": "Boost your Blender workflow with essential tools for efficient VFX and post-processing. Simplify compositing, and finishing touches with this powerful addon.",
    "warning": "",
    "doc_url": "https://github.com/Aaqil101/Post-Library",
    "category": "Nodes",
}

import importlib
import sys

import bpy

# Map Blender version (major, minor) to your submodule folder names
VERSION_MAP = {
    (4, 2): "v4_2",
    (4, 3): "v4_3",
    (4, 4): "v4_4",
    (4, 5): "v4_5",  # Fallback will default to 4.5 behavior
}

# Get the current Blender version (major, minor)
blender_version = bpy.app.version[:2]
folder_name = VERSION_MAP.get(blender_version, "v4_5")

# Construct import path
module_path = f"{__name__}.{folder_name}"

# Load the version-specific module
try:
    if module_path in sys.modules:
        importlib.reload(sys.modules[module_path])
    else:
        importlib.import_module(module_path)

    version_module = sys.modules[module_path]

except ImportError as e:
    print(f"[Post Library] Failed to load version module '{folder_name}': {e}")
    version_module = None


def register():
    if version_module:
        version_module.register()
    else:
        print("[Post Library] Register failed: version module not loaded")


def unregister():
    if version_module:
        version_module.unregister()
