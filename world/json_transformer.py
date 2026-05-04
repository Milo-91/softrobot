# It all from EvoWorld

def add_from_array(
    self, 
    name: str, 
    structure: np.ndarray, 
    x: int, 
    y: int, 
    connections: Optional[np.ndarray] = None) -> None:
    """
    Add a single object to the world from array.

    Args:
        name (str): object name.
        structure (np.ndarray): `(n, m)` array specifing the voxel structure of the object. See `evogym.VOXEL_TYPES`. 
        x (int): x-position of the bottom & leftmost voxel of the object. Starts at `0`.
        y (int): y-position of the bottom & leftmost voxel of the object. Starts at `0`.
        connections (Optional[np.ndarray]): `(2, k)` array specifying `k` pairwise voxel connections. Voxels are specified by their index into the 1D array `np.flatten(structure)`. The default behavior assumes all adjacent voxels are connected. (default = None)
    """
    new_obj = WorldObject.from_array(name, structure, connections)
    new_obj.set_pos(x, y)
    self.add_object(new_obj)

def load_from_parsed_json(self, name: str, json_data: Any, grid_size: Pair) -> None:
    """
    Load object from parsed `json` data. It is recommended to use `WorldObject.load_from_json()` instead.

    Args:
        name (str): object name.
        json_data (Any): parsed json data.
        grid_size (Pair): grid size of world object is loaded from.
    """
    self.name = name

    # read in indices
    voxels = []
    index_to_voxel = {}
    num_voxels = len(json_data['indices'])
    for i in range(num_voxels):
        index_curr = json_data['indices'][i]
        voxels.append(
            Pair(index_curr % grid_size.x, index_curr // grid_size.x))
        index_to_voxel[index_curr] = voxels[-1].copy()

    if len(voxels) == 0:
        raise ValueError(f'object {self.name} has no voxels')

    #compute bounding box
    max_voxel = voxels[0].copy()
    min_voxel = voxels[0].copy()

    for voxel in voxels:
        max_voxel = max_voxel.each_max(voxel)
        min_voxel = min_voxel.each_min(voxel)

    # translate voxels according to bounding box
    self.pos = min_voxel.copy()
    self.grid_size = max_voxel - min_voxel + Pair(1, 1)

    self.voxels = []
    for voxel in voxels:
        self.voxels.append(voxel - self.pos)

    for index in index_to_voxel.keys():
        index_to_voxel[index] = index_to_voxel[index] - self.pos

    # set grid and neighbors
    grid: List[List[int]] = []
    for y in range(self.grid_size.y):
        grid.append([])
        for x in range(self.grid_size.x):
            grid[-1].append(0)

    self.neighbors = {}
    for voxel in self.voxels:
        self.neighbors[voxel] = []

    for i in range(num_voxels):
        index_curr = json_data['indices'][i]
        voxel_curr = index_to_voxel[index_curr]
        grid[voxel_curr.y][voxel_curr.x] = json_data['types'][i]
        for nei in json_data['neighbors'][f'{index_curr}']:
            if not nei in index_to_voxel:
                raise ValueError(
                    f'object {self.name} has voxels with invalid neighbors'
                )
            nei_voxel = index_to_voxel[nei]
            self.neighbors[voxel_curr].append(nei_voxel)

    self.grid = np.array(grid)
