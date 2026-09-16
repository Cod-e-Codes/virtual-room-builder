"""Exception hierarchy for the virtual room builder."""

from __future__ import annotations


class VirtualRoomBuilderError(Exception):
    """Base class for all errors raised by this package."""


class InvalidDimensionError(VirtualRoomBuilderError):
    """A length, width, height, or other size was not positive."""


class OutOfBoundsError(VirtualRoomBuilderError):
    """An item does not fit inside the room's bounds."""


class InvalidPlacementError(VirtualRoomBuilderError):
    """A door is off a wall, or a floorplan connection or layout is invalid."""
