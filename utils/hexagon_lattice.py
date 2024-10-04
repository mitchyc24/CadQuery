import cadquery as cq
import math
from collections import deque

def hexagon(center, radius, rotation=0):
    """
    Create a hexagon with the given center, radius, and rotation angle.
    
    Parameters:
    - center: Tuple of (x, y) coordinates for the center of the hexagon.
    - radius: The distance from the center to any vertex of the hexagon.
    - rotation: The rotation angle in degrees to orient the hexagon.
    
    Returns:
    - A CadQuery Workplane object representing the hexagon.
    """
    x, y = center
    angle_rad = math.radians(rotation)
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)
    
    # Original points of a hexagon centered at the origin
    points = [
        (radius, 0),
        (radius/2, radius * (3**0.5)/2),
        (-radius/2, radius * (3**0.5)/2),
        (-radius, 0),
        (-radius/2, -radius * (3**0.5)/2),
        (radius/2, -radius * (3**0.5)/2),
        (radius, 0)  # Closing the hexagon by returning to the first point
    ]
    
    # Rotate and translate the points
    rotated_points = []
    for px, py in points:
        # Rotate the point
        rotated_px = px * cos_theta - py * sin_theta
        rotated_py = px * sin_theta + py * cos_theta
        # Translate the point to the center position
        rotated_points.append((x + rotated_px, y + rotated_py))
    
    # Create the hexagon using the rotated and translated points
    hexagon = cq.Workplane("XY").polyline(rotated_points).close()
    return hexagon

def hex_neighbors_bfs(axial_coord, max_depth):
    visited = set()
    queue = deque()
    q, r = axial_coord
    queue.append((q, r, 0))  # (q, r, depth)
    visited.add((q, r))

    # Define the six possible directions in axial coordinates
    directions = [
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, 0),
        (-1, 1),
        (0, 1)
    ]

    while queue:
        q, r, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for dq, dr in directions:
            neighbor = (q + dq, r + dr)
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor[0], neighbor[1], depth + 1))
    return visited

def axial_to_cartesian(q, r, radius):
    x = radius * math.sqrt(3) * (q + r / 2)
    y = radius * 1.5 * r
    return (x, y)

def hex_lattice(center, radius, depth):
    visited = hex_neighbors_bfs(center, depth)
    points = [axial_to_cartesian(q, r, radius) for q, r in visited]
    return points