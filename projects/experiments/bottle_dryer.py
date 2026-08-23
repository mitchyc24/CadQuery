import cadquery as cq
from cqlib.io_utils import export_stl
from ocp_vscode import show
import argparse
import sys

def build() -> cq.Workplane:
    """Build the bottle_dryer model."""
    model = cq.Workplane("XY").box(10, 10, 10)
    return model


if __name__ == "__main__":
    argparse.ArgumentParser(description="Bottle Dryer Model Builder")
    ##if --build is passed, build the model and export it to STL
    model = build()
    if '--build' in sys.argv:
        export_stl(model, "bottle_dryer.stl")
    else:
        show(model)
    
