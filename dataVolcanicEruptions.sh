#!/bin/bash

###############################################################################
# (2014) Volcanic Eruptions (2D)
###############################################################################

mkdir 2014_volcanic_eruptions_2D
cd 2014_volcanic_eruptions_2D

mkdir nonProcessed
mkdir processed

#for part in 0 1 2 3; do
#  wget https://cloud.sdsc.edu/v1/AUTH_sciviscontest/2014/data/viscontest14-airs_part$part.tar.bz2
#done
#cat viscontest14-airs_part* | tar xjf -

wget https://cloud.sdsc.edu/v1/AUTH_sciviscontest/2014/data/viscontest14-airs_part0.tar.bz2
tar -xjf viscontest14-airs_part0.tar.bz2
rm viscontest14-airs_part0.tar.bz2

for ts in 150_am 150_pm 151_am 151_pm 156_am 156_pm 157_am 157_pm 164_am 164_pm 165_am 165_pm; do 
  mv ./airs_part0/volcano_2011_$ts.vtk ./nonProcessed/
done

rm -r ./airs_part0/

pvpython dataVolcanicEruptions.py

cd ..

