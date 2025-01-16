from helpers import (Color, CompositorNodeNames)
from dataclasses import dataclass, field

class FilterNodeNames:
    """
    Class to store the names of various nodes and sockets used in the Filter Node Manager.
    """
    Glare: str = "Glare"
    Blur: str = "Blur"

@dataclass
class GlareType:
    """
    Enumeration of different types of glare effects.

    Attributes:
    ---
        BLOOM (str): Represents the Bloom glare effect.
        GHOSTS (str): Represents the Ghosts glare effect.
        STREAKS (str): Represents the Streaks glare effect.
        FOG_GLOW (str): Represents the Fog Glow glare effect.
        SIMPLE_STAR (str): Represents the Simple Star glare effect.
    """
    BLOOM: str = 'BLOOM'  # Bloom glare effect
    GHOSTS: str = 'GHOSTS'  # Ghosts glare effect
    STREAKS: str = 'STREAKS'  # Streaks glare effect
    FOG_GLOW: str = 'FOG_GLOW'  # Fog Glow glare effect
    SIMPLE_STAR: str = 'SIMPLE_STAR'  # Simple Star glare effect

@dataclass
class GlareQuality:
    """
    Enumeration of different quality levels for the glare effect.

    Attributes:
    ---
        LOW (str): Represents low quality for the glare effect.
        MEDIUM (str): Represents medium quality for the glare effect.
        HIGH (str): Represents high quality for the glare effect.
    """
    LOW: str = 'LOW'  # Low quality
    MEDIUM: str = 'MEDIUM'  # Medium quality
    HIGH: str = 'HIGH'  # High quality

@dataclass
class GlareSettings:
    """
    Settings for the Glare node (Compositor).

    Attributes:
    ---
        angle_offset (float): Angle offset for the glare effect.
        color_modulation (float): Color modulation for the glare effect.
        fade (float): Fade-out value for the glare effect.
        glare_type (str): Type of glare effect, e.g. GlareType.BLOOM, GlareType.GHOSTS, etc...
        iterations (int): Number of iterations for the glare effect.
        mix (float): Mix value for the glare effect.
        quality (str): Quality of the glare effect, e.g. GlareQuality.LOW, etc...
        size (int): Size of the glare effect.
        streaks (int): Number of streaks for the glare effect.
        threshold (float): Threshold value for the glare effect.
        use_rotate_45 (bool): Whether to use a 45-degree rotation for the glare effect.
    """
    angle_offset: float = 0.0
    color_modulation: float = 0.25
    fade: float = 0.9
    glare_type: str = GlareType.STREAKS  # Options: GlareType.BLOOM, GlareType.GHOSTS, GlareType.STREAKS, GlareType.FOG_GLOW, GlareType.SIMPLE_STAR
    iterations: int = 3
    mix: float = 0.0
    quality: str = GlareQuality.LOW  # Options: GlareQuality.LOW, GlareQuality.MEDIUM, GlareQuality.HIGH
    size: int = 8
    streaks: int = 4
    threshold: float = 1.0
    use_rotate_45: bool = True

@dataclass
class BlurAspectCorrection:
    """
    Class to store the aspect correction modes for the Blur node (Compositor).

    Attributes:
    ---
        NONE (str): No aspect correction.
        Y (str): Aspect correction along the Y-axis.
        X (str): Aspect correction along the X-axis.
    """
    NONE: str = 'NONE'
    Y: str = 'Y'
    X: str = 'X'

@dataclass
class BlurFilterType:
    """
    Enumerations of different filter types for the Blur node (Compositor).

    Attributes:
    ---
        FLAT (str): Flat filter type.
        TENT (str): Tent filter type.
        QUAD (str): Quad filter type.
        CUBIC (str): Cubic filter type.
        GAUSS (str): Gauss filter type.
        FAST_GAUSS (str): Fast Gauss filter type.
        CATROM (str): Catrom filter type.
        MITCH (str): Mitch filter type.
    """
    FLAT: str = 'FLAT'
    TENT: str = 'TENT'
    QUAD: str = 'QUAD'
    CUBIC: str = 'CUBIC'
    GAUSS: str = 'GAUSS'
    FAST_GAUSS: str = 'FAST_GAUSS'
    CATROM: str = 'CATROM'
    MITCH: str = 'MITCH'

