"""A bookshelf with a configurable number of shelves."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from virtual_room_builder.errors import InvalidDimensionError
from virtual_room_builder.furniture.base import Furniture
from virtual_room_builder.geometry import Bounds, Direction, FloatArray, box_edges, box_vertices

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D


@dataclass
class Bookshelf(Furniture):
    """A bookshelf anchored at (x, y), facing ``direction``.

    North/south run the case length along x with depth toward -y/+y.
    East/west run the case length along y with depth toward +x/-x.
    """

    length: float = 5.0
    height: float = 3.0
    depth: float = 1.0
    num_shelves: int = 4
    shelf_color: str = "sienna"

    def _validate_dimensions(self) -> None:
        self._require_positive(length=self.length, height=self.height, depth=self.depth)
        if self.num_shelves < 0:
            raise InvalidDimensionError(
                f"Bookshelf.num_shelves must be >= 0, got {self.num_shelves}"
            )

    def _corner_and_extents(self) -> tuple[float, float, float, float]:
        """Return (corner_x, corner_y, dx, dy) for box_vertices, local to (x, y)."""
        if self.direction is Direction.NORTH:
            return 0.0, -self.depth, self.length, self.depth
        if self.direction is Direction.SOUTH:
            return 0.0, 0.0, self.length, self.depth
        if self.direction is Direction.EAST:
            return 0.0, 0.0, self.depth, self.length
        return -self.depth, 0.0, self.depth, self.length  # WEST

    def _case_vertices(self) -> FloatArray:
        cx, cy, dx, dy = self._corner_and_extents()
        return box_vertices(self.x + cx, self.y + cy, 0.0, dx, dy, self.height)

    def _shelf_vertices(self, z: float) -> FloatArray:
        """The four corners of one flat shelf at height z, as a closed loop."""
        cx, cy, dx, dy = self._corner_and_extents()
        x0, y0 = self.x + cx, self.y + cy
        return np.array(
            [
                [x0, y0, z],
                [x0 + dx, y0, z],
                [x0 + dx, y0 + dy, z],
                [x0, y0 + dy, z],
            ],
            dtype=np.float64,
        )

    def bounds(self) -> Bounds:
        return Bounds.from_vertices(self._case_vertices())

    def render(self, ax: Axes3D) -> None:
        case = self._case_vertices()
        self._draw_edges(ax, box_edges(case), self.color, linewidth=1.2)

        if self.num_shelves == 0:
            return

        shelf_heights = np.linspace(0, self.height, self.num_shelves + 2)[1:-1]
        for shelf_z in shelf_heights:
            shelf = self._shelf_vertices(float(shelf_z))
            edges = [
                (shelf[0], shelf[1]),
                (shelf[1], shelf[2]),
                (shelf[2], shelf[3]),
                (shelf[3], shelf[0]),
            ]
            self._draw_edges(ax, edges, self.shelf_color, linewidth=1.2)
