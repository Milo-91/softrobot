import EC_algorithms.GA as GA
from multiprocessing import Pool, Manager
import numpy as np
from EC_algorithms.utils import *


def Search(robot_m, options, prefix, evaluator, local_search, logger, pbar):
  popsize = options.popsize
  elites_percentage = 0.1
  mutprob = 0.3
  gen_count = 0
  LS_avg_improvement = 0
  LS_successful_rate = 0
  LS_individual_count = 0

  # GA
  best_robot, population, meantime = GA.Search(robot_m, options, prefix, evaluator, None, logger, pbar)
  record_md(f'{prefix}_evolve.md', content=f"best robot after GA: {best_robot.score}")
  # reset pbar
  pbar.total = options.post_step
  pbar.n = 0
  pbar.refresh()
  gen_count = options.gen_count

  # LS
  with Manager() as manager:
    eval_count = manager.Value('i', 0)
    lock = manager.Lock()

    while eval_count.value < options.post_step:
      # print(f'eval {eval_count.value}')
      # print(f'post_step {options.post_step}')
      elites = sorted(enumerate(population), key=lambda x: x[1].score, reverse=True)[:max(int(popsize*elites_percentage), 1)]
      # print(elites)
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

      # Analyze successful rate of local search
      for i in range(len(elites)):
        if population[elites[i][0]].score < robots[i].score:
          LS_avg_improvement += robots[i].score - population[elites[i][0]].score
          LS_successful_rate += 1
        population[elites[i][0]] = robots[i]

      LS_individual_count += len(elites)

      # print(f'eval_count {eval_count.value}')
      # print(f'post_step {options.post_step}')

      best_index = elites_fitness.index(max(elites_fitness))
      if best_robot.score < robots[best_index].score:
        best_score = elites_fitness[best_index]
        best_robot = robots[best_index]
        # print(f"New best score at evaluation {eval_count.value}: {best_robot.score}")
        pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} popsize: {popsize}')
        record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation after local search {eval_count.value}: {best_robot.score}")
        best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
        logger.record_best_robot(eval_count.value + options.evo_step, best_robot.score)

      for ind in sorted(population, key=lambda x: x.score, reverse=True):
        record_md(f'{prefix}_evolve.md', content=f"population id: {ind.id}, score: {ind.score}")
      fitness = [x.score for x in population]
      fitness = sorted(fitness, reverse=True)
      logger.record_population(gen_count, fitness)

      # record_LS_informations
      record_md(f'{prefix}_evolve.md', content=f"LS avg improvement: {(LS_avg_improvement / LS_individual_count):05}\nLS successful rate: {(100 * LS_successful_rate / LS_individual_count):05}")
      logger.record_LS_informations(eval_count.value + options.evo_step, LS_avg_improvement / LS_individual_count, LS_successful_rate / LS_individual_count)
      sim = calculate_similarity(population)
      logger.record_similarity(eval_count.value + options.evo_step, sim)
      gen_count += 1
      
  return best_robot, population, meantime
