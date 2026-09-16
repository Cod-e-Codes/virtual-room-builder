from __future__ import annotations

import numpy as np
import pytest

from virtual_room_builder.geometry import (
    Bounds,
    Direction,
    box_edges,
    box_vertices,
    rotate_xy,
)


def test_direction_rotation_degrees() -> None:
    assert Direction.NORTH.rotation_degrees == 0.0
    assert Direction.WEST.rotation_degrees == 90.0
    assert Direction.SOUTH.rotation_degrees == 180.0
    assert Direction.EAST.rotation_degrees == 270.0


def test_rotate_xy_zero_degrees_is_identity() -> None:
    points = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    rotated = rotate_xy(points, 0.0, origin=(0.0, 0.0))
    np.testing.assert_allclose(rotated, points)


def test_rotate_xy_ninety_degrees() -> None:
    points = np.array([[1.0, 0.0, 0.0]])
    rotated = rotate_xy(points, 90.0, origin=(0.0, 0.0))
    np.testing.assert_allclose(rotated, [[0.0, 1.0, 0.0]], atol=1e-10)


def test_rotate_xy_preserves_z() -> None:
    points = np.array([[1.0, 0.0, 5.0]])
    rotated = rotate_xy(points, 90.0, origin=(0.0, 0.0))
    assert rotated[0, 2] == 5.0


def test_rotate_xy_rejects_wrong_shape() -> None:
    with pytest.raises(ValueError):
        rotate_xy(np.array([[1.0, 2.0]]), 90.0, origin=(0.0, 0.0))


def test_box_vertices_shape() -> None:
    v = box_vertices(0, 0, 0, 2, 3, 4)
    assert v.shape == (8, 3)
    assert v[:, 0].max() == 2
    assert v[:, 1].max() == 3
    assert v[:, 2].max() == 4


def test_box_edges_count() -> None:
    v = box_vertices(0, 0, 0, 1, 1, 1)
    edges = box_edges(v)
    assert len(edges) == 12


def test_bounds_from_vertices() -> None:
    v = box_vertices(1, 2, 3, 4, 5, 6)
    bounds = Bounds.from_vertices(v)
    assert bounds.min_x == 1
    assert bounds.max_x == 5
    assert bounds.min_y == 2
    assert bounds.max_y == 7
    assert bounds.min_z == 3
    assert bounds.max_z == 9


def test_bounds_fits_within_true() -> None:
    bounds = Bounds(0, 5, 0, 5, 0, 5)
    assert bounds.fits_within(10, 10, 10)


def test_bounds_fits_within_false_when_exceeding() -> None:
    bounds = Bounds(0, 11, 0, 5, 0, 5)
    assert not bounds.fits_within(10, 10, 10)


def test_bounds_fits_within_false_when_negative() -> None:
    bounds = Bounds(-1, 5, 0, 5, 0, 5)
    assert not bounds.fits_within(10, 10, 10)


def test_bounds_exact_boundary_fits() -> None:
    bounds = Bounds(0, 10, 0, 10, 0, 10)
    assert bounds.fits_within(10, 10, 10)
