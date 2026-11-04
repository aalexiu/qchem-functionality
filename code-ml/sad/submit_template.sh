#!/bin/bash

#SBATCH -J c60-sad
#SBATCH -o sad.log
#SBATCH -e sad.log
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

qchem -nt 48 sad.in sad.out