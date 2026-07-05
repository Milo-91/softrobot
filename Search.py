import time, os, random
import importlib, json, csv
from multiprocessing import Pool, Value, Manager
import numpy as np
import EC_algorithms as EC
from EC_algorithms.logger import Logger
from EC_algorithms.local_search.hill_climbing import HillClimbing
from EC_algorithms.local_search.tabu_search import TabuSearch
from EC_algorithms.local_search.evolution_strategy import EvolutionStrategy
from evaluation.evaluate import Evaluator

from optparse import OptionParser
from tqdm import tqdm


class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.

    Adapted from:
    https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)

def mean(l):
  return sum(l)/len(l)


def random_search(robot_m, world, options, prefix, logger):
  best_robot = None
  best_score = None


  rep = 0
  meantime = []

  while rep < options.evo_step:  
    paramlist = []
    for _ in range(options.numprocs):
      paramlist.append((robot_m.get_random(), world, options.sim_step))

    with Pool(options.numprocs) as p:
      scores = p.starmap(evaluate, paramlist)

    rep += options.numprocs

    for _ in scores:
      meantime.append(_[1])

    # print(paramlist)
    # print(f"Mean sim time at {rep}: {mean(meantime)}")


    best_index = scores.index(max(scores))

    if (best_robot is None or best_score < scores[best_index][0]):
      best_score = scores[best_index][0]
      best_robot = paramlist[best_index][0]
      print(f"New best score at evaluation {rep}: {best_score}")
      best_robot.save_json(f"{prefix}_robot_{rep:05}.json")

  return meantime

def ES_search(robot_m, world, options, prefix, logger, pbar):
  evaluator = Evaluator(world, options.sim_step, options.evo_step, options.strong_evaluation)
  
  pbar.set_description(f"{pbar.desc.split('/')[0]}/({options.popsize},{options.lamb})-{options.search_algorithm}")
  pbar.set_postfix_str(f'best_robot: 0 sigma: {options.mutation_size}')
  return EC.ES.Search(robot_m, options, prefix, evaluator, None, logger, pbar)



def GA_search(robot_m, world, options, prefix, logger, pbar):
  evaluator = Evaluator(world, options.sim_step, options.evo_step, options.strong_evaluation)
  local_search_algorithms = {
    "HC": HillClimbing,
    "TS": TabuSearch
  }
  if options.local_search_algorithm != None:
    local_search = local_search_algorithms[options.local_search_algorithm](evaluator, options.lamb, options.mutation_size)
  else:
    local_search = None

  return EC.GA.Search(robot_m, options, prefix, evaluator, local_search, logger, pbar)



def MA_search(robot_m, world, options, prefix, logger, pbar):
  evaluator = Evaluator(world, options.sim_step, options.evo_step, options.strong_evaluation)
  local_search_algorithms = {
    "HC": HillClimbing,
    "TS": TabuSearch,
    "ES": EvolutionStrategy,
  }
  if options.local_search_algorithm == 'ES':
    local_search = local_search_algorithms[options.local_search_algorithm](evaluator, options.mu, options.lamb, options.numprocs, options.mutation_size)
  elif options.local_search_algorithm == None:
    print("MA need local search")
    exit(1)
  else:
    local_search = local_search_algorithms[options.local_search_algorithm](evaluator, options.lamb, options.mutation_size)

  return EC.MA.Search(robot_m, options, prefix, evaluator, local_search, logger, pbar)



def GA_ES_search(robot_m, world, options, prefix, logger, pbar):
  evaluator = Evaluator(world, options.sim_step, options.evo_step, options.strong_evaluation, options.strong_evaluation, options.strong_evaluation, options.strong_evaluation, options.strong_evaluation, options.strong_evaluation, options.strong_evaluation, options.strong_evaluation, options.strong_evaluation)
  local_search_algorithms = {
    "ES": EvolutionStrategy,
  }
  if options.local_search_algorithm == 'ES':
    local_search = local_search_algorithms[options.local_search_algorithm](evaluator, options.mu, options.lamb, options.numprocs, options.mutation_size)
  else:
    print("GA+ES need ES local search")
    exit(1)

  return EC.GA_ES.Search(robot_m, options, prefix, evaluator, local_search, logger, pbar)



def GA_Post_LS_search(robot_m, world, options, prefix, logger, pbar):
  evaluator = Evaluator(world, options.sim_step, options.evo_step + options.post_step, options.strong_evaluation)
  local_search_algorithms = {
    "HC": HillClimbing,
    "TS": TabuSearch
  }
  if options.local_search_algorithm != None:
    local_search = local_search_algorithms[options.local_search_algorithm](evaluator, options.lamb, options.mutation_size)
  else:
    print("MA need local search")
    exit(1)

  return EC.GA_Post_LS.Search(robot_m, options, prefix, evaluator, local_search, logger, pbar)



