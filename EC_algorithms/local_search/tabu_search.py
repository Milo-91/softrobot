import numpy as np
from EC_algorithms.utils import record_md

class TabuSearch:

    MAX_ITERATIONS = 5

    def __init__(self, evaluator):
        self.evaluator = evaluator

    def __mutate__(self, robot, visited):
        count = 0
        while True:
            old_shape = robot.shape.copy()
            pos = tuple(np.random.randint(0,5,2))
            if pos in visited:
                count += 1
                continue
            new_voxel = np.random.randint(0,4)
            if new_voxel >= robot.shape[pos]:
                new_voxel += 1
            robot.shape[pos] = new_voxel
            if robot.valid():
                visited.add(pos)
                break

            robot.shape = old_shape
            count += 1
            if count > 5000:
                raise Exception("Can't find a valid mutation after 5000 tries!")
 

    def Search(self, robot, prefix, eval_count, lock):
        visited = set()
        best_robot = robot.copy()
        best_robot.set_score(robot.score)
        mean_time = []
        for _ in range(self.MAX_ITERATIONS):
            self.__mutate__(robot, visited)
            new_score, sim_time = self.evaluator.evaluate(robot, eval_count, lock)
            robot.set_score(new_score)
            record_md(f'{prefix}_evolve.md', content='tabu new_pop', robot=robot)
            mean_time.append(sim_time)
            if new_score > best_robot.score:
                best_robot = robot.copy()
                best_robot.set_score(robot.score)
                record_md(f'{prefix}_evolve.md', content='tabu best robot', robot=best_robot)
        
        return best_robot, best_robot.score, mean_time

