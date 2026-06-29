import subprocess
import time



if __name__ == '__main__':
    algorithm = "GA"
    local_search = "HC"
    sim_step = "400"
    evo_step = "10000"
    popsize = "100"
    # tasks = ["ObstacleTraverser-v0T.json", "ObstacleTraverser-v1T.json", "Climber-v0T.json"]
    tasks = ["Climber-v0T.json"]
    logdir = f"log/20260629/popsize{popsize}/"
    numprocs = "16" #TODO change it on server
    
    sim_list = [
        (0.9, 8.0),
        (0.3, 32),
        (0.5, 0.5),
        (1, 0)
    ]

    strat_time = time.time()

    import_from_list = True
    if import_from_list:
        for task in tasks:
            for sim in sim_list:
                sub_logdir = f'{logdir}/{task[:-5]}/r{sim[0]}_t{sim[1]}/'
                for i in range(5):
                    if local_search == None:
                        filename = f'{sub_logdir}{task[:-5]}_{algorithm}_{popsize}_{time.strftime("%m%d%H%M")}_{rho}_{tau}'
                    else:
                        filename = f'{sub_logdir}{task[:-5]}_{algorithm}_{local_search}_{popsize}_{time.strftime("%m%d%H%M")}_{rho}_{tau}'
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
                            "--rho", str(sim[0]),
                            "--tau", str(sim[1]),
                            "--filename", filename,
                            "-L", local_search,
                            f"world/evogym_world/T_world/{task}",
                            "basicrobot",
                        ])
    else:
        for task in tasks:
            rho = 0.3
            while rho < 1: 
                tau = 0.5
                while tau <= 32:
                    sub_logdir = f'{logdir}/{task[:-5]}/r{rho}_t{tau}/'
                    for i in range(5):
                        if local_search == None:
                            filename = f'{sub_logdir}{task[:-5]}_{algorithm}_{popsize}_{time.strftime("%m%d%H%M")}_{rho}_{tau}'
                        else:
                            filename = f'{sub_logdir}{task[:-5]}_{algorithm}_{local_search}_{popsize}_{time.strftime("%m%d%H%M")}_{rho}_{tau}'
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
                            f"world/evogym_world/T_world/{task}",
                            "basicrobot",
                        ])
                    
                    # update tau
                    tau = round(tau * 4, 5)
                # update rho
                rho = round(rho + 0.2, 1)

        rho = 1
        tau = 0
        sub_logdir = f'{logdir}/{task[:-5]}/r{1}_t{0}/'
        for i in range(5):
            if local_search == None:
                filename = f'{sub_logdir}{task[:-5]}_{algorithm}_{popsize}_{time.strftime("%m%d%H%M")}_{rho}_{tau}'
            else:
                filename = f'{sub_logdir}{task[:-5]}_{algorithm}_{local_search}_{popsize}_{time.strftime("%m%d%H%M")}_{rho}_{tau}'
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
    end_time = time.time()
    print(f'time: {end_time - start_time}')
