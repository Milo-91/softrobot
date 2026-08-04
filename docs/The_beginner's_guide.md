---
time: 2026/04/14 ~ 2026/07/29
author: LIN CHE CHENG
---
# Links
My Github: https://github.com/Milo-91/softrobot
# Preface
Welcome. This is my reflection paper of my directed research for four month. I studied about Evogym and Evolutionary Algorithm. I will record my journey including what I studied, what I did, and what troubles I met. Hope this reflection can help you in your research.
# Environments
The environments I used is the project wrote by Claus, called YASRE. This is a simple version of Evogym. You can just follow installation guide on YASRE to install it. The only problem I met is when I install CMake, I got a version conflict. error log `CMake Error at externals/pybind11/CMakeLists.txt:8 (cmake_minimum_required): Compatibility with CMake < 3.5 has been removed from CMake.`. How did I solve is delete the cmake_minimum_required row in each code. 

Note: Because Evogym is a little bit old project, I suggest you to create en environments with virtual environments like conda or docker.
# Tutorial on YARSE
Although I believe you can understand how to use YASRE quickly by reading README and its code, I will simply explain the function of each code, so you can get up to speed quickly. 

There are two main codes in YASRE, `Search.py` and `Visualize.py`. You can use `Search.py` to evolve robots. You need to put json file of a world and class name of robot in robot folder as arguments at least. `Visualize.py` is used to visualize your simulation. By selecting a world and a robot, you can create a gif of the simulation result, or you can print on the screen by adding `-S` option.

My adjustments is I created a folder called EC_algorithms. I store every algorithm in here. And I also created a lot of versions of Plot function. `Plot.py` plots average fitness, similarity, effects of local search for many runs of simulation. `Plot_pop.py` plots population distribution of single run of simulation. `Plot_two_graph.py` is a version can draw the informations without effects of local search. In the original YASRE project, there are only Walker-v0T task. In order to try more tasks in evogym, I created a simple code to transfer evogym world to YASRE compatible json file, which called `json_transformer.py` in the world folder. 

I will introduce my project in detail later.
# My softrobot project
## Structure
```
softrobot/ 
├── Search.py 
├── Visualize.py 
├── Plot.py 
├── run.sh 
├── EC_algorithms/ 
│ ├── GA.py 
│ ├── ES.py 
│ ├── MA.py 
│ ├── Initialze_population.py 
│ ├── logger.py 
│ ├── utils.py 
│ └── local_search/ 
│ ├── hill_climbing.py 
│ ├── evolution_strategy.py 
│ └── tabu_search.py 
├── world/ 
│ ├── json_transformer.py 
│ ├── walk_line.py 
│ ├── climb.py 
│ ├── walk_obstacle.py 
│ └── evogym_world/ 
│ ├── T_world/ 
│ └── sim_files/ 
├── robot/ 
│ └── basicrobot.py 
├── log/ 
└── evaluation/ 
└── evaluate.py
```
- **run.sh**: Used to run batch processes with one command. `$./run.sh`
- **EC_algorithms/**: To store algorithms and functions used by algorithms.
- **EC_algorithms/utils.py**: Functions used by algorithms.
- **EC_algorithms/logger.py**: A object used for record information during the algorithm running.
- **world/**: Objects define calculation method or start position for different task. The world json files store in evogym_world folder. sim_files include the world files in Evogym that not transform yet. T_world folder include the world files compatible with  YASRE.
- **world/json_transformer.py**: A function can transform world in Evogym to a json file can be used in YASRE. 
- **robot/**: Store objects for robot.
- **log/**: Store log files. You can change the path with `-d` option in Search.py.
- **evaluation/evaluate.py**: Define evaluation method.  
## Algorithms
The algorithms I designed is Genetic Algorithm (GA), Memetic Algorithm (MA), Evolutionary Strategy (ES), GA with Initial Population, and some local search algorithms (Hill Climbing, Tabu Search). 
All parameters can be adjust in the `Search.py`. 

Below are the algorithms I studied.
- [test]("Genetic Algorithm (GA).md")
- [[Memetic Algorithm (MA)]]
- [](Local Search.md)
## Analysis methods
- [](fitness analysis.md)
- [[simulation analysis]]
- [[effect of local search analysis]]
- [[population distribution analysis]]
# References I read
## Books
- **Introduction to Evolutionary Computing**: I read this book for understand basic concepts of Evolutionary Computing, I suggest to reading this before researching.
-  **Handbook of Heuristics**: I read this book for understanding MA. If you also want to take research on MA, you can read this book.
## Papers
- **Evolution gym: a large-scale benchmark for evolving soft robots**: Evogym paper.
# My final presentation
[[Tsukuba_final_presentation]]
