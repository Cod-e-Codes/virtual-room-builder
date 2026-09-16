"""The room shell: the four walls, floor, and ceiling wireframe."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from virtual_room_builder.draw import add_segments
from virtual_room_builder.errors import InvalidDimensionError
from virtual_room_builder.geometry import box_edges, box_vertices

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D


@dataclass(frozen=True)
class Room:
    """A rectangular room with the given floor plan and ceiling height.

    The room occupies x in [0, length], y in [0, width], z in [0, height].
    """

    length: float
    width: float
    height: float
    wall_color: str = "black"

    def __post_init__(self) -> None:
        for name, value in (
            ("length", self.length),
            ("width", self.width),
            ("height", self.height),
        ):
            if value <= 0:
                raise InvalidDimensionError(f"Room {name} must be positive, got {value}")

    def render(self, ax: Axes3D) -> None:
        vertices = box_vertices(0, 0, 0, self.length, self.width, self.height)
        add_segments(ax, box_edges(vertices), color=self.wall_color, linewidth=1.5)
