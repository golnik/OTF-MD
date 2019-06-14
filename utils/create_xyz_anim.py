import configparser
import sys
import os
import numpy as np

#path to OTF-MD
my_dir     = os.path.dirname(os.path.realpath(__file__))
OTFMD_path = "../source/"
sys.path.append(os.path.join(my_dir,OTFMD_path))

from input import InputParams
from input import Input
from geometry import Geometry
from externalrun import ExternalRun

#conversion coefficients
amu2em = 1822.888530063
fs2au = 41.341374575751
A2bohr = 1.8897259886

if __name__ == "__main__":
    #get input file
    if len(sys.argv) > 1:
        inp_fname = sys.argv[1]
    else:
        raise Exception("Input file is not provided.")
    
    #analyze input file
    input = Input(inp_fname)
    
    #required propagation parameters
    dt = input.inp_params.prop_dt * fs2au
    nsteps = input.inp_params.prop_steps
    
    #create external run object
    erun = ExternalRun(input.inp_params)
    
    for it in range(nsteps+1):
        geom = Geometry()

        #read geometry and velocity from file
        xyz_fname = input.inp_params.subst_variables(input.inp_params.xyz_out_fname,it)
        geom.read_xyz(xyz_fname)
        
        geom.print_xyz(sys.stdout)