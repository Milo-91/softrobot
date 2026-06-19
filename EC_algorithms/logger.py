import csv

class CSVLogger:
  def __init__(self, prefix):
    self.best_robot_filename = f'{prefix}_best_record.csv'
    self.similarity_filename = f'{prefix}_similarity_record.csv'
    self.ls_filename = f'{prefix}_ls_record.csv'
    self.best_robot_columns = ['eval_count', 'score']
    self.similarity_columns = ['gen_count', 'similarity']
    self.ls_columns = ['gen_count', 'LS_avg_improvement', 'LS_successful_rate'] 

    # init csv files
    with open(self.best_robot_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(self.best_robot_columns)
    with open(self.similarity_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(self.similarity_columns)
    with open(self.ls_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(self.ls_columns)

  def record_best_robot(self, eval_count, score):
    with open(self.best_robot_filename, 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow([eval_count, score])

  def record_similarity(self, num_gen, similarity):
    with open(self.similarity_filename, 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow([num_gen, similarity])

  def record_LS_informations(self, num_gen, LS_avg_improvement, LS_successful_rate):
    with open(self.ls_filename, 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow([num_gen, LS_avg_improvement, LS_successful_rate])
