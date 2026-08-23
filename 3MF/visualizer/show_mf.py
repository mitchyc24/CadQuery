import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D  # Ensure this import is present

# list all xml files in the current directory
xml_files = [f for f in os.listdir('.') if f.endswith('.xml')]

# Ask user to select a file
print("Available files:")
for i, file in enumerate(xml_files):
    print(f"{i + 1}. {file}")

# Get user input
choice = int(input("Enter the number of the file you want to visualize: "))

# Parse the 3MF XML content
tree = ET.parse(xml_files[choice-1])  # Replace with your 3MF file path
root = tree.getroot()

# Namespace for the 3MF XML format
namespace = {'n': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}

# Extract vertices and triangles
vertices = []
triangles = []

# Find all vertices in the XML
for vertex in root.findall('.//n:vertex', namespace):
    x = float(vertex.get('x', 0))
    y = float(vertex.get('y', 0))
    z = float(vertex.get('z', 0))
    vertices.append([x, y, z])

# Find all triangles in the XML
for triangle in root.findall('.//n:triangle', namespace):
    v1 = int(triangle.get('v1', 0))
    v2 = int(triangle.get('v2', 0))
    v3 = int(triangle.get('v3', 0))
    triangles.append([v1, v2, v3])

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # Ensure the subplot is 3D

# Plot the vertices and triangles
for triangle in triangles:
    # Check if triangle indices are within the range of vertices
    if all(v < len(vertices) for v in triangle):
        v0 = vertices[triangle[0]]
        v1 = vertices[triangle[1]]
        v2 = vertices[triangle[2]]
        
        # Create a polygon for each triangle
        poly3d = [[v0, v1, v2]]
        # Make poly3d a collection
        poly3d_collection = Poly3DCollection(poly3d, alpha=0.5)
        ax.add_collection(poly3d_collection)
    else:
        print(f"Invalid triangle indices: {triangle}")

# Extract x, y, z coordinates from vertices for setting limits
x_coords, y_coords, z_coords = zip(*vertices)


f = lambda x: int(x) if x else 0

x_min = f(min(x_coords))
x_max = f(max(x_coords))
y_min = f(min(y_coords))
y_max = f(max(y_coords))
z_min = f(min(z_coords))
z_max = f(max(z_coords))

# Set plot limits and labels
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('X')
ax.set_ylabel('Y')

plt.title('3MF Object Visualization')
plt.show()
