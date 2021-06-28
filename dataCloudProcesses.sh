#!/bin/bash

###############################################################################
# (2017) Cloud processes (2D)
###############################################################################

mkdir 2017_cloud_processes_2D
cd 2017_cloud_processes_2D

mkdir nonProcessed
mkdir processed

cd nonProcessed

gdown https://drive.google.com/uc?id=1VY16BAxLP9nhz4DZleJVf_43I3HlLTJZ
tar -xf 2017_cloud_processes_2D.tar.xz
rm 2017_cloud_processes_2D.tar.xz

cd ..

pvpython dataCloudProcesses.py

cd ..
