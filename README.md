# Milo's Softrobot Project (adapted from [Yet Another Soft Robot Evolver](https://codeberg.org/caranha/YASRE))

This repository uses [Evolution Gym](https://evolutiongym.github.io).
It's a project in my short-term exchange period in University of Tsukuba.

![](log/robust_compare.gif)

## Files
- `Search.py`: uses simple search algorithms to optimize the robot body 
for a given task. Random Search, GA and ES are implemented. Use `python 
Search.py -h` for options.

- `Visualize.py`: Visualizes the result of one robot running on one 
world file (note: it does not need to be the same ones that ran together 
originally!). Use `python Visualize -h` for options.

- `run.sh`: Used to run batch processes with one command. `$./run.sh`

- `EC_algorithms/`: To store algorithms and functions used by algorithms.

- `EC_algorithms/utils.py`: Functions used by algorithms.

- `EC_algorithms/logger.py`: A object used for record information during the algorithm running.

- `world/`: Objects define calculation method or start position for different task. The world json files store in evogym_world folder. sim_files include the world files in Evogym that not transform yet. T_world folder include the world files compatible with  YASRE.

- `world/json_transformer.py`: A function can transform world in Evogym to a json file can be used in YASRE. 

- `robot/`: Contain objects for robot.

- `log/`: Store log files. You can change the path with `-d` option in Search.py.

- `evaluation/evaluate.py`: Define evaluation method.  

## How to Install:
- Create a local python 3.10 environment using pyenv or similar
- Install evogym: `pip install evogym --upgrade` (See evogym repository for details)
- Install linux dependencies (for evogym): `sudo apt install xorg-dev libglu1-mesa-dev`
- Install python dependencies (for evogym): `pip install glfw PyOpenGL ttkbootstrap` 
- Install python dependencies (for this repo): `pip install pygifsicle imageio`

## Report
