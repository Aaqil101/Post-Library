from dataclasses import dataclass
from typing import Any, Optional

from bpy.types import NodeTreeInterfaceSocket


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
    # General
    NONE: str = "NONE"

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
    """

    default_value: Any = 0.0
    min_value: Any = 0.0
    max_value: Any = 1.0
    subtype: str = "NONE"
    attribute_domain: str = "POINT"
    hide_value: bool = False


ALLOWED_SUBTYPES: dict[str, set[str]] = {
    SocketType.FLOAT: {
        SubType.NONE,
        SubType.PERCENTAGE,
        SubType.FACTOR,
        SubType.ANGLE,
        SubType.TIME,
        SubType.TIME_ABSOLUTE,
        SubType.DISTANCE,
        SubType.WAVELENGTH,
        SubType.COLOR_TEMPERATURE,
        SubType.FREQUENCY,
    },
    SocketType.VECTOR: {
        SubType.NONE,
        SubType.TRANSLATION,
        SubType.DIRECTION,
        SubType.VELOCITY,
        SubType.ACCELERATION,
        SubType.EULER,
        SubType.XYZ,
    },
    SocketType.COLOR: {"NONE"},  # ✅ Allow "NONE" for NodeSocketColor
}


def is_valid_subtype(socket_type: str, subtype: str) -> bool:
    """
    Checks if the given subtype is valid for the given socket type.

    Args:
        socket_type (str): The type of the socket.
        subtype (str): The subtype to check.

    Returns:
        bool: True if the subtype is valid, False otherwise.
    """
    return subtype in ALLOWED_SUBTYPES.get(socket_type, set())


class NodeTreeSocket:
    """
    A class for managing sockets in a NodeTree.

    Attributes:
        node_tree (NodeTree): The node tree to manage sockets in.
    """

    def __init__(self, *, node_tree) -> None:
        """
        Initialize a NodeTreeSocket instance.

        Args:
            node_tree (NodeTree): The node tree to manage sockets in.
        """

        self.node_tree: Any = node_tree

    def create_socket(
        self,
        *,
        name: str,
        in_out: str,
        socket_type: str,
        parent: Optional[str] = None,
        description: Optional[str] = "",
        settings: Optional[SocketSettings] = None,
    ) -> Any:
        """
        Creates a new socket in the node tree.

        Args:
            name (str): The name of the socket.
            in_out (str): The direction of the socket. Must be 'INPUT' or 'OUTPUT'.
            socket_type (str): The type of the socket. Must be one of the values in `SocketType`.
            parent (Optional[str], optional): The name of the parent socket. Defaults to None.
            description (Optional[str], optional): The description of the socket. Defaults to "".
            settings (Optional[SocketSettings], optional): The settings for the socket. Defaults to `SocketSettings()` if not specified.

        Raises:
            ValueError: If the in_out or socket_type is invalid.

        Returns:
            NodeSocket: The newly created socket.
        """
        if in_out not in (InOut.INPUT, InOut.OUTPUT):
            raise ValueError(
                f"Invalid in_out value: {in_out}. Must be 'INPUT' or 'OUTPUT'."
            )

        if socket_type not in (
            # SocketType.BOOLEAN, # TODO: Implement BOOLEAN socket type
            SocketType.VECTOR,
            # SocketType.INTEGER, # TODO: Implement INTEGER socket type
            SocketType.FLOAT,
            SocketType.COLOR,
        ):
            raise ValueError(
                f"Invalid socket_type: {socket_type}. Must be one of {SocketType.__annotations__.values()}"
            )

        # Use default settings if none are provided
        if settings is None:
            settings = SocketSettings()

        # Validate subtype
        if not is_valid_subtype(socket_type, settings.subtype):
            raise ValueError(
                f"Invalid subtype {settings.subtype} for socket type {socket_type}."
            )

        # Create a new socket
        socket: NodeTreeInterfaceSocket = self.node_tree.interface.new_socket(
            name=name,
            in_out=in_out,
            socket_type=socket_type,
            description=description,
            parent=parent,
        )

        if socket_type == SocketType.FLOAT and SocketType.VECTOR:
            socket.min_value = settings.min_value
            socket.max_value = settings.max_value
            socket.subtype = settings.subtype

        socket.default_value = settings.default_value
        socket.attribute_domain = settings.attribute_domain
        socket.hide_value = settings.hide_value

        return socket

    def create_panels(self, *, name: str):
        pass
