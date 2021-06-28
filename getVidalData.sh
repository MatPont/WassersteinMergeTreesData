#!/bin/bash

# You will need python and gdown library (pip install gdown) https://github.com/wkentaro/gdown
# or you can manually download the data at the google drive link below

if [ -f ./2014_isabel_3D/isabella_velocity_goodEnsemble.vti -a -f ./sea_surface_height/seaSurfaceHeightGoodEnsemble.vti -a -f ./starting_vortex/startingVortexGoodEnsemble.vti -a -f ./vortex_street/vortexStreetGoodEnsemble2.vti ]; then
  exit
fi

if [ ! -f data.zip ]; then
  gdown https://drive.google.com/uc?id=1fxPAUmYT4UAUHh7K0w83znckyw_NTLan
  gunzip data.zip
fi

mkdir 2004_isabel_3D
mv data/isabella_velocity_goodEnsemble.vti 2004_isabel_3D/

mkdir sea_surface_height
mv data/seaSurfaceHeightGoodEnsemble.vti sea_surface_height/

mkdir starting_vortex
mv data/startingVortexGoodEnsemble.vti starting_vortex/

mkdir vortex_street
mv data/vortexStreetGoodEnsemble2.vti vortex_street/

rm -r data/
