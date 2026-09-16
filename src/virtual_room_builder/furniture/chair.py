"""A simple four-legged chair with a seat and backrest."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from virtual_room_builder.draw import add_segments
from virtual_room_builder.furniture.base import Furniture
from virtual_room_builder.geometry import Bounds, FloatArray, rotate_xy

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D

_SEAT_HEIGHT = 0.5
_BACK_TOP = 1.0
_SIZE = 1.0

# Canonical north-facing layout relative to the anchor:
# seat occupies [0, -1] x [0, -1], backrest on the -y edge so a sitter faces +y.
# Indices 0-3 legs, 4-7 seat, 8-11 backrest top.
_LOCAL = np.array(
    [
        [0.0, 0.0, 0.0],
        [-_SIZE, 0.0, 0.0],
        [-_SIZE, -_SIZE, 0.0],
        [0.0, -_SIZE, 0.0],
        [0.0, 0.0, _SEAT_HEIGHT],
        [-_SIZE, 0.0, _SEAT_HEIGHT],
        [-_SIZE, -_SIZE, _SEAT_HEIGHT],
        [0.0, -_SIZE, _SEAT_HEIGHT],
        [0.0, 0.0, _BACK_TOP],
        [-_SIZE, 0.0, _BACK_TOP],
        [-_SIZE, -_SIZE, _BACK_TOP],
        [0.0, -_SIZE, _BACK_TOP],
    ],
    dtype=np.float64,
)

# Legs, seat rectangle, three-edge backrest (two uprights + top bar).
_CHAIR_EDGES = [
    (0, 4), (1, 5), (2, 6), (3, 7),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (7, 11), (6, 10), (10, 11),
]


@dataclass
class Chair(Furniture):
    """A chair anchored at (x, y), facing ``direction``.

    Authored facing north, then rotated into place. Seat at z=0.5,
    backrest top at z=1.0.
    """

    def _placed_vertices(self) -> FloatArray:
        rotated = rotate_xy(_LOCAL, self.direction.rotation_degrees, origin=(0.0, 0.0))
        placed = rotated.copy()
        placed[:, 0] += self.x
        placed[:, 1] += self.y
        return placed

    def bounds(self) -> Bounds:
        return Bounds.from_vertices(self._placed_vertices())

    def render(self, ax: Axes3D, origin: tuple[float, float] = (0.0, 0.0)) -> None:
        v = self._placed_vertices()
        add_segments(
            ax,
            [(v[i], v[j]) for i, j in _CHAIR_EDGES],
            color=self.color,
            linewidth=1.0,
            origin=origin,
        )
