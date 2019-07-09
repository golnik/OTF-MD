import configparser
import sys
import os
import numpy as np
import argparse
import re

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

#read hessian from string
def get_hessian(string,n_coords):
    hess_pattern = r'[^\S\r\n]*\$hessian\s+((?:.*\n){%s})' % n_coords
    hess_regex = re.compile(hess_pattern,re.IGNORECASE|re.MULTILINE)

    match = re.search(hess_regex,string)

    hess_str = match.group(1)

    hess = []
    for line in hess_str.splitlines():
        hess_row = [float(i) for i in line.split()]
        hess.append(hess_row)

    return hess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    p_required = parser.add_argument_group('required arguments')

    p_required.add_argument("input",type=str,
                        help='Path to input file.',
                        metavar=('INPUT_FILE'))

    p_required.add_argument("-hess_fname",type=str,required=True,
                        help='Path to file with hessian.',
                        metavar=('HESS_FILE'))

    p_required.add_argument("-out_path",type=str,required=True,
                        help='Path to directory where output trajectory will be written.',
                        metavar=('OUT_PATH'))

    #parse arguments
    args = parser.parse_args()

    #get input file
    inp_fname = args.input
    hess_fname = args.hess_fname
    out_path = args.out_path

    #check that out_path direcory does not exists already
    if os.path.exists(out_path):
        raise Exception("Specified output directory already exists!")

    #analyze input file
    input = Input(inp_fname)

    #required propagation parameters
    dt = input.inp_params.prop_dt * fs2au
    nsteps = input.inp_params.prop_steps

    #create external run object
    erun = ExternalRun(input.inp_params)

    #hess matrix
    hess = None

    #loop over time steps
    for it in range(nsteps+1):
        #output directory and files
        out_dir = os.path.join(out_path,"step_%i" % (it+1))
        out_file = os.path.join(out_dir,"step_%i.dat" % (it+1))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        print("Time step %s, output file %s" % (it+1,out_file))

        #output stream
        out_stream = open(out_file,'w')

        geom = Geometry()

        #read geometry file
        xyz_fname = input.inp_params.subst_variables(input.inp_params.xyz_out_fname,it)
        geom.read_xyz(xyz_fname)

        #read mol file
        geom.read_mol(input.inp_params.mol_fname)

        #get energy and gradients from output file
        eg_out_fname = input.inp_params.subst_variables(input.inp_params.eg_out_fname,it)
        energy, grad = erun.read_EG_out(eg_out_fname)

        n_coords = geom.get_n_coords()
        n_atoms = geom.get_n_atoms()

        #read hessian (only once)
        if hess == None:
            #read hess from file
            with open(hess_fname,'r') as file:
                data_str = file.read()
                hess = get_hessian(data_str,n_coords)

        #write geometry section
        out_stream.write("$geom\n    ")
        for i_coord in range(n_coords):
            coord = geom.get_i_coord(i_coord)
            out_stream.write("%s " % (coord/A2bohr))
        out_stream.write("\n$END\n")

        #write atomic masses section
        out_stream.write("$atomic mass\n    ")
        for i_atom in range(n_atoms):
            mass = geom.get_i_mass(i_atom)
            out_stream.write("%s " % (mass/amu2em))
        out_stream.write("\n$END\n")

        #write potential section
        out_stream.write("$potential\n    ")
        out_stream.write("%s" % energy)
        out_stream.write("\n$END\n")

        #write force section
        out_stream.write("$force\n    ")
        for i_coord in range(n_coords):
            out_stream.write("%s " % (-grad[i_coord]))
        out_stream.write("\n$END\n")

        #write hessian section
        out_stream.write("$hessian\n")
        for i_coord in range(n_coords):
            out_stream.write("    ")
            for j_coord in range(n_coords):
                out_stream.write("%s " % hess[i_coord][j_coord])
            out_stream.write("\n")
        out_stream.write("$END\n")

        out_stream.close()