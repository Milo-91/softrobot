import numpy as np
from multiprocessing import Pool, Manager
from EC_algorithms.utils import *

class EvolutionStrategy:
  
  def __init__(self, evaluator, mu, lamb, numprocs, mutation_size=1):
    self.evaluator = evaluator
    self.mu = mu
    self.lamb = lamb
    self.MUTATION_SIZE = mutation_size
    self.numprocs = numprocs
    self.rng = None

  def __init_random_state__(self):
    self.rng = np.random.default_rng()

  def __mutate__(self, robot):
    for _ in range(self.MUTATION_SIZE):
      count = 0
      while True:
          old_shape = robot.shape.copy()
          pos = tuple(self.rng.integers(low=0, high=5, size=2))
          new_voxel = self.rng.integers(low=0, high=5)
          robot.shape[pos] = new_voxel
          if robot.valid():
              break

          robot.shape = old_shape
          count += 1
          if count > 5000:
              raise Exception("Can't find a valid mutation after 5000 tries!")

  def Generate_Offspring(self, parent, eval_count, lock):
    offspring = []
    meantime = []
    fitness = []
    self.__init_random_state__()
    for _ in range(self.lamb):
      newrobot = parent.copy()
      self.__mutate__(newrobot)
      score, sim_time = self.evaluator.evaluate(newrobot, eval_count, lock)
      fitness.append(score)
      offspring.append(newrobot)
      meantime.append(sim_time)
  
    return offspring, fitness, meantime


  def Search(self, population, prefix, eval_count, lock, logger, pbar):
    # selection
    parents = sorted(population, key=lambda x:x.score, reverse=True)[:self.mu]

    paramlist = []
    for ind in parents:
      paramlist.append((ind, eval_count, lock))

    with Pool(self.numprocs) as p:
      results = p.starmap(self.Generate_Offspring, paramlist)
    pbar.update(eval_count.value - pbar.n)

    newpop = []
    fitness = []
    meantime = []
    for result in results:
      newpop += result[0]
      fitness += result[1]
      meantime += result[2]

    # analyze successful rate of mutation
    avg_improvement = 0
    successful_rate = 0
    for parent, result in zip(population, results):
      for score in result[1]:
        if parent.score < score:
          avg_improvement += score - parent.score
          successful_rate += 1

    # adaptive mutation size
    if successful_rate / len(newpop) > 0.25: # mutation size is too small
      self.MUTATION_SIZE += 1
    elif successful_rate / len(newpop) < 0.15: # mutation size is too big
      if self.MUTATION_SIZE > 1:
        self.MUTATION_SIZE -= 1
    logger.record_mutation_size(eval_count.value, self.MUTATION_SIZE)

    # record_LS_informations
    record_md(f'{prefix}_evolve.md', content=f"LS avg improvement: {(avg_improvement / len(newpop)):.5f}\nLS successful rate: {(100 * successful_rate / len(newpop)):.5f}")
    logger.record_LS_informations(eval_count.value, avg_improvement / len(newpop), successful_rate / len(newpop))


    # set score
    for i in range(len(newpop)):
      newpop[i].set_score(fitness[i])

    return newpop, meantime
