import cadquery as cq

# Create a 10mm cube
cube = cq.Workplane("XY").box(10, 10, 10)

# Export the cube object to an STL file
cq.exporters.export(cube, 'stl/cube.stl')
