"""Join scenes at named, opposite-wall doors into a floorplan."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from virtual_room_builder.door import Door
from virtual_room_builder.errors import InvalidPlacementError
from virtual_room_builder.scene import Scene

if TYPE_CHECKING:
    from matplotlib.figure import Figure
    from mpl_toolkits.mplot3d import Axes3D

_OPPOSITE = {
    "south": "north",
    "north": "south",
    "west": "east",
    "east": "west",
}

_Connection = tuple[str, str, str, str]

# Scene.figure puts a room in a cubic axes box. A 15x15x4 room is therefore
# drawn with Z about 15/4 of true scale. FloorPlan uses the first room's
# longer floor side the same way so ceilings are not pancake-flat or cube-tall.


@dataclass
class FloorPlan:
    """Named rooms joined by shared doors, laid out in world XY."""

    rooms: dict[str, Scene] = field(default_factory=dict)
    _connections: list[_Connection] = field(default_factory=list)

    def add(self, name: str, scene: Scene) -> FloorPlan:
        if name in self.rooms:
            raise InvalidPlacementError(f"Room {name!r} is already on the floorplan")
        self.rooms[name] = scene
        return self

    def connect(self, room_a: str, door_a: str, room_b: str, door_b: str) -> FloorPlan:
        if room_a == room_b:
            raise InvalidPlacementError(f"Cannot connect room {room_a!r} to itself")
        if room_a not in self.rooms:
            raise InvalidPlacementError(f"Unknown room {room_a!r}")
        if room_b not in self.rooms:
            raise InvalidPlacementError(f"Unknown room {room_b!r}")
        self._connections.append((room_a, door_a, room_b, door_b))
        return self

    def origins(self) -> dict[str, tuple[float, float]]:
        """World origin of each room, first added room at (0, 0)."""
        return self._layout()

    def validate(self) -> None:
        """Raise if any room, door pairing, graph, or overlap is invalid."""
        if not self.rooms:
            raise InvalidPlacementError("Floorplan has no rooms")
        for scene in self.rooms.values():
            scene.validate()
        self._named_doors_by_room()
        origins = self._layout()
        self._check_overlap(origins)

    def render(self, ax: Axes3D) -> None:
        """Draw every room at its laid-out origin without validating first."""
        origins = self._layout()
        for name, scene in self.rooms.items():
            scene.render(ax, origin=origins[name], fit_axes=False)

        min_x, max_x, min_y, max_y, max_z = self._world_bounds(origins)
        dx = max_x - min_x
        dy = max_y - min_y
        ax.set_xlim([min_x, max_x])
        ax.set_ylim([min_y, max_y])
        ax.set_zlim([0, max_z])
        ax.set_box_aspect((dx, dy, self._z_box(max_z)))
        ax.set_zticks([0, max_z / 2, max_z])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

    def figure(self) -> Figure:
        """Validate placement then build a matplotlib figure of the floorplan."""
        self.validate()
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=(9, 7))
        ax = fig.add_subplot(111, projection="3d")
        self.render(ax)
        ax.view_init(elev=30, azim=-60)
        return fig

    def _z_box(self, max_z: float) -> float:
        first = next(iter(self.rooms.values()))
        return max(first.room.length, first.room.width, max_z)

    def _named_doors_by_room(self) -> dict[str, dict[str, Door]]:
        named: dict[str, dict[str, Door]] = {}
        for room_name, scene in self.rooms.items():
            found: dict[str, Door] = {}
            for door in scene.doors:
                if door.name is None:
                    continue
                if door.name in found:
                    raise InvalidPlacementError(
                        f"Room {room_name!r} has duplicate door name {door.name!r}"
                    )
                found[door.name] = door
            named[room_name] = found
        return named

    def _door(self, named: dict[str, dict[str, Door]], room_name: str, door_name: str) -> Door:
        doors = named[room_name]
        if door_name not in doors:
            raise InvalidPlacementError(
                f"Room {room_name!r} has no door named {door_name!r}"
            )
        return doors[door_name]

    def _check_pair(
        self,
        room_a: str,
        scene_a: Scene,
        door_a: Door,
        room_b: str,
        scene_b: Scene,
        door_b: Door,
    ) -> None:
        if door_a.orientation != door_b.orientation:
            raise InvalidPlacementError(
                f"Doors {room_a!r}/{door_a.name!r} and {room_b!r}/{door_b.name!r} "
                f"must share orientation, got {door_a.orientation!r} and {door_b.orientation!r}"
            )
        if door_a.width != door_b.width:
            raise InvalidPlacementError(
                f"Doors {room_a!r}/{door_a.name!r} and {room_b!r}/{door_b.name!r} "
                f"must share width, got {door_a.width} and {door_b.width}"
            )
        if door_a.height != door_b.height:
            raise InvalidPlacementError(
                f"Doors {room_a!r}/{door_a.name!r} and {room_b!r}/{door_b.name!r} "
                f"must share height, got {door_a.height} and {door_b.height}"
            )
        side_a = door_a.wall_side(scene_a.room.length, scene_a.room.width)
        side_b = door_b.wall_side(scene_b.room.length, scene_b.room.width)
        if _OPPOSITE[side_a] != side_b:
            raise InvalidPlacementError(
                f"Doors {room_a!r}/{door_a.name!r} ({side_a}) and "
                f"{room_b!r}/{door_b.name!r} ({side_b}) must sit on opposite walls"
            )

    def _child_origin(
        self,
        parent_origin: tuple[float, float],
        parent_door: Door,
        child_door: Door,
    ) -> tuple[float, float]:
        px, py = parent_origin
        return (px + parent_door.x - child_door.x, py + parent_door.y - child_door.y)

    def _layout(self) -> dict[str, tuple[float, float]]:
        if not self.rooms:
            return {}

        named = self._named_doors_by_room()
        adjacency: dict[str, list[tuple[str, Door, Door]]] = defaultdict(list)
        for room_a, door_a_name, room_b, door_b_name in self._connections:
            scene_a = self.rooms[room_a]
            scene_b = self.rooms[room_b]
            door_a = self._door(named, room_a, door_a_name)
            door_b = self._door(named, room_b, door_b_name)
            self._check_pair(room_a, scene_a, door_a, room_b, scene_b, door_b)
            adjacency[room_a].append((room_b, door_a, door_b))
            adjacency[room_b].append((room_a, door_b, door_a))

        root = next(iter(self.rooms))
        origins: dict[str, tuple[float, float]] = {root: (0.0, 0.0)}
        queue: deque[str] = deque([root])
        while queue:
            current = queue.popleft()
            for neighbor, parent_door, child_door in adjacency[current]:
                placed = self._child_origin(origins[current], parent_door, child_door)
                existing = origins.get(neighbor)
                if existing is None:
                    origins[neighbor] = placed
                    queue.append(neighbor)
                elif existing != placed:
                    raise InvalidPlacementError(
                        f"Room {neighbor!r} origin {placed} from {current!r} "
                        f"disagrees with already placed origin {existing}"
                    )

        missing = [name for name in self.rooms if name not in origins]
        if missing:
            raise InvalidPlacementError(
                "All rooms must be connected to the first room, "
                f"disconnected: {missing!r}"
            )
        return origins

    def _check_overlap(self, origins: dict[str, tuple[float, float]]) -> None:
        names = list(self.rooms)
        for i, name_a in enumerate(names):
            scene_a = self.rooms[name_a]
            ax, ay = origins[name_a]
            a_max_x = ax + scene_a.room.length
            a_max_y = ay + scene_a.room.width
            for name_b in names[i + 1 :]:
                scene_b = self.rooms[name_b]
                bx, by = origins[name_b]
                b_max_x = bx + scene_b.room.length
                b_max_y = by + scene_b.room.width
                if ax < b_max_x and bx < a_max_x and ay < b_max_y and by < a_max_y:
                    raise InvalidPlacementError(
                        f"Rooms {name_a!r} and {name_b!r} have overlapping interiors"
                    )

    def _world_bounds(
        self, origins: dict[str, tuple[float, float]]
    ) -> tuple[float, float, float, float, float]:
        min_x = min(origins[name][0] for name in self.rooms)
        max_x = max(origins[name][0] + self.rooms[name].room.length for name in self.rooms)
        min_y = min(origins[name][1] for name in self.rooms)
        max_y = max(origins[name][1] + self.rooms[name].room.width for name in self.rooms)
        max_z = max(scene.room.height for scene in self.rooms.values())
        return min_x, max_x, min_y, max_y, max_z
