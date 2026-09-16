"""Example scene and floorplan."""

from __future__ import annotations

from virtual_room_builder import (
    Bookshelf,
    Chair,
    Couch,
    Direction,
    Door,
    FloorPlan,
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


def _living_room() -> Scene:
    scene = Scene(room=Room(length=14, width=14, height=4))
    scene.add_door(Door(x=6, y=0, height=2, orientation="horizontal"))
    scene.add_door(Door(x=0, y=6, height=2, orientation="vertical", name="to_kitchen"))
    scene.add_door(Door(x=14, y=6, height=2, orientation="vertical", name="to_bedroom"))
    scene.add_door(Door(x=6, y=14, height=2, orientation="horizontal", name="to_dining"))

    scene.add(Couch(x=0.5, y=0.5, direction=Direction.NORTH, length=5, depth=3, color="green"))
    scene.add(Couch(x=14, y=9, direction=Direction.WEST, length=4, depth=3, color="green"))
    scene.add(Table(x=1.5, y=4, length=4, width=2.5, top_height=0.5, color="peru"))
    scene.add(Chair(x=3.5, y=6.5, direction=Direction.SOUTH, color="black"))
    scene.add(Chair(x=5.5, y=5.5, direction=Direction.WEST, color="black"))
    scene.add(Lamp(x=0, y=12, height=1.5, color="orange"))
    scene.add(Lamp(x=12, y=0, height=1.5, color="orange"))
    scene.add(
        Bookshelf(
            x=0,
            y=13,
            length=5,
            height=3,
            num_shelves=4,
            color="sienna",
            shelf_color="black",
            direction=Direction.SOUTH,
        )
    )
    scene.add(
        Bookshelf(
            x=9,
            y=13,
            length=2,
            height=2,
            num_shelves=2,
            color="saddlebrown",
            shelf_color="tan",
            direction=Direction.SOUTH,
        )
    )
    return scene


def _kitchen() -> Scene:
    scene = Scene(room=Room(length=12, width=14, height=4))
    scene.add_door(Door(x=12, y=6, height=2, orientation="vertical", name="to_living"))
    scene.add_door(Door(x=5, y=14, height=2, orientation="horizontal", name="to_study"))

    scene.add(
        Bookshelf(
            x=1,
            y=1,
            length=4,
            height=3,
            depth=1,
            num_shelves=3,
            color="sienna",
            shelf_color="tan",
            direction=Direction.WEST,
        )
    )
    scene.add(
        Bookshelf(
            x=1,
            y=9,
            length=4,
            height=3,
            depth=1,
            num_shelves=3,
            color="sienna",
            shelf_color="tan",
            direction=Direction.WEST,
        )
    )
    scene.add(Table(x=4, y=3, length=4, width=3, top_height=0.9, color="peru"))
    scene.add(Chair(x=6, y=3, direction=Direction.NORTH, color="black"))
    scene.add(Chair(x=6, y=6, direction=Direction.SOUTH, color="black"))
    scene.add(Chair(x=4, y=5, direction=Direction.EAST, color="black"))
    scene.add(Chair(x=8, y=5, direction=Direction.WEST, color="black"))
    scene.add(Lamp(x=11, y=0, height=1.2, color="orange"))
    scene.add(Lamp(x=11, y=12, height=1.2, color="orange"))
    return scene


def _bedroom() -> Scene:
    scene = Scene(room=Room(length=12, width=14, height=4))
    scene.add_door(Door(x=0, y=6, height=2, orientation="vertical", name="to_living"))
    scene.add_door(Door(x=5, y=14, height=2, orientation="horizontal", name="to_guest"))

    scene.add(
        Couch(x=2.5, y=0.5, direction=Direction.NORTH, length=7, depth=3.5, color="steelblue")
    )
    scene.add(Lamp(x=0.5, y=0.5, height=1.2, color="orange"))
    scene.add(Lamp(x=10.5, y=0.5, height=1.2, color="orange"))
    scene.add(Table(x=1, y=9, length=3, width=2, top_height=0.75, color="peru"))
    scene.add(Chair(x=5, y=10.5, direction=Direction.WEST, color="black"))
    scene.add(
        Bookshelf(
            x=0,
            y=13,
            length=4,
            height=3,
            num_shelves=4,
            color="saddlebrown",
            shelf_color="tan",
            direction=Direction.SOUTH,
        )
    )
    scene.add(
        Bookshelf(
            x=8,
            y=13,
            length=3,
            height=2,
            num_shelves=2,
            color="sienna",
            shelf_color="black",
            direction=Direction.SOUTH,
        )
    )
    scene.add(Lamp(x=11, y=12, height=1.5, color="orange"))
    return scene


def _dining() -> Scene:
    scene = Scene(room=Room(length=14, width=10, height=4))
    scene.add_door(Door(x=6, y=0, height=2, orientation="horizontal", name="to_living"))
    scene.add_door(Door(x=0, y=4, height=2, orientation="vertical", name="to_study"))
    scene.add_door(Door(x=14, y=4, height=2, orientation="vertical", name="to_guest"))

    scene.add(Table(x=4, y=3.5, length=6, width=3, top_height=0.75, color="peru"))
    scene.add(Chair(x=6, y=3.5, direction=Direction.NORTH, color="black"))
    scene.add(Chair(x=8, y=3.5, direction=Direction.NORTH, color="black"))
    scene.add(Chair(x=6, y=7.5, direction=Direction.SOUTH, color="black"))
    scene.add(Chair(x=8, y=7.5, direction=Direction.SOUTH, color="black"))
    scene.add(Chair(x=4, y=5.5, direction=Direction.EAST, color="black"))
    scene.add(Chair(x=10, y=5.5, direction=Direction.WEST, color="black"))
    scene.add(
        Bookshelf(
            x=0.5,
            y=9,
            length=4,
            height=2.5,
            num_shelves=2,
            color="sienna",
            shelf_color="tan",
            direction=Direction.SOUTH,
        )
    )
    scene.add(
        Bookshelf(
            x=9.5,
            y=9,
            length=4,
            height=2.5,
            num_shelves=2,
            color="sienna",
            shelf_color="tan",
            direction=Direction.SOUTH,
        )
    )
    scene.add(Lamp(x=0, y=0, height=1.5, color="orange"))
    scene.add(Lamp(x=13, y=0, height=1.5, color="orange"))
    return scene


def _study() -> Scene:
    scene = Scene(room=Room(length=12, width=10, height=4))
    scene.add_door(Door(x=5, y=0, height=2, orientation="horizontal", name="to_kitchen"))
    scene.add_door(Door(x=12, y=4, height=2, orientation="vertical", name="to_dining"))

    scene.add(
        Bookshelf(
            x=1,
            y=1,
            length=3,
            height=3,
            num_shelves=4,
            color="saddlebrown",
            shelf_color="black",
            direction=Direction.WEST,
        )
    )
    scene.add(
        Bookshelf(
            x=1,
            y=6,
            length=3,
            height=3,
            num_shelves=4,
            color="sienna",
            shelf_color="tan",
            direction=Direction.WEST,
        )
    )
    scene.add(Table(x=4, y=6, length=5, width=2, top_height=0.75, color="peru"))
    scene.add(Chair(x=7, y=6, direction=Direction.NORTH, color="black"))
    scene.add(
        Bookshelf(
            x=8,
            y=9,
            length=3,
            height=2,
            num_shelves=2,
            color="saddlebrown",
            shelf_color="tan",
            direction=Direction.SOUTH,
        )
    )
    scene.add(Lamp(x=0, y=9, height=1.5, color="orange"))
    scene.add(Lamp(x=11, y=8, height=1.2, color="orange"))
    scene.add(Chair(x=10, y=3, direction=Direction.NORTH, color="black"))
    return scene


def _guest_room() -> Scene:
    scene = Scene(room=Room(length=12, width=10, height=4))
    scene.add_door(Door(x=5, y=0, height=2, orientation="horizontal", name="to_bedroom"))
    scene.add_door(Door(x=0, y=4, height=2, orientation="vertical", name="to_dining"))

    scene.add(Couch(x=3, y=0.5, direction=Direction.NORTH, length=6, depth=3, color="olive"))
    scene.add(Lamp(x=1, y=0.5, height=1.2, color="orange"))
    scene.add(Lamp(x=10, y=0.5, height=1.2, color="orange"))
    scene.add(Table(x=9, y=5, length=2, width=2, top_height=0.75, color="peru"))
    scene.add(Chair(x=9, y=6, direction=Direction.EAST, color="black"))
    scene.add(
        Bookshelf(
            x=0.5,
            y=9,
            length=4,
            height=3,
            num_shelves=3,
            color="sienna",
            shelf_color="black",
            direction=Direction.SOUTH,
        )
    )
    scene.add(
        Bookshelf(
            x=8,
            y=9,
            length=3,
            height=2,
            num_shelves=2,
            color="saddlebrown",
            shelf_color="tan",
            direction=Direction.SOUTH,
        )
    )
    return scene


def default_floorplan() -> FloorPlan:
    """Living, kitchen, dining, study, bedroom, and guest rooms joined at shared doors."""
    plan = FloorPlan()
    plan.add("living", _living_room())
    plan.add("kitchen", _kitchen())
    plan.add("bedroom", _bedroom())
    plan.add("dining", _dining())
    plan.add("study", _study())
    plan.add("guest", _guest_room())
    plan.connect("living", "to_kitchen", "kitchen", "to_living")
    plan.connect("living", "to_bedroom", "bedroom", "to_living")
    plan.connect("living", "to_dining", "dining", "to_living")
    plan.connect("kitchen", "to_study", "study", "to_kitchen")
    plan.connect("bedroom", "to_guest", "guest", "to_bedroom")
    plan.connect("dining", "to_study", "study", "to_dining")
    plan.connect("dining", "to_guest", "guest", "to_dining")
    return plan
