import numpy as np

from input import InputParams
from input import Input
from geometry import Geometry
from externalrun import ExternalRun

def Optimize(geom,erun,input):
    n_coords = geom.get_n_coords()

    if input.inp_params.opt_method == 'GradDescent':
        nsteps   = 20
        alpha    = 0.05 #a.u.
        g_thresh = 1e-4 #gradient threshold (let's see if this works)

        for it in range(nsteps):
            # save geometry
            xyz_out = input.inp_params.subst_variables(
                input.inp_params.xyz_out_fname, it
            )
            with open(xyz_out, "w") as f:
                geom.print_xyz(f)

            # run electronic structure calculation
            erun.run_external(it)

            # read energy and gradient
            eg_out = input.inp_params.subst_variables(
                input.inp_params.eg_out_fname, it
            )
            energy, grad = erun.read_EG_out(eg_out)

            # compute RMS gradient
            grad_rms = np.sqrt(np.mean(np.asarray(grad)**2))

            # check convergence
            if grad_rms < g_thresh:
                print(f"Converged at step {it}: RMS grad = {grad_rms:.3e}")
                break

            # steepest descent update
            for i in range(n_coords):
                geom.set_i_coord(
                    i, geom.get_i_coord(i) - alpha * grad[i]
                )

    else:
        raise Exception("Unknown optimization method is requested.")

    print("Optimization completed! [not really :)]")

    return
