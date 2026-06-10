import importlib, csv, random
from multiprocessing import Pool, Manager
import numpy as np


def tournament(pop, fit, k = 2):
  idx = random.sample(range(len(pop)), k)
  tpop = []
  tfit = []
  for i in idx:
    tpop.append(pop[i])
    tfit.append(fit[i])

  maxidx = tfit.index(max(tfit))

  return tpop[maxidx]

def Search(robot_m, world, options, prefix, evaluator, local_search):
  popsize = options.popsize
  elites_percentage = 0.1
  mutprob = 0.3
  with open(f'{prefix}_evolve.txt', 'a') as f:
    print(f'local search algorithm: {options.local_search_algorithm}\npopsize: {popsize}\nevo_step: {options.evo_step}\n', file=f)

  with Manager() as manager:
    eval_count = manager.Value('i', 0)
    lock = manager.Lock()

    # Initial population
    population = []
  
    for _ in range(popsize):
      r = robot_m.get_random()
      population.append(r)
      r.save_txt('initial', f'{prefix}_evolve.txt')
  
  
    evalpars = []
    for ind in population:
      evalpars.append((ind, eval_count, lock))
  
    with Pool(options.numprocs) as p:
      scores = p.starmap(evaluator.evaluate, evalpars)
  
    fitness = [s[0] for s in scores]
    meantime = [s[1] for s in scores]
  
    best_index = fitness.index(max(fitness))
    best_score = scores[best_index][0]
    best_robot = evalpars[best_index][0]
    print(f"New best score at evaluation {eval_count.value}: {best_score}")
    with open(f'{prefix}_evolve.txt', 'a') as f:
      print(f"New best score at evaluation in initialization {eval_count.value}: {best_score}", file=f)
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
        evalpars.append((ind, eval_count, lock))
  
      with Pool(options.numprocs) as p:
        scores = p.starmap(evaluator.evaluate, evalpars)
  
      fitness = [s[0] for s in scores]
      for s in scores:
        meantime.append(s[1])
  
      best_index = fitness.index(max(fitness))
  
      if best_score < scores[best_index][0]:
        best_score = scores[best_index][0]
        best_robot = evalpars[best_index][0]
        print(f"New best score at evaluation {eval_count.value}: {best_score}")
        with open(f'{prefix}_evolve.txt', 'a') as f:
          print(f"New best score at evaluation in iteration {eval_count.value}: {best_score}", file=f)
        best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
        with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
          writer = csv.writer(f)
          writer.writerow([eval_count.value, best_score])
  
      if local_search != None:
        # sort offsprings
        elites_indices = np.argsort(fitness)[::-1]
        # local search
        parameters = []
        for i in elites_indices[:int(popsize*elites_percentage)]:
          parameters.append((population[i], fitness[i], prefix, eval_count, lock))
  
        with Pool(options.numprocs) as p:
          scores = p.starmap(local_search.Search, parameters)
  
        elites_fitness = [s[0] for s in scores]
        for s in scores:
          meantime += s[1]
  
        best_index = elites_fitness.index(max(elites_fitness))
  
        if best_score < scores[best_index][0]:
          best_score = scores[best_index][0]
          best_robot = evalpars[best_index][0]
          print(f"New best score at evaluation {eval_count.value}: {best_score}")
          with open(f'{prefix}_evolve.txt', 'a') as f:
            print(f"New best score at evaluation after local search {eval_count.value}: {best_score}", file=f)
          best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
          with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([eval_count.value, best_score])

        for i in range(len(elites_fitness)):
          fitness[elites_indices[i]] = elites_fitness[i]

    print(f'eval_count: {eval_count.value}')
    with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow([eval_count.value, best_score])

  return meantime

