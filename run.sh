#! /bin/bash

for i in {1..10}; do python Search.py -A ES -e 10000 -d log/20260721/Robust/Climber-v0T/ES/ --popsize 100 --numprocs 32 --mu 20 --lamb 5 --mutation_size 2 world/evogym_world/T_world/Climber-v0T.json  basicrobot; done
for i in {1..10}; do python Search.py -A ES -e 10000 -d log/20260721/Robust/ObstacleTraverser-v0T/ES/ --popsize 100 --numprocs 32 --mu 20 --lamb 5 --mutation_size 2 world/evogym_world/T_world/ObstacleTraverser-v0T.json  basicrobot; done
for i in {1..10}; do python Search.py -A ES -e 10000 -d log/20260721/Robust/ObstacleTraverser-v1T/ES/ --popsize 100 --numprocs 32 --mu 20 --lamb 5 --mutation_size 2 world/evogym_world/T_world/ObstacleTraverser-v1T.json  basicrobot; done
