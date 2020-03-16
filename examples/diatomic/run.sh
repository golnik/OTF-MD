#!/bin/bash -l

module purge
module load intel/18.0.5
module load python/3.7.3

source /home/ngolubev/Packages/virtualenv/x86_E5v4_Mellanox_intel/bin/activate
python ../../source/OTF-MD.py input.ini

exit 0
