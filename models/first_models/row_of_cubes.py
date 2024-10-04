import cadquery as cq
from utils.util_functions import load_csv_points, export_stl

def get_cubes():
    """
    Generates a row of cubes.
    
    Returns:
        cq.Workplane: The generated cubes model.
    """

    for i in range(5):
        cube = cq.Workplane("XY").box(10, 10, 10).translate((i*20, 0, 0))
        if i == 0:
            cubes = cube
        else:
            cubes = cubes.union(cube)

    return cubes

def main():
    cubes = get_cubes()
    if cubes:
        # Export the vent model to 'vent.stl' within the configured STL output directory
        export_stl(cubes, 'cubes.stl')  # 'vent.stl' will be placed inside 'stl_output_dir'
    else:
        print("Cubes model was not created. Export skipped.")

if __name__ == "__main__":
    main()