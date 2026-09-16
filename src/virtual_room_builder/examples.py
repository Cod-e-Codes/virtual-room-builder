"""Example scenes."""

from __future__ import annotations

from virtual_room_builder import (
    Bookshelf,
    Chair,
    Couch,
    Direction,
    Door,
    Lamp,
    Room,
    Scene,
    Table,
)


def default_scene() -> Scene:
    """A sample 15x15x4 room with doors, chairs, table, lamps, bookshelves, and a couch."""
    scene = Scene(room=Room(length=15, width=15, height=4))

    scene.add_door(Door(x=5, y=0, height=2, orientation="horizontal"))
    scene.add_door(Door(x=0, y=5, height=2, orientation="vertical"))

    scene.add(Chair(x=7, y=5, direction=Direction.NORTH, color="black"))
    scene.add(Chair(x=7, y=9, direction=Direction.SOUTH, color="black"))
    scene.add(Chair(x=5, y=7, direction=Direction.EAST, color="black"))
    scene.add(Chair(x=9, y=8, direction=Direction.WEST, color="black"))

    scene.add(Table(x=5, y=5.5, top_height=0.75, color="peru"))

    scene.add(Lamp(x=0, y=14, height=1, color="orange"))
    scene.add(Lamp(x=14, y=14, height=2, color="orange"))

    scene.add(
        Bookshelf(
            x=2,
            y=14,
            height=3,
            num_shelves=4,
            color="sienna",
            shelf_color="black",
            direction=Direction.SOUTH,
        )
    )
    scene.add(
        Bookshelf(
            x=8,
            y=14,
            height=2,
            num_shelves=2,
            color="saddlebrown",
            shelf_color="tan",
            direction=Direction.SOUTH,
        )
    )

    scene.add(
        Couch(
            x=15,
            y=1,
            direction=Direction.WEST,
            length=7,
            depth=3,
            color="green",
        )
    )

    return scene
