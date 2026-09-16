"""Draw wireframe segments onto 3D axes."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import numpy as np
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from virtual_room_builder.geometry import FloatArray

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D

# mplot3d assigns one depth to each collection. Keep pieces short so a wall
# edge that runs from the camera to the far corner does not sort as a unit.
_MAX_SEGMENT_LENGTH = 1.0


class _ViewDepthLine3DCollection(Line3DCollection):  # type: ignore[misc]
    """Line collection whose sort depth is the farther floor-plan endpoint.

    Tall wall pieces then share depth with the floor they stand on, so
    receding back-wall and back-floor edges stay behind objects in the room.
    Matplotlib's default uses the closest projected point, which pulls tall
    back-wall pieces in front when the camera is elevated.
    """

    def do_3d_projection(self) -> float:
        super().do_3d_projection()
        pts = np.asarray(self._segments3d[0], dtype=np.float64)
        _, _, tzs = proj3d.proj_transform(
            pts[:, 0],
            pts[:, 1],
            np.zeros(len(pts)),
            self.axes.M,
        )
        return float(np.max(tzs))


def _split_edge(start: FloatArray, end: FloatArray) -> list[tuple[FloatArray, FloatArray]]:
    start_a = np.asarray(start, dtype=np.float64)
    end_a = np.asarray(end, dtype=np.float64)
    span = end_a - start_a
    length = float(np.linalg.norm(span))
    if length <= _MAX_SEGMENT_LENGTH:
        return [(start_a, end_a)]
    n = int(np.ceil(length / _MAX_SEGMENT_LENGTH))
    ts = np.linspace(0.0, 1.0, n + 1)
    pts = start_a + np.outer(ts, span)
    return [(pts[i], pts[i + 1]) for i in range(n)]


def add_segments(
    ax: Axes3D,
    edges: Sequence[tuple[FloatArray, FloatArray]],
    *,
    color: str,
    linewidth: float = 1.0,
) -> None:
    """Add each edge piece as a Line3DCollection sorted by floor-plan depth."""
    for start, end in edges:
        for piece_start, piece_end in _split_edge(start, end):
            ax.add_collection3d(
                _ViewDepthLine3DCollection(
                    [np.asarray([piece_start, piece_end], dtype=np.float64)],
                    colors=color,
                    linewidths=linewidth,
                )
            )
