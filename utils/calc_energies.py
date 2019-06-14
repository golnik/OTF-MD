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
fs2au = 41.341374575751
#A2bohr = 1.8897259886

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

    #loop over time steps
    for it in range(nsteps+1):
        geom = Geometry()

        #read geometry and velocity from file
        xyz_fname = input.inp_params.subst_variables(input.inp_params.xyz_out_fname,it)
        geom.read_xyz(xyz_fname)
        vel_fname = input.inp_params.subst_variables(input.inp_params.vel_out_fname,it)
        geom.read_vel(vel_fname)

        #read mass file
        geom.read_mol(input.inp_params.mol_fname)

        #parameters of molecule
        n_coords = geom.get_n_coords()
        n_atoms = geom.get_n_atoms()
        masses = [mass for mass in geom.atomic_masses]

        #get energy and gradients from output file
        eg_out_fname = input.inp_params.subst_variables(input.inp_params.eg_out_fname,it)
        energy, grad = erun.read_EG_out(eg_out_fname)

        time = it*dt/fs2au

        #calculate kinetic energy
        output = sys.stdout
        output.write("%s " % time)
        T = 0.0
        for i_atom in range(n_atoms):
            v_i = np.zeros(3)
            for i_coord in range(3):
                v_i[i_coord] = geom.get_i_vel(3*i_atom+i_coord)

            v = np.sqrt(v_i[0]**2 + v_i[1]**2 + v_i[2]**2)

            T += 0.5 * masses[i_atom] * v**2

        #potential energy
        V = energy

        #print output
        output.write("%s %s %s\n" %(T,V,T+V))