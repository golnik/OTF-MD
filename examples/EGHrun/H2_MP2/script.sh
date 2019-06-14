#!/bin/bash -l

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load intel/18.0.2
module load intel-mpi/2018.2.199
module load python/3.6.5

source /home/ngolubev/Packages/virtualenv/x86_E5v4_Mellanox_intel/bin/activate

geom_xyz=$1
geom_mol="/home/ngolubev/programs/OTF-MD/examples/EGHrun/H2/geometry.mol"

script_template="/home/ngolubev/programs/OTF-MD/examples/EGHrun/H2/scf_adc.in"

tmp_dir="$TMPDIR/EGHrun/calc/"

EGH_out=$2

time srun python /home/ngolubev/programs/EGHrun/source/EGHrun.py -g $geom_xyz $geom_mol -rs $script_template -tdir $tmp_dir --calc_grad -EGH_out $EGH_out

exit 0
