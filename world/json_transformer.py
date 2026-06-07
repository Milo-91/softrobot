# Transform evogym json file to YARSE json file

import json
import numpy as np
from typing import Any, List, Dict, Optional


def add_from_json(file_path: str):
    with open(file_path, 'r') as infile:
        state = json.load(infile)

    file_grid_size = (state['grid_width'], state['grid_height'])

    # read in objects
    for name, obj_data in state['objects'].items():

        # assert lists of same length
        if not len(obj_data['indices']) == len(obj_data['types']):
            raise ValueError(
                f'cannot read in file {file_path} with corrupted object {name}'
            )
        if not len(obj_data['indices']) == len(obj_data['neighbors']):
            raise ValueError(
                f'cannot read in file {file_path} with corrupted object {name}'
            )

        array = load_from_parsed_json(obj_data, file_grid_size)
        return array


def load_from_parsed_json(json_data: Any, grid_size):
    # read in indices
    voxels = []
    index_to_voxel = {}
    num_voxels = len(json_data['indices'])
    for i in range(num_voxels):
        index_curr = json_data['indices'][i]
        voxels.append((index_curr % grid_size[0], index_curr // grid_size[0]))
        index_to_voxel[index_curr] = voxels[-1]

    if len(voxels) == 0:
        raise ValueError(f'object has no voxels')

    #compute bounding box
    max_voxel = voxels[0]
    min_voxel = voxels[0]

    for voxel in voxels:
        max_voxel = (max(max_voxel[0], voxel[0]), max(max_voxel[1], voxel[1]))
        min_voxel = (min(min_voxel[0], voxel[0]), min(min_voxel[1], voxel[1]))

    print(f'max voxel: {max_voxel}')
    print(f'min voxel: {min_voxel}')

    # translate voxels according to bounding box
    pos = min_voxel
    grid_size = (max_voxel[0] - min_voxel[0] + 1, max_voxel[1] - min_voxel[1] + 1)

    selfvoxels = []
    for voxel in voxels:
        selfvoxels.append((voxel[0] - pos[0], voxel[1] - pos[1]))
        print(f'selfvoxel: {(voxel[0] - pos[0], voxel[1] - pos[1])}')

    for index in index_to_voxel.keys():
        index_to_voxel[index] = (index_to_voxel[index][0] - pos[0], index_to_voxel[index][1] - pos[1])

    # set grid and neighbors
    print(f'grid size: x: {grid_size[0]}, y: {grid_size[1]}')
    grid: List[List[int]] = []
    for y in range(grid_size[1]):
        grid.append([])
        for x in range(grid_size[0]):
            grid[-1].append(0)

    neighbors = {}
    for voxel in selfvoxels:
        neighbors[voxel] = []

    for i in range(num_voxels):
        index_curr = json_data['indices'][i]
        voxel_curr = index_to_voxel[index_curr]
        print(f'voxel_curr: x: {voxel_curr[0]}, y: {voxel_curr[0]}')
        grid[voxel_curr[1]][voxel_curr[0]] = json_data['types'][i]
        for nei in json_data['neighbors'][f'{index_curr}']:
            if not nei in index_to_voxel:
                raise ValueError(
                    f'object has voxels with invalid neighbors'
                )
            nei_voxel = index_to_voxel[nei]
            neighbors[voxel_curr].append(nei_voxel)

   
    return np.array(grid)


def save_json(class_name, filename, grid):
    with open(filename, "w") as out_f:
        data = {"class": class_name,
                "floor": np.flip(grid, axis = 0).tolist()
            }
        json.dump(data,
                  out_f,
                  separators = (',', ':'))

def main():
    grid = add_from_json('/Users/linchecheng/Desktop/上課用/大五下/TsukubaResearch/YASRE/log/evogym_world/sim_files/ObstacleTraverser-v0.json')
    save_json('world.walk_line', 'ObstacleTraverser-v0.json', grid)

if __name__ == '__main__':
    main()
    
