world = ObstacleTraverser-v1T.json
evo_step = 10000
popsize = 100
log_file = 20260623/$popsize
numprocs = 7


python Search.py -A GA -e $evo_step -p $log_file --popsize $popsize --pop_shrink --numprocs $numprocs --rho $rho --tau $tau log/evogym_world/T_world/$world basicrobot
