#! /bin/bash

for i in {1..10}; do python Search.py -A GA -e 10000 -d log/20260717/Robust/ObstacleTraverser-v1T/GA/ --popsize 100 --numprocs 12 --strong_evaluation world/evogym_world/T_world/ObstacleTraverser-v1T.json  basicrobot; done
for i in {1..10}; do python Search.py -A GA -e 10000 -d log/20260717/Robust/Climber-v0T/GA/ --popsize 100 --numprocs 12 --strong_evaluation world/evogym_world/T_world/Climber-v0T.json  basicrobot; done
for i in {1..10}; do python Search.py -A GA -e 10000 -d log/20260717/Robust/ObstacleTraverser-v0T/GA/ --popsize 100 --numprocs 12 --strong_evaluation world/evogym_world/T_world/ObstacleTraverser-v0T.json  basicrobot; done
