from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SocketType:
    """
    Enum for the type of a socket.

    Attributes:
        BOOLEAN: str
            The socket type is a boolean.
        VECTOR: str
            The socket type is a vector.
        INTEGER: str
            The socket type is an integer.
        FLOAT: str
            The socket type is a float.
        COLOR: str
            The socket type is a color.
    """

    # BOOLEAN: str = "NodeSocketBool"  # TODO: Implement BOOLEAN socket type
    VECTOR: str = "NodeSocketVector"
    # INTEGER: str = "NodeSocketInt"  # TODO: Implement INTEGER socket type
    FLOAT: str = "NodeSocketFloat"
    COLOR: str = "NodeSocketColor"


@dataclass
class SubType:
    # For Float
    PERCENTAGE: str = "PERCENTAGE"
    FACTOR: str = "FACTOR"
    ANGLE: str = "ANGLE"
    TIME: str = "TIME"
    TIME_ABSOLUTE: str = "TIME_ABSOLUTE"
    DISTANCE: str = "DISTANCE"
    WAVELENGTH: str = "WAVELENGTH"
    COLOR_TEMPERATURE: str = "COLOR_TEMPERATURE"
    FREQUENCY: str = "FREQUENCY"

    # For Vector
    TRANSLATION: str = "TRANSLATION"
    DIRECTION: str = "DIRECTION"
    VELOCITY: str = "VELOCITY"
    ACCELERATION: str = "ACCELERATION"
    EULER: str = "EULER"
    XYZ: str = "XYZ"


@dataclass
class InOut:
    """
    Enum for the direction of a socket.

    Attributes:
        INPUT: str
            The socket is an input.
        OUTPUT: str
            The socket is an output.
    """

    INPUT: str = "INPUT"
    OUTPUT: str = "OUTPUT"


@dataclass
class SocketSettings:
    """
    Data class to store the settings for a socket.

    Attributes:
        default_value: Any = 0.0
            The default value of the socket.
        min_value: Any = 0.0
            The minimum value of the socket.
        max_value: Any = 1.0
            The maximum value of the socket.
        subtype: str = "NONE"
            The subtype of the socket. Can be one of the values in `SubType`.
        attribute_domain: str = "POINT"
            The attribute domain of the socket. Can be one of the values in
            `AttributeDomain`.
        hide_value: bool = False
            Whether to hide the value of the socket.
        description: str = ""
            A description of the socket.
    """

    default_value: Any = 0.0
    min_value: Any = 0.0
    max_value: Any = 1.0
    subtype: str = "NONE"
    attribute_domain: str = "POINT"
    hide_value: bool = False
    description: str = ""


class NodeTreeSocket:
    """
    A class for managing sockets in a NodeTree.

    Attributes:
        node_tree (NodeTree): The node tree to manage sockets in.
    """

    def __init__(self, *, node_tree):
        """
        Initialize a NodeTreeSocket instance.

        Args:
            node_tree (NodeTree): The node tree to manage sockets in.
        """

        self.node_tree = node_tree

    def is_valid_subtype(socket_type: str, subtype: str) -> bool:
        return subtype in ALLOWD_SUBTYPES.get(socket_type, set())

    def create_socket(
        self,
        *,
        name: str,
        in_out: str,
        socket_type: str,
        parent: Optional[str] = None,
        settings: Optional[SocketSettings] = None,
    ):
        """
        Create a new socket in the node tree.

        Args:
            name (str): The name of the socket.
            in_out (str): The type of the socket. Must be 'INPUT' or 'OUTPUT'.
            socket_type (str): The type of socket. Must be one of the values in `SocketType`.
            parent (str, optional): The parent socket of the new socket. Defaults to None.
            settings (SocketSettings, optional): The settings for the socket. Defaults to None.

        Raises:
            ValueError: If `in_out` or `socket_type` is invalid.

        Returns:
            socket
        """
        if in_out not in (InOut.INPUT, InOut.OUTPUT):
            raise ValueError(
                f"Invalid in_out value: {in_out}. Must be 'INPUT' or 'OUTPUT'."
            )

        if socket_type not in (
            SocketType.BOOLEAN,
            SocketType.VECTOR,
            SocketType.INTEGER,
            SocketType.FLOAT,
            SocketType.COLOR,
        ):
            raise ValueError(
                f"Invalid socket_type: {socket_type}. Must be one of {SocketType.__annotations__.values()}"
            )

        # Use default settings if none are provided
        if settings is None:
            settings = SocketSettings()

        # Create a new socket
        socket = self.node_tree.new_socket(name, in_out, socket_type, parent)
        socket.default_value = settings.default_value
        socket.min_value = settings.min_value
        socket.max_value = settings.max_value
        socket.subtype = settings.subtype
        socket.attribute_domain = settings.attribute_domain
        socket.hide_value = settings.hide_value
        socket.description = settings.description
        return socket
