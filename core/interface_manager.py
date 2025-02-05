from typing import Optional
from typing import Any
from dataclasses import dataclass


@dataclass
class SocketType:
    BOOLEAN: str = "NodeSocketBool"
    VECTOR: str = "NodeSocketVector"
    INTEGER: str = "NodeSocketInt"
    FLOAT: str = "NodeSocketFloat"
    COLOR: str = "NodeSocketColor"


@dataclass
class SubType:
    if SocketType.FLOAT == True:
        PERCENTAGE: str = "PERCENTAGE"
        FACTOR: str = "FACTOR"
        ANGLE: str = "ANGLE"
        TIME: str = "TIME"
        TIME_ABSOLUTE: str = "TIME_ABSOLUTE"
        DISTANCE: str = "DISTANCE"
        WAVELENGTH: str = "WAVELENGTH"
        COLOR_TEMPERATURE: str = "COLOR_TEMPERATURE"
        FREQUENCY: str = "FREQUENCY"
    elif SocketType.VECTOR == True:
        TRANSLATION: str = "TRANSLATION"
        DIRECTION: str = "DIRECTION"
        VELOCITY: str = "VELOCITY"
        ACCELERATION: str = "ACCELERATION"
        EULER: str = "EULER"
        XYZ: str = "XYZ"


@dataclass
class InOut:
    INPUT: str = "INPUT"
    OUTPUT: str = "OUTPUT"


@dataclass
class SocketSettings:
    default_value: Any = 0.0
    min_value: Any = 0.0
    max_value: Any = 1.0
    subtype: str = "NONE"
    attribute_domain: str = "POINT"
    description: str = ""


class NodeTreeSocket:
    def __init__(self, *, node_tree):
        self.node_tree = node_tree

    def create_socket(
        self,
        *,
        name: str,
        in_out: str,
        socket_type: str,
        parent: Optional[str] = None,
        settings: Optional[SocketSettings] = None,
    ):
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

        if settings is None:
            settings = SocketSettings()

        self.node_tree.new_socket(name, in_out, socket_type, parent)
