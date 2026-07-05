import time, os

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
  def __init__(self, world, sim_step, evo_step):
    self.world = world
    self.sim_step = sim_step
    self.evo_step = evo_step

  def update_evo_step(self, evo_step):
    self.evo_step = evo_step

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
  
    self.world.sim = None
    #FIXME: should fix the world state engine 
    #       to avoid reloading the json file all the time
  
    etime = time.time()

    return score, (etime - stime)
  
