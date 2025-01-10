from helpers import (hexcode_to_rgb, hex_color_add)
from dataclasses import dataclass, field

class LayoutNodeNames:
    Frame = "Frame"
    Reroute = "Reroute"

@dataclass
class SocketColor:
    """
    A data class representing different types of socket colors.

    Attributes:
        NodeSocketColor (str): The color socket type for color nodes.
        NodeSocketFloat (str): The float socket type for numerical values.
        NodeSocketVector (str): The vector socket type for vector data.
    """
    NodeSocketColor: str = "NodeSocketColor"  # Color socket type
    NodeSocketFloat: str = "NodeSocketFloat"  # Float socket type
    NodeSocketVector: str = "NodeSocketVector"  # Vector socket type

@dataclass
class FrameSettings:
    """
    Settings for the Frame node in the OE Bloom node group.

    Attributes:
        label_size (int): Size of the label text. Defaults to 20.
        shrink (bool): Whether to shrink the frame to fit the node. Defaults to False.
    """
    label_size: int = 20
    shrink: bool = False

@dataclass
class RerouteSettings:
    """
    Settings for the Reroute node in the OE Bloom node group.

    Attributes:
        socket_idname (str): The type of socket to use for the reroute node. Options are:
            SocketColor.NodeSocketColor, SocketColor.NodeSocketFloat, SocketColor.NodeSocketVector
    """
    socket_idname: str = SocketColor.NodeSocketColor # Options: SocketColor.NodeSocketColor, SocketColor.NodeSocketFloat, SocketColor.NodeSocketVector

class LayoutNodeManager:
    """
    A class for managing the layout of nodes in a node group, such as setting the size and color of nodes.

    Attributes:
        node_group (NodeTree): The node group to manage nodes in.
        node_color (list): A list containing two elements for color addition, which will be converted to RGB.
        use_custom_color (bool): Whether to use a custom color for the nodes. Defaults to False.
    """
    def __init__(self, node_group, node_color: list, use_custom_color=False):       
        """
        Initialize a LayoutNodeManager instance.

        Args:
            node_group (NodeTree): The node group to manage nodes in.
            node_color (list): A list containing two elements for color addition, which will be converted to RGB.
            use_custom_color (bool, optional): Whether to use a custom color for the nodes. Defaults to False.
        """
        self.node_group = node_group
        self.use_custom_color = use_custom_color

        # Validate and convert the color inputs
        if len(node_color) != 2:
            raise ValueError("node_color must contain exactly two elements.")
        self.node_color = hexcode_to_rgb(
            hex_color_add(
                node_color[0],
                node_color[1]
            )
        )

    def create_frame_node(self, frame_name=LayoutNodeNames.Frame, frame_label=LayoutNodeNames.Frame, settings=None):
        """
        Create a Frame node in a node group and apply the specified settings.

        Args:
            frame_name (str, optional): Name of the Frame node. Defaults to "Frame".
            frame_label (str, optional): Label of the Frame node. Defaults to "Frame".
            settings (FrameSettings, optional): Settings for the Frame node. Defaults to FrameSettings() if not specified.

        Returns:
            Node: The newly created Frame node.
        """
        # Use default settings if none are provided
        if settings is None:
            settings = FrameSettings()

        # Create the Frame node
        frame_node = self.node_group.nodes.new("NodeFrame")
        frame_node.name = frame_name
        frame_node.label = frame_label
        frame_node.use_custom_color = self.use_custom_color
        frame_node.color = self.node_color

        # Apply settings from the FrameSettings instance
        frame_node.label_size = settings.label_size
        frame_node.shrink = settings.shrink

        return frame_node

    def create_reroute_node(self, reroute_name=LayoutNodeNames.Reroute, reroute_label=LayoutNodeNames.Reroute, settings=None):
        # Use default settings if none are provided
        if settings is None:
            settings = RerouteSettings()

        # Create the Reroute node
        reroute_node = self.node_group.nodes.new("NodeReroute")
        reroute_node.name = reroute_name
        reroute_node.label = reroute_label

        # Apply settings from the RerouteSettings instance
        reroute_node.socket_idname = settings.socket_idname

        return reroute_node