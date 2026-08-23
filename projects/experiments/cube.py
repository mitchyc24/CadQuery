import cadquery as cq
from cqlib.io_utils import export_stl


def build() -> cq.Workplane:
    """Build a 10mm test cube."""
    return cq.Workplane("XY").box(10, 10, 10)


if __name__ == "__main__":
    export_stl(build(), 'cube.stl')
