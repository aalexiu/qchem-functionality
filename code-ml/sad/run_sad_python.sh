#!/bin/bash

module load cpu/0.17.3b
module load gcc/10.2.0/npcyll4
module load py-numpy/1.20.3/4o6jrav

mkdir sad_files

for i in {1..500};
do

index=$((0 + i));

cd $i
cp ../sad.py .

python3 sad.py

cp ./sad.npy ../sad_files/sad_$index.npy

cd ..

echo $index finished

done
