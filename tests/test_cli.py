from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import pytest

from virtual_room_builder.cli import main


def test_cli_writes_output(tmp_path) -> None:
    out = tmp_path / "room.png"
    assert main(["--output", str(out)]) == 0
    assert out.is_file()
    assert out.stat().st_size > 0


def test_cli_writes_room_example(tmp_path) -> None:
    out = tmp_path / "room.png"
    assert main(["--example", "room", "--output", str(out)]) == 0
    assert out.is_file()
    assert out.stat().st_size > 0


def test_cli_writes_floorplan_example(tmp_path) -> None:
    out = tmp_path / "floorplan.png"
    assert main(["--example", "floorplan", "--output", str(out)]) == 0
    assert out.is_file()
    assert out.stat().st_size > 0


def test_cli_room_and_floorplan_renders_differ(tmp_path) -> None:
    room = tmp_path / "room.png"
    floorplan = tmp_path / "floorplan.png"
    assert main(["--example", "room", "--output", str(room)]) == 0
    assert main(["--example", "floorplan", "--output", str(floorplan)]) == 0
    assert room.read_bytes() != floorplan.read_bytes()


def test_cli_rejects_unknown_example() -> None:
    with pytest.raises(SystemExit):
        main(["--example", "attic"])


def test_cli_rejects_nonpositive_dpi() -> None:
    with pytest.raises(SystemExit):
        main(["--dpi", "0"])
