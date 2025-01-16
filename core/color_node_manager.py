from helpers import (Color, CompositorNodeNames)
from typing import Tuple
from dataclasses import dataclass, field

class ColorNodeNames:
    """
    Class to store the names of various nodes used in the ColorNodeManager class.
    """
    Hue_Saturation_Value = "Hue/Saturation/Value"  # Name of the Hue Saturation node.
    Mix_Color = "Mix Color"  # Name of the MixColor node.

@dataclass
class BlendType:
    """
    Enumerations of different color blend types that can be used in the MixColor node.

    Attributes:
    ---
        DARKEN (str): Darken blend type. The result color is the lowest value of each component.
        MULTIPLY (str): Multiply blend type. The result color is each component multiplied by the 
            corresponding component of the other color.
        BURN (str): Burn blend type. The result color is the darkest possible color that can be made
            by multiplying or screening the two colors.
        LIGHTEN (str): Lighten blend type. The result color is the highest value of each component.
        SCREEN (str): Screen blend type. The result color is the inverse of each component multiplied
            by the corresponding component of the other color.
        DODGE (str): Dodge blend type. The result color is the brightest possible color that can be
            made by multiplying or screening the two colors.
        ADD (str): Add blend type. The result color is each component of the two colors added together.
        OVERLAY (str): Overlay blend type. The result color is a combination of multiply and screen
            blend types.
        SOFT_LIGHT (str): Soft Light blend type. The result color is a combination of multiply and
            screen blend types with a bias towards the background color.
        LINEAR_LIGHT (str): Linear Light blend type. The result color is a combination of multiply and
            screen blend types with a bias towards the foreground color.
        DIFFERENCE (str): Difference blend type. The result color is the absolute difference between
            each component of the two colors.
        EXCLUSION (str): Exclusion blend type. The result color is similar to difference, but with a
            bias towards the background color.
        SUBTRACT (str): Subtract blend type. The result color is each component of the first color
            minus the corresponding component of the second color.
        DIVIDE (str): Divide blend type. The result color is each component of the first color divided
            by the corresponding component of the second color.
        HUE (str): Hue blend type. The result color has the hue of the first color and the saturation
            and value of the second color.
        SATURATION (str): Saturation blend type. The result color has the saturation of the first color
            and the hue and value of the second color.
        COLOR (str): Color blend type. The result color has the hue and saturation of the first color
            and the value of the second color.
        VALUE (str): Value blend type. The result color has the value of the first color and the hue and
            saturation of the second color.
    """
    MIX: str = 'MIX'
    DARKEN: str = 'DARKEN'
    MULTIPLY: str = 'MULTIPLY'
    BURN: str = 'BURN'
    LIGHTEN: str = 'LIGHTEN'
    SCREEN: str = 'SCREEN'
    DODGE: str = 'DODGE'
    ADD: str = 'ADD'
    OVERLAY: str = 'OVERLAY'
    SOFT_LIGHT: str = 'SOFT_LIGHT'
    LINEAR_LIGHT: str = 'LINEAR_LIGHT'
    DIFFERENCE: str = 'DIFFERENCE'
    EXCLUSION: str = 'EXCLUSION'
    SUBTRACT: str = 'SUBTRACT'
    DIVIDE: str = 'DIVIDE'
    HUE: str = 'HUE'
    SATURATION: str = 'SATURATION'
    COLOR: str = 'COLOR'
    VALUE: str = 'VALUE'

@dataclass
class MixColorSettings:
    """
    Settings for the MixColor node in a node group.

    Attributes:
    ---
        node_color (Tuple[float, float, float]): RGB color for the MixColor node. Defaults to BROWN.
        blend_type (str): Blend type for the MixColor node. Options include DARKEN, MULTIPLY, BURN, etc. Defaults to MIX.
        use_alpha (bool): Whether to use alpha in the MixColor node. Defaults to False.
        use_clamp (bool): Whether to clamp values in the MixColor node. Defaults to False.
        fac_default_value (float): Default value for the Fac input of the MixColor node. Defaults to 0.0.
        hide_fac (bool): Whether to hide the Fac input of the MixColor node. Defaults to False.
        hide_col1 (bool): Whether to hide the Color1 input of the MixColor node. Defaults to False.
        hide_col2 (bool): Whether to hide the Color2 input of the MixColor node. Defaults to False.
    """
    node_color: Tuple[float, float, float] = Color.BROWN
    blend_type: str = BlendType.MIX  # Blend type for the MixColor node
    use_alpha: bool = False  # Use alpha in the MixColor node
    use_clamp: bool = False  # Clamp values in the MixColor node
    fac_default_value: float = 0.0  # Default value for the Fac input
    hide_fac: bool = False  # Hide the Fac input
    hide_col1: bool = False  # Hide the Color1 input
    hide_col2: bool = False  # Hide the Color2 input

