#!/bin/bash

###############################################################################
# (2008) Ionization front (2D)
###############################################################################

mkdir 2008_ionization_front_2D
cd 2008_ionization_front_2D

mkdir nonProcessed
mkdir processed

wget https://cloud.sdsc.edu/v1/AUTH_sciviscontest/2008/data_files/zslices.multifield.zip
unzip zslices.multifield.zip

wget https://cloud.sdsc.edu/v1/AUTH_sciviscontest/2008/Data/density_to_vtk.c
gcc density_to_vtk.c -o density_to_vtk

for ts in 0025 0026 0027 0028 0075 0076 0077 0078 0125 0126 0127 0128 0175 0176 0177 0178; do
  ./density_to_vtk ./multifield.$ts.zslice.txt
  mv multifield.$ts.zslice.txt.density.vtk ./nonProcessed/
done

rm zslices.multifield.zip
rm multifield.*.zslice.txt
rm density_to_vtk.c density_to_vtk

pvpython dataIonizationFront2D.py

cd ..
