class HillClimbing:

  MAX_ITERATIONS = 3

  def __init__(self, evaluator):
    self.evaluator = evaluator

  def Search(self, robot, score, prefix, eval_count, lock):
    best_score = score
    mean_time = []
    for _ in range(self.MAX_ITERATIONS):
      new_pop = robot.copy()
      new_pop.mutate()
      new_pop.save_txt('hill new_pop', f'{prefix}_evolve.txt')
      new_score, sim_time = self.evaluator.evaluate(robot, eval_count, lock)
      mean_time.append(sim_time)
      if new_score > best_score:
        robot = new_pop
        best_score = new_score
        new_pop.save_txt('hill best robot', f'{prefix}_evolve.txt')

    return best_score, mean_time
