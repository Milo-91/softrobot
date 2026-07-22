#! /bin/bash

# MA+ES
for i in {1..5}; do python Search.py -A MA -L ES -e 10000 -d log/20260722/ObstacleTraverser-v0T/MA+ES/ --popsize 100 --numprocs 30 world/evogym_world/T_world/ObstacleTraverser-v0T.json basicrobot; done
for i in {1..5}; do python Search.py -A MA -L ES -e 10000 -d log/20260722/ObstacleTraverser-v1T/MA+ES/ --popsize 100 --numprocs 30 world/evogym_world/T_world/ObstacleTraverser-v1T.json basicrobot; done
for i in {1..5}; do python Search.py -A MA -L ES -e 10000 -d log/20260722/Climber-v0T/MA+ES/ --popsize 100 --numprocs 30 world/evogym_world/T_world/Climber-v0T.json basicrobot; done
