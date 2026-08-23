import math
import cadquery as cq
from cqlib.io_utils import export_stl

class KeyHolder:
    """
    A class to represent a key holder model.

    """
    def __init__(self, circle_radius, num_cylinders, cylinder_radius, cylinder_length):
        """
        Constructs all the necessary attributes for the key holder model.

        Parameters:
            circle_radius (float): The radius of the circle.
            num_cylinders (int): The number of cylinders to generate.
            cylinder_radius (float): The radius of the cylinder.
            cylinder_length (float): The length of the cylinder.
        """
        self.circle_radius = circle_radius
        self.num_cylinders = num_cylinders
        self.cylinder_radius = cylinder_radius
        self.cylinder_length = cylinder_length




    def calculate_circle_position(self , deg):
        """
        Calculates the position of a circle based on the number of cylinders.

        Parameters:
            deg (int): The degree of the circle.

        Returns:
            tuple: The (x, y, z) position of the circle.
        """
        x = self.circle_radius * math.cos(math.radians(deg))
        y = self.circle_radius * math.sin(math.radians(deg))
        return (x, y, 0)

    def generate(self):
        """
        Generates a key holder model (currently just a single cylinder).
        
        Returns:
            cq.Workplane: The generated key holder model.
        """

        key_holder = cq.Workplane("XY")

        for deg in range(0, 360, 360 // self.num_cylinders):
            position = self.calculate_circle_position(deg)
            print(f"Creating cylinder at position {position} with orientation {deg} degrees.")
            rod = self.create_cylinder(self.cylinder_radius, self.cylinder_length, position, orientation=(45*math.sin(math.radians(deg)), -60*math.cos(math.radians(deg)) , 0))
            key_holder = key_holder.union(rod)

        return key_holder
    
    def create_cylinder(self, radius, length, position, orientation=(0, 0, 0)):
        """
        Creates a cylinder with the specified radius, length, position, and orientation.

        Parameters:
            radius (float): The radius of the cylinder.
            length (float): The length of the cylinder.
            position (tuple): The position of the cylinder (x, y, z).
            orientation (cadquery.Vector): The orientation of the cylinder.

        Returns:
            cq.Workplane: The created cylinder.
        """
        return (cq.Workplane("XY")
                .transformed(offset=position, rotate=orientation)
                .circle(radius)
                .extrude(length))



if __name__ == "__main__":
    key_holder = KeyHolder(circle_radius=60, num_cylinders=60, cylinder_radius=2, cylinder_length=100).generate()
    if key_holder:
        export_stl(key_holder, 'key_holder.stl')
        print("Key holder model created and exported successfully.")
    else:
        print("Key holder model was not created. Export skipped.")
