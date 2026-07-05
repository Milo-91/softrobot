#! /bin/bash

for i in {1..10}; do python Search.py -A GA+ES -L ES -e 10000 -d log/20260706/Robust/ObstacleTraverser-v1T/GA+ES/ --popsize 100 --mu 20 --lamb 5 --mutation_size 2 --numprocs 16 --strong_evaluation world/evogym_world/T_world/ObstacleTraverser-v1T.json  basicrobot; done
for i in {1..10}; do python Search.py -A GA+ES -L ES -e 10000 -d log/20260706/Robust/Climber-v0T/GA+ES/ --popsize 100 --mu 20 --lamb 5 --mutation_size 2 --numprocs 16 --strong_evaluation world/evogym_world/T_world/Climber-v0T.json  basicrobot; done
