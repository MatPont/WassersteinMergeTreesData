#!/bin/bash

###############################################################################
# (2018) Asteroid Impact (3D) (clustering)
###############################################################################

mkdir 2018_asteroid_impact_3D_clustering
cd 2018_asteroid_impact_3D_clustering

mkdir nonProcessed
mkdir processed

#for ts in yA11,34883 yA31,49978 yA32,220062 yB11,37894 yB31,46521 yC11,30975 yC31,48663; do
  #name=`echo $ts | cut -d',' -f 1`
  #ts=`echo $ts | cut -d',' -f 2`
  #wget https://oceans11.lanl.gov/deepwaterimpact/$name/300x300x300-FourScalars_resolution/pv_insitu_300x300x300_$ts.vti
  #mv pv_insitu_300x300x300_$ts.vti ./nonProcessed/pv_insitu_300x300x300_${name}_$ts.vti
#done

cd nonProcessed

gdown https://drive.google.com/uc?id=1aDJ9VbjGutVVct8mALDG5AJMpCWz61td
tar -xf 2018_asteroid_impact_3D_clustering.tar.xz
rm 2018_asteroid_impact_3D_clustering.tar.xz

cd ..

pvpython dataAsteroidImpact.py

cd ..
