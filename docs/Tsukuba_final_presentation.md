---
marp: true
theme: default
---

<style>  
section.small-text {  
font-size: 20px;  
}  
</style>

<style>  
section.median-text {  
font-size: 28px;  
}  
</style>
# Evogym

#### LIN CHE CHENG

---
# Topic
## 1. Improve efficiency  on Genetic Algorithm through Local Search

## 2. Stability-Oriented Evaluation

---
<!-- _class: median-text -->
# Evogym
Evogym is a simulation environment that can simulate many different tasks with soft robots. 

A soft robot is composed of 5 different materials. Each kind of materials has its own spring constant.

My research focuses on using evolutionary computing algorithms to modify the body of soft robots in order to find a suitable robot.

![bg vertical fit right](images/Evogym_illustration_1.png)
![bg fit right](images/Evogym_illustration_2.png)

---

# Local Search

Local Search is a local optimization algorithm which only imporves the solution by moving to a better neighborhood. Because of its greedy nature, it can quickly find a local optimum. In the other hand, it lacks exploration ability.

I try to combine Local Search and Genetic Algorithm (GA) to develop a hybrid approach that can find a solution more efficiently. 

| Features\Algorithm     | Local Search | Genetic Algorithm (GA) |
| ---------------------- | ------------ | ---------------------- |
| Population Convergence | slow         | quick                  |
| Exploration            | poor         | good                   |
| Evolution              | individual   | population             |

---

# Algorithms

To integrate Local Search with GA, I explored two approaches. The first approach applies Local Search before the GA. The second approach interleaves Local Search with the GA.

![width:900](images/Integrate_LS_with_GA_in_two_approaches.png)

---
<!-- _class: median-text -->
# Memetic Algorithm (MA)
In the MA, Local Search performed behind the GA in each round.
For reducing the computational cost, Local Search is applied to only a certain proportion of the population.


![bg fit right](images/GA_with_local_search_flow_chart.png)

---
<!-- _class: small-text -->
# Experiment Results

My analysis focuses on three aspects: fitness, similarity, and the effects by Local Search.

I also compared two Local Search algorithms, Hill Climbing and Evolutionary Strategy, to investigate their impact on the overall performance.

Applying Local Search before GA can enables the algorithm to identify better individuals in the early stages.

The MA achieves lowest similarity while maintaining a high fitness in final.

For effects of Local Search, Evolutionary Strategy (ES) performs better than Hill Climbing (HC).

**Task**:
1. Climber-v0T
2. ObstacleTraverser-v0T
![bg fit vertical right](images/LS_at_different_stages_Climber-v0T.png)
![bg fit right](images/LS_at_different_stages_ObstacleTraverser-v0T.png)


---

# Stability-Oriented Evaluation

The method of fitness evaluation in Evogym usually use the distance to start point as score.
**formula**: 
$$
fitness = position2 - position1
$$

![width:800](images/score_evaluation.png)

---
<!-- _class: small-text -->
# Stability-Oriented Evaluation

However, robots fail to learn the locomotion strategy required for the task in some cases. Therefore, I designed a new evaluation method to encourage the robots to learn the correct locomotion behavior.

There is a bonus simulation $\Delta t$ continues the original simulation. We calculate the speeds for each of the two stages seperately and its $ratio = (speed2 - speed1) / |speed1|$. The final score will be the original score multiplied by $sigmoid(ratio)$.

**formula**: 
$$
\begin{align}
& sigmoid(x) = \frac{1}{(1+e^{-4(x+1)})} \\
& fitness_{mod} = fitness \times sigmoid(ratio) \\
\end{align}
$$

![width:550](images/sigmoid_function.png)![width:550](images/score_strong_evaluation.png)

---
<!-- _class: small-text -->
# Experiment Results

**Task**: Climber-v0T
Upper part: my evaluation
Lower part: old evaluation

The successful rate from 40% up to 90%.
![bg fit right:70%](images/robust_compare.gif)

---

# Future Works

1. Compared with conventional Local Search, ES is more effective at finding high-quality solutions. In future work, I plan to integrate more ES-related techniques into my framework.
2. Currently, the Stability-Oriented Evaluation is limited to tasks involving repetitive motions and may lead to reduced speed. Future work will focus on generalizing the approach to a broader range of tasks.