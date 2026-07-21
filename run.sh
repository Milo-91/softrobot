#! /bin/bash

# GA+Init_pop
for i in {1..10}; do python Search.py -A GA --init_pop LS -L HC --pre_step 2000 -e 10000 -d log/20260721/popsize100/Climber-v0T/GA+Init_pop/ --popsize 100 --numprocs 16 world/evogym_world/T_world/Climber-v0T.json  basicrobot; done
for i in {1..10}; do python Search.py -A GA --init_pop LS -L HC --pre_step 2000 -e 10000 -d log/20260721/popsize100/ObstacleTraverser-v0T/GA+Init_pop/ --popsize 100 --numprocs 16 world/evogym_world/T_world/ObstacleTraverser-v0T.json  basicrobot; done
for i in {1..10}; do python Search.py -A GA --init_pop LS -L HC --pre_step 2000 -e 10000 -d log/20260721/popsize100/ObstacleTraverser-v1T/GA+Init_pop/ --popsize 100 --numprocs 16 world/evogym_world/T_world/ObstacleTraverser-v1T.json  basicrobot; done
# MA+HC
for i in {1..5}; do python Search.py -A MA -L HC -e 10000 -d log/20260721/popsize100/ObstacleTraverser-v0T/MA+HC/ --popsize 100 --numprocs 16 world/evogym_world/T_world/ObstacleTraverser-v0T.json  basicrobot; done
for i in {1..5}; do python Search.py -A MA -L HC -e 10000 -d log/20260721/popsize100/ObstacleTraverser-v1T/MA+HC/ --popsize 100 --numprocs 16 world/evogym_world/T_world/ObstacleTraverser-v1T.json  basicrobot; done
for i in {1..5}; do python Search.py -A MA -L HC -e 10000 -d log/20260721/popsize100/Climber-v0T/MA+HC/ --popsize 100 --numprocs 16 world/evogym_world/T_world/Climber-v0T.json  basicrobot; done
# GA
for i in {1..5}; do python Search.py -A GA -e 10000 -d log/20260721/popsize100/ObstacleTraverser-v0T/GA/ --popsize 100 --numprocs 16 world/evogym_world/T_world/ObstacleTraverser-v0T.json  basicrobot; done
for i in {1..5}; do python Search.py -A GA -e 10000 -d log/20260721/popsize100/ObstacleTraverser-v1T/GA/ --popsize 100 --numprocs 16 world/evogym_world/T_world/ObstacleTraverser-v1T.json  basicrobot; done
for i in {1..5}; do python Search.py -A GA -e 10000 -d log/20260721/popsize100/Climber-v0T/GA/ --popsize 100 --numprocs 16 world/evogym_world/T_world/Climber-v0T.json  basicrobot; done
