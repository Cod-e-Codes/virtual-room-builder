"""A rectangular table with a top and four legs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from virtual_room_builder.furniture.base import Furniture
from virtual_room_builder.geometry import Bounds, FloatArray, rotate_xy

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D


@dataclass
class Table(Furniture):
    """A table anchored at (x, y).

    x, y is the local origin corner. direction rotates the table about that
    anchor. Drawn as a single top rectangle and four vertical leg lines.
    """

    length: float = 4.0
    width: float = 4.0
    top_height: float = 0.75

    def _validate_dimensions(self) -> None:
        self._require_positive(
            length=self.length,
            width=self.width,
            top_height=self.top_height,
        )

    def _top_corners(self) -> FloatArray:
        """Four corners of the table top at z = top_height, in local coords."""
        return np.array(
            [
                [0.0, 0.0, self.top_height],
                [self.length, 0.0, self.top_height],
                [self.length, self.width, self.top_height],
                [0.0, self.width, self.top_height],
            ],
            dtype=np.float64,
        )

    def _placed_top(self) -> FloatArray:
        v = self._top_corners()
        v = rotate_xy(v, self.direction.rotation_degrees, origin=(0.0, 0.0))
        v = v.copy()
        v[:, 0] += self.x
        v[:, 1] += self.y
        return v

    def bounds(self) -> Bounds:
        top = self._placed_top()
        floor = top.copy()
        floor[:, 2] = 0.0
        return Bounds.from_vertices(np.vstack([top, floor]))

    def render(self, ax: Axes3D, origin: tuple[float, float] = (0.0, 0.0)) -> None:
        top = self._placed_top()
        top_edges = [
            (top[0], top[1]),
            (top[1], top[2]),
            (top[2], top[3]),
            (top[3], top[0]),
        ]
        self._draw_edges(ax, top_edges, self.color, linewidth=1.5, origin=origin)

        legs = []
        for corner in top:
            bottom = corner.copy()
            bottom[2] = 0.0
            legs.append((bottom, corner))
        self._draw_edges(ax, legs, self.color, linewidth=1.2, origin=origin)
