import cadquery as cq
from cqlib.io_utils import export_stl


def main():

    base = cq.Workplane("XY").box(150, 150, 150)

    export_stl(base, 'cat_feeder_base.stl')


if __name__ == "__main__":
    main()