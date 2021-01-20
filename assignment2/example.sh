#!/bin/bash

#./example.sh > example.txt

echo "Hello world" > example.txt
echo "This is the last line" >> example.txt

tag=$( tail -n 1 example.txt )

declare -i counter=0
(( counter=counter+3 ))



start=$(sed ''`expr ${counter} + 1`'q;d' example.txt)
echo $start

echo $counter


echo $tag
