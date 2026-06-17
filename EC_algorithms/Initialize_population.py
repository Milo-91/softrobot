from EC_algorithms.utils import *

def with_local_search(prefix, evaluator, eval_count, lock, local_search):
  population = []
  elites_percentage = 0.1

  for _ in range(popsize):
    r = robot_m.get_random()
    population.append(r)

  evalpars = []
  for ind in population:
    evalpars.append((ind, eval_count, lock))

  with Pool(options.numprocs) as p:
    scores = p.starmap(evaluator.evaluate, evalpars)

  fitness = [s[0] for s in scores]
  meantime = [s[1] for s in scores]

  # set scores
  for i in range(popsize):
    population[i].set_score(fitness[i])
    record_md(f'{prefix}_evolve.md', robot=population[i])

  # analyze similarity
  sim = calculate_similarity(population)
  record_similarity(gen_count, sim, f'{prefix}_similarity_record.csv')
  gen_count += 1

  best_index = fitness.index(max(fitness))
  best_score = scores[best_index][0]
  best_robot = evalpars[best_index][0]
  if best_robot.score != best_score:
    print('error for score setting')
    exit(1)
  print(f"New best score at evaluation {eval_count.value}: {best_robot.score}")
  record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation in initialization {eval_count.value}: {best_robot.score}")
  best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
  record_best_robot(eval_count.value, best_robot.score, f'{prefix}_best_record.csv')

  elites = sorted(enumerate(population), key=lambda x: x[1].score,reverse=True)[:max(int(popsize*elites_percentage), 1)]
  print(elites[:int(popsize*elites_percentage)+1])
  # 10% elites can perform local search
  parameters = []
  for elite in elites:
    parameters.append((elite[1], prefix, eval_count, lock))
  
  with Pool(options.numprocs) as p:
    results = p.starmap(local_search.Search, parameters)
  
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
    print(f"New best score at evaluation {eval_count.value}: {best_robot.score}")
    record_md(f'{prefix}_evolve.md', content=f"New best score at evaluation after local search {eval_count.value}: {best_robot.score}")
    best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
    record_best_robot(eval_count.value, best_robot.score, f'{prefix}_best_record.csv')
  return population
