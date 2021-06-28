#!/bin/bash

###############################################################################
# (2015) Dark matter (3D)
###############################################################################

# You will need:
# - python-dev (sudo apt-get install python-dev)
# - python2 with packages (sudo apt-get install python2)
# --- numpy (pip2 install numpy)
# --- vtk (pip2 install vtk)
# --- Cython (pip2 install Cython)
# --- sdfpy (pip2 install sdfpy)
# --- sdf (pip2 install sdf)

mkdir 2015_dark_matter_3D
cd 2015_dark_matter_3D

mkdir nonProcessed
mkdir processed

for ts in 0.0200 0.0300 0.0400 0.0500 0.0600 0.0700 0.0800 0.0900 0.1000 0.1100 0.2700 0.2800 0.2900 0.3000 0.3100 0.3200 0.3300 0.3400 0.3500 0.3600 0.5900 0.6000 0.6100 0.6200 0.6300 0.6400 0.6500 0.6600 0.6700 0.6800 0.9100 0.9200 0.9300 0.9400 0.9500 0.9600 0.9700 0.9800 0.9900 1.0000; do
  wget https://darksky.slac.stanford.edu/scivis2015/data/ds14_scivis_0128/ds14_scivis_0128_e4_dt04_$ts
  python2 vtkDarkSkyParticles.py ds14_scivis_0128_e4_dt04_$ts
  rm ds14_scivis_0128_e4_dt04_$ts 
  mv ds14_scivis_0128_e4_dt04_$ts.vtp ./nonProcessed/
done

pvpython dataDarkMatter.py

cd ..
