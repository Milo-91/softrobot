#! /bin/bash

for i in {1..3}; do python Search.py -A MA -e 10000 -d log/20260705/popsize100/ObstacleTraverser-v0T/MA+ESa/ --popsize 100 --mu 20 --lamb 5 --mutation_size 2 --numprocs 16 -L ES world/evogym_world/T_world/ObstacleTraverser-v0T.json  basicrobot; done
for i in {1..3}; do python Search.py -A MA -e 10000 -d log/20260705/popsize100/ObstacleTraverser-v1T/MA+ESa/ --popsize 100 --mu 20 --lamb 5 --mutation_size 2 --numprocs 16 -L ES world/evogym_world/T_world/ObstacleTraverser-v1T.json  basicrobot; done
for i in {1..3}; do python Search.py -A MA -e 10000 -d log/20260705/popsize100/Climber-v0T/MA+ESa/ --popsize 100 --mu 20 --lamb 5 --mutation_size 2 --numprocs 16 -L ES world/evogym_world/T_world/Climber-v0T.json  basicrobot; done
