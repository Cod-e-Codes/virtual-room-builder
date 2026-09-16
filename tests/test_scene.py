from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from virtual_room_builder.door import Door
from virtual_room_builder.errors import OutOfBoundsError
from virtual_room_builder.examples import default_scene
from virtual_room_builder.furniture.chair import Chair
from virtual_room_builder.room import Room
from virtual_room_builder.scene import Scene


def _line_collections(ax) -> list[Line3DCollection]:
    return [c for c in ax.collections if isinstance(c, Line3DCollection)]


def _segment3d(coll: Line3DCollection) -> np.ndarray:
    return np.asarray(coll._segments3d[0], dtype=np.float64)


def _linewidth(coll: Line3DCollection) -> float:
    return float(np.asarray(coll.get_linewidth(), dtype=np.float64).reshape(-1)[0])


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


def test_render_uses_view_depth_collections() -> None:
    fig = default_scene().figure()
    ax = fig.axes[0]
    assert ax.computed_zorder is True
    collections = _line_collections(ax)
    assert collections
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_near_chair_draws_in_front_of_far_chair() -> None:
    scene = Scene(room=Room(length=12, width=12, height=3))
    scene.add(Chair(x=2, y=2))
    scene.add(Chair(x=10, y=10))
    fig = scene.figure()
    ax = fig.axes[0]
    fig.canvas.draw()

    near_z: list[float] = []
    far_z: list[float] = []
    for coll in _line_collections(ax):
        pts = _segment3d(coll)
        xs, ys = pts[:, 0], pts[:, 1]
        if np.all(xs <= 2.1) and np.all(ys <= 2.1):
            near_z.append(coll.get_zorder())
        elif np.all(xs >= 8.9) and np.all(ys >= 8.9):
            far_z.append(coll.get_zorder())

    assert near_z
    assert far_z
    assert max(near_z) > max(far_z)
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_east_chair_draws_in_front_of_far_table_edges() -> None:
    fig = default_scene().figure()
    ax = fig.axes[0]
    fig.canvas.draw()

    chair_z: list[float] = []
    far_table_z: list[float] = []
    for coll in _line_collections(ax):
        pts = _segment3d(coll)
        if np.any(pts[:, 0] > 9.05) and np.all(pts[:, 0] <= 10.05) and np.all(
            (pts[:, 1] >= 6.9) & (pts[:, 1] <= 8.1)
        ):
            chair_z.append(coll.get_zorder())
        elif np.all(pts[:, 0] >= 8.4) and np.all(pts[:, 1] >= 8.4) and np.all(pts[:, 2] <= 0.8):
            far_table_z.append(coll.get_zorder())

    assert chair_z
    assert far_table_z
    assert max(chair_z) > max(far_table_z)
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_wireframe_pieces_are_at_most_unit_length() -> None:
    fig = default_scene().figure()
    ax = fig.axes[0]
    for coll in _line_collections(ax):
        pts = _segment3d(coll)
        length = float(np.linalg.norm(pts[1] - pts[0]))
        assert length <= 1.0 + 1e-9
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_northwest_lamp_draws_in_front_of_back_room_edges() -> None:
    fig = default_scene().figure()
    ax = fig.axes[0]
    fig.canvas.draw()

    lamp_z: list[float] = []
    west_floor_z: list[float] = []
    nw_vertical_z: list[float] = []
    north_floor_z: list[float] = []
    for coll in _line_collections(ax):
        pts = _segment3d(coll)
        lw = _linewidth(coll)
        if (
            lw == 1.2
            and np.all(pts[:, 0] <= 1.05)
            and np.all(pts[:, 1] >= 13.9)
            and np.all(pts[:, 2] <= 1.05)
        ):
            lamp_z.append(coll.get_zorder())
        if lw != 1.5:
            continue
        on_west = np.all(np.abs(pts[:, 0]) <= 0.05)
        on_north = np.all(np.abs(pts[:, 1] - 15.0) <= 0.05)
        on_floor = np.all(pts[:, 2] <= 0.05)
        if on_west and on_floor and np.all(pts[:, 1] >= 13.0):
            west_floor_z.append(coll.get_zorder())
        if on_west and np.all(pts[:, 1] >= 14.4):
            nw_vertical_z.append(coll.get_zorder())
        if on_north and on_floor and np.all(pts[:, 0] <= 2.1):
            north_floor_z.append(coll.get_zorder())

    assert lamp_z
    assert west_floor_z
    assert nw_vertical_z
    assert north_floor_z
    front = max(lamp_z)
    assert front > max(west_floor_z)
    assert front > max(nw_vertical_z)
    assert front > max(north_floor_z)
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_west_door_draws_in_front_of_west_floor_and_far_wall() -> None:
    fig = default_scene().figure()
    ax = fig.axes[0]
    fig.canvas.draw()

    door_z: list[float] = []
    west_floor_z: list[float] = []
    far_wall_z: list[float] = []
    for coll in _line_collections(ax):
        pts = _segment3d(coll)
        lw = _linewidth(coll)
        on_west = np.all(np.abs(pts[:, 0]) <= 0.05)
        along_door = np.all((pts[:, 1] >= 4.9) & (pts[:, 1] <= 7.1))
        if on_west and along_door and np.all(pts[:, 2] <= 2.05) and lw == 2.0:
            door_z.append(coll.get_zorder())
        elif on_west and along_door and np.all(pts[:, 2] <= 0.05) and lw == 1.5:
            west_floor_z.append(coll.get_zorder())
        elif on_west and np.all(pts[:, 1] >= 12.0) and lw == 1.5:
            far_wall_z.append(coll.get_zorder())

    assert door_z
    assert west_floor_z
    assert far_wall_z
    front = max(door_z)
    assert front > max(west_floor_z)
    assert front > max(far_wall_z)
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_bookshelves_draw_in_front_of_north_floor() -> None:
    fig = default_scene().figure()
    ax = fig.axes[0]
    fig.canvas.draw()

    left_shelf_z: list[float] = []
    right_shelf_z: list[float] = []
    north_floor_left_z: list[float] = []
    north_floor_right_z: list[float] = []
    for coll in _line_collections(ax):
        pts = _segment3d(coll)
        lw = _linewidth(coll)
        on_north_floor = (
            lw == 1.5
            and np.all(np.abs(pts[:, 1] - 15.0) <= 0.05)
            and np.all(pts[:, 2] <= 0.05)
        )
        if on_north_floor and np.all((pts[:, 0] >= 1.9) & (pts[:, 0] <= 7.1)):
            north_floor_left_z.append(coll.get_zorder())
        elif on_north_floor and np.all((pts[:, 0] >= 7.9) & (pts[:, 0] <= 13.1)):
            north_floor_right_z.append(coll.get_zorder())
        elif lw == 1.2 and np.all(pts[:, 1] >= 13.9):
            if np.all((pts[:, 0] >= 1.9) & (pts[:, 0] <= 7.1)):
                left_shelf_z.append(coll.get_zorder())
            elif np.all((pts[:, 0] >= 7.9) & (pts[:, 0] <= 13.1)):
                right_shelf_z.append(coll.get_zorder())

    assert left_shelf_z
    assert right_shelf_z
    assert north_floor_left_z
    assert north_floor_right_z
    assert max(left_shelf_z) > max(north_floor_left_z)
    assert max(right_shelf_z) > max(north_floor_right_z)
    import matplotlib.pyplot as plt

    plt.close(fig)