def main():
  options, args = parse_args()

  if not os.path.exists(options.logdir):
    os.makedirs(options.logdir, exist_ok=True)


  today  = time.strftime("%m%d%H%M")
  if options.filename == None:
    if options.local_search_algorithm != None:
      prefix = f"{options.logdir}{os.sep}{options.prefix}{(args[0].split('/')[-1])[:-5]}_{options.search_algorithm}_{options.local_search_algorithm}_{options.popsize}_{today}_{options.rho}_{options.tau}"
    else:
      prefix = f"{options.logdir}{os.sep}{options.prefix}{(args[0].split('/')[-1])[:-5]}_{options.search_algorithm}_{options.popsize}_{today}_{options.rho}_{options.tau}"
  else:
    prefix = options.filename

  # init csv constructor
  logger = Logger(prefix)

  # Loading the world from a module (random) or file (fixed)
  if (args[0][-5:] == ".json"):
    print(f"Loading world from file {args[0]}.")
    with open(args[0], "r") as in_f:
      _rdata = json.loads(in_f.read())
      world_m = importlib.import_module(_rdata["class"])
    world = world_m.get_fromfile(args[0])
    world.world_file = args[0]

  else:
    print(f"Creating new world from module {args[0]}.")
    world_m = importlib.import_module("."+args[0], "world")
    world = world_m.get_random()
    world.save_json(f"{prefix}_world.json")
    world.world_file = f"{prefix}_world.json"

  # Loading robot from a module
  robot_m = importlib.import_module("."+args[1], "robot")

  # Running the optimization
  algorithms = {
    "random": random_search,
    "ES": ES_search,
    "GA": GA_search,
    "MA": MA_search,
    "GA+PLS": GA_Post_LS_search,
    "GA+ES": GA_ES_search,
  }

  # init tqdm
  if options.local_search_algorithm != None:
    pbar = tqdm(total=options.evo_step, desc=f"{(args[0].split('/')[-1])[:-5]}/{options.search_algorithm}+{options.local_search_algorithm}/({options.rho},{options.tau})", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {postfix}')
  else:
    pbar = tqdm(total=options.evo_step, desc=f"{(args[0].split('/')[-1])[:-5]}/{options.search_algorithm}/({options.rho},{options.tau})", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {postfix}')
  pbar.set_postfix_str(f'best_robot: 0 popsize: {options.popsize}')

  _, _, simtime = algorithms[options.search_algorithm](robot_m, world, options, prefix, logger, pbar)

  pbar.close()
  
  print(f"Simulation times: avg: {mean(simtime)}, max: {max(simtime)}, min: {min(simtime)}")


def parse_args():
  usage = "usage: %prog [options] <world type> <robot type>"
  desc = """Performs a random search on the environment "world type", using
"robot type". By default, creates a json file named
`world_robot_MMDD_ID.json` for every robot that achieves a better
score.
"""
  import world, robot
  
  parser = OptionParser(usage = usage, description = desc) 

  parser.add_option("-s", "--sim_step", default = 400,
                    type="int", action="store",
                    help="Number of Simulation Steps. Default 400.")
  
  parser.add_option("-e", "--evo_step", default = 400,
                    type="int", action="store",
                    help="Number of Evaluations. Default 400.")

  parser.add_option("--post_step", default = 200,
                    type="int", action="store",
                    help="Number of post local search Evaluation. Default 200.")

  parser.add_option("--pre_step", default = 200,
                    type="int", action="store",
                    help="Number of pre local search Evaluation. Default 200.")

  algorithms = ["random", "ES", "GA", "MA", "GA+PLS", "GA+ES"]
  parser.add_option("-A", "--search_algorithm",
                    type = "choice", choices = algorithms,
                    default = algorithms[0],
                    help="Which search algorithm to use. Default random.")

  parser.add_option("-d", "--logdir",
                    type = "string", default = "log",
                    help = "directory to save log files. Default 'log'")

  parser.add_option("-p", "--prefix",
                    type = "string", default = "",
                    help = "Prefix string for log files")
  
  parser.add_option("--numprocs",
                    type ="int", default = 6,
                    help = "Number of cores to use for parallel processing. Default 5")

  parser.add_option("--popsize",
                    type ="int", default = 100,
                    help = "Number of population size. Default 100")

  local_algorithms = ["HC", "TS", "ES"]
  parser.add_option("-L", "--local_search_algorithm",
                    type = "choice", choices = local_algorithms,
                    default = None,
                    help="Which local search algorithm to use in MA. Default None(GA).")

  init_method = ["LS"]
  parser.add_option("--init_pop",
                    type = "choice", choices = init_method,
                    default = None,
                    help="Which initial method to be used. Default None(random).")

  parser.add_option("--rho",
                    type = "float", default = 1,
                    help = "Parameter of population shrink. Default is 1(no change).")
  
  parser.add_option("--tau",
                    type = "float", default = 1,
                    help = "Parameter of population shrink. Default is 1.")

  parser.add_option("--mu",
                    type = "int", default = 20,
                    help = "Parameter in (mu, labmda)-ES. Default is 20.")

  parser.add_option("--lamb",
                    type = "int", default = 5,
                    help = "Parameter in (mu, labmda)-ES. Default is 5.")

  parser.add_option("--mutation_size",
                    type = "int", default = 2,
                    help = "Parameter of mutation size in ES. Default is 2.")

  parser.add_option("--adaptive_mutation_size",
                    action = "store_true",
                    help = "Parameter of mutation size in ES. Default is 2.")

  parser.add_option("--strong_evaluation",
                    action = "store_true",
                    help = "This flag means whether to use strong evaluation.")

  parser.add_option("--filename",
                    default = None,
                    help = "Predecide filename before program running.")

  # parser.add_option("-q", "--quiet", default=True,
  #                   action="store_false", dest="verbose",
  #                   help="Suppress progress output to stdout")
  
  options, args = parser.parse_args()

  if len(args) != 2:
    parser.error("You must provide 2 arguments: world type and robot type")

  # TODO: Detect invalid arguments (non-existing module, invalid file)

  return options, args


if __name__ == "__main__":
  main()
