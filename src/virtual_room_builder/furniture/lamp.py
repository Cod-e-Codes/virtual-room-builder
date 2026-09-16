"""A simple box lamp."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from virtual_room_builder.furniture.base import Furniture
from virtual_room_builder.geometry import Bounds, FloatArray, box_edges, box_vertices, rotate_xy

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D


@dataclass
class Lamp(Furniture):
    """A lamp anchored at (x, y).

    x, y is the local origin corner of the footprint. direction rotates the
    lamp about that anchor.
    """

    height: float = 1.5
    footprint: float = 1.0
    color: str = "orange"

    def _validate_dimensions(self) -> None:
        self._require_positive(height=self.height, footprint=self.footprint)

    def _vertices(self) -> FloatArray:
        local = box_vertices(0.0, 0.0, 0.0, self.footprint, self.footprint, self.height)
        rotated = rotate_xy(local, self.direction.rotation_degrees, origin=(0.0, 0.0))
        placed = rotated.copy()
        placed[:, 0] += self.x
        placed[:, 1] += self.y
        return placed

    def bounds(self) -> Bounds:
        return Bounds.from_vertices(self._vertices())

    def render(self, ax: Axes3D) -> None:
        v = self._vertices()
        self._draw_edges(ax, box_edges(v), self.color, linewidth=1.2)
