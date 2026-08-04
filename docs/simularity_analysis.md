---
tags:
  - fleeting
---
# Introduction
Analyzing the simulation in each stage of population. Calculating method is according to Hamming Disctance.
The information will be stored in `{prefix}_simulation_record.csv`
# Formula
Pairwise hamming distance
$mean\_distance = \frac{\sum_i^n d_i}{d_{max} * n} \in [0, 1], d_i \text{ is hamming distance of any two robots.}$
$similarity = \frac{1}{\alpha * mean\_distance} \in [0.1, \infty), \alpha=10$
```python
def hamming_distance(r1, r2):
    # calculate the total number of different voxels
    r1_shape = list(itertools.chain(*(r1.shape.tolist())))
    r2_shape = list(itertools.chain(*(r2.shape.tolist())))
    distance = sum(r1 != r2 for r1, r2 in zip(r1_shape, r2_shape))
    normalized_distance = distance / len(r1_shape)

    return normalized_distance

def calculate_similarity(population):
    distance = 0
    alpha = 10
    count = 0
    for r1 in population:
        for r2 in population:
            if r1.id == r2.id:
                continue
            distance += hamming_distance(r1, r2)
            count += 1
    
    mean_distance = distance / count

    return 1 / (alpha * mean_distance + 1) # similarity = 1 / (alpha * distance + 1) alpha is scaling factor which make the distance in [0, 10]
```