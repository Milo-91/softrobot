import random
from multiprocessing import Pool, Manager
import numpy as np
from EC_algorithms.utils import *


class Mutation:

  def __init__(self, prefix, evaluator, lamb, mutation_size=2):
    self.evaluator = evaluator
    self.lamb = lamb
    self.MUTATION_SIZE = mutation_size
    self.prefix = prefix
    self.rng = None

  def __mutate__(self, robot):
    for _ in range(self.MUTATION_SIZE):
      count = 0
      while True:
          old_shape = robot.shape.copy()
          pos = tuple(self.rng.integers(low=0, high=5, size=2))
          new_voxel = self.rng.integers(low=0, high=5)
          robot.shape[pos] = new_voxel
          if robot.valid():
              record_md(f'{self.prefix}_evolve.md', content=f'change {pos} with {new_voxel}')
              break

          robot.shape = old_shape
          count += 1
          if count > 5000:
              raise Exception("Can't find a valid mutation after 5000 tries!")

  def __init_random_state__(self):
    self.rng = np.random.default_rng()

  def update_mutation_size(self, mutation_size):
    self.MUTATION_SIZE = mutation_size

  def Generate_Offspring(self, parent, eval_count, lock):
    offspring = []
    meantime = []
    fitness = []
    self.__init_random_state__()
    for _ in range(self.lamb):
      newrobot = parent.copy()
      record_md(f'{self.prefix}_evolve.md', content='parent', robot=newrobot)
      self.__mutate__(newrobot)
      score, sim_time = self.evaluator.evaluate(newrobot, eval_count, lock)
      record_md(f'{self.prefix}_evolve.md', content='child', robot=newrobot)
      fitness.append(score)
      offspring.append(newrobot)
      meantime.append(sim_time)
  
    return offspring, fitness, meantime


# (mu+lambda)-ES
def Search(robot_m, options, prefix, evaluator, local_search, logger, pbar):
  mu = options.mu
  lamb = options.lamb # lambda
  gen_count = 0
  Generator = Mutation(prefix, evaluator, lamb, mutation_size=options.mutation_size)

  record_md(f'{prefix}_evolve.md', content=f'- mu: {mu}\n- lambda: {lamb}\n- evo_step: {options.evo_step}\n- mutation_size: {options.mutation_size}\n')

  with Manager() as manager:
    eval_count = manager.Value('i', 0)
    lock = manager.Lock()

    # Initial population
    record_md(f'{prefix}_evolve.md', content=f'# Generation {gen_count}')
    population = []
  
    for _ in range(mu):
      r = robot_m.get_random()
      population.append(r) 
  
    evalpars = []
    for ind in population:
      evalpars.append((ind, eval_count, lock))
  
    with Pool(options.numprocs) as p:
      scores = p.starmap(evaluator.evaluate, evalpars)
    pbar.update(eval_count.value - pbar.n)
  
    fitness = [s[0] for s in scores]
    meantime = [s[1] for s in scores]

    # set scores
    for i in range(mu):
      population[i].set_score(fitness[i])

    # analyze similarity
    sim = calculate_similarity(population)
    logger.record_similarity(eval_count.value, sim)
    gen_count += 1
  
    best_index = fitness.index(max(fitness))
    best_score = scores[best_index][0]
    best_robot = evalpars[best_index][0]
    pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} sigma: {options.mutation_size}')
    record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation in initialization {eval_count.value}: {best_robot.score}")
    best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
    logger.record_best_robot(eval_count.value, best_robot.score)

    while eval_count.value < options.evo_step:
      record_md(f'{prefix}_evolve.md', content=f'# Generation {gen_count}')

      paramlist = []
      for ind in population:
        paramlist.append((ind, eval_count, lock))

      with Pool(options.numprocs) as p:
        results = p.starmap(Generator.Generate_Offspring, paramlist)
      pbar.update(eval_count.value - pbar.n)

      newpop = []
      fitness = []
      for result in results:
        newpop += result[0]
        fitness += result[1]
        meantime += result[2]
      # print(f'newpop: {newpop}')
      # print(f'fitness: {fitness}')

      # analyze successful rate of mutation
      avg_improvement = 0
      successful_rate = 0
      for parent, result in zip(population, results):
        for score in result[1]:
          if parent.score < score:
            avg_improvement += score - parent.score
            successful_rate += 1

      # adaptive mutation size
      if options.adaptive_mutation_size == True:
        if successful_rate / len(newpop) > 0.25: # mutation size is too small
          options.mutation_size += 1
          Generator.update_mutation_size(options.mutation_size)
        elif successful_rate / len(newpop) < 0.15: # mutation size is too big
          if options.mutation_size > 1:
            options.mutation_size -= 1
            Generator.update_mutation_size(options.mutation_size)
        pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} sigma: {options.mutation_size}')
        logger.record_mutation_size(eval_count.value, options.mutation_size)

      # record_LS_informations
      record_md(f'{prefix}_evolve.md', content=f"LS avg improvement: {(avg_improvement / len(newpop)):.5f}\nLS successful rate: {(100 * successful_rate / len(newpop)):.5f}")
      logger.record_LS_informations(eval_count.value, avg_improvement / len(newpop), successful_rate / len(newpop))

      # set score
      for i in range(len(newpop)):
        newpop[i].set_score(fitness[i])

      # selection
      population = sorted(newpop, key=lambda x: x.score, reverse=True)[:mu]

      # record population
      for ind in population:
        record_md(f'{prefix}_evolve.md', content=f"population id: {ind.id}, score: {ind.score}")
      logger.record_population(gen_count, eval_count.value, [p.score for p in population])

      # analyze similarity
      sim = calculate_similarity(population)
      logger.record_similarity(eval_count.value, sim)
      gen_count += 1

      # record best robot
      if best_robot.score < population[0].score:
        best_robot = population[0]
        pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} sigma: {options.mutation_size}')
        record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation in iteration {eval_count.value}: {best_robot.score}")
        best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
        logger.record_best_robot(eval_count.value, best_robot.score)

    logger.record_best_robot(eval_count.value, best_robot.score)
  return best_robot, population, meantime
