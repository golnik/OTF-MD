#!/bin/bash -l

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load intel/18.0.5
module load intel-mpi/2018.4.274
module load python/3.7.3

geom_xyz=$1
geom_mol="geometry.mol"

script_template="scf_adc.in"

tmp_dir="$TMPDIR/EGHrun/calc/"

EGH_out=$2

source /home/ngolubev/Packages/virtualenv/x86_E5v4_Mellanox_intel/bin/activate
time srun python /home/ngolubev/programs/EGHrun/source/EGHrun.py -g $geom_xyz $geom_mol -rs $script_template -tdir $tmp_dir --calc_grad -EGH_out $EGH_out --z_sym

exit 0
