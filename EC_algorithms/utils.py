import itertools
import csv


def record_md(filename, content=None, robot=None):
    with open(filename, 'a') as f:
        if content != None:
            print(content, file=f)
        if robot != None:
            print(f'## {robot.id}', file=f)
            print(f'score: {robot.score}', file=f)
            print(*(robot.shape.tolist()), sep='\n', file=f)

def hamming_distance(r1, r2):
    # calculate the total number of different voxels
    r1_shape = list(itertools.chain(*(r1.shape.tolist())))
    r2_shape = list(itertools.chain(*(r2.shape.tolist())))
    distance = sum(r1 != r2 for r1, r2 in zip(r1_shape, r2_shape))
    normalized_distance = distance / len(r1_shape)

    return normalized_distance


def calculate_similarity(population):
    # pair-wise hamming distance
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

    return 1 / (alpha * mean_distance + 1) # similarity = 1 / (alpha * distance + 1) alpha is scaling factor which make the distance \in [0, 10]
