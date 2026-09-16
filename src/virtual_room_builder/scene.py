"""Compose a room and its furniture into a renderable scene."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from virtual_room_builder.door import Door
from virtual_room_builder.furniture.base import Furniture
from virtual_room_builder.room import Room

if TYPE_CHECKING:
    from matplotlib.figure import Figure
    from mpl_toolkits.mplot3d import Axes3D


@dataclass
class Scene:
    """A room, its doors, and its furniture, ready to validate and render."""

    room: Room
    doors: list[Door] = field(default_factory=list)
    furniture: list[Furniture] = field(default_factory=list)

    def add_door(self, door: Door) -> Scene:
        self.doors.append(door)
        return self

    def add(self, item: Furniture) -> Scene:
        self.furniture.append(item)
        return self

    def validate(self) -> None:
        """Raise if any item does not fit or is not validly placed.

        Checks room containment for furniture and doors, and wall attachment
        for doors. Does not detect pairwise overlap between items.
        """
        for item in self.furniture:
            item.check_fits(self.room.length, self.room.width, self.room.height)
        for door in self.doors:
            door.check_fits(self.room.length, self.room.width, self.room.height)

    def render(self, ax: Axes3D) -> None:
        """Draw the scene onto an existing axes without validating first.

        Call validate() or figure() when you need containment and placement
        checks before drawing.
        """
        self.room.render(ax)
        for door in self.doors:
            door.render(ax)
        for item in self.furniture:
            item.render(ax)

        ax.set_xlim([0, self.room.length])
        ax.set_ylim([0, self.room.width])
        ax.set_zlim([0, self.room.height])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

    def figure(self) -> Figure:
        """Validate placement then build a matplotlib figure of the scene."""
        self.validate()
        import matplotlib.pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        self.render(ax)
        return fig
