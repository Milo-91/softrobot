import json
import numpy as np
from evogym import is_connected

def get_random(base_robot=None, w = 5, h = 5):
    r = SinRobot()
    r.randomize(base_robot, w, h)
    return r

def get_fromfile(filename):
    r = SinRobot()
    r.load_json(filename)
    return r

class SinRobot:
    def __init__(self):
        self.shape = np.array([[1]])

    def valid(self):
        return (is_connected(self.shape) and
                (3 in self.shape or 4 in self.shape))

    def save_json(self, filename):
        with open(filename, "w") as out_f:
            data = {"class": __name__, "shape": self.shape.tolist()}
            json.dump(data,
                      out_f,
                      separators = (',', ':'))

    def load_json(self, filename):
        with open(filename, "r") as in_f:
            rdata = json.loads(in_f.read())
            if rdata["class"] != __name__:
                raise Exception("Invalid File!")
            self.shape = np.array(rdata["shape"])

    def copy(self):
        _new = SinRobot()
        _new.shape = self.shape.copy()
        return _new
                
    def randomize(self, base_robot, w = 5, h = 5):
        count = 0
        while True:
            # Only change the voxels which base_robot[i] == -1
            if base_robot is not None:
                print(f"base_robot:\n{base_robot}")
                change_indexs = (base_robot == -1)
                self.shape = base_robot.copy()
                self.shape[change_indexs] = np.random.randint(0, 5, size=change_indexs.sum())
                print(f"base_robot:\n{base_robot}")
                print(f"robot:\n{self.shape}")
                if self.valid():
                    break
                count += 1
                if(count > 5000):
                    raise Exception("Can't find a valid random robot after 5000 tries!")
            else:
                self.shape = np.random.randint(0,5,(w,h))
                if self.valid():
                    break
                count += 1
                if (count > 5000):
                    raise Exception("Can't find a valid random robot after 5000 tries!")
    
    def count_actuators(self):
        count = 0
        for _x in self.shape.flatten():
            if _x == 3 or _x == 4:
                count += 1

        return count

    def action(self, steps):
        action = []
        for _ in range(self.count_actuators()):
            action.append(np.sin(steps/3 + (_*0.1))+1)
        return np.array(action)
