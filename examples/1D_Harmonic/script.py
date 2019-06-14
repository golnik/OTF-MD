import numpy as np
import sys

#potential
def V(x):
    return x**2

#gradient
def grad(x):
    return 2.*x

#function to read geometry file
def read_geom(fname):
    with open(fname,'r') as file:
        lines_xyz = file.readlines()
        lines_xyz = lines_xyz[2]
    x = float(lines_xyz.split()[1])
    
    A2bohr = 1.8897259886
    x *= A2bohr
    
    return x

geom_xyz = sys.argv[1]  #get geometry file name
eg_out   = sys.argv[2]  #get EG output file name

#read geometry and return x position
x = read_geom(geom_xyz)

#write EG output file
with open(eg_out,'w') as file:
    file.write("$energy\n")
    file.write(" %s\n" % V(x))
    file.write("$gradient\n")
    file.write(" %s 0.0 0.0\n" % grad(x))
