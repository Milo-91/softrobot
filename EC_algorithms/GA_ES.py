import importlib, random
from multiprocessing import Pool, Manager
import numpy as np
from EC_algorithms.utils import *
from EC_algorithms.Initialize_population import *


def tournament(pop, k = 2):
  idx = random.sample(range(len(pop)), k)
  tpop = []
  tfit = []
  for i in idx:
    tpop.append(pop[i])
    tfit.append(pop[i].score)

  maxidx = tfit.index(max(tfit))

  return tpop[maxidx]

def Search(robot_m, options, prefix, evaluator, local_search, logger, pbar):
  popsize = options.popsize
  elites_percentage = 0.1
  mutprob = 0.3
  gen_count = 0

  record_md(f'{prefix}_evolve.md', content=f'- local search algorithm: {options.local_search_algorithm}\n- popsize: {popsize}\n- evo_step: {options.evo_step}\n- elites percentage: {elites_percentage}\n- rho: {options.rho}\n- tau: {options.tau}')

  with Manager() as manager:
    eval_count = manager.Value('i', 0)
    lock = manager.Lock()

    # Initial population
    record_md(f'{prefix}_evolve.md', content=f'# Generation {gen_count}')
    population = []
  
    for _ in range(popsize):
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
    for i in range(popsize):
      population[i].set_score(fitness[i])
      record_md(f'{prefix}_evolve.md', robot=population[i])

    # analyze similarity
    sim = calculate_similarity(population)
    logger.record_similarity(eval_count.value, sim)
  
    # record best robot
    best_index = fitness.index(max(fitness))
    best_score = scores[best_index][0]
    best_robot = evalpars[best_index][0]
    pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} popsize: {popsize}')
    record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation in initialization {eval_count.value}: {best_robot.score}")
    best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
    logger.record_best_robot(eval_count.value, best_robot.score)

    # record poulation
    fitness = [x.score for x in population]
    fitness = sorted(fitness, reverse=True)
    logger.record_population(gen_count, eval_count.value, fitness)
    for ind in sorted(population, key=lambda x: x.score, reverse=True):
      record_md(f'{prefix}_evolve.md', content=f"population id: {ind.id}, score: {ind.score}")
    gen_count += 1
  
    while eval_count.value < options.evo_step:
      # GA block
      for i in range(5): # each GA has 5 generations     
        record_md(f'{prefix}_evolve.md', content=f'# Generation {gen_count}')
        newpop = []
        for _ in range(popsize):
          # selection & crossover
          p1 = tournament(population, k = 2)
          p2 = tournament(population, k = 2)
          offspring = robot_m.crossover(p1, p2)
          record_md(f'{prefix}_evolve.md', content='after crossover', robot=offspring)
          # mutation
          if random.random() < mutprob:
            offspring = robot_m.mutate(offspring)
            record_md(f'{prefix}_evolve.md', content='after mutation', robot=offspring)
          newpop.append(offspring)
  
        population = newpop
  
        evalpars = []
        for ind in population:
          evalpars.append((ind, eval_count, lock))
  
        with Pool(options.numprocs) as p:
          scores = p.starmap(evaluator.evaluate, evalpars)
        pbar.update(eval_count.value - pbar.n)
  
        fitness = [s[0] for s in scores]
        for s in scores:
          meantime.append(s[1])
        
        # set scores
        for i in range(popsize):
          population[i].set_score(fitness[i])
          record_md(f'{prefix}_evolve.md', content='offsping', robot=population[i])

        # record best robot
        best_index = fitness.index(max(fitness))
        if best_robot.score < scores[best_index][0]:
          best_score = scores[best_index][0]
          best_robot = evalpars[best_index][0]
          pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} popsize: {popsize}')
          record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation in iteration {eval_count.value}: {best_robot.score}")
          best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
          logger.record_best_robot(eval_count.value, best_robot.score)

        # record population
        fitness = [x.score for x in population]
        fitness = sorted(fitness, reverse=True)
        logger.record_population(gen_count, eval_count.value, fitness)
        for ind in sorted(population, key=lambda x: x.score, reverse=True):
          record_md(f'{prefix}_evolve.md', content=f"population id: {ind.id}, score: {ind.score}")

        # analyze similarity
        sim = calculate_similarity(population)
        logger.record_similarity(eval_count.value, sim)

        gen_count += 1
 
      # ES block
      for i in range(5): # each ES has 5 generations
        record_md(f'{prefix}_evolve.md', content=f'# Generation {gen_count}')
        population, sim_time = local_search.Search(population, prefix, eval_count, lock, logger, pbar)
        meantime += sim_time

        # record best robot
        population = sorted(population, key=lambda x:x.score, reverse=True)
        if best_robot.score < population[0].score:
          best_score = population[0].score
          best_robot = population[0]
          pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} popsize: {popsize}')
          record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation after local search {eval_count.value}: {best_robot.score}")
          best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
          logger.record_best_robot(eval_count.value, best_robot.score)

        # record population
        fitness = [x.score for x in population]
        fitness = sorted(fitness, reverse=True)
        logger.record_population(gen_count, eval_count.value, fitness)
        for ind in sorted(population, key=lambda x: x.score, reverse=True):
          record_md(f'{prefix}_evolve.md', content=f"population id: {ind.id}, score: {ind.score}")

        # analyze similarity
        sim = calculate_similarity(population)
        logger.record_similarity(eval_count.value, sim)

        gen_count += 1

    logger.record_best_robot(eval_count.value, best_robot.score)

  # for PLS
  options.gen_count = gen_count
  options.popsize = popsize
  return best_robot, population, meantime

