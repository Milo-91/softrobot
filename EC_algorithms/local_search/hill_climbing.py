class HillClimbing:

  MAX_ITERATIONS = 5

  def __init__(self, evaluator):
    self.evaluator = evaluator

  def Search(self, robot, score, prefix, eval_count, lock):
    best_score = score
    best_robot = robot.copy()
    mean_time = []
    for _ in range(self.MAX_ITERATIONS):
      new_pop = best_robot.copy()
      new_pop.mutate()
      new_pop.save_txt('hill new_pop', f'{prefix}_evolve.txt')
      new_score, sim_time = self.evaluator.evaluate(robot, eval_count, lock)
      mean_time.append(sim_time)
      if new_score > best_score:
        best_robot = new_robot
        best_score = new_score
        new_pop.save_txt(f'hill best robot, score: {best_score}', f'{prefix}_evolve.txt')
    
    robot.shape = best_robot.shape.copy()
    return best_score, mean_time
