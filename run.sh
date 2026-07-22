#! /bin/bash

for i in {1..5}; do python Search.py -A GA --init_pop LS -L HC -e 10000 --pre_step 10000 -d log/20260722/popsize100/ObstacleTraverser-v0T/HC/ --popsize 100 --numprocs 30 world/evogym_world/T_world/ObstacleTraverser-v0T.json basicrobot; done
for i in {1..5}; do python Search.py -A GA --init_pop LS -L HC -e 10000 --pre_step 10000 -d log/20260722/popsize100/ObstacleTraverser-v1T/HC/ --popsize 100 --numprocs 30 world/evogym_world/T_world/ObstacleTraverser-v1T.json basicrobot; done
