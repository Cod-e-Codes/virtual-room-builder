from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from virtual_room_builder.errors import InvalidDimensionError, OutOfBoundsError
from virtual_room_builder.furniture.bookshelf import Bookshelf
from virtual_room_builder.furniture.chair import Chair
from virtual_room_builder.furniture.couch import Couch
from virtual_room_builder.furniture.lamp import Lamp
from virtual_room_builder.furniture.table import Table
from virtual_room_builder.geometry import Direction


def _axes():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    return fig, ax


@pytest.mark.parametrize("direction", list(Direction))
def test_chair_renders_in_every_direction(direction: Direction) -> None:
    fig, ax = _axes()
    chair = Chair(x=5, y=5, direction=direction)
    chair.render(ax)
    plt.close(fig)


def test_chair_string_direction_is_coerced() -> None:
    chair = Chair(x=5, y=5, direction="south")
    assert chair.direction is Direction.SOUTH


def test_chair_rejects_invalid_direction() -> None:
    with pytest.raises(ValueError):
        Chair(x=5, y=5, direction="northwest")


def test_chair_bounds_is_one_by_one() -> None:
    chair = Chair(x=5, y=5, direction=Direction.NORTH)
    bounds = chair.bounds()
    assert bounds.max_x - bounds.min_x == pytest.approx(1.0)
    assert bounds.max_y - bounds.min_y == pytest.approx(1.0)


def test_table_rejects_non_positive_dimensions() -> None:
    with pytest.raises(InvalidDimensionError):
        Table(x=0, y=0, length=0)


def test_table_renders() -> None:
    fig, ax = _axes()
    table = Table(x=5, y=5, length=4, width=4, top_height=0.75)
    table.render(ax)
    plt.close(fig)


def test_table_bounds_matches_footprint() -> None:
    table = Table(x=5, y=5, length=4, width=3, top_height=0.75)
    bounds = table.bounds()
    assert bounds.max_x - bounds.min_x == pytest.approx(4.0)
    assert bounds.max_y - bounds.min_y == pytest.approx(3.0)


def test_lamp_rejects_zero_height() -> None:
    with pytest.raises(InvalidDimensionError):
        Lamp(x=0, y=0, height=0)


def test_lamp_renders() -> None:
    fig, ax = _axes()
    lamp = Lamp(x=0, y=0, height=1.5)
    lamp.render(ax)
    plt.close(fig)


def test_bookshelf_rejects_negative_shelves() -> None:
    with pytest.raises(InvalidDimensionError):
        Bookshelf(x=0, y=0, num_shelves=-1)


def test_bookshelf_zero_shelves_still_renders() -> None:
    fig, ax = _axes()
    shelf = Bookshelf(x=0, y=0, num_shelves=0)
    shelf.render(ax)
    plt.close(fig)


@pytest.mark.parametrize("direction", list(Direction))
def test_bookshelf_renders_in_every_direction(direction: Direction) -> None:
    fig, ax = _axes()
    shelf = Bookshelf(x=5, y=5, direction=direction, num_shelves=3)
    shelf.render(ax)
    plt.close(fig)


def test_couch_rejects_seat_taller_than_backrest() -> None:
    with pytest.raises(InvalidDimensionError):
        Couch(x=0, y=0, seat_height=5, backrest_height=3)


def test_couch_renders() -> None:
    fig, ax = _axes()
    couch = Couch(x=0, y=0, direction=Direction.NORTH)
    couch.render(ax)
    plt.close(fig)


def test_furniture_out_of_bounds_raises() -> None:
    chair = Chair(x=15.5, y=5, direction=Direction.NORTH)
    with pytest.raises(OutOfBoundsError):
        chair.check_fits(15, 15, 4)


def test_furniture_in_bounds_passes() -> None:
    chair = Chair(x=7, y=5, direction=Direction.NORTH)
    chair.check_fits(15, 15, 4)


