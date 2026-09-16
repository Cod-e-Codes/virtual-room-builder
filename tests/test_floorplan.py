from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from virtual_room_builder.door import Door
from virtual_room_builder.errors import InvalidPlacementError
from virtual_room_builder.examples import default_floorplan
from virtual_room_builder.floorplan import FloorPlan
from virtual_room_builder.room import Room
from virtual_room_builder.scene import Scene


def _line_collections(ax) -> list[Line3DCollection]:
    return [c for c in ax.collections if isinstance(c, Line3DCollection)]


def _segment3d(coll: Line3DCollection) -> np.ndarray:
    return np.asarray(coll._segments3d[0], dtype=np.float64)


def _west_join(*, living_y: float = 4.0, kitchen_y: float = 4.0) -> FloorPlan:
    living = Scene(room=Room(length=15, width=12, height=4))
    living.add_door(
        Door(x=0, y=living_y, height=2, width=2, orientation="vertical", name="to_kitchen")
    )
    kitchen = Scene(room=Room(length=10, width=12, height=4))
    kitchen.add_door(
        Door(x=10, y=kitchen_y, height=2, width=2, orientation="vertical", name="to_living")
    )
    plan = FloorPlan()
    plan.add("living", living)
    plan.add("kitchen", kitchen)
    plan.connect("living", "to_kitchen", "kitchen", "to_living")
    return plan


def _north_join(*, living_x: float = 2.0, attic_x: float = 2.0) -> FloorPlan:
    living = Scene(room=Room(length=10, width=8, height=3))
    living.add_door(
        Door(x=living_x, y=8, height=2, width=2, orientation="horizontal", name="to_attic")
    )
    attic = Scene(room=Room(length=10, width=6, height=3))
    attic.add_door(
        Door(x=attic_x, y=0, height=2, width=2, orientation="horizontal", name="to_living")
    )
    plan = FloorPlan()
    plan.add("living", living)
    plan.add("attic", attic)
    plan.connect("living", "to_attic", "attic", "to_living")
    return plan


def test_west_join_places_kitchen_at_negative_x() -> None:
    plan = _west_join(living_y=4.0, kitchen_y=4.0)
    assert plan.origins() == {"living": (0.0, 0.0), "kitchen": (-10.0, 0.0)}


def test_west_join_offsets_y_when_door_anchors_differ() -> None:
    plan = _west_join(living_y=4.0, kitchen_y=1.0)
    assert plan.origins()["kitchen"] == (-10.0, 3.0)


def test_north_join_places_attic_at_parent_width() -> None:
    plan = _north_join(living_x=2.0, attic_x=2.0)
    assert plan.origins() == {"living": (0.0, 0.0), "attic": (0.0, 8.0)}


def test_north_join_offsets_x_when_door_anchors_differ() -> None:
    plan = _north_join(living_x=3.0, attic_x=1.0)
    assert plan.origins()["attic"] == (2.0, 8.0)


def test_width_mismatch_raises() -> None:
    living = Scene(room=Room(length=10, width=10, height=3))
    living.add_door(Door(x=10, y=2, height=2, width=2, orientation="vertical", name="to_b"))
    other = Scene(room=Room(length=8, width=10, height=3))
    other.add_door(Door(x=0, y=2, height=2, width=3, orientation="vertical", name="to_a"))
    plan = FloorPlan()
    plan.add("a", living)
    plan.add("b", other)
    plan.connect("a", "to_b", "b", "to_a")
    with pytest.raises(InvalidPlacementError, match="width"):
        plan.origins()


def test_height_mismatch_raises() -> None:
    living = Scene(room=Room(length=10, width=10, height=3))
    living.add_door(Door(x=10, y=2, height=2, width=2, orientation="vertical", name="to_b"))
    other = Scene(room=Room(length=8, width=10, height=3))
    other.add_door(Door(x=0, y=2, height=3, width=2, orientation="vertical", name="to_a"))
    plan = FloorPlan()
    plan.add("a", living)
    plan.add("b", other)
    plan.connect("a", "to_b", "b", "to_a")
    with pytest.raises(InvalidPlacementError, match="height"):
        plan.origins()


def test_same_wall_pair_raises() -> None:
    a = Scene(room=Room(length=10, width=10, height=3))
    a.add_door(Door(x=2, y=0, height=2, width=2, orientation="horizontal", name="south"))
    b = Scene(room=Room(length=10, width=10, height=3))
    b.add_door(Door(x=2, y=0, height=2, width=2, orientation="horizontal", name="south"))
    plan = FloorPlan()
    plan.add("a", a)
    plan.add("b", b)
    plan.connect("a", "south", "b", "south")
    with pytest.raises(InvalidPlacementError, match="opposite"):
        plan.origins()


def test_unknown_door_name_raises() -> None:
    plan = _west_join()
    plan.connect("living", "missing", "kitchen", "to_living")
    with pytest.raises(InvalidPlacementError, match="missing"):
        plan.origins()


