from __future__ import annotations

import numpy as np
import pytest

from virtual_room_builder.draw import _MAX_SEGMENT_LENGTH, _split_edge


def test_short_edge_is_not_split() -> None:
    start = np.array([0.0, 0.0, 0.0])
    end = np.array([0.5, 0.0, 0.0])
    pieces = _split_edge(start, end)
    assert len(pieces) == 1
    np.testing.assert_allclose(pieces[0][0], start)
    np.testing.assert_allclose(pieces[0][1], end)


def test_long_edge_splits_into_unit_pieces() -> None:
    start = np.array([0.0, 0.0, 0.0])
    end = np.array([0.0, 14.0, 0.0])
    pieces = _split_edge(start, end)
    assert len(pieces) == 14
    for piece_start, piece_end in pieces:
        length = float(np.linalg.norm(piece_end - piece_start))
        assert length == pytest.approx(_MAX_SEGMENT_LENGTH)
    np.testing.assert_allclose(pieces[0][0], start)
    np.testing.assert_allclose(pieces[-1][1], end)
