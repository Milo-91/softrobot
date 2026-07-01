import random
from multiprocessing import Pool, Manager
import numpy as np
from EC_algorithms.utils import *


def Search(robot_m, options, prefix, evaluator, local_search, logger, pbar):
  # 1+lambda ES: Get the best robot out of 5 mutations with elitism
  offspring = 5 # lambda
  gen_count = 0

  with Manager() as manager:
    eval_count = manager.Value('i', 0)
    lock = manager.Lock()

    best_robot = robot_m.get_random()
    best_score, time = evaluator.evaluate(best_robot, eval_count, lock)

    best_robot.set_score(best_score)

    meantime = []
    meantime.append(time)
    population = []
    while eval_count.value < options.evo_step:
      paramlist = []
      for _ in range(offspring):
        newrobot = best_robot.copy()
        newrobot = robot_m.mutate(newrobot, size=2)
        paramlist.append((newrobot, eval_count, lock))
        population.append(newrobot)

      with Pool(options.numprocs) as p:
        scores = p.starmap(evaluator.evaluate, paramlist)
      pbar.update(eval_count.value - pbar.n)

      for _ in scores:
        meantime.append(_[1])

      # set score
      fitness = [s[0] for s in scores]
      for i in range(offspring):
        population[i].set_score(fitness[i])
        record_md(f'{prefix}_evolve.md', robot=population[i])
      for ind in sorted(population, key=lambda x: x.score, reverse=True):
        record_md(f'{prefix}_evolve.md', content=f"population id: {ind.id}, score: {ind.score}")
      fitness = sorted(fitness, reverse=True)
      logger.record_population(gen_count, fitness)

      # analyze similarity
      sim = calculate_similarity(population)
      logger.record_similarity(eval_count.value, sim)
      gen_count += 1

      best_index = fitness.index(max(fitness))
      if best_robot.score < scores[best_index][0]:
        best_robot = paramlist[best_index][0]
        pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} popsize: {offspring}')
        record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation in iteration {eval_count.value}: {best_robot.score}")
        best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
        logger.record_best_robot(eval_count.value, best_robot.score)

    logger.record_best_robot(eval_count.value, best_robot.score)
  return best_robot, population, meantime
