# models/python/vent/vent.py

import cadquery as cq
from utils.functions import load_csv_points, export_stl

def get_vent():
    """
    Generates the vent model using points from a CSV file.
    
    Returns:
        cq.Workplane: The generated vent model.
    """
    # Load points from 'points.csv' located in the same directory as vent.py
    points = load_csv_points('points.csv')
   
    if not points:
        print("No points found. Vent model cannot be created.")
        return None
    
    outter_profile = cq.Workplane("XY").polyline(points).close()
    inner_profile = cq.Workplane("XY").polyline(points).close().offset2D(-5)

    # Extrude the surface between the inner and outter profiles
    outter_shape = outter_profile.extrude(10) 
    inner_shape = inner_profile.extrude(10)  
    vent = outter_shape.cut(inner_shape)  

    top_profile = cq.Workplane("XY").polyline(points).close().offset2D(10).transformed(offset=(0,0,10))
    top_shape = top_profile.extrude(2)


    vent = vent.union(top_shape)


    return vent

def main():
    vent = get_vent()
    if vent:
        # Export the vent model to 'vent.stl' within the configured STL output directory
        export_stl(vent, 'vent.stl')  # 'vent.stl' will be placed inside 'stl_output_dir'
    else:
        print("Vent model was not created. Export skipped.")

if __name__ == "__main__":
    main()