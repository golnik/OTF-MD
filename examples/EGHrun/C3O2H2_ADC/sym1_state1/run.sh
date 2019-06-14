#!/bin/bash -l

#SBATCH --nodes 5
#SBATCH --ntasks-per-node 7
#SBATCH --cpus-per-task 4
#SBATCH --time=24:00:00
#SBATCH --account=lcpt
#SBATCH --exclusive
#SBATCH --mem 8000mb

module purge
module load intel/18.0.2
module load python/3.6.5

source /home/ngolubev/Packages/virtualenv/x86_E5v4_Mellanox_intel/bin/activate
python /home/ngolubev/programs/OTF-MD/source/OTF-MD.py input.ini

exit 0
