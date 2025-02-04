from helpers import Color, CompositorNodeNames
from typing import Tuple
from dataclasses import dataclass, field


class UtilitiesNodeNames:
    """
    Class to store the names of various utility nodes.
    """

    Switch = "Switch"


@dataclass
class SwitchSettings:
    """
    Settings for the Switch node in the OE Bloom node group.

    Attributes:
        node_color (Tuple[float, float, float]): Color of the node. Defaults to LIGHT_GRAY.
        check (bool): Whether to check the Switch node. Defaults to False.
        off (list): Color of the "Off" output of the Switch node. Defaults to pure white.
        on (list): Color of the "On" output of the Switch node. Defaults to pure white.
    """

    node_color: Tuple[float, float, float] = Color.LIGHT_GRAY  # LIGHT_GRAY Color
    check: bool = False
    off: list = (0.8, 0.8, 0.8, 1.0)  # White Color
    on: list = (0.8, 0.8, 0.8, 1.0)  # White Color


class UtilitiesNodeManager:
    def __init__(self, *, node_group, use_custom_color=False):
        """
        Initialize a UtilitiesNodeManager instance.

        Args:
            node_group (NodeTree): The node group to manage nodes in.
            use_custom_color (bool, optional): Whether to use a custom color for the nodes. Defaults to False.
        """
        self.node_group = node_group
        self.use_custom_color = use_custom_color

    def create_switch_node(
        self,
        *,
        switch_name=UtilitiesNodeNames.Switch,
        switch_label=UtilitiesNodeNames.Switch,
        settings=None
    ):
        """
        Create a Switch node in a node group and apply the specified settings.

        Args:
            switch_name (str, optional): Name of the Switch node. Defaults to "Switch".
            switch_label (str, optional): Label of the Switch node. Defaults to "Switch".
            settings (SwitchSettings, optional): Settings for the Switch node. Defaults to SwitchSettings() if not specified.

        Returns:
            Node: The newly created Switch node.
        """
        # Use default settings if none are provided
        if settings is None:
            settings = SwitchSettings()

        # Create the Switch node
        switch_node = self.node_group.nodes.new(CompositorNodeNames.SWITCH)
        switch_node.label = switch_label
        switch_node.name = switch_name
        switch_node.use_custom_color = self.use_custom_color

        # Apply settings from the SwitchSettings instance
        if self.use_custom_color:
            switch_node.color = settings.node_color
        else:
            print(
                "Custom color usage is disabled. Please set 'use_custom_color' to True to apply custom colors."
            )

        switch_node.check = settings.check
        switch_node.inputs[0].default_value = settings.off
        switch_node.inputs[1].default_value = settings.on

        return switch_node
