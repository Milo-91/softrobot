import time, os, random
import importlib, json, csv
from multiprocessing import Pool, Value
import numpy as np

from optparse import OptionParser

counter = None

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


def evaluate(robot, world, sim_step, evo_step):
  # set max evo step
  if counter.value >= evo_step:
    return 0, 0
  with counter.get_lock():
    counter.value += 1

  stime = time.time()
  world.restart()
  world.set_robot(robot)
  with suppress_stdout_stderr():
    world.reset()   

  for _ in range(sim_step):
    world.step()

  score = world.get_score()

  world.sim = None
  #FIXME: should fix the world state engine 
  #       to avoid reloading the json file all the time

  etime = time.time()

  return score, (etime - stime)


def GA_search(robot_m, world, options, prefix):
  popsize = 20
  mutprob = 0.3
  eval_count = Value('i', 0)

  def tournament(pop, fit, k = 2):
    idx = random.sample(range(len(pop)), k)
    tpop = []
    tfit = []
    for i in idx:
      tpop.append(pop[i])
      tfit.append(fit[i])

    maxidx = tfit.index(max(tfit))

    return tpop[maxidx]

  # Initial population
  population = []
  rep = popsize

  for _ in range(popsize):
    r = robot_m.get_random()
    population.append(r)

  evalpars = []
  for ind in population:
    evalpars.append((ind, world, options.sim_step, options.evo_step))

  with Pool(options.numprocs, initializer=mulpro_init, initargs=(eval_count,)) as p:
    scores = p.starmap(evaluate, evalpars)

  fitness = [s[0] for s in scores]
  meantime = [s[1] for s in scores]

  best_index = fitness.index(max(fitness))
  best_score = scores[best_index][0]
  best_robot = evalpars[best_index][0]
  print(f"New best score at evaluation {eval_count.value}: {best_score}")
  best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json") 
  with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([eval_count.value, best_score])

  while eval_count.value < options.evo_step:
    newpop = []
    rep += popsize

    for _ in range(popsize):
      p1 = tournament(population, fitness, k = 2)
      p2 = tournament(population, fitness, k = 2)
      offspring = p1.crossover(p2)
      if random.random() < mutprob:
        offspring.mutate()
      newpop.append(offspring)

    population = newpop 

    evalpars = []
    for ind in population:
      evalpars.append((ind, world, options.sim_step, options.evo_step))

    with Pool(options.numprocs, initializer=mulpro_init, initargs=(eval_count,)) as p:
      scores = p.starmap(evaluate, evalpars)

    fitness = [s[0] for s in scores]
    for s in scores:
      meantime.append(s[1])

    best_index = fitness.index(max(fitness))

    if best_score < scores[best_index][0]:
      best_score = scores[best_index][0]
      best_robot = evalpars[best_index][0]
      print(f"New best score at evaluation {eval_count.value}: {best_score}")
      best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json") 
      with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([eval_count.value, best_score])

  print(f'eval_count = {eval_count.value}')
  with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([eval_count.value, best_score])
  return meantime










def ES_search(robot_m, world, options, prefix):
  # 1+lambda ES: Get the best robot out of 5 mutations with elitism
  offspring = 5 # lambda
  eval_count = Value('i', 0)

  best_robot = robot_m.get_random()
  mulpro_init(eval_count)
  best_score = evaluate(best_robot, world, options.sim_step, options.evo_step)[0]
  rep = 1

  meantime = []

  while eval_count.value < options.evo_step:
    paramlist = []
    for _ in range(offspring):
      newrobot = best_robot.copy()
      newrobot.mutate(2)
      paramlist.append((newrobot, world, options.sim_step, options.evo_step))

    with Pool(options.numprocs, initializer=mulpro_init, initargs=(eval_count,)) as p:
      scores = p.starmap(evaluate, paramlist)

    rep += offspring

    for _ in scores:
      meantime.append(_[1])

    # print(f"Mean sim time at {rep}: {mean(meantime)}")


    best_index = scores.index(max(scores))

    if best_score < scores[best_index][0]:
      best_score = scores[best_index][0]
      best_robot = paramlist[best_index][0]
      print(f"New best score at evaluation {rep}: {best_score}")
      best_robot.save_json(f"{prefix}_robot_{rep:05}.json") 
      with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([eval_count.value, best_score])

  print(f'eval_count = {eval_count.value}')
  with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([eval_count.value, best_score])
  return meantime


def random_search(robot_m, world, options, prefix):
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


def random_opt_search(robot_m, world, options, prefix):
  base_robot = None

  rep = 0
  meantime = []
  top_k = []
  hun_count = 0
  k = 10
  threshold = 6

  while rep < options.evo_step:  
    paramlist = []
    numprocs = options.numprocs
    if options.numprocs > (100 - hun_count):
      numprocs = 100 - hun_count
    for _ in range(numprocs):
      paramlist.append((robot_m.get_random(base_robot), world, options.sim_step))

    with Pool(numprocs) as p:
      scores = p.starmap(evaluate, paramlist)

    rep += numprocs
    hun_count += numprocs


    for _ in scores:
      meantime.append(_[1])

    temp_robot = [(paramlist[i][0], scores[i][0]) for i in range(numprocs)]
    top_k.extend(temp_robot)
    top_k.sort(key=lambda x: x[-1], reverse=True)
    top_k = top_k[:k]

    # print(f"socres\n{scores}")
    # print(f"meantime\n{meantime}")
    # print(f"top_{k}\n{top_k}")
    # print(f"Mean sim time at {rep}: {mean(meantime)}")


    if hun_count == 100:
      temp_arr = np.stack([r[0].shape for r in top_k], axis=0)
      H, W = temp_arr.shape[1:]
      base_robot = np.full((H, W), -1)
      for i in range(H):
        for j in range(W):
          arr = [(temp_arr[:, i, j] == n).sum() for n in range(5)]
          for l in range(5):
            if arr[l] >= threshold:
              base_robot[i][j] = l

      hun_count = 0
      print(base_robot)
      # store base_robot
      with open(f'{prefix}_base_robit.txt', "a") as out_f:
        s = np.array2string(
          base_robot,
        )
        out_f.write(s + '\n')

      count = 0
      for r in top_k:
        count += 1
        r[0].save_json(f"{prefix}_robot_{rep:04}_{count}.json")

  return meantime


