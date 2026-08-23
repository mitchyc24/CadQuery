# CadQuery

Personal CAD models generated using the [CadQuery](https://cadquery.readthedocs.io/) library, plus a couple of small experiments for generating raw 3MF mesh XML.

## Repository structure

```
CadQuery/
├── config.ini            # Shared configuration (e.g. STL output directory)
├── requirements.txt       # Python dependencies
├── cqlib/                 # Shared library code used by every model
│   ├── io_utils.py        # export_stl(), load_config(), load_csv_points()
│   └── hexagon_lattice.py # Hexagon/lattice geometry helpers
├── projects/              # Every model script lives here, grouped by project
│   ├── cat_feeder/
│   ├── experiments/        # Early/learning models
│   ├── repairs/             # One-off replacement/repair parts
│   └── threemf/             # Raw 3MF mesh XML generation + a visualizer
├── build/                  # All generated output (STL, 3MF XML) - gitignored
│   ├── stl/
│   └── 3mf/
└── scripts/
    ├── build.py            # Build one, several, or all models
    └── new_model.py        # Scaffold a new model script
```

## Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Workflow: designing a model and generating an STL

1. **Scaffold a new model** (or copy an existing script under `projects/<group>/`):

   ```powershell
   python scripts/new_model.py experiments phone_stand
   ```

   This creates `projects/experiments/phone_stand.py` with the standard shape every model follows:

   ```python
   import cadquery as cq
   from cqlib.io_utils import export_stl


   def build() -> cq.Workplane:
       """Build the phone_stand model."""
       model = cq.Workplane("XY").box(10, 10, 10)
       return model


   if __name__ == "__main__":
       export_stl(build(), "phone_stand.stl")
   ```

2. **Edit `build()`** with your actual CadQuery geometry.

3. **Build it** — same command no matter which model or folder it lives in:

   ```powershell
   python scripts/build.py phone_stand
   ```

   Other useful forms:

   ```powershell
   python scripts/build.py --list          # see every available model name
   python scripts/build.py --all           # build every model in the repo
   python scripts/build.py cube key_holder # build several specific models
   ```

4. **Find the output** in `build/stl/<name>.stl` (the folder is configurable via `stl_output_dir` in [config.ini](config.ini)). Open it in your slicer to check the result.

### Notes

- `scripts/build.py` finds a model by scanning `projects/` for any script that calls `export_stl(...)` — no manual registration needed, it "just works" once a script follows the pattern above.
- Shared helpers (`export_stl`, `load_csv_points`, `hexagon`, `hex_lattice`, ...) live in `cqlib/` and are imported the same way from any model, e.g. `from cqlib.io_utils import export_stl`.
- Models that load points from a CSV (e.g. `projects/repairs/vent.py`) use `load_csv_points('file.csv')`, which resolves the path relative to the calling script's own folder.
- `projects/threemf/` is a separate, standalone experiment for generating raw 3MF mesh XML (not STL) — run it directly with `python -m projects.threemf.generate_3mf`, and inspect output with `python projects/threemf/visualizer/show_mf.py` (run from inside `build/3mf/` so it can find the generated `.xml` file).
