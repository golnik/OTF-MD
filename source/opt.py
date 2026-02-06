import numpy as np

from input import InputParams
from input import Input
from geometry import Geometry
from externalrun import ExternalRun

def Optimize(geom,erun,input):
    n_coords = geom.get_n_coords()
    g_thresh = input.inp_params.opt_thrs
    maxsteps = input.inp_params.opt_maxsteps

    grad_rms = 0.

    if input.inp_params.opt_method == 'GradDescent':
        alpha    = 0.05 #a.u.

        for it in range(maxsteps):
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

            print("step %d out of %d. RMS: %.4E, TRSH: %.4E" % (it,maxsteps,grad_rms,g_thresh))

            # check convergence
            if grad_rms < g_thresh:
                print(f"Converged at step {it}: RMS grad = {grad_rms:.3e}")
                break

            # steepest descent update
            for i in range(n_coords):
                geom.set_i_coord(
                    i, geom.get_i_coord(i) - alpha * grad[i]
                )

    elif input.inp_params.opt_method == 'Newton':
        for it in range(maxsteps):
            # save geometry
            xyz_out = input.inp_params.subst_variables(
                input.inp_params.xyz_out_fname, it
            )
            with open(xyz_out, "w") as f:
                geom.print_xyz(f)

            # run electronic structure calculation
            erun.run_external(it)

            # read energy, gradient, and hessian
            eg_out = input.inp_params.subst_variables(
                input.inp_params.eg_out_fname, it
            )
            energy, grad, hess = erun.read_EGH_out(eg_out)

            # compute RMS gradient
            grad_rms = np.sqrt(np.mean(np.asarray(grad)**2))

            print("step %d out of %d. RMS: %.4E, TRSH: %.4E" % (it,maxsteps,grad_rms,g_thresh))

            # check convergence
            if grad_rms < g_thresh:
                print(f"Converged at step {it}: RMS grad = {grad_rms:.3e}")
                break

            #invert hessian
            hess_1 = np.linalg.inv(hess)
            H_1g = hess_1.dot(grad)

            # update geometry
            for i in range(n_coords):
                geom.set_i_coord(
                    i, geom.get_i_coord(i) - H_1g[i]
                )            

    else:
        raise Exception("Unknown optimization method is requested.")

    if grad_rms < g_thresh:
        print("Optimization converged!")
    else:
        print("Optimization didn't converge! RMS: %.4E, TRSH: %.4E" % (grad_rms,g_thresh))

    return
