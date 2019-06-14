#!/bin/bash -l

module purge
module load intel/18.0.2
module load python/3.6.5

source /home/ngolubev/Packages/virtualenv/x86_E5v4_Mellanox_intel/bin/activate
python ../../source/OTF-MD.py example.ini

exit 0
