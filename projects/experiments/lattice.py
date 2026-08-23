import cadquery as cq
import math
from cqlib.io_utils import export_stl

# TODO: incomplete - cq.Voxel is not a real CadQuery API, this needs a working implementation
def wave_lattice():
    function_1 = lambda x: math.sin(x)

    voxel = cq.Voxel(10, 
