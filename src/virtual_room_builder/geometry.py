"""Shared geometry primitives.

Shapes are typically built facing north and rotated into place with
rotate_xy when a direction is needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]

_BOX_EDGE_INDICES: tuple[tuple[int, int], ...] = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
)


class Direction(str, Enum):
    """Compass direction a piece of furniture faces."""

    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

    @property
    def rotation_degrees(self) -> float:
        # Counterclockwise from north: west is +90, east is +270.
        return {
            Direction.NORTH: 0.0,
            Direction.WEST: 90.0,
            Direction.SOUTH: 180.0,
            Direction.EAST: 270.0,
        }[self]


def rotate_xy(points: FloatArray, degrees: float, origin: tuple[float, float]) -> FloatArray:
    """Rotate points around the z-axis about ``origin`` in the xy-plane."""
    if points.shape[-1] != 3:
        raise ValueError("rotate_xy expects Nx3 points (x, y, z)")

    theta = np.radians(degrees)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    rotation = np.array([[cos_t, -sin_t], [sin_t, cos_t]])

    ox, oy = origin
    rotated = points.copy()
    xy = points[:, :2] - np.array([ox, oy])
    rotated[:, :2] = xy @ rotation.T + np.array([ox, oy])
    return np.asarray(rotated, dtype=np.float64)


def box_vertices(
    x: float, y: float, z: float, dx: float, dy: float, dz: float
) -> FloatArray:
    """Axis-aligned box with (x, y, z) as the corner nearest the origin."""
    return np.array(
        [
            [x, y, z],
            [x + dx, y, z],
            [x + dx, y + dy, z],
            [x, y + dy, z],
            [x, y, z + dz],
            [x + dx, y, z + dz],
            [x + dx, y + dy, z + dz],
            [x, y + dy, z + dz],
        ],
        dtype=np.float64,
    )


def box_edges(vertices: FloatArray) -> list[tuple[FloatArray, FloatArray]]:
    """The twelve edges of a box."""
    return [(vertices[i], vertices[j]) for i, j in _BOX_EDGE_INDICES]


@dataclass(frozen=True)
class Bounds:
    """Axis-aligned bounding box in room coordinates."""

    min_x: float
    max_x: float
    min_y: float
    max_y: float
    min_z: float
    max_z: float

    def fits_within(self, room_length: float, room_width: float, room_height: float) -> bool:
        return (
            0 <= self.min_x
            and self.max_x <= room_length
            and 0 <= self.min_y
            and self.max_y <= room_width
            and 0 <= self.min_z
            and self.max_z <= room_height
        )

    @classmethod
    def from_vertices(cls, vertices: FloatArray) -> Bounds:
        return cls(
            min_x=float(vertices[:, 0].min()),
            max_x=float(vertices[:, 0].max()),
            min_y=float(vertices[:, 1].min()),
            max_y=float(vertices[:, 1].max()),
            min_z=float(vertices[:, 2].min()),
            max_z=float(vertices[:, 2].max()),
        )
