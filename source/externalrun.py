import subprocess
import re
import sys
import numpy as np

from input import InputParams

A2bohr = 1.8897259886

class ExternalRun(object):
    def __init__(self, inp_params):
        self.inp_params = inp_params

    def run_external(self, tstep, out_stream=sys.stdout):
        command = self.inp_params.subst_variables(self.inp_params.run_command,tstep)

        #print information about command
        out_stream.write(" The following command will be executed:\n")
        out_stream.write("  %s\n" % command)

        #initiate subprocess for calculations
        process = subprocess.Popen(command.split(),
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   bufsize=1,universal_newlines=True)

        #process.wait() #wait till process finishes
        
        #get output
        #output, error = process.communicate()

        #print output produced by script
        #out_stream.write(output)
        
        while process.poll() is None:
            out = process.stdout.readline()
            out_stream.write(out)

    def read_EG_out(self, fname):
        '''
        Read energy and gradient from EG_out file
        '''
        with open(fname,'r') as file:
            data_str = file.read()

            energy = self.get_energy(data_str)
            grad = self.get_gradient(data_str)

        return energy,grad

    def read_EGH_out(self, fname):
        '''
        Read energy, gradient, and Hessian from EGH_out file
        '''
        with open(fname,'r') as file:
            data_str = file.read()

            energy = self.get_energy(data_str)
            grad = self.get_gradient(data_str)
            hess = self.get_hessian(data_str)

        return energy,grad,hess

    def get_gradient(self, string):
        grad_pattern = r'[^\S\r\n]*\$gradient\s+(.*)$'
        grad_regex = re.compile(grad_pattern,re.IGNORECASE|re.MULTILINE)

        match = re.search(grad_regex,string)

        grad = [float(i) for i in match.group(1).split()]

        return grad

    def get_energy(self, string):
        energy_pattern = r'[^\S\r\n]*\$energy\s+([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)$'
        energy_regex = re.compile(energy_pattern,re.IGNORECASE|re.MULTILINE)

        match = re.search(energy_regex,string)

        energy = float(match.group(1))

        return energy
    
    def get_hessian(self, string):
        hess_pattern = r'[^\S\r\n]*\$hessian\s+((?:.|\n)*)$'
        hess_regex = re.compile(hess_pattern,re.IGNORECASE|re.MULTILINE)

        match = re.search(hess_regex,string)

        hess_list = [float(i) for i in match.group(1).split()]
        hess_arr  = np.array(hess_list)

        size = int(np.sqrt(len(hess_arr)))
        hess = np.reshape(hess_arr, (size, size))
    
        return hess