@dataclass
class HueSatSettings:
    """
    Settings for the Hue/Saturation/Value node in a node group.

    Attributes:
    ---
        node_color (Tuple[float, float, float]): RGB color for the Hue/Saturation/Value node. Defaults to BROWN.
        img_default_value (list): Default value for the Image input of the Hue/Saturation/Value node. Defaults to (1.0, 1.0, 1.0, 1.0).
        hue_default_value (float): Default value for the Hue input of the Hue/Saturation/Value node. Defaults to 0.5.
        sat_default_value (float): Default value for the Saturation input of the Hue/Saturation/Value node. Defaults to 1.0.
        val_default_value (float): Default value for the Value input of the Hue/Saturation/Value node. Defaults to 1.0.
        fac_default_value (float): Default value for the Factor input of the Hue/Saturation/Value node. Defaults to 1.0.
        hide_img (bool): Hide the Image input of the Hue/Saturation/Value node. Defaults to False.
        hide_hue (bool): Hide the Hue input of the Hue/Saturation/Value node. Defaults to False.
        hide_sat (bool): Hide the Saturation input of the Hue/Saturation/Value node. Defaults to False.
        hide_val (bool): Hide the Value input of the Hue/Saturation/Value node. Defaults to False.
        hide_fac (bool): Hide the Factor input of the Hue/Saturation/Value node. Defaults to False.
    """
    node_color: Tuple[float, float, float] = Color.BROWN
    img_default_value: list = (1.0, 1.0, 1.0, 1.0)
    hue_default_value: float = 0.5
    sat_default_value: float = 1.0
    val_default_value: float = 1.0
    fac_default_value: float = 1.0
    hide_img: bool = False
    hide_hue: bool = False
    hide_sat: bool = False
    hide_val: bool = False
    hide_fac: bool = False

class ColorNodeManager:
    """
    Manager for color-related nodes in a node group.

    This class is used to create and configure color-related nodes in a node group.

    Attributes:
    ---
    node_group (NodeTree): The node group to manage nodes in.
    node_color (tuple): RGB color for the nodes. Defaults to BROWN.
    use_custom_color (bool): Whether to use a custom color for the nodes. Defaults to True.
    """
    def __init__(self, *, node_group, use_custom_color=False):
        """
        Initialize a ColorNodeManager instance.

        Args:
            node_group (NodeTree): The node group to manage nodes in.
            node_color (tuple): RGB color for the nodes managed by this instance. Defaults to BROWN.
            use_custom_color (bool, optional): Whether to use a custom color for the nodes. Defaults to True.
        """
        self.node_group = node_group
        self.use_custom_color = use_custom_color

    def create_mixcolor_node(self, *, mixcolor_name=ColorNodeNames.Mix_Color, mixcolor_label=ColorNodeNames.Mix_Color, settings=None):
        """
        Create a MixColor node in a node group and apply the specified settings.

        Args:
            mixcolor_name (str, optional): Name of the MixColor node. Defaults to "Mix Color".
            mixcolor_label (str, optional): Label of the MixColor node. Defaults to "Mix Color".
            settings (MixColorSettings, optional): Settings for the MixColor node. Defaults to MixColorSettings() if not specified.

        Returns:
            Node: The newly created MixColor node.
        """
        # Use default settings if none are provided
        if settings is None:
            settings = MixColorSettings()

        # Create the MixColor node
        mixcolor_node = self.node_group.nodes.new(CompositorNodeNames.MIX_RGB)
        mixcolor_node.name = mixcolor_name
        mixcolor_node.label = mixcolor_label
        mixcolor_node.use_custom_color = self.use_custom_color
        
        if self.use_custom_color:
            mixcolor_node.color = settings.node_color
        else:
            print("Custom color usage is disabled. Please set 'use_custom_color' to True to apply custom colors.")

        # Apply settings from the MixColorSettings instance
        mixcolor_node.blend_type = settings.blend_type
        mixcolor_node.use_alpha = settings.use_alpha
        mixcolor_node.use_clamp = settings.use_clamp

        # Configure the Fac input
        mixcolor_node.inputs[0].default_value = settings.fac_default_value
        mixcolor_node.inputs[0].hide = settings.hide_fac

        # Configure the Color1 input
        mixcolor_node.inputs[1].hide = settings.hide_col1

        # Configure the Color2 input
        mixcolor_node.inputs[2].hide = settings.hide_col2

        return mixcolor_node
    
    def create_huesat_node(self, *, huesat_name=ColorNodeNames.Hue_Saturation_Value, huesat_label=ColorNodeNames.Hue_Saturation_Value, settings=None):
        """
        Create a Hue/Saturation/Value node in a node group and apply the specified settings.

        Args:
            huesat_name (str, optional): Name of the Hue/Saturation/Value node. Defaults to "Hue Saturation Value".
            huesat_label (str, optional): Label of the Hue/Saturation/Value node. Defaults to "Hue Saturation Value".
            settings (HueSatSettings, optional): Settings for the Hue/Saturation/Value node. Defaults to HueSatSettings() if not    specified.

        Returns:
            Node: The newly created Hue/Saturation/Value node.
        """
        # Use default settings if none are provided
        if settings is None:
            settings = HueSatSettings()

        # Create the Hue/Saturation/Value Node
        huesat_node = self.node_group.nodes.new(CompositorNodeNames.HUE_SATURATION_VALUE)
        huesat_node.name = huesat_name
        huesat_node.label = huesat_label
        huesat_node.use_custom_color = self.use_custom_color

        if self.use_custom_color:
            huesat_node.color = settings.node_color
        else:
            print("Custom color usage is disabled. Please set 'use_custom_color' to True to apply custom colors.")

        # Apply settings from the HueSatSettings instance
        # Configure the Image input
        huesat_node.inputs[0].default_value = settings.img_default_value
        huesat_node.inputs[0].hide = settings.hide_img

        # Configure the Hue input
        huesat_node.inputs[1].default_value = settings.hue_default_value
        huesat_node.inputs[1].hide = settings.hide_hue

        # Configure the Saturation input
        huesat_node.inputs[2].default_value = settings.sat_default_value
        huesat_node.inputs[2].hide = settings.hide_sat

        # Configure the Value input
        huesat_node.inputs[3].default_value = settings.val_default_value
        huesat_node.inputs[3].hide = settings.hide_val

        # Configure the Factor input
        huesat_node.inputs[4].default_value = settings.fac_default_value
        huesat_node.inputs[4].hide = settings.hide_fac

        return huesat_node