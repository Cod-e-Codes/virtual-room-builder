"""A couch with a backrest, seat, and two armrests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from virtual_room_builder.draw import add_segments
from virtual_room_builder.errors import InvalidDimensionError
from virtual_room_builder.furniture.base import Furniture
from virtual_room_builder.geometry import Bounds, FloatArray, rotate_xy

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D


@dataclass
class Couch(Furniture):
    """A couch anchored at (x, y), facing ``direction``.

    Authored facing north: length along x, backrest on the -y side,
    seat toward +y. Drawn as a sparse wireframe (seat outline, vertical
    backrest panel, two armrest frames) to match the chair and table style.
    """

    length: float = 7.0
    depth: float = 3.0
    backrest_height: float = 1.2
    seat_height: float = 0.5
    armrest_height: float = 0.85
    color: str = "green"

    def _validate_dimensions(self) -> None:
        self._require_positive(
            length=self.length,
            depth=self.depth,
            backrest_height=self.backrest_height,
            seat_height=self.seat_height,
            armrest_height=self.armrest_height,
        )
        if self.seat_height >= self.backrest_height:
            raise InvalidDimensionError("Couch.seat_height must be less than backrest_height")
        if self.armrest_height > self.backrest_height:
            raise InvalidDimensionError("Couch.armrest_height must not exceed backrest_height")

    def _local_vertices(self) -> FloatArray:
        """Sparse local vertices for a north-facing couch.

        Layout (indices):
          0-3   seat top rectangle (z = seat_height)
          4-5   backrest top bar (z = backrest_height) on the seat rear edge
          6-9   left armrest frame (near x=0)
          10-13 right armrest frame (near x=length)
        """
        L = self.length
        D = self.depth
        sh = self.seat_height
        bh = self.backrest_height
        ah = self.armrest_height
        # Seat occupies y in [0, D]; backrest is a vertical panel at y = 0.
        return np.array(
            [
                # 0-3 seat top
                [0.0, 0.0, sh],
                [L, 0.0, sh],
                [L, D, sh],
                [0.0, D, sh],
                # 4-5 backrest top bar (vertical panel at y=0, no depth slab)
                [0.0, 0.0, bh],
                [L, 0.0, bh],
                # 6-9 left armrest (x=0 plane): floor front, floor rear, top rear, top front
                [0.0, D, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, ah],
                [0.0, D, ah],
                # 10-13 right armrest (x=L plane)
                [L, D, 0.0],
                [L, 0.0, 0.0],
                [L, 0.0, ah],
                [L, D, ah],
            ],
            dtype=np.float64,
        )

    # Sparse edges: seat outline, vertical backrest, two arm frames.
    # Armrests are open at the floor (no bottom segment).
    _EDGES = [
        # Seat top rectangle
        (0, 1), (1, 2), (2, 3), (3, 0),
        # Backrest: top bar + two uprights from seat rear
        (4, 5), (0, 4), (1, 5),
        # Left armrest: rear upright, top, front upright
        (7, 8), (8, 9), (9, 6),
        # Right armrest: rear upright, top, front upright
        (11, 12), (12, 13), (13, 10),
    ]

    def _placed_vertices(self) -> FloatArray:
        local = self._local_vertices()
        placed = rotate_xy(local, self.direction.rotation_degrees, origin=(0.0, 0.0))
        placed = placed.copy()
        placed[:, 0] += self.x
        placed[:, 1] += self.y
        return placed

    def bounds(self) -> Bounds:
        return Bounds.from_vertices(self._placed_vertices())

    def render(self, ax: Axes3D, origin: tuple[float, float] = (0.0, 0.0)) -> None:
        v = self._placed_vertices()
        add_segments(
            ax,
            [(v[i], v[j]) for i, j in self._EDGES],
            color=self.color,
            linewidth=1.2,
            origin=origin,
        )