def test_duplicate_door_names_in_one_room_raise() -> None:
    living = Scene(room=Room(length=15, width=12, height=4))
    living.add_door(Door(x=0, y=2, height=2, width=2, orientation="vertical", name="to_kitchen"))
    living.add_door(Door(x=0, y=6, height=2, width=2, orientation="vertical", name="to_kitchen"))
    kitchen = Scene(room=Room(length=10, width=12, height=4))
    kitchen.add_door(Door(x=10, y=2, height=2, width=2, orientation="vertical", name="to_living"))
    plan = FloorPlan()
    plan.add("living", living)
    plan.add("kitchen", kitchen)
    plan.connect("living", "to_kitchen", "kitchen", "to_living")
    with pytest.raises(InvalidPlacementError, match="duplicate"):
        plan.origins()


def test_disconnected_room_raises() -> None:
    plan = _west_join()
    extra = Scene(room=Room(length=5, width=5, height=3))
    extra.add_door(Door(x=0, y=1, height=2, width=2, orientation="vertical", name="unused"))
    plan.add("spare", extra)
    with pytest.raises(InvalidPlacementError, match="disconnected"):
        plan.origins()


def test_inconsistent_cycle_raises() -> None:
    a = Scene(room=Room(length=10, width=10, height=3))
    a.add_door(Door(x=10, y=0, height=2, width=2, orientation="vertical", name="east"))
    a.add_door(Door(x=0, y=10, height=2, width=2, orientation="horizontal", name="north"))
    b = Scene(room=Room(length=10, width=10, height=3))
    b.add_door(Door(x=0, y=0, height=2, width=2, orientation="vertical", name="west"))
    b.add_door(Door(x=0, y=0, height=2, width=2, orientation="horizontal", name="south"))
    plan = FloorPlan()
    plan.add("a", a)
    plan.add("b", b)
    plan.connect("a", "east", "b", "west")
    plan.connect("a", "north", "b", "south")
    with pytest.raises(InvalidPlacementError, match="disagrees"):
        plan.origins()


def test_interior_overlap_raises() -> None:
    a = Scene(room=Room(length=10, width=20, height=3))
    a.add_door(Door(x=10, y=0, height=2, width=2, orientation="vertical", name="to_b"))
    a.add_door(Door(x=10, y=5, height=2, width=2, orientation="vertical", name="to_c"))
    b = Scene(room=Room(length=10, width=10, height=3))
    b.add_door(Door(x=0, y=0, height=2, width=2, orientation="vertical", name="to_a"))
    c = Scene(room=Room(length=10, width=10, height=3))
    c.add_door(Door(x=0, y=0, height=2, width=2, orientation="vertical", name="to_a"))
    plan = FloorPlan()
    plan.add("a", a)
    plan.add("b", b)
    plan.add("c", c)
    plan.connect("a", "to_b", "b", "to_a")
    plan.connect("a", "to_c", "c", "to_a")
    with pytest.raises(InvalidPlacementError, match="overlapping"):
        plan.validate()


def test_adjacent_rooms_do_not_count_as_overlap() -> None:
    plan = _west_join()
    plan.validate()
    assert plan.origins()["kitchen"][0] + 10.0 == plan.origins()["living"][0]


def test_figure_axis_limits_are_union_of_translated_rooms() -> None:
    plan = _west_join()
    fig = plan.figure()
    ax = fig.axes[0]
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    zlim = ax.get_zlim()
    assert float(xlim[0]) == -10.0
    assert float(xlim[1]) == 15.0
    assert float(ylim[0]) == 0.0
    assert float(ylim[1]) == 12.0
    assert float(zlim[0]) == 0.0
    assert float(zlim[1]) == 4.0

    west_kitchen = False
    for coll in _line_collections(ax):
        pts = _segment3d(coll)
        if np.all(pts[:, 0] == -10.0):
            west_kitchen = True
            break
    assert west_kitchen
    nx, ny, nz = (float(v) for v in ax.get_box_aspect())
    assert math.isclose(nx * 12.0, ny * 25.0, rel_tol=0.0, abs_tol=1e-9)
    assert math.isclose(nx * 15.0, nz * 25.0, rel_tol=0.0, abs_tol=1e-9)
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_default_floorplan_origins() -> None:
    plan = default_floorplan()
    assert plan.origins() == {
        "living": (0.0, 0.0),
        "kitchen": (-12.0, 0.0),
        "bedroom": (14.0, 0.0),
        "dining": (0.0, 14.0),
        "study": (-12.0, 14.0),
        "guest": (14.0, 14.0),
    }
    fig = plan.figure()
    ax = fig.axes[0]
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    zlim = ax.get_zlim()
    assert float(xlim[0]) == -12.0
    assert float(xlim[1]) == 26.0
    assert float(ylim[0]) == 0.0
    assert float(ylim[1]) == 24.0
    assert float(zlim[0]) == 0.0
    assert float(zlim[1]) == 4.0
    nx, ny, nz = (float(v) for v in ax.get_box_aspect())
    assert math.isclose(nx * 24.0, ny * 38.0, rel_tol=0.0, abs_tol=1e-9)
    assert math.isclose(nx * 14.0, nz * 38.0, rel_tol=0.0, abs_tol=1e-9)
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_z_box_uses_first_room_floor_side() -> None:
    assert default_floorplan()._z_box(4.0) == 14.0
    assert _west_join()._z_box(4.0) == 15.0
