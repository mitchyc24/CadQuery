#!/usr/bin/env python3
"""Scaffold a new model script with the boilerplate this repo's build.py expects.

Usage:
    python scripts/new_model.py <group> <name>

Example:
    python scripts/new_model.py experiments phone_stand
    -> creates projects/experiments/phone_stand.py
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = '''import cadquery as cq
from cqlib.io_utils import export_stl


def build() -> cq.Workplane:
    """Build the {name} model."""
    model = cq.Workplane("XY").box(10, 10, 10)
    return model


if __name__ == "__main__":
    export_stl(build(), "{name}.stl")
'''


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new CadQuery model script.")
    parser.add_argument("group", help="Project subfolder under projects/ (created if missing)")
    parser.add_argument("name", help="Model name (used for the .py filename and default .stl name)")
    args = parser.parse_args()

    target_dir = ROOT / "projects" / args.group
    target_path = target_dir / f"{args.name}.py"

    if target_path.exists():
        print(f"'{target_path.relative_to(ROOT)}' already exists.")
        sys.exit(1)

    target_dir.mkdir(parents=True, exist_ok=True)
    target_path.write_text(TEMPLATE.format(name=args.name), encoding="utf-8")
    print(f"Created {target_path.relative_to(ROOT)}")
    print(f"Build it with: python scripts/build.py {args.name}")


if __name__ == "__main__":
    main()