@dataclass
class BlurSettings:
    """
    Settings for the Blur node (Compositor).

    Attributes:
    ---
        aspect_correction (str): Aspect correction mode. Options: BlurAspectCorrection.NONE, etc...
        factor (int): Overall blur factor.
        factor_x (int): Horizontal blur factor.
        factor_y (int): Vertical blur factor.
        filter_type (str): Type of filter to use for blurring. Options: BlurFilterType.FLAT, etc...
        size_x (int): Horizontal size of the blur.
        size_y (int): Vertical size of the blur.
        use_bokeh (bool): Whether to use bokeh effect in the blur.
        use_extended_bounds (bool): Whether to use extended bounds for the blur.
        use_gamma_correction (bool): Whether to use gamma correction for the blur.
        use_relative (bool): Whether to use relative sizing for the blur.
        use_variable_size (bool): Whether to use variable size for the blur.
    """
    aspect_correction: str = BlurAspectCorrection.NONE # Options: BlurAspectCorrection.NONE, BlurAspectCorrection.Y, BlurAspectCorrection.X
    factor: int = 0.0
    factor_x: int = 0.0
    factor_y: int = 0.0
    filter_type: str = BlurFilterType.GAUSS # Options: BlurFilterType.FLAT, BlurFilterType.TENT, BlurFilterType.QUAD, BlurFilterType.CUBIC, BlurFilterType.GAUSS, BlurFilterType.FAST_GAUSS, BlurFilterType.CATROM, BlurFilterType.MITCH
    size_x: int = 0
    size_y: int = 0
    use_bokeh: bool = False
    use_extended_bounds: bool = False
    use_gamma_correction: bool = False
    use_relative: bool = False
    use_variable_size: bool = False

class FilterNodeManager:
    """
    Manages Filter Nodes in a Node Group

    This class provides methods to create and manage filter nodes 
    within a specified node group in Blender's compositor.

    Attributes:
    ---
    node_group (NodeTree): The node group to manage nodes in.
    node_color (tuple): RGB color for the nodes. Defaults to DARK_PURPLE.
    use_custom_color (bool): Whether to use a custom color for the nodes. Defaults to False.
    """
    def __init__(self, *, node_group, node_color=Color.DARK_PURPLE, use_custom_color=False):
        """
        Initialize a FilterNodeManager instance.

        Args:
            node_group (NodeTree): The node group to manage nodes in.
            node_color (tuple): RGB color for the nodes managed by this instance. Defaults to DARK_PURPLE.
            use_custom_color (bool, optional): Whether to use a custom color for the nodes. Defaults to False.
        """
        self.node_group = node_group
        self.use_custom_color = use_custom_color
        self.node_color = node_color

    def create_glare_node(self, *, glare_name=FilterNodeNames.Glare, glare_label=FilterNodeNames.Glare, settings=None):
        """
        Create a Glare node in a node group and apply the specified settings.

        Args:
            glare_name (str, optional): Name of the Glare node. Defaults to "Glare".
            glare_label (str, optional): Label of the Glare node. Defaults to "Glare".
            settings (GlareSettings, optional): Settings for the Glare node. Defaults to GlareSettings() if not specified.

        Returns:
            Node: The newly created Glare node.
        """
        # Use default settings if none are provided
        if settings is None:
            settings = GlareSettings()

        # Create the Glare node
        glare_node = self.node_group.nodes.new(CompositorNodeNames.GLARE)
        glare_node.name = glare_name
        glare_node.label = glare_label
        glare_node.use_custom_color = self.use_custom_color

        if self.use_custom_color:
            glare_node.color = self.node_color
        else:
            print("Custom color usage is disabled. Please set 'use_custom_color' to True to apply custom colors.")

        # Apply settings from the GlareSettings instance
        for field_name in settings.__dataclass_fields__:
            value = getattr(settings, field_name)
            if hasattr(glare_node, field_name):
                setattr(glare_node, field_name, value)

        return glare_node

    def create_blur_node(self, *, blur_name=FilterNodeNames.Blur, blur_label=FilterNodeNames.Blur, settings=None):
        """
        Create a Blur node in a node group and apply the specified settings.

        Args:
            blur_name (str, optional): Name of the Blur node. Defaults to "Blur".
            blur_label (str, optional): Label of the Blur node. Defaults to "Blur".
            settings (BlurSettings, optional): Settings for the Blur node. Defaults to BlurSettings() if not specified.

        Returns:
            Node: The newly created Blur node.
        """
        # Use default settings if none are provided
        if settings is None:
            settings = BlurSettings()

        # Create the Blur node
        blur_node = self.node_group.nodes.new(CompositorNodeNames.BLUR)
        blur_node.name = blur_name
        blur_node.label = blur_label
        blur_node.use_custom_color = self.use_custom_color

        if self.use_custom_color:
            blur_node.color = self.node_color
        else:
            print("Custom color usage is disabled. Please set 'use_custom_color' to True to apply custom colors.")

        # Apply settings from the BlurSettings instance
        for field_name in settings.__dataclass_fields__:
            value = getattr(settings, field_name)
            if hasattr(blur_node, field_name):
                setattr(blur_node, field_name, value)

        return blur_node