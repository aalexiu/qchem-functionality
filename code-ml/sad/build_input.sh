#!/bin/bash

for i in {1..500};
do

python3 qchem_out_to_in.py $i

mkdir $i
mv sad.in $i

python3 change_filename.py $i

mv ./submit.sh ./$i

echo $i finished

done
