import configparser
import sys
import os
import numpy as np

from input import InputParams
from input import Input
from geometry import Geometry
from externalrun import ExternalRun
from prop import Propagate
from opt import Optimize

if __name__ == "__main__":
    #get input file
    if len(sys.argv) > 1:
        inp_fname = sys.argv[1]
    else:
        raise Exception("Input file is not provided.")
    
    #analyze input file
    input = Input(inp_fname)

    #create tmp directory
    if not os.path.exists(input.inp_params.tmp_dir):
        os.makedirs(input.inp_params.tmp_dir)

    #load initial geometry and velocities if available
    geom = Geometry()
    geom.read_xyz(input.inp_params.xyz_fname)
    geom.read_mol(input.inp_params.mol_fname)
    if input.inp_params.vel_fname is not None:
        geom.read_vel(input.inp_params.vel_fname)

    #create external run object
    erun = ExternalRun(input.inp_params)

    ############################################################################

    if input.inp_params.task == 'opt':
        Optimize(geom,erun,input)
    elif input.inp_params.task == 'prop':
        Propagate(geom,erun,input)
    else:
        raise Exception("Unknown task is requested.")