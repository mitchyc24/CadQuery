import cadquery as cq


def points2skirt(points: tuple, length: int, thickness: int) -> cq.Workplane:
    """
    Create a skirt around a set of points. Depth and Thickness in mm
    """

    # Create the profile using corner points
    profile = cq.Workplane("XY").polyline(points)

    # Extrude the profile to create a thin plate for the skirt
    outside = profile.close().extrude(length)  # Extrude to thickness mm thickness

    # Create the inner profile
    inner_profile = cq.Workplane("XY").polyline(points)

    # Extrude the inner profile to create a thin plate for the skirt
    inside = inner_profile.close().offset2D(-thickness).extrude(length) # Extrude to thickness + depth mm thickness

    # Subtract the inner profile from the outer profile to create the skirt
    skirt = outside.cut(inside)
    

    cq.exporters.export(skirt, 'stl/skirt.stl')
    return skirt


if __name__ == "__main__":
    points = [
        (1,7),
        (2,7),
        (4,6),
        (6,4),
        (10,0),
        (10,-4),
        (7,-6),
        (4,-7),
        (2,-7),
        (-2,-7),
        (-4,-6),
        (-6,-4),
        (-8,-2),
        (-10,-1),
        (-11,1),
        (-11,3),
        (-9,5),
        (-8,5),
        (-6,5),
    ]


    scale_factor = 6.35
    points = [(x*scale_factor, y*scale_factor) for x, y in points]
    points2skirt(points, 20, 2)