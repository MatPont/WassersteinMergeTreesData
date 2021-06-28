#!/bin/bash

###############################################################################
# (2016) Viscous fingering (3D)
###############################################################################

mkdir 2016_viscous_fingering_3D
cd 2016_viscous_fingering_3D

mkdir nonProcessed
mkdir processed

for name in 0.20/020 0.30/030 0.44/044; do
  runTodo="01 02 03 04 05"
  if [ "$name" == "0.20/020" ]; then
    runTodo="01 03 04 05 06" # run 02 is not available for 0.20/020 configuration
  fi
  for run in $runTodo; do
    if [ "$name" == "0.20/020" ]; then
      postfix="_2"
    else
      postfix=""
    fi
    wget https://cloud.sdsc.edu/v1/AUTH_sciviscontest/2016/smoothinglength_${name}_run${run}$postfix.tar.bz2
    preName=`echo $name | cut -d'/' -f 1`
    postName=`echo $name | cut -d'/' -f 2`
    tar -xjf ${postName}_run${run}$postfix.tar.bz2
    mv smoothinglength_$preName/run$run/120.vtu ./nonProcessed/${preName}_run${run}_120.vtu
    rm ${postName}_run${run}$postfix.tar.bz2
    rm -r smoothinglength_$preName/
  done
done

pvpython dataViscousFingering.py

cd ..

