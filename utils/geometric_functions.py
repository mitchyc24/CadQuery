import cadquery as cq




def hexagon(center=(0,0), radius=1):
    """
    Create a hexagon with the given center and radius.
    """
    hexagon = cq.Workplane("XY").polyline([
        (radius, 0),
        (radius/2, radius*(3**0.5)/2),
        (-radius/2, radius*(3**0.5)/2),
        (-radius, 0),
        (-radius/2, -radius*(3**0.5)/2),
        (radius/2, -radius*(3**0.5)/2),
        (radius, 0)
    ]).close()
    return hexagon


def distribute_points(d, num):
    points = []
    count = 0
    row = 0

    while count < num:
        # Calculate the y-coordinate based on the row
        y = row * d
        
        # Calculate the starting x-coordinate based on the row
        start_x = (0.5 * d) if row % 2 else 0
        
        # Calculate the number of points in the current row
        points_in_row = (num - count) if count + d // 2 >= num else d
        
        for i in range(points_in_row):
            x = start_x + i * d
            points.append((x, y))
            count += 1
            if count >= num:
                break
                
        row += 1

    return points
