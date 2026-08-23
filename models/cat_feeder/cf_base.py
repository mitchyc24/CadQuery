import cadquery as cq
import os


def main():

    base = cq.Workplane("XY").box(150, 150, 150)

    export_stl(base, 'cat_feeder_base.stl')



def export_stl(model, filename):
    try:
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Navigate up one level to the project root
        project_root = os.path.dirname(script_dir)
        
        # Define the output directory
        output_dir = os.path.join(project_root, 'stl_files')
        
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create the full path for the output file
        output_path = os.path.join(output_dir, filename)
        
        # Export the model to STL
        cq.exporters.export(model, output_path)
        print(f"STL file successfully exported to '{output_path}'.")
    except Exception as e:
        print(f"Failed to export STL file: {e}")
        raise



if __name__ == "__main__":
    main()