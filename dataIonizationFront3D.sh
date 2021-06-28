#!/bin/bash

###############################################################################
# (2008) Ionization front (3D)
###############################################################################

mkdir 2008_ionization_front_3D
cd 2008_ionization_front_3D

mkdir nonProcessed
mkdir processed

wget https://cloud.sdsc.edu/v1/AUTH_sciviscontest/2008/Data/density_to_vtk.c
gcc density_to_vtk.c -o density_to_vtk

for ts in 0025 0026 0027 0028 0075 0076 0077 0078 0125 0126 0127 0128 0175 0176 0177 0178; do
  wget https://cloud.sdsc.edu/v1/AUTH_sciviscontest/2008/data_files/multifield.$ts.txt.gz
  gunzip multifield.$ts.txt.gz
  ./density_to_vtk ./multifield.$ts.txt
  rm multifield.$ts.txt
  mv multifield.$ts.txt.density.vtk ./nonProcessed/
done

rm density_to_vtk.c density_to_vtk

pvpython dataIonizationFront3D.py

cd ..
