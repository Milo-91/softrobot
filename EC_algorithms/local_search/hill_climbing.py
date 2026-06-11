from EC_algorithms.utils import record_md
import numpy as np

class HillClimbing:

  MAX_ITERATIONS = 5

  def __init__(self, evaluator):
    self.evaluator = evaluator

  def __mutate__(self, robot):
      count = 0
      while True:
          old_shape = robot.shape.copy()
          pos = tuple(np.random.randint(0,5,2))
          new_voxel = np.random.randint(0,4)
          if new_voxel >= robot.shape[pos]:
              new_voxel += 1
          robot.shape[pos] = new_voxel
          if robot.valid():
              break

          robot.shape = old_shape
          count += 1
          if count > 5000:
              raise Exception("Can't find a valid mutation after 5000 tries!")

  def Search(self, robot, prefix, eval_count, lock):
    best_robot = robot.copy()
    mean_time = []
    for _ in range(self.MAX_ITERATIONS):
      new_pop = best_robot.copy()
      self.__mutate__(new_pop)
      record_md(f'{prefix}_evolve.md', content='hill new_pop', robot=new_pop)
      new_score, sim_time = self.evaluator.evaluate(robot, eval_count, lock)
      mean_time.append(sim_time)
      if new_score > best_robot.score:
        best_robot = robot
        best_robot.set_score(new_score)
        record_md(f'{prefix}_evolve.md', content=f'hill best robot, score: {best_robot.score}', robot=best_robot)
    
    return best_robot, best_robot.score, mean_time
