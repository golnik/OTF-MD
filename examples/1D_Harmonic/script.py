import numpy as np
import sys

def V(x):
    return x**2

def grad(x):
    return 2.*x

#function to read geometry file
def read_geom(fname):
    with open(fname,'r') as file:
        lines_xyz = file.readlines()
        lines_xyz = lines_xyz[2]
    x = float(lines_xyz.split()[1])
    return x
    
geom_xyz = sys.argv[1]
eg_out   = sys.argv[2]

x = read_geom(geom_xyz)

with open(eg_out,'w') as file:
    file.write("$energy\n")
    file.write(" %s\n" % V(x))
    file.write("$gradient\n")
    file.write(" %s 0.0 0.0\n" % grad(x))