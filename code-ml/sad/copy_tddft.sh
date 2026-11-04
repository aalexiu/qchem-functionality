#!/bin/bash

mkdir copy-tddft

for i in {1..5};
do
index=$((20*$i));

cd cd38se38_TDDFT_$index

index2=$((0+$index));

cp cd38se38_tddft.out ../copy-tddft/cd38se38_tddft_$index2.out
cd ..

echo $index2 finished

done
