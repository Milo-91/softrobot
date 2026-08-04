---
tags:
  - fleeting
---
# Introduction
A classic algorithm of Evolutionary Computing. GA is basically composed by 7 components.
1. population
2. objective function 
3. DNA
4. stop criteria
5. selection
6. crossover 
7. mutate
## Population
A bunch of robots. The origin population are from random, and the offspring are based on Selection algorithm.
```python
# Initial population
population = []
rep = popsize

for _ in range(popsize):
	r = robot_m.get_random()
	population.append(r)

# Selection algorithm
# ...
	population = newpop
```

## Objective function
Maximize the scores in task.
## DNA
The inputs that we want to optimize. Take evogym as an example, a DNA will be a list of voxels.
## Stop criteria
The number of generating robots match the number of total step(options.evo_step).
## Selection
Select the Population in the next round, which called offspring. In YASRE, it use Tournament selection to select the offspring. 
### Tournament Selection
1. Set tournament size (k) and the number of offspring (popsize).
2. Random choose k robots from the population.
3. Find the best one. 
4. Repeat step 2-4 until reaching popsize.

```python
def tournament(pop, fit, k = 2):
	idx = random.sample(range(len(pop)), k)
	tpop = []
	tfit = []
	for i in idx:
	    tpop.append(pop[i])
	    tfit.append(fit[i])

	maxidx = tfit.index(max(tfit))

	return tpop[maxidx]

# def GA
# ...
	for _ in range(popsize):
	    p1 = tournament(population, fitness, k = 2)
	    p2 = tournament(population, fitness, k = 2)
	    offspring = p1.crossover(p2)
		if random.random() < mutprob:
		    offspring.mutate()
	    newpop.append(offspring)
	
	    population = newpop
```
## Crossover
Mix two robot to create the offspring. In evogym, the crossover step split two robot from row. random choose row 0 to row 4 to perform crossover. Return a valid one as the offspring. 
```python
def crossover(self, mate):
	count = 0
	while True:
		count += 1
		child1 = self.copy()
		child2 = self.copy()
		pos = np.random.randint(0,4)
		for i in range(5):
			if i > pos:
				for j in range(5):
					child1.shape[(i,j)] = self.shape[(i,j)]
					child2.shape[(i,j)] = mate.shape[(i,j)]
			else:
				for j in range(5):
					child1.shape[(i,j)] = mate.shape[(i,j)]
					child2.shape[(i,j)] = self.shape[(i,j)]
		if child1.valid():
			return child1
		if child2.valid():
			return child2
```
## Mutate
A mutate step will only mutate one position of body, and the position is randomly selected.  It will redo if the new robot is invalid.
```python
# Search.py
mutprob = 0.3 # There is 30% probability of a mutation occurring
if random.random() < mutprob:
	offspring.mutate()

# robot.py
def mutate(self, size = 1):
	for _ in range(size):
		count = 0
		while True:
			old_shape = self.shape.copy()
			pos = tuple(np.random.randint(0,5,2)) # randomly select one position to mutate
			self.shape[pos] = np.random.randint(0,5)
			if self.valid():
				break

			self.shape = old_shape
			count += 1
			if count > 5000:
				raise Exception("Can't find a valid mutation after 5000 tries!")
```
