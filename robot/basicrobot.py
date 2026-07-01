import json
import numpy as np
from evogym import is_connected
import uuid

def get_random(w = 5, h = 5):
    r = SinRobot()
    r.randomize(w, h)
    return r

def get_fromfile(filename):
    r = SinRobot()
    r.load_json(filename)
    return r

def mutate(parent, size = 1):
    child = SinRobot(shape=parent.shape.copy())
    for _ in range(size):
        count = 0
        while True:
            old_shape = child.shape.copy()
            pos = tuple(np.random.randint(0,5,2))
            new_voxel = np.random.randint(0,5)
            child.shape[pos] = new_voxel
            if child.valid():
                break

            child.shape = old_shape
            count += 1
            if count > 5000:
                raise Exception("Can't find a valid mutation after 5000 tries!")
    return child
            
def crossover(parent1, parent2):
    count = 0

    while True:
        count += 1
        child1 = parent1.copy()
        child2 = parent1.copy()

        pos = np.random.randint(0,4)

        for i in range(5):
            if i > pos:
                for j in range(5):
                    child1.shape[(i,j)] = parent1.shape[(i,j)]
                    child2.shape[(i,j)] = parent2.shape[(i,j)]
            else:
                for j in range(5):
                    child1.shape[(i,j)] = parent2.shape[(i,j)]
                    child2.shape[(i,j)] = parent1.shape[(i,j)]

        if child1.valid():
            return child1
        if child2.valid():
            return child2

        if count > 5000:
            return parent1.copy()


class SinRobot:
    
    def __init__(self, shape=None):
        self.id = uuid.uuid4().hex
        self.score = 0
        if shape is None:
            self.shape = np.array([[1]])
        else:
            self.shape = shape

    def set_score(self, score):
        self.score = score

    @classmethod
    def get_id(cls):
        cls.index += 1
        return cls.index

    def valid(self):
        return (is_connected(self.shape) and
                (3 in self.shape or 4 in self.shape))

    def save_json(self, filename):
        with open(filename, "w") as out_f:
            data = {"class": __name__, "shape": self.shape.tolist()}
            json.dump(data,
                      out_f,
                      separators = (',', ':'))

    def save_txt(self, comment, filename):
        with open(filename, 'a') as f:
            print(comment, file=f)
            print(f'id: {self.id}', file=f)
            print(f'score: {self.score}', file=f)
            print(*(self.shape.tolist()), sep='\n', file=f)
            print('\n', file=f)

    def load_json(self, filename):
        with open(filename, "r") as in_f:
            rdata = json.loads(in_f.read())
            if rdata["class"] != __name__:
                raise Exception("Invalid File!")
            self.shape = np.array(rdata["shape"])

    def copy(self):
        _new = SinRobot(self.shape.copy())
        return _new
            
    def randomize(self, w = 5, h = 5):
        count = 0;
        while True:
            self.shape = np.random.randint(0,5,(w,h))
            # print(self.shape)
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

