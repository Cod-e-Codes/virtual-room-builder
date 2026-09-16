# Virtual Room Builder

Compose and render simple 3D room layouts with matplotlib.

Wireframe walls, floors, and furniture with bounds checking so a piece
placed outside the room fails loudly instead of rendering wrong.

![Example room](screenshot.png)

## Install

Requires Python 3.10+.

```bash
pip install -e ".[dev]"
```

## Usage

```bash
virtual-room-builder
```

Opens an interactive matplotlib window with the example room. Write an image
instead of opening a window:

```bash
virtual-room-builder --output room.png
```

Use as a library:

```python
from virtual_room_builder import Room, Scene, Chair, Table, Direction

scene = Scene(room=Room(length=12, width=10, height=3))
scene.add(Chair(x=3, y=3, direction=Direction.NORTH, color="black"))
scene.add(Table(x=2, y=2, length=3, width=3, top_height=0.75, color="peru"))

fig = scene.figure()  # validates containment first, then renders
fig.savefig("room.png")
```

Furniture pieces are dataclasses: `Chair`, `Table`, `Lamp`, `Bookshelf`,
`Couch`. Each takes an `x`, `y` anchor (the local origin corner) and a
`Direction` (`NORTH`, `SOUTH`, `EAST`, `WEST`). Chair, table, lamp, and couch
rotate about that anchor. Bookshelf uses facing-dependent extents:
north/south run length along x, east/west along y, with depth toward the
facing side.

`Door` takes an `orientation` of `"horizontal"` or `"vertical"`. Horizontal
doors must sit on the south (y=0) or north wall; vertical doors must sit on
the west (x=0) or east wall.

`Scene.figure()` and `Scene.validate()` check room containment for furniture
and wall attachment for doors. They do not detect furniture-to-furniture
overlap. `Scene.render(ax)` draws without validating.

## Project layout

- `src/virtual_room_builder/geometry.py` - shared rotation and box math
- `src/virtual_room_builder/room.py` - the room shell
- `src/virtual_room_builder/door.py` - doorway markers
- `src/virtual_room_builder/furniture/` - chair, table, lamp, bookshelf, couch
- `src/virtual_room_builder/scene.py` - composes a room with its furniture, validates fit
- `src/virtual_room_builder/cli.py` - command-line entry point
- `src/virtual_room_builder/examples.py` - the default example scene
- `tests/` - pytest suite covering geometry, each furniture item, and scene validation

## Contributing

Pull requests are welcome. Open an issue first for larger changes. Run:

```bash
pytest
ruff check src tests
mypy src
```

## License

MIT © 2026 Cody Marsengill. See [LICENSE](LICENSE).
