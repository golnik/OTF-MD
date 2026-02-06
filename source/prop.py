import numpy as np

from input import InputParams
from input import Input
from geometry import Geometry
from externalrun import ExternalRun

#conversion coefficients
fs2au = 41.341374575751

def Propagate(geom,erun,input):
    #required propagation parameters
    n_coords = geom.get_n_coords()
    n_atoms = geom.get_n_atoms()
    masses = [mass for mass in geom.atomic_masses]
    dt = input.inp_params.prop_dt * fs2au
    
    nsteps = input.inp_params.prop_steps

    #initial step
    
    #save initial geometry
    xyz_out_fname = input.inp_params.subst_variables(input.inp_params.xyz_out_fname,0)
    with open(xyz_out_fname,'w') as file:
        geom.print_xyz(file)
    
    #save initial velocities
    vel_out_fname = input.inp_params.subst_variables(input.inp_params.vel_out_fname,0)
    with open(vel_out_fname,'w') as file:
        geom.print_vel(file)    
    
    #perform external calculations of energy and gradient
    erun.run_external(0)

    #get energy and gradients from output file
    eg_out_fname = input.inp_params.subst_variables(input.inp_params.eg_out_fname,0)
    energy, grad = erun.read_EG_out(eg_out_fname)

    #propagation
    for it in range(nsteps):
        tstep = it+1

        #convert gradients to accelerations
        acc = np.zeros(n_coords)
        for i_atom in range(n_atoms):
            for i_coord in range(3):
                acc[3*i_atom+i_coord] = -grad[3*i_atom+i_coord] / masses[i_atom]

        #propagate geometry to next time step
        for i_coord in range(n_coords):
            coord = geom.get_i_coord(i_coord)
            coord += geom.get_i_vel(i_coord) * dt + 0.5 * acc[i_coord] * dt**2
            geom.set_i_coord(i_coord,coord)

        #save updated geometry to file
        xyz_out_fname = input.inp_params.subst_variables(input.inp_params.xyz_out_fname,tstep)
        with open(xyz_out_fname,'w') as file:
            geom.print_xyz(file)

        #perform external calculations of energy and gradient
        erun.run_external(tstep)

        #get energy and gradients from output file
        eg_out_fname = input.inp_params.subst_variables(input.inp_params.eg_out_fname,tstep)
        energy_dt, grad_dt = erun.read_EG_out(eg_out_fname)

        #grad to accelerations
        acc_dt = np.zeros(n_coords)
        for i_atom in range(n_atoms):
            for i_coord in range(3):
                acc_dt[3*i_atom+i_coord] = -grad_dt[3*i_atom+i_coord] / masses[i_atom]

        #propagate velocities
        for i_coord in range(n_coords):
            vel = geom.get_i_vel(i_coord)
            vel += 0.5 * (acc[i_coord] + acc_dt[i_coord]) * dt
            geom.set_i_vel(i_coord,vel)
            
        #save new velocities to file
        vel_out_fname = input.inp_params.subst_variables(input.inp_params.vel_out_fname,tstep)
        with open(vel_out_fname,'w') as file:
            geom.print_vel(file)
        
        #shift gradients on previous timestep
        grad = grad_dt

    return