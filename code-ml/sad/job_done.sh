#!/bin/bash

for i in {1..500};
do

cd $i

echo $i
echo $i success | grep "Thank" sad.out

cd ..

done
