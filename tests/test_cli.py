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


def test_cli_rejects_nonpositive_dpi() -> None:
    with pytest.raises(SystemExit):
        main(["--dpi", "0"])
