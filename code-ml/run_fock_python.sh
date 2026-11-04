#!/bin/bash

module load cpu/0.17.3b
module load gcc/10.2.0/npcyll4
module load py-numpy/1.20.3/4o6jrav

mkdir fock

python3 fock.py