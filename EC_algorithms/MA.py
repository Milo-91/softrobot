import importlib, random
from multiprocessing import Pool, Manager
import numpy as np
from EC_algorithms.utils import *
from EC_algorithms.Initialize_population import *


def tournament(pop, k = 5):
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
  LS_avg_improvement = 0
  LS_successful_rate = 0
  LS_individual_count = 0

  record_md(f'{prefix}_evolve.md', content=f'- local search algorithm: {options.local_search_algorithm}\n- popsize: {popsize}\n- evo_step: {options.evo_step}\n- elites percentage: {elites_percentage}\n- rho: {options.rho}\n- tau: {options.tau}')

  with Manager() as manager:
    eval_count = manager.Value('i', 0)
    lock = manager.Lock()

    # Initial population
    record_md(f'{prefix}_evolve.md', content=f'# Generation {gen_count}')
    if options.init_pop == None:
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
      gen_count += 1
  
      best_index = fitness.index(max(fitness))
      best_score = scores[best_index][0]
      best_robot = evalpars[best_index][0]
      # print(f"New best score at evaluation {eval_count.value}: {best_robot.score}")
      pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} popsize: {popsize}')
      record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation in initialization {eval_count.value}: {best_robot.score}")
      best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
      logger.record_best_robot(eval_count.value, best_robot.score)

    else:
      init_pop_methods = {
        'LS': with_local_search
      }
      population, best_robot, meantime = init_pop_methods[options.init_pop](robot_m, options, prefix, evaluator, eval_count, lock, local_search)

    for ind in sorted(population, key=lambda x: x.score, reverse=True):
      record_md(f'{prefix}_evolve.md', content=f"population id: {ind.id}, score: {ind.score}")
    fitness = [x.score for x in population]
    fitness = sorted(fitness, reverse=True)
    logger.record_population(gen_count, fitness)
 
    while eval_count.value < options.evo_step:
      record_md(f'{prefix}_evolve.md', content=f'# Generation {gen_count}')
      newpop = []
      for _ in range(popsize):
        p1 = tournament(population, k = 2)
        p2 = tournament(population, k = 2)
        offspring = robot_m.crossover(p1, p2)
        record_md(f'{prefix}_evolve.md', content='after crossover', robot=offspring)
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
  
      best_index = fitness.index(max(fitness))
      if best_robot.score < scores[best_index][0]:
        best_score = scores[best_index][0]
        best_robot = evalpars[best_index][0]
        # print(f"New best score at evaluation {eval_count.value}: {best_robot.score}")
        pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} popsize: {popsize}')
        record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation in iteration {eval_count.value}: {best_robot.score}")
        best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
        logger.record_best_robot(eval_count.value, best_robot.score)

      for ind in sorted(population, key=lambda x: x.score, reverse=True):
        record_md(f'{prefix}_evolve.md', content=f"population id: {ind.id}, score: {ind.score}")
      fitness = [x.score for x in population]
      fitness = sorted(fitness, reverse=True)
      logger.record_population(gen_count, fitness)
  
      # Local Search block
      if options.local_search_algorithm != None:
        # sort offsprings
        elites = sorted(enumerate(population), key=lambda x: x[1].score,reverse=True)[:max(int(popsize*elites_percentage), 1)]
        # print(elites[:int(popsize*elites_percentage)+1])
        # 10% elites can perform local search
        parameters = []
        for elite in elites:
          parameters.append((elite[1], prefix, eval_count, lock))
  
        with Pool(options.numprocs) as p:
          results = p.starmap(local_search.Search, parameters)
        pbar.update(eval_count.value - pbar.n)
  
        robots = [r[0] for r in results]
        elites_fitness = [r[1] for r in results]
        for r in results:
          meantime += r[2]

        for i in range(len(elites)):
          # analyze successful rate of local search
          if population[elites[i][0]].score < robots[i].score:
            LS_avg_improvement += robots[i].score - population[elites[i][0]].score
            LS_successful_rate += 1
          population[elites[i][0]] = robots[i]

        LS_individual_count += len(elites)
  
        best_index = elites_fitness.index(max(elites_fitness))
  
        if best_robot.score < robots[best_index].score:
          best_score = elites_fitness[best_index]
          best_robot = robots[best_index]
          # print(f"New best score at evaluation {eval_count.value}: {best_robot.score}")
          pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} popsize: {popsize}')
          record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation after local search {eval_count.value}: {best_robot.score}")
          best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
          logger.record_best_robot(eval_count.value, best_robot.score)

        for ind in sorted(population, key=lambda x: x.score, reverse=True):
          record_md(f'{prefix}_evolve.md', content=f"population id: {ind.id}, score: {ind.score}")
        fitness = [x.score for x in population]
        fitness = sorted(fitness, reverse=True)
        logger.record_population(gen_count, fitness)

        # record_LS_informations
        record_md(f'{prefix}_evolve.md', content=f"LS avg improvement: {(LS_avg_improvement / LS_individual_count):05}\nLS successful rate: {(100 * LS_successful_rate / LS_individual_count):05}")
        logger.record_LS_informations(eval_count, LS_avg_improvement / LS_individual_count, LS_successful_rate / LS_individual_count)
      sim = calculate_similarity(population)
      logger.record_similarity(eval_count.value, sim)
      gen_count += 1

      # population shrink block
      if options.rho != 1:
        # sort
        population = sorted(population, key=lambda x: x.score, reverse=True)
        # drop
        popsize = round(options.popsize * (1 - (1 - options.rho)*(eval_count.value / options.evo_step)**options.tau))
        population = population[:popsize]
        # print(f'popsize: {popsize}')
        record_md(f'{prefix}_evolve.md', content=f"gen: {gen_count}\nnew popsize after shrink: {popsize}")

    pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} popsize: {popsize}')
    # print(f'eval_count: {eval_count.value}')
    # print(f'best score: {best_robot.score}')
    logger.record_best_robot(eval_count.value, best_robot.score)

  options.gen_count = gen_count
  options.popsize = popsize
  return best_robot, population, meantime

