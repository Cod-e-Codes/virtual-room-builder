from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import pytest

from virtual_room_builder.door import Door
from virtual_room_builder.errors import (
    InvalidDimensionError,
    InvalidPlacementError,
    OutOfBoundsError,
)


def test_door_horizontal_bounds() -> None:
    door = Door(x=5, y=0, height=2, width=2, orientation="horizontal")
    bounds = door.bounds()
    assert bounds.min_x == 5
    assert bounds.max_x == 7
    assert bounds.min_y == 0
    assert bounds.max_y == 0


def test_door_vertical_bounds() -> None:
    door = Door(x=0, y=5, height=2, width=2, orientation="vertical")
    bounds = door.bounds()
    assert bounds.min_x == 0
    assert bounds.max_x == 0
    assert bounds.min_y == 5
    assert bounds.max_y == 7


def test_door_rejects_invalid_orientation() -> None:
    with pytest.raises(ValueError):
        Door(x=0, y=0, height=2, orientation="diagonal")


def test_door_rejects_zero_height() -> None:
    with pytest.raises(InvalidDimensionError):
        Door(x=0, y=0, height=0)


def test_door_rejects_zero_width() -> None:
    with pytest.raises(InvalidDimensionError):
        Door(x=0, y=0, height=2, width=0)


def test_door_check_fits_passes_when_inside() -> None:
    door = Door(x=5, y=0, height=2, width=2, orientation="horizontal")
    door.check_fits(15, 15, 4)


def test_door_check_fits_raises_when_outside() -> None:
    door = Door(x=14, y=0, height=2, width=2, orientation="horizontal")
    with pytest.raises(OutOfBoundsError):
        door.check_fits(15, 15, 4)


def test_door_check_fits_raises_when_too_tall() -> None:
    door = Door(x=5, y=0, height=10, width=2, orientation="horizontal")
    with pytest.raises(OutOfBoundsError):
        door.check_fits(15, 15, 4)


def test_door_render_does_not_raise() -> None:
    import matplotlib.pyplot as plt

    door = Door(x=5, y=0, height=2, width=2, orientation="horizontal")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    door.render(ax)
    plt.close(fig)


def test_horizontal_door_rejects_off_wall() -> None:
    door = Door(x=5, y=5, height=2, width=2, orientation="horizontal")
    with pytest.raises(InvalidPlacementError):
        door.check_fits(15, 15, 4)


def test_vertical_door_rejects_off_wall() -> None:
    door = Door(x=5, y=5, height=2, width=2, orientation="vertical")
    with pytest.raises(InvalidPlacementError):
        door.check_fits(15, 15, 4)


def test_horizontal_door_on_north_wall_passes() -> None:
    door = Door(x=5, y=15, height=2, width=2, orientation="horizontal")
    door.check_fits(15, 15, 4)


def test_vertical_door_on_east_wall_passes() -> None:
    door = Door(x=15, y=5, height=2, width=2, orientation="vertical")
    door.check_fits(15, 15, 4)

