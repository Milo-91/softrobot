#! /bin/bash

for i in {1..5}; do python Search.py -A GA -e 5000 -d log/20260721/Compare/Hurdler-v0T/GA/ --popsize 100 --numprocs 12 world/evogym_world/T_world/Hurdler-v0T.json  basicrobot; done
for i in {1..5}; do python Search.py -e 300 -A GA -e 5000 -d log/20260721/Compare/UpStepper-v0T/GA/ --popsize 100 --numprocs 12 world/evogym_world/T_world/UpStepper-v0T.json  basicrobot; done
# GA robust
for i in {1..5}; do python Search.py -A GA -e 5000 -d log/20260721/robust/Hurdler-v0T/GA/ --popsize 100 --numprocs 12 --strong_evluation world/evogym_world/T_world/Hurdler-v0T.json  basicrobot; done
for i in {1..5}; do python Search.py -e 300 -A GA -e 5000 -d log/20260721/robust/UpStepper/GA/ --popsize 100 --numprocs 12 --strong_evluation world/evogym_world/T_world/UpStepper-v0T.json  basicrobot; done
for i in {1..5}; do python Search.py -A GA -e 5000 -d log/20260721/robust/ObstacleTraverser-v0T/GA/ --popsize 100 --numprocs 12 --strong_evaluation world/evogym_world/T_world/ObstacleTraverser-v0T.json  basicrobot; done
for i in {1..10}; do python Search.py -A GA -e 5000 -d log/20260721/robust/Climber-v0T/GA/ --popsize 100 --numprocs 12 --strong_evaluation world/evogym_world/T_world/Climber-v0T.json  basicrobot; done
