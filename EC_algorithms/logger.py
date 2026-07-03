import csv
import json

class Logger:
  def __init__(self, prefix):
    self.best_robot_filename = f'{prefix}_best_record.csv'
    self.similarity_filename = f'{prefix}_similarity_record.csv'
    self.ls_filename = f'{prefix}_ls_record.csv'
    self.population_filename = f'{prefix}_population_record.jsonl'
    self.mutation_filename = f'{prefix}_mutation_size_record.csv'

    # init csv files
    with open(self.best_robot_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['eval_count', 'score'])
    with open(self.similarity_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['eval_count', 'similarity'])
    with open(self.ls_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['eval_count', 'LS_avg_improvement', 'LS_successful_rate'])
    with open(self.mutation_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['eval_count', 'mutation_size'])
    # init json files
    with open(self.population_filename, 'w') as f:
      f.write("")


  def record_best_robot(self, eval_count, score):
    with open(self.best_robot_filename, 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow([eval_count, score])

  def record_similarity(self, eval_count, similarity):
    with open(self.similarity_filename, 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow([eval_count, similarity])

  def record_LS_informations(self, eval_count, LS_avg_improvement, LS_successful_rate):
    with open(self.ls_filename, 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow([eval_count, LS_avg_improvement, LS_successful_rate])

  def record_mutation_size(self, eval_count, mutation_size):
    with open(self.mutation_filename, 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow([eval_count, mutation_size])

  def record_population(self, gen_count, eval_count, fitness):
    fitness = sorted(fitness, reverse=True)
    data = {
      "gen": gen_count,
      'eval_count': eval_count,
      "fitness": fitness
    }
    with open(self.population_filename, 'a') as f:
      f.write(json.dumps(data) + '\n')
