import cadquery as cq
from cqlib.io_utils import export_stl


def build(d1=150, d2=200, border_thickness=10) -> cq.Workplane:
    """Build a rhombus cover plate with a border frame. Diagonals d1/d2 and border_thickness are in mm."""
    half_d1 = d1 / 2
    half_d2 = d2 / 2

    # Create the rhombus profile using corner points
    rhombus = cq.Workplane("XY").polyline([
        (-half_d1, 0),    # Left middle point
        (0, half_d2),     # Top middle point
        (half_d1, 0),     # Right middle point
        (0, -half_d2),    # Bottom middle point
        (-half_d1, 0)     # Close the loop back to start
    ])

    # Extrude the profile to create a thin plate for the cover
    cover = rhombus.close().extrude(5)  # Extrude to 5 mm thickness

    # Add a border around the rhombus to create the frame
    border = cover.faces(">Z").wires().toPending().offset2D(border_thickness).extrude(5)
    return border


if __name__ == "__main__":
    export_stl(build(), 'rhombus_cover.stl')