@pytest.mark.parametrize(
    "direction,min_x,max_x,min_y,max_y",
    [
        (Direction.NORTH, 4.0, 5.0, 4.0, 5.0),
        (Direction.SOUTH, 5.0, 6.0, 5.0, 6.0),
        (Direction.EAST, 4.0, 5.0, 5.0, 6.0),
        (Direction.WEST, 5.0, 6.0, 4.0, 5.0),
    ],
)
def test_chair_rotated_bounds(
    direction: Direction, min_x: float, max_x: float, min_y: float, max_y: float
) -> None:
    chair = Chair(x=5, y=5, direction=direction)
    bounds = chair.bounds()
    assert bounds.min_x == pytest.approx(min_x)
    assert bounds.max_x == pytest.approx(max_x)
    assert bounds.min_y == pytest.approx(min_y)
    assert bounds.max_y == pytest.approx(max_y)


@pytest.mark.parametrize(
    "direction,min_x,max_x,min_y,max_y",
    [
        (Direction.NORTH, 2.0, 7.0, 4.0, 5.0),
        (Direction.SOUTH, 2.0, 7.0, 5.0, 6.0),
        (Direction.EAST, 2.0, 3.0, 5.0, 10.0),
        (Direction.WEST, 1.0, 2.0, 5.0, 10.0),
    ],
)
def test_bookshelf_rotated_bounds(
    direction: Direction, min_x: float, max_x: float, min_y: float, max_y: float
) -> None:
    shelf = Bookshelf(x=2, y=5, length=5, depth=1, direction=direction)
    bounds = shelf.bounds()
    assert bounds.min_x == pytest.approx(min_x)
    assert bounds.max_x == pytest.approx(max_x)
    assert bounds.min_y == pytest.approx(min_y)
    assert bounds.max_y == pytest.approx(max_y)


def test_couch_west_bounds_against_east_wall() -> None:
    couch = Couch(x=15, y=1, direction=Direction.WEST, length=7, depth=3)
    bounds = couch.bounds()
    assert bounds.max_x == pytest.approx(15.0)
    assert bounds.min_x == pytest.approx(12.0)
    assert bounds.min_y == pytest.approx(1.0)
    assert bounds.max_y == pytest.approx(8.0)


def test_couch_bounds_match_length_and_depth() -> None:
    couch = Couch(x=0, y=0, direction=Direction.NORTH, length=7, depth=3)
    bounds = couch.bounds()
    assert bounds.max_x - bounds.min_x == pytest.approx(7.0)
    assert bounds.max_y - bounds.min_y == pytest.approx(3.0)


@pytest.mark.parametrize(
    "direction,min_x,max_x,min_y,max_y",
    [
        (Direction.NORTH, 0.0, 2.0, 0.0, 2.0),
        (Direction.WEST, -2.0, 0.0, 0.0, 2.0),
        (Direction.SOUTH, -2.0, 0.0, -2.0, 0.0),
        (Direction.EAST, 0.0, 2.0, -2.0, 0.0),
    ],
)
def test_lamp_rotated_bounds(
    direction: Direction, min_x: float, max_x: float, min_y: float, max_y: float
) -> None:
    lamp = Lamp(x=0, y=0, footprint=2.0, direction=direction)
    bounds = lamp.bounds()
    assert bounds.min_x == pytest.approx(min_x)
    assert bounds.max_x == pytest.approx(max_x)
    assert bounds.min_y == pytest.approx(min_y)
    assert bounds.max_y == pytest.approx(max_y)


@pytest.mark.parametrize(
    "direction,min_x,max_x,min_y,max_y",
    [
        (Direction.NORTH, 5.0, 9.0, 5.0, 8.0),
        (Direction.WEST, 2.0, 5.0, 5.0, 9.0),
        (Direction.SOUTH, 1.0, 5.0, 2.0, 5.0),
        (Direction.EAST, 5.0, 8.0, 1.0, 5.0),
    ],
)
def test_table_rotated_bounds(
    direction: Direction, min_x: float, max_x: float, min_y: float, max_y: float
) -> None:
    table = Table(x=5, y=5, length=4, width=3, direction=direction)
    bounds = table.bounds()
    assert bounds.min_x == pytest.approx(min_x)
    assert bounds.max_x == pytest.approx(max_x)
    assert bounds.min_y == pytest.approx(min_y)
    assert bounds.max_y == pytest.approx(max_y)

