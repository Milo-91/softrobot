#! /bin/bash

for i in {1..5}; do python Search.py -A MA -L HC -e 10000 -d log/20260702/popsize100/Climber-v0T/HC/ --mutation_size 2 --popsize 100 --numproc 16 world/evogym_world/T_world/Climber-v0T.json basicrobot; done
for i in {1..5}; do python Search.py -A MA -L TS -e 10000 -d log/20260702/popsize100/ObstacleTraverser-v1T/TS/ --mutation_size 2 --popsize 100 --numproc 16 world/evogym_world/T_world/ObstacleTraverser-v1T.json basicrobot; done
for i in {1..5}; do python Search.py -A MA -L TS -e 10000 -d log/20260702/popsize100/Climber-v0T/TS/ --mutation_size 2 --popsize 100 --numproc 16 world/evogym_world/T_world/Climber-v0T.json basicrobot; done
for i in {1..5}; do python Search.py -A MA -L HC -e 10000 -d log/20260702/popsize100/ObstacleTraverser-v0T/HC/ --mutation_size 2 --popsize 100 --numproc 16 world/evogym_world/T_world/ObstacleTraverser-v0T.json basicrobot; done
for i in {1..5}; do python Search.py -A MA -L TS -e 10000 -d log/20260702/popsize100/ObstacleTraverser-v0T/TS/ --mutation_size 2 --popsize 100 --numproc 16 world/evogym_world/T_world/ObstacleTraverser-v0T.json basicrobot; done
