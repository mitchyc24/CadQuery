import cadquery as cq
import math



def hexagon(center, radius):
    """
    Create a hexagon with the given center and radius.
    """
    x, y = center
    points = [
        (radius, 0),
        (radius/2, radius*(3**0.5)/2),
        (-radius/2, radius*(3**0.5)/2),
        (-radius, 0),
        (-radius/2, -radius*(3**0.5)/2),
        (radius/2, -radius*(3**0.5)/2),
        (radius, 0)
    ]
    points = [(x + p[0], y + p[1]) for p in points]
    hexagon = cq.Workplane("XY").polyline(points).close()
    return hexagon


def hex_lattice(center=(0, 0), spacing=10, layers=1):
    # Initialize the list of points with the center point
    points = []
    
    if layers == 0:
        return [center]  # Return only the center point
    
    points.append(center)  # Add the center point

    # Generate points for each layer
    for layer in range(1, layers + 1):
        for i in range(6 * layer):  # 6 points for each layer
            angle = math.pi/2 + math.radians(i * (360 / (6 * layer)))  # Evenly distribute points in the layer
            # Calculate the coordinates for the points in this layer
            x = center[0] + layer * spacing * math.cos(angle)
            y = center[1] + layer * spacing * math.sin(angle)
            points.append((x, y))  # Add the calculated point to the list

    return points