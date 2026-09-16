"""Shared base for all furniture items."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from virtual_room_builder.errors import InvalidDimensionError, OutOfBoundsError
from virtual_room_builder.geometry import Bounds, Direction, FloatArray

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D


@dataclass
class Furniture(ABC):
    """Common fields and behavior for every furniture item.

    x, y is the anchor point on the floor in room coordinates.
    direction is the compass direction the item faces.

    All items are drawn as wireframes. matplotlib's Axes3D does not
    depth-sort filled faces reliably against other artists, so solid
    fills produce z-fighting from most camera angles.
    """

    x: float
    y: float
    direction: Direction = Direction.NORTH
    color: str = "black"

    def __post_init__(self) -> None:
        if isinstance(self.direction, str):
            self.direction = Direction(self.direction)
        self._validate_dimensions()

    def _validate_dimensions(self) -> None:
        """Subclasses override to check their own size fields are positive."""
        return None

    def _require_positive(self, **fields: float) -> None:
        for name, value in fields.items():
            if value <= 0:
                raise InvalidDimensionError(
                    f"{type(self).__name__}.{name} must be positive, got {value}"
                )

    @abstractmethod
    def bounds(self) -> Bounds:
        """Axis-aligned bounds in room coordinates. Used for fit checks."""

    def check_fits(self, room_length: float, room_width: float, room_height: float) -> None:
        bounds = self.bounds()
        if not bounds.fits_within(room_length, room_width, room_height):
            raise OutOfBoundsError(
                f"{type(self).__name__} at ({self.x}, {self.y}) facing "
                f"{self.direction.value} does not fit in a "
                f"{room_length}x{room_width}x{room_height} room "
                f"(item spans x[{bounds.min_x:.2f}, {bounds.max_x:.2f}], "
                f"y[{bounds.min_y:.2f}, {bounds.max_y:.2f}], "
                f"z[{bounds.min_z:.2f}, {bounds.max_z:.2f}])"
            )

    @abstractmethod
    def render(self, ax: Axes3D) -> None:
        """Draw this item onto the 3D axes."""

    def _draw_edges(
        self,
        ax: Axes3D,
        edges: list[tuple[FloatArray, FloatArray]],
        color: str,
        linewidth: float = 1.0,
    ) -> None:
        for start, end in edges:
            ax.plot(*zip(start, end, strict=True), color=color, linewidth=linewidth)
