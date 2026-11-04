#!/bin/bash

mkdir out

for i in {1..5};
do
	index=$((20*$i));

	cd cd38se38_TDDFT_$index

	cp cd38se38_tddft.out ../out/cd38se38_tddft_$index.out
	cd ..

	echo $index finished

done

