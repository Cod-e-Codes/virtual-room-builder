"""Command-line entry point."""

from __future__ import annotations

import argparse
import sys

from virtual_room_builder.errors import VirtualRoomBuilderError
from virtual_room_builder.examples import default_scene


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="virtual-room-builder",
        description="Render a 3D room layout with matplotlib.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Write the render to this file instead of opening an interactive window.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="DPI to use when writing to a file (default: 150).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.dpi <= 0:
        parser.error("--dpi must be a positive integer")

    if args.output:
        import matplotlib

        matplotlib.use("Agg")

    scene = default_scene()

    try:
        fig = scene.figure()
    except VirtualRoomBuilderError as exc:
        print(f"Scene validation failed: {exc}", file=sys.stderr)
        return 1

    if args.output:
        fig.savefig(args.output, dpi=args.dpi, bbox_inches="tight")
        print(f"Wrote render to {args.output}")
    else:
        import matplotlib.pyplot as plt

        plt.show()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
