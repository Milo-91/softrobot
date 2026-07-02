#! /bin/bash


for i in {1..3}; do python Search.py -A ES -e 10000 -d log/20260702/from_eclab/1/ --popsize 20 --lamb 5 --mutation_size 1 --numprocs 20 world/evogym_world/T_world/ObstacleTraverser-v1T.json basicrobot; done &
for i in {1..3}; do python Search.py -A ES -e 10000 -d log/20260702/from_eclab/2/ --popsize 20 --lamb 5 --mutation_size 2 --numprocs 20 world/evogym_world/T_world/ObstacleTraverser-v1T.json basicrobot; done &
for i in {1..3}; do python Search.py -A ES -e 10000 -d log/20260702/from_eclab/3/ --popsize 20 --lamb 5 --mutation_size 3 --numprocs 20 world/evogym_world/T_world/ObstacleTraverser-v1T.json basicrobot; done &
for i in {1..3}; do python Search.py -A ES -e 10000 -d log/20260702/from_eclab/4/ --popsize 20 --lamb 5 --mutation_size 4 --numprocs 20 world/evogym_world/T_world/ObstacleTraverser-v1T.json basicrobot; done &
for i in {1..3}; do python Search.py -A ES -e 10000 -d log/20260702/from_eclab/5/ --popsize 20 --lamb 5 --mutation_size 5 --numprocs 20 world/evogym_world/T_world/ObstacleTraverser-v1T.json basicrobot; done &
