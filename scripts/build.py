#!/usr/bin/env python3
"""Build one, several, or all CadQuery models with a single consistent command.

Usage:
    python scripts/build.py --list                 # show available model names
    python scripts/build.py cube key_holder         # build specific models
    python scripts/build.py --all                   # build every model
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT / "projects"


def discover_models():
    """Find every model script (one that exports an STL) under projects/, keyed by filename stem."""
    models = {}
    for path in sorted(PROJECTS_DIR.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        if "export_stl(" in path.read_text(encoding="utf-8"):
            models[path.stem] = path
    return models


def run_model(name, path):
    module = ".".join(path.relative_to(ROOT).with_suffix("").parts)
    print(f"\n=== Building '{name}' ({path.relative_to(ROOT)}) ===")
    result = subprocess.run([sys.executable, "-m", module], cwd=ROOT)
    return result.returncode == 0


def main():
    models = discover_models()

    parser = argparse.ArgumentParser(description="Build CadQuery models into STL files.")
    parser.add_argument("names", nargs="*", help="Model name(s) to build")
    parser.add_argument("--all", action="store_true", help="Build every available model")
    parser.add_argument("--list", action="store_true", help="List available model names and exit")
    args = parser.parse_args()

    if args.list or not (args.all or args.names):
        print("Available models:")
        for name in sorted(models):
            print(f"  {name}")
        return

    if args.all:
        targets = models
    else:
        targets = {}
        for name in args.names:
            if name not in models:
                print(f"Unknown model '{name}'. Run with --list to see available models.")
                sys.exit(1)
            targets[name] = models[name]

    failures = [name for name, path in targets.items() if not run_model(name, path)]

    print("\n=== Build summary ===")
    print(f"Built: {len(targets) - len(failures)}/{len(targets)}")
    if failures:
        print(f"Failed: {', '.join(failures)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
