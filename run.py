import subprocess
import time

if __name__ == '__main__':
    algorithm = "GA"
    local_search = None
    sim_step = "400"
    evo_step = "100"
    popsize = "10"
    tasks = ["ObstacleTraverser-v0T.json", "ObstacleTraverser-v1T.json", "Climber-v0T.json"]
    logdir = f"log/20260623/{popsize}/"
    numprocs = "7" #TODO change it on server
    
    for task in tasks:
        rho = 0.4
        while rho < 1: 
            tau = 0.5
            while tau <= 32:
                record_files = []
                sub_logdir = f'{logdir}/{task[:-5]}/r{rho}_t{tau}/'
                for i in range(5):
                    if local_search == None:
                        filename = f'{sub_logdir}{task[:-5]}_{algorithm}_{popsize}_{time.strftime("%m%d%H%M")}_{rho}_{tau}'
                    else:
                        filename = f'{sub_logdir}{task[:-5]}_{algorithm}_{local_search}_{popsize}_{time.strftime("%m%d%H%M")}_{rho}_{tau}'
                    record_files.append(filename)
                    print(f'[{i}/5]')
                    subprocess.run([
                        "python",
                        "Search.py",
                        "-A", algorithm,
                        "-s", sim_step,
                        "-e", evo_step,
                        "-d", sub_logdir,
                        "--popsize", popsize,
                        "--numprocs", numprocs,
                        "--rho", str(rho),
                        "--tau", str(tau),
                        "--filename", filename,
                        f"log/evogym_world/T_world/{task}",
                        "basicrobot",
                    ])
                
                # update tau
                tau *= 2
            # update rho
            rho += 0.2
