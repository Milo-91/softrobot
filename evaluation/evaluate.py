import time, os
import random
import numpy as np
import math
import sys

class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.

    Adapted from:
    https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)

class Evaluator:
  def __init__(self, world, sim_step, evo_step, strong_evaluation):
    self.world = world
    self.sim_step = sim_step
    self.evo_step = evo_step
    self.strong_evaluation = strong_evaluation
    self.beta = 70

  def update_evo_step(self, evo_step):
    self.evo_step = evo_step

  def __beta_softplus__(self, x):
    return np.log(1 + math.e ** (x * self.beta))

  def evaluate(self, robot, eval_count, lock):
    # set max evo step
    with lock:
      if eval_count.value >= self.evo_step:
        # print('max evo step reached')
        return 0, 0
      eval_count.value += 1
  
    stime = time.time()
    self.world.restart()
    self.world.set_robot(robot)
    with suppress_stdout_stderr():
      self.world.reset()   
  
    for _ in range(self.sim_step):
      self.world.step()
  
    score = self.world.get_score()
    speed = score / self.sim_step

    if self.strong_evaluation:
      # use delta t to test
      delta_t = int(self.sim_step * random.uniform(0.25, 0.75))
      for _ in range(delta_t):
        self.world.step()

      delta_score = self.world.get_score()
      delta_speed = (delta_score - score) / delta_t

      print(f'old score: {score}')
      score = score * max(min(delta_speed / (speed + sys.float_info.epsilon), 1), 0)
      print(f'new score: {score}')
      
  
    self.world.sim = None
    #FIXME: should fix the world state engine 
    #       to avoid reloading the json file all the time
  
    etime = time.time()

    return score, (etime - stime)
  
