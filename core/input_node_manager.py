from helpers import (Color, CompositorNodeNames)
from typing import Tuple, List
from dataclasses import dataclass, field

class InputNodeNames:
    """
    Class to store the names of various nodes and sockets used in the Input Node Manager
    """
    Group_Input = "Group Input"

@dataclass
class GroupInputSettings:
    """
    Settings for the Group Input node in the OE Bloom node group.

    Attributes:
        node_color (Tuple[float, float, float]): Color of the node. Defaults to DARK_GRAY.
        outputs_to_hide (List[int]): Indices of outputs to hide from the user in the Group Input node.
    """
    node_color: Tuple[float, float, float] = Color.DARK_GRAY  # Default to pure DARK_GRAY
    outputs_to_hide: List[int] = field(default_factory=list)  # Indices of outputs to hide

class InputNodeManager:
    """
    Manager for creating Group Input nodes in a node group.

    Attributes:
        node_group (NodeTree): The node group to manage nodes in.
        use_custom_color (bool): Whether to use a custom color for the nodes.
    """
    def __init__(self, *, node_group, use_custom_color: bool = False):
        """
        Initialize an InputNodeManager instance.

        Args:
            node_group (NodeTree): The node group to manage nodes in.
            use_custom_color (bool, optional): Whether to use a custom color for the nodes. Defaults to False.
        """
        self.node_group = node_group
        self.use_custom_color = use_custom_color

    def create_group_input_node(self, *, group_input_name=InputNodeNames.Group_Input, group_input_label=InputNodeNames.Group_Input, settings: GroupInputSettings=None):
        """
        Create a Group Input node in a node group and apply the specified settings.

        Args:
            group_input_name (str, optional): Name of the Group Input node. Defaults to "Group Input".
            group_input_label (str, optional): Label of the Group Input node. Defaults to "Group Input".
            settings (GroupInputSettings, optional): Settings for the Group Input node. Defaults to GroupInputSettings() if not specified.

        Returns:
            Node: The newly created Group Input node.
        """
        # Use default settings if none are provided
        if settings is None:
            settings = GroupInputSettings()

        # Create the Group Input node
        group_input_node = self.node_group.nodes.new(CompositorNodeNames.GROUP_INPUT)
        group_input_node.name = group_input_name
        group_input_node.label = group_input_label
        group_input_node.use_custom_color = self.use_custom_color

        # Apply settings from the GroupInputSettings instance
        # Apply color
        if self.use_custom_color:
            group_input_node.color = settings.node_color
        else:
            print("Custom color usage is disabled. Please set 'use_custom_color' to True to apply custom colors.")

        # Hide specified outputs
        for output_index in settings.outputs_to_hide:
            if output_index < len(group_input_node.outputs):
                group_input_node.outputs[output_index].hide = True

        return group_input_node