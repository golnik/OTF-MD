import numpy as np
import sys
import re

A2bohr = 1.8897259886

class HarmonicPotential:
    def __init__(self,q0,E,G,H):
        self.q0 = q0
        self.E = E
        self.G = G
        self.H = H
    
    def V(self,q):
        qq0 = q-q0
        V = self.E + G.dot(qq0) + 0.5 * qq0.dot(H.dot(qq0))
        return V[0]

    def grad(self,q):
        qq0 = q-q0
        return G + 0.5 * H.dot(qq0) + 0.5 * qq0.dot(H)

#function to read geometry file
def read_geom_xyz(fname_xyz):
    inp_xyz = open(fname_xyz,'r')

    lines_xyz = inp_xyz.readlines()
    lines_xyz = lines_xyz[2:]

    atoms  = []
    coords = []

    for line in lines_xyz:
        data = line.split()

        atoms.append(data[0])

        for i_coord in range(3):
            coords.append(float(data[i_coord+1])*A2bohr)

    inp_xyz.close()
    
    natoms = len(atoms)
    
    return natoms,coords

#function to read abinitio data
def read_abinitio(fname):
    with open(fname,'r') as file:
        content = file.read()
    
    pattern_tmp = '%s([^n]+?)\$END'
    
    geom_str  = re.search(pattern_tmp % "\$geom"     ,content).group(1)
    pot_str   = re.search(pattern_tmp % "\$potential",content).group(1)
    force_str = re.search(pattern_tmp % "\$force"    ,content).group(1)
    hess_str  = re.search(pattern_tmp % "\$hessian"  ,content).group(1)
    
    geom_data  = np.asarray([float(i)*A2bohr for i in geom_str.split()])
    pot_data   = np.asarray([float(i) for i in pot_str.split()])
    force_data = np.asarray([float(i) for i in force_str.split()])
    hess_data  = np.asarray([float(i) for i in hess_str.split()])

    ncoords = len(geom_data)
    
    hess_data = np.reshape(hess_data, (ncoords,ncoords))

    return geom_data,pot_data,force_data,hess_data

geom_xyz = sys.argv[1]  #get geometry file name
eg_out   = sys.argv[2]  #get EG output file name

#read abinitio data
q0,E,G,H = read_abinitio("abinitio_EGH.dat")

#read geometry
natoms,coords = read_geom_xyz(geom_xyz)

#create harmonic potential
HP = HarmonicPotential(q0,E,G,H)

#compute energy and gradient
V = HP.V(coords)
grad = HP.grad(coords)

#write EG output file
with open(eg_out,'w') as file:
    file.write("$energy\n")
    file.write(" %s\n" % V)
    file.write("$gradient\n")
    for icoord in range(len(coords)):
        file.write(" %s" % grad[icoord])
