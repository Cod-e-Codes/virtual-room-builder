from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import pytest

from virtual_room_builder.errors import InvalidDimensionError
from virtual_room_builder.room import Room


def test_room_valid_dimensions() -> None:
    room = Room(length=10, width=8, height=3)
    assert room.length == 10
    assert room.width == 8
    assert room.height == 3


@pytest.mark.parametrize("field_name", ["length", "width", "height"])
def test_room_rejects_zero_dimension(field_name: str) -> None:
    kwargs = {"length": 10.0, "width": 8.0, "height": 3.0}
    kwargs[field_name] = 0.0
    with pytest.raises(InvalidDimensionError):
        Room(**kwargs)


@pytest.mark.parametrize("field_name", ["length", "width", "height"])
def test_room_rejects_negative_dimension(field_name: str) -> None:
    kwargs = {"length": 10.0, "width": 8.0, "height": 3.0}
    kwargs[field_name] = -1.0
    with pytest.raises(InvalidDimensionError):
        Room(**kwargs)


def test_room_render_does_not_raise() -> None:
    import matplotlib.pyplot as plt

    room = Room(length=10, width=8, height=3)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    room.render(ax)
    plt.close(fig)
