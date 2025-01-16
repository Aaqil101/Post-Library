from helpers import (Color, CompositorNodeNames)
from typing import Tuple, List
from dataclasses import dataclass, field

class OutputNodeNames:
    """
    Class to store the names of various nodes and sockets used in the Output Node Manager
    """
    Group_Output = "Group Output"

@dataclass
class GroupOutputSettings:
    """
    Class to store the settings for the Group Output node in the Output Node Manager

    Attributes:
        node_color (Tuple[float, float, float]): RGB color for the Group Output node. Defaults to DARK_GRAY.
        outputs_to_hide (List[int]): Indices of outputs to hide from the user in the Group Output node.
        is_active_output (bool): Whether the Group Output node is the active output of the node group. Defaults to False.
    """
    node_color: Tuple[float, float, float] = Color.DARK_GRAY
    outputs_to_hide: List[int] = field(default_factory=list)
    is_active_output: bool = False

class OutputNodeManager:
    """
    Manages the Group Output node in the Output Node Manager.

    This class provides methods to create and manage the Group Output node in a node group.

    Attributes:
        node_group (NodeTree): The node group to manage nodes in.
        use_custom_color (bool): Whether to use a custom color for the nodes. Defaults to False.
    """
    def __init__(self, *, node_group, use_custom_color=False):
        """
        Initialize an OutputNodeManager instance.

        Args:
            node_group (NodeTree): The node group to manage nodes in.
            use_custom_color (bool, optional): Whether to use a custom color for the nodes. Defaults to False.
        """
        self.node_group = node_group
        self.use_custom_color = use_custom_color
    
    def create_group_output_node(self, *, group_output_name=OutputNodeNames.Group_Output, group_output_label=OutputNodeNames.Group_Output, settings=None):
        """
        Create a Group Output node in a node group and apply the specified settings.

        Args:
            group_output_name (str, optional): Name of the Group Output node. Defaults to "Group Output".
            group_output_label (str, optional): Label of the Group Output node. Defaults to "Group Output".
            settings (GroupOutputSettings, optional): Settings for the Group Output node. Defaults to GroupOutputSettings() if not specified.

        Returns:
            Node: The newly created Group Output node.
        """
        # Use the default settings if none are provided
        if settings is None:
            settings = GroupOutputSettings()

        # Create the Group Input node
        group_output_node = self.node_group.nodes.new(CompositorNodeNames.GROUP_OUTPUT)
        group_output_node.name = group_output_name
        group_output_node.label = group_output_label
        group_output_node.use_custom_color = self.use_custom_color

        # Apply settings from the GroupOutputSettings instance
        # Apply color
        if self.use_custom_color:
            group_output_node.color = settings.node_color
        else:
            print("Custom color usage is disabled. Please set 'use_custom_color' to True to apply custom colors.")

        # Hide specified outputs
        for output_index in settings.outputs_to_hide:
            if output_index < len(group_output_node.outputs):
                group_output_node.outputs[output_index].hide = True

        return group_output_node