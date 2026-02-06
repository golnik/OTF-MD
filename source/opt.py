import numpy as np

from input import InputParams
from input import Input
from geometry import Geometry
from externalrun import ExternalRun

def Optimize(geom,erun,input):

    Nsteps = 10

    for istep in range(Nsteps):
        print("Optimization step %s" % istep)

    print("Optimization completed! [not really :)]")

    return