def hill_climbing(pop, score, max_iterations, world, sim_step, evo_step, prefix):
  best_score = score
  mean_time = []
  # print('local search')
  for _ in range(max_iterations):
    new_pop = pop.copy()
    new_pop.mutate()
    new_pop.save_txt('hill new_pop', f'{prefix}_evolve.txt')
    new_score, sim_time = evaluate(new_pop, world, sim_step, evo_step)
    mean_time.append(sim_time)
    if new_score > best_score:
      pop = new_pop
      best_score = new_score
      new_pop.save_txt('hill best robot', f'{prefix}_evolve.txt')
  
  return best_score, mean_time

def mulpro_init(args):
  global counter
  counter = args

def MA_search(robot_m, world, options, prefix):
  # GA + hill climbing
  popsize = 20
  mutprob = 0.3
  max_iterations = 3

  eval_count = Value('i', 0)

  def tournament(pop, fit, k = 2):
    idx = random.sample(range(len(pop)), k)
    tpop = []
    tfit = []
    for i in idx:
      tpop.append(pop[i])
      tfit.append(fit[i])

    maxidx = tfit.index(max(tfit))

    return tpop[maxidx]

  # Initial population
  population = []

  for _ in range(popsize):
    r = robot_m.get_random()
    population.append(r)
    r.save_txt('initial', f'{prefix}_evolve.txt')


  evalpars = []
  for ind in population:
    evalpars.append((ind, world, options.sim_step, options.evo_step))

  with Pool(options.numprocs, initializer=mulpro_init, initargs=(eval_count,)) as p:
    scores = p.starmap(evaluate, evalpars)

  fitness = [s[0] for s in scores]
  meantime = [s[1] for s in scores]

  best_index = fitness.index(max(fitness))
  best_score = scores[best_index][0]
  best_robot = evalpars[best_index][0]
  print(f"New best score at evaluation {eval_count.value}: {best_score}")
  best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
  with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([eval_count.value, best_score])

  while eval_count.value < options.evo_step:
    newpop = []

    for _ in range(popsize):
      p1 = tournament(population, fitness, k = 2)
      p2 = tournament(population, fitness, k = 2)
      p1.save_txt('parent1', f'{prefix}_evolve.txt')
      p2.save_txt('parent2', f'{prefix}_evolve.txt')
      offspring = p1.crossover(p2)
      offspring.save_txt('after crossover', f'{prefix}_evolve.txt')
      if random.random() < mutprob:
        offspring.mutate()
        offspring.save_txt('after mutation', f'{prefix}_evolve.txt')
      newpop.append(offspring)

    population = newpop

    evalpars = []
    for ind in population:
      evalpars.append((ind, world, options.sim_step, options.evo_step))

    with Pool(options.numprocs, initializer=mulpro_init, initargs=(eval_count,)) as p:
      scores = p.starmap(evaluate, evalpars)

    fitness = [s[0] for s in scores]
    for s in scores:
      meantime.append(s[1])

    best_index = fitness.index(max(fitness))

    if best_score < scores[best_index][0]:
      best_score = scores[best_index][0]
      best_robot = evalpars[best_index][0]
      print(f"New best score at evaluation {eval_count.value}: {best_score}")
      best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
      with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([eval_count.value, best_score])

    # local search (hill climbing)
    parameters = []
    for i in range(len(newpop)):
      parameters.append([newpop[i], fitness[i], max_iterations, world, options.sim_step, options.evo_step, prefix])

    with Pool(options.numprocs, initializer=mulpro_init, initargs=(eval_count,)) as p:
      scores = p.starmap(hill_climbing, parameters)

    fitness = [s[0] for s in scores]
    for s in scores:
      meantime += s[1]

    best_index = fitness.index(max(fitness))

    if best_score < scores[best_index][0]:
      best_score = scores[best_index][0]
      best_robot = evalpars[best_index][0]
      print(f"New best score at evaluation {eval_count.value}: {best_score}")
      best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
      with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([eval_count.value, best_score])

  print(f'eval_count = {eval_count.value}')
  with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([eval_count.value, best_score])

  return meantime




def main():
  options, args = parse_args()

  if not os.path.exists(options.logdir):
    os.mkdir(options.logdir)


  today  = time.strftime("%m%d%H%M")
  prefix = f"{options.logdir}{os.sep}{options.prefix}_{options.search_algorithm}_{today}"

  # csv record file
  with open(f'{prefix}_best_record.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['eval_count', 'score'])
  # debug file
  with open(f'{prefix}_evolve.txt', 'w') as f:
    print('evolve', file=f)

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
    "random_opt": random_opt_search,
    "ES": ES_search,
    "GA": GA_search,
    "MA": MA_search,
  }

  simtime = algorithms[options.search_algorithm](robot_m, world, options, prefix)
  
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

  algorithms = ["random", "random_opt", "ES", "GA", "MA"]
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
                    type ="int", default = 5,
                    help = "Number of cores to use for parallel processing. Default 5")
  
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
