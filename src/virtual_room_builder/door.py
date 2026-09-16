"""A doorway rectangle on a wall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from virtual_room_builder.draw import add_segments
from virtual_room_builder.errors import (
    InvalidDimensionError,
    InvalidPlacementError,
    OutOfBoundsError,
)
from virtual_room_builder.geometry import Bounds, FloatArray

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D


@dataclass
class Door:
    """A doorway on a wall, anchored at (x, y).

    orientation "horizontal" opens along x and must sit on the south wall
    (y = 0) or the north wall (y = room width).
    orientation "vertical" opens along y and must sit on the west wall
    (x = 0) or the east wall (x = room length).
    name is the id FloorPlan.connect looks up. Unnamed doors cannot be joined.
    """

    x: float
    y: float
    height: float
    width: float = 2.0
    orientation: str = "horizontal"
    color: str = "red"
    name: str | None = None

    def __post_init__(self) -> None:
        if self.height <= 0:
            raise InvalidDimensionError(f"Door.height must be positive, got {self.height}")
        if self.width <= 0:
            raise InvalidDimensionError(f"Door.width must be positive, got {self.width}")
        if self.orientation not in ("horizontal", "vertical"):
            raise ValueError(
                f"Door.orientation must be 'horizontal' or 'vertical', got {self.orientation!r}"
            )

    def _vertices(self) -> FloatArray:
        """Four corners of the flat doorway rectangle."""
        if self.orientation == "horizontal":
            return np.array(
                [
                    [self.x, self.y, 0.0],
                    [self.x + self.width, self.y, 0.0],
                    [self.x + self.width, self.y, self.height],
                    [self.x, self.y, self.height],
                ],
                dtype=np.float64,
            )
        return np.array(
            [
                [self.x, self.y, 0.0],
                [self.x, self.y + self.width, 0.0],
                [self.x, self.y + self.width, self.height],
                [self.x, self.y, self.height],
            ],
            dtype=np.float64,
        )

    def bounds(self) -> Bounds:
        return Bounds.from_vertices(self._vertices())

    def check_fits(self, room_length: float, room_width: float, room_height: float) -> None:
        bounds = self.bounds()
        if not bounds.fits_within(room_length, room_width, room_height):
            raise OutOfBoundsError(
                f"Door at ({self.x}, {self.y}) does not fit in a "
                f"{room_length}x{room_width}x{room_height} room "
                f"(door spans x[{bounds.min_x:.2f}, {bounds.max_x:.2f}], "
                f"y[{bounds.min_y:.2f}, {bounds.max_y:.2f}], "
                f"z[{bounds.min_z:.2f}, {bounds.max_z:.2f}])"
            )
        self.wall_side(room_length, room_width)

    def wall_side(self, room_length: float, room_width: float) -> str:
        """Return south, north, west, or east for a door on that wall."""
        if self.orientation == "horizontal":
            if self.y == 0:
                return "south"
            if self.y == room_width:
                return "north"
            raise InvalidPlacementError(
                f"Horizontal door at y={self.y} must sit on the south wall "
                f"(y=0) or north wall (y={room_width})"
            )
        if self.x == 0:
            return "west"
        if self.x == room_length:
            return "east"
        raise InvalidPlacementError(
            f"Vertical door at x={self.x} must sit on the west wall "
            f"(x=0) or east wall (x={room_length})"
        )

    def render(self, ax: Axes3D, origin: tuple[float, float] = (0.0, 0.0)) -> None:
        v = self._vertices()
        add_segments(
            ax,
            [(v[0], v[1]), (v[1], v[2]), (v[2], v[3]), (v[3], v[0])],
            color=self.color,
            linewidth=2,
            origin=origin,
        )
