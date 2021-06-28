#!/bin/bash

###############################################################################
# (2006) Earthquake (3D)
###############################################################################

mkdir 2006_earthquake_3D
cd 2006_earthquake_3D

mkdir nonProcessed
mkdir processed

cd nonProcessed

for ts in 002700 002900 003100 003300 007700 007900 008100 008300 011700 011900 012100 012300; do
  wget https://cloud.sdsc.edu/v1/AUTH_sciviscontest/2006/data_files/TS21z_X_R2_$ts.gz
  wget https://cloud.sdsc.edu/v1/AUTH_sciviscontest/2006/data_files/TS21z_Y_R2_$ts.gz
  wget https://cloud.sdsc.edu/v1/AUTH_sciviscontest/2006/data_files/TS21z_Z_R2_$ts.gz
  gunzip TS21z_X_R2_$ts.gz
  gunzip TS21z_Y_R2_$ts.gz
  gunzip TS21z_Z_R2_$ts.gz
done

cd ..

pvpython dataEarthquake.py

cd ..
