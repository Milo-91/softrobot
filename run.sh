#! /bin/bash

# Robust
for i in {1..10}; do python Search.py -A GA -e 10000 -d log/20260723/Robust/Climber-v0T/GA/ --strong_evaluation --popsize 100 --numprocs 30 world/evogym_world/T_world/Climber-v0T.json basicrobot; done
# Compare
for i in {1..10}; do python Search.py -A GA -e 10000 -d log/20260723/Compare/Climber-v0T/GA/ --popsize 100 --numprocs 30 world/evogym_world/T_world/Climber-v0T.json basicrobot; done

for i in {1..5}; do python Search.py -A GA --init_pop LS -L ES --pre_step 2000 -e 10000 -d log/20260723/popsize100/Climber-v0T/GA+Init_pop(ES)/ --popsize 100 --numprocs 30 world/evogym_world/T_world/Climber-v0T.json basicrobot; done
for i in {1..5}; do python Search.py -A GA --init_pop LS -L ES --pre_step 2000 -e 10000 -d log/20260723/popsize100/ObstacleTraverser-v0T/GA+Init_pop(ES)/ --popsize 100 --numprocs 30 world/evogym_world/T_world/ObstacleTraverser-v0T.json basicrobot; done
for i in {1..5}; do python Search.py -A GA --init_pop LS -L ES --pre_step 2000 -e 10000 -d log/20260723/popsize100/ObstacleTraverser-v1T/GA+Init_pop(ES)/ --popsize 100 --numprocs 30 world/evogym_world/T_world/ObstacleTraverser-v1T.json basicrobot; done
