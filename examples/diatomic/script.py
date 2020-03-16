import numpy as np
import sys

r0 = 1.8

def V(x,y,z):
    r=np.sqrt(x**2 + y**2 + z**2)
    return (r-r0)**2

def grad(dx,dy,dz):
    r=np.sqrt(dx**2 + dy**2 + dz**2)

    gx = 2.*dx*(r-r0)/r
    gy = 2.*dy*(r-r0)/r
    gz = 2.*dz*(r-r0)/r

    return gx,gy,gz

#function to read geometry file
def read_geom(fname):
    with open(fname,'r') as file:
        lines_xyz = file.readlines()
        lines_xyz = lines_xyz[2:]
    
    x = []
    y = []
    z = []
    
    for line in lines_xyz:
        data = line.split()
        x.append(float(data[1]))
        y.append(float(data[2]))
        z.append(float(data[3]))

    dx = x[0]-x[1]
    dy = y[0]-y[1]
    dz = z[0]-z[1]
    
    return dx,dy,dz
    
geom_xyz = sys.argv[1]
eg_out   = sys.argv[2]

dx,dy,dz = read_geom(geom_xyz)

gx,gy,gz = grad(dx,dy,dz)

with open(eg_out,'w') as file:
    file.write("$energy\n")
    file.write(" %s\n" % V(dx,dy,dz))
    file.write("$gradient\n")
    file.write(" %s %s %s" % (gx,gy,gz))
    file.write(" %s %s %s\n" % (-gx,-gy,-gz))
