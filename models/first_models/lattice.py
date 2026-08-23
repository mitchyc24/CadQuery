import cadquery as cq
import math
from utils.util_functions import export_stl

def wave_lattice():
    function_1 = lambda x: math.sin(x)

    voxel = cq.Voxel(10, 
