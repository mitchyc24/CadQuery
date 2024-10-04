import cadquery as cq

# Define the diagonal lengths of the rhombus in mm
d1 = 150  # 15 cm
d2 = 200  # 20 cm

# Calculate half lengths to determine corner positions
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
border_thickness = 10  # Thickness of the border in mm
border = cover.faces(">Z").wires().toPending().offset2D(border_thickness).extrude(5)




cq.exporters.export(border, 'stl/vent_cover.stl')