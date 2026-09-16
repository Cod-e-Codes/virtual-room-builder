from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import pytest

from virtual_room_builder.door import Door
from virtual_room_builder.errors import OutOfBoundsError
from virtual_room_builder.examples import default_scene
from virtual_room_builder.furniture.chair import Chair
from virtual_room_builder.room import Room
from virtual_room_builder.scene import Scene


def test_default_scene_validates_cleanly() -> None:
    scene = default_scene()
    scene.validate()


def test_default_scene_renders_to_figure() -> None:
    fig = default_scene().figure()
    assert fig is not None
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_scene_validate_catches_out_of_bounds_furniture() -> None:
    scene = Scene(room=Room(length=5, width=5, height=3))
    scene.add(Chair(x=100, y=100))
    with pytest.raises(OutOfBoundsError):
        scene.validate()


def test_scene_validate_catches_out_of_bounds_door() -> None:
    scene = Scene(room=Room(length=5, width=5, height=3))
    scene.add_door(Door(x=100, y=0, height=2))
    with pytest.raises(OutOfBoundsError):
        scene.validate()


def test_scene_add_returns_self_for_chaining() -> None:
    scene = Scene(room=Room(length=10, width=10, height=3))
    result = scene.add(Chair(x=1, y=1))
    assert result is scene


def test_figure_raises_on_out_of_bounds_furniture() -> None:
    scene = Scene(room=Room(length=5, width=5, height=3))
    scene.add(Chair(x=100, y=100))
    with pytest.raises(OutOfBoundsError):
        scene.figure()

