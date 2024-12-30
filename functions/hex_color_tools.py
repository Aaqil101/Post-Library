"""
Utility functions for working with color
"""

from typing import Tuple

# what I did is that I downloaded the bpy Building Blocks from Victor Stepanov's github repository.
# (https://github.com/CGArtPython/bpy-building-blocks)

# and then I modified the code to fit my needs based on this tutorial.
# (https://youtu.be/knc1CGBhJeU?list=TLPQMTcwOTIwMjRqvGTVRWN4sg)

def hexcode_to_rgb(hexcode: str) -> Tuple[float]:
    """
    Converting from a color in the form of a hex triplet string (en.wikipedia.org/wiki/Web_colors#Hex_triplet)
    to a Linear RGB

    Supports: "#RRGGBB" or "RRGGBB"

    Note: We are converting into Linear RGB since Blender uses a Linear Color Space internally
    https://docs.blender.org/manual/en/latest/render/color_management.html
    """
    # remove the leading '#' symbol if present
    if hexcode.startswith("#"):
        hexcode = hexcode[1:]

    assert len(hexcode) == 6, f"RRGGBB is the supported hex color format: {hexcode}"

    # extracting the Red color component - RRxxxx
    red = int(hexcode[:2], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_red = red / 255

    # extracting the Green color component - xxGGxx
    green = int(hexcode[2:4], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_green = green / 255

    # extracting the Blue color component - xxxxBB
    blue = int(hexcode[4:6], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_blue = blue / 255

    return tuple([srgb_red, srgb_green, srgb_blue])

def hex_color_add(color1, color2):
    """
    This function takes two hex color codes, adds their RGB components, and clamps each component to a maximum of 255.
    The resulting RGB components are then combined back into a hex color code.
    """
    # Split the hex codes into RGB components
    r1, g1, b1 = int(color1[:2], 16), int(color1[2:4], 16), int(color1[4:], 16)
    r2, g2, b2 = int(color2[:2], 16), int(color2[2:4], 16), int(color2[4:], 16)
    
    # Add the components and clamp each to a maximum of 255
    r = min(r1 + r2, 255)
    g = min(g1 + g2, 255)
    b = min(b1 + b2, 255)
    
    # Combine the components back into a hex color
    return f'{r:02X}{g:02X}{b:02X}'