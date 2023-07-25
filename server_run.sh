#!/bin/bash
for i in 2
do
   for gpu in 0 1 3 4 5 6 7
   do
    docker compose run --name "elena_neurom_product_GPU$gpu""_$i" -d -e CUDA_VISIBLE_DEVICES="$gpu" neuromod_production
   done
done