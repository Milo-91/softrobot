import os, time, sys
import importlib, json
import numpy as np

from optparse import OptionParser

def main():
  options, args = parse_args()

  today  = time.strftime("%m%d%H%M")
  prefix = options.prefix

  # Loading the world from a module (random) or file (fixed)
  if (args[0][-5:] == ".json"):
    print(f"Loading world from file {args[0]}.")
    with open(args[0], "r") as in_f:
      _rdata = json.loads(in_f.read())
      world_m = importlib.import_module(_rdata["class"])
    world = world_m.get_fromfile(args[0])

  else:
    print(f"Creating new world from module {args[0]}.")
    world_m = importlib.import_module("."+args[0], "world")
    world = world_m.get_random()
    world.save_json(f"{prefix}world_{today}.json")

  # Loading robot from a module
  robot_m = importlib.import_module("."+args[1], "robot")
  best_robot = None
  best_score = None
  
  for rep in range(options.evo_step):
    if (best_robot is None):
      robot = robot_m.get_random()
    else:
      world.clear_robot()
      if (options.search_algorithm == "random"):
        robot = robot_m.get_random()
      if (options.search_algorithm == "ES"):
        robot = best_robot.copy()
        robot.mutate(size = 2)

    robot = robot_m.get_random()

    world.set_robot(robot)
    world.reset()
    
    for _ in range(options.sim_step):
      world.step()

      score = world.get_score()

    if (best_robot is None or best_score < score):
      best_score = score
      best_robot = robot.copy()
      print("New best score: {}".format(best_score))
      best_robot.save_json(f"{prefix}robot_{today}_{rep:05}.json")

  

def parse_args():
  usage = "usage: %prog [options] <world type> <robot type>"
  desc = """Performs a random search on the environment "world type", using
"robot type". By default, creates a json file named
`world_robot_MMDD_ID.json` for every robot that achieves a better
score.
"""
  import world, robot
  
  parser = OptionParser(usage = usage, description = desc) 

  parser.add_option("-s", "--sim_step", default = 400,
                    type="int", action="store",
                    help="Number of Simulation Steps")
  
  parser.add_option("-e", "--evo_step", default = 400,
                    type="int", action="store",
                    help="Number of Random Search Steps")

  algorithms = ["random", "ES"]
  parser.add_option("-A", "--search_algorithm",
                    type = "choice", choices = algorithms,
                    default = algorithms[0],
                    help="Which search algorithm to use")

  parser.add_option("-p", "--prefix",
                    type = "string", default = "",
                    help = "Prefix string for log files")
  
  # parser.add_option("-q", "--quiet", default=True,
  #                   action="store_false", dest="verbose",
  #                   help="Suppress progress output to stdout")
  
  options, args = parser.parse_args()

  if len(args) != 2:
    parser.error("You must provide 2 arguments: world type and robot type")

  # TODO: Detect invalid arguments (non-existing module, invalid file)

  return options, args


if __name__ == "__main__":
  main()
