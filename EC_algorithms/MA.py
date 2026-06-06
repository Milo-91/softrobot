import importlib, csv, random
from multiprocessing import Pool, Manager


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
  popsize = 20
  mutprob = 0.3

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
        best_robot.save_json(f"{prefix}_robot_{eval_count.value:05}.json")
        with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
          writer = csv.writer(f)
          writer.writerow([eval_count.value, best_score])
  
      # local search (hill climbing)
      parameters = []
      for i in range(len(newpop)):
        parameters.append((newpop[i], fitness[i], prefix, eval_count, lock))
  
      with Pool(options.numprocs) as p:
        scores = p.starmap(local_search.Search, parameters)
  
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

    print(f'eval_count: {eval_count.value}')
    with open(f'{prefix}_best_record.csv', 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow([eval_count.value, best_score])

  return meantime

