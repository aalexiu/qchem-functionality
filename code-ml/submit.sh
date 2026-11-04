#!/bin/bash

#SBATCH -J cd60-min-aimd
#SBATCH -o test.log
#SBATCH -e test.log
#SBATCH --partition=shared
#SBATCH --mem=100000
#SBATCH -t 48:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH --account=mit178

module purge
module load cpu/0.15.4
module load gcc/10.2.0
module load mvapich2/2.3.6
module load qchem/6.0.2

export QCSCRATCH=/scratch/$USER/job_$SLURM_JOB_ID

scratch="scratch_c60_aimd_2"     #name of directory where to read scratch files from (for SCF_GUESS)
                                    
scratch2="scratch_c60_aimd_3"    # name of the directory to save your scratch files to

curr_d=$PWD             # current directory, where you submit the job from

rm -r $QCSCRATCH/$scratch
cp -r $scratch $QCSCRATCH

qchem -save -nt 48 aimd.in aimd.out $scratch

rm -r $curr_d/$scratch2             # remove pre-existing scratch files with the
                                    # same name from your current directory

cp -r $QCSCRATCH/$scratch $curr_d/$scratch2  # copy new scratch files back to home