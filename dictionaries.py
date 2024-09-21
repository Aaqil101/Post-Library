from color_convertor import hexcode_to_rgb

"""
COLORS_DICT is a dictionary of color hex codes mapped to their corresponding linear RGB values

The colors are from the Blender color scheme and are used in the PostLibrary Addon.
"""
COLORS_DICT = {
        "LIGHT_RED": hexcode_to_rgb("#94493E"),
        "DARK_RED": hexcode_to_rgb("#823A35"),
        "LIGHT_BLUE": hexcode_to_rgb("#646E66"),
        "DARK_BLUE": hexcode_to_rgb("#4C6160"),
        "LIGHT_PURPLE": hexcode_to_rgb("#846167"),
        "DARK_PURPLE": hexcode_to_rgb("#77535F"),
        "BROWN": hexcode_to_rgb("#866937"),
        "GRAY": hexcode_to_rgb("#59514B"),
    }