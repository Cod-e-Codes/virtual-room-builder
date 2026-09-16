"""Virtual room builder: compose and render simple 3D room layouts."""

from virtual_room_builder.door import Door
from virtual_room_builder.errors import (
    InvalidDimensionError,
    InvalidPlacementError,
    OutOfBoundsError,
    VirtualRoomBuilderError,
)
from virtual_room_builder.furniture.bookshelf import Bookshelf
from virtual_room_builder.furniture.chair import Chair
from virtual_room_builder.furniture.couch import Couch
from virtual_room_builder.furniture.lamp import Lamp
from virtual_room_builder.furniture.table import Table
from virtual_room_builder.geometry import Direction
from virtual_room_builder.room import Room
from virtual_room_builder.scene import Scene

__version__ = "1.0.0"

__all__ = [
    "Bookshelf",
    "Chair",
    "Couch",
    "Direction",
    "Door",
    "InvalidDimensionError",
    "InvalidPlacementError",
    "Lamp",
    "OutOfBoundsError",
    "Room",
    "Scene",
    "Table",
    "VirtualRoomBuilderError",
    "__version__",
]
