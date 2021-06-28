#!/bin/bash

###############################################################################
# (2018) Asteroid Impact (3D) (Temporal Subsampling)
###############################################################################

mkdir 2018_asteroid_impact_3D_temporal_subsampling
cd 2018_asteroid_impact_3D_temporal_subsampling

mkdir nonProcessed
mkdir processed

#for ts in 01141 03429 05700 07920 09782 13306 16317 18124 19599 21255 28649 31737 34654 37273 39476 44229 45793 47190 48557 49978; do
  #wget https://oceans11.lanl.gov/deepwaterimpact/yA31/300x300x300-FourScalars_resolution/pv_insitu_300x300x300_$ts.vti
  #mv pv_insitu_300x300x300_$ts.vti ./nonProcessed/
#done

cd nonProcessed

gdown https://drive.google.com/uc?id=1MPYTRxi8ecZUqnthrUmxewtkQcEWYnZE
tar -xf 2018_asteroid_impact_3D_temporal_subsampling.tar.xz
rm 2018_asteroid_impact_3D_temporal_subsampling.tar.xz

cd ..

pvpython dataAsteroidImpactTS.py

cd ..
