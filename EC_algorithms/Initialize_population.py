from EC_algorithms.utils import *
from multiprocessing import Pool


def with_local_search(robot_m, options, prefix, evaluator, eval_count, lock, local_search, logger, pbar):
  population = []
  popsize = options.popsize
  gen_count = 0
  elites_percentage = 0.2
  LS_avg_improvement = 0
  LS_successful_rate = 0
  LS_individual_count = 0

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
  pbar.set_postfix_str(f'best_robot: {best_robot.score:.5f} popsize: {popsize}')
  record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation in initialization {eval_count.value}: {best_robot.score}")
  best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
  logger.record_best_robot(eval_count.value, best_robot.score)

  for ind in sorted(population, key=lambda x: x.score, reverse=True):
    record_md(f'{prefix}_evolve.md', content=f"population id: {ind.id}, score: {ind.score}")
  fitness = [x.score for x in population]
  fitness = sorted(fitness, reverse=True)
  logger.record_population(gen_count, fitness)

  while eval_count.value < options.pre_step:
    elites = sorted(enumerate(population), key=lambda x: x[1].score,reverse=True)[:max(int(popsize*elites_percentage), 1)]
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
    logger.record_LS_informations(eval_count.value, LS_avg_improvement / LS_individual_count, LS_successful_rate / LS_individual_count)
    sim = calculate_similarity(population)
    logger.record_similarity(eval_count.value, sim)
    gen_count += 1

  return gen_count, population, best_robot, meantime
