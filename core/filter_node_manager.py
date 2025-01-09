from helpers import Color
from dataclasses import dataclass, field

class FilterNodeManager_Names:
    """
    Class to store the names of various nodes and sockets used in the Filter Node Manager.
    """
    Glare: str = "Glare"
    Blur: str = "Blur"

@dataclass
class GlareSettings:
    """
    Settings for the Glare node (Compositor).

    Attributes:
    ---
        angle_offset (float): Angle offset for the glare effect.
        color_modulation (float): Color modulation for the glare effect.
        fade (float): Fade-out value for the glare effect.
        glare_type (str): Type of glare effect, e.g. 'BLOOM', 'GHOSTS', 'STREAKS'.
        iterations (int): Number of iterations for the glare effect.
        mix (float): Mix value for the glare effect.
        quality (str): Quality of the glare effect, e.g. 'LOW', 'MEDIUM', 'HIGH'.
        size (int): Size of the glare effect.
        streaks (int): Number of streaks for the glare effect.
        threshold (float): Threshold value for the glare effect.
        use_rotate_45 (bool): Whether to use a 45-degree rotation for the glare effect.
    """
    angle_offset: float = 0.0
    color_modulation: float = 0.25
    fade: float = 0.9
    glare_type: str = 'STREAKS'  # Options: 'BLOOM', 'GHOSTS', 'STREAKS', 'FOG_GLOW', 'SIMPLE_STAR'
    iterations: int = 3
    mix: float = 0.0
    quality: str = 'LOW'  # Options: 'LOW', 'MEDIUM', 'HIGH'
    size: int = 8
    streaks: int = 4
    threshold: float = 1.0
    use_rotate_45: bool = True

@dataclass
class BlurSettings:
    """
    Settings for the Blur node (Compositor).

    Attributes:
    ---
        aspect_correction (str): Aspect correction mode. Options: 'NONE', 'Y', 'X'.
        factor (int): Overall blur factor.
        factor_x (int): Horizontal blur factor.
        factor_y (int): Vertical blur factor.
        filter_type (str): Type of filter to use for blurring. Options: 'FLAT', 'TENT', 'QUAD', 'CUBIC', 'GAUSS', 'FAST_GAUSS', 'CATROM', 'MITCH'.
        size_x (int): Horizontal size of the blur.
        size_y (int): Vertical size of the blur.
        use_bokeh (bool): Whether to use bokeh effect in the blur.
        use_extended_bounds (bool): Whether to use extended bounds for the blur.
        use_gamma_correction (bool): Whether to use gamma correction for the blur.
        use_relative (bool): Whether to use relative sizing for the blur.
        use_variable_size (bool): Whether to use variable size for the blur.
    """
    aspect_correction: str = 'NONE' # Options: 'NONE', 'Y', 'X'
    factor: int = 0.0
    factor_x: int = 0.0
    factor_y: int = 0.0
    filter_type: str = 'GAUSS' # Options: 'FLAT', 'TENT', 'QUAD', 'CUBIC', 'GAUSS', 'FAST_GAUSS', 'CATROM', 'MITCH'
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
    def __init__(self, node_group, node_color=Color.DARK_PURPLE, use_custom_color=False):
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

    def create_glare_node(self, glare_name=FilterNodeManager_Names.Glare, glare_label=FilterNodeManager_Names.Glare, settings=None):
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
        glare_node = self.node_group.nodes.new("CompositorNodeGlare")
        glare_node.name = glare_name
        glare_node.label = glare_label
        glare_node.use_custom_color = self.use_custom_color
        glare_node.color = self.node_color

        # Apply settings from the GlareSettings instance
        for field_name in settings.__dataclass_fields__:
            value = getattr(settings, field_name)
            if hasattr(glare_node, field_name):
                setattr(glare_node, field_name, value)

        return glare_node

    def create_blur_node(self, blur_name=FilterNodeManager_Names.Blur, blur_label=FilterNodeManager_Names.Blur, settings=None):
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
        blur_node = self.node_group.nodes.new("CompositorNodeBlur")
        blur_node.name = blur_name
        blur_node.label = blur_label
        blur_node.use_custom_color = self.use_custom_color
        blur_node.color = self.node_color

        # Apply settings from the BlurSettings instance
        for field_name in settings.__dataclass_fields__:
            value = getattr(settings, field_name)
            if hasattr(blur_node, field_name):
                setattr(blur_node, field_name, value)

        return blur_node