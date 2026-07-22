#! /bin/bash

# GA robust
for i in {1..5}; do python Search.py -A GA -e 5000 -d log/20260721/robust/Hurdler-v0T/GA/ --popsize 100 --numprocs 32 --strong_evluation world/evogym_world/T_world/Hurdler-v0T.json  basicrobot; done
for i in {1..5}; do python Search.py -A GA -e 5000 -d log/20260721/robust/UpStepper-v0T/GA/ --popsize 100 --numprocs 32 --strong_evluation world/evogym_world/T_world/UpStepper-v0T.json  basicrobot; done
