import numpy as np


def load_inputs(path): 
    with open(path) as file: 
        inputs = file.readlines()
    return [[int(i) for i in input.strip()] for input in inputs]

def get_adj(i, j, bound_i, bound_j): 
    points_check = np.array([[i-1, j], [i+1, j], [i, j-1], [i, j+1]])
    points_check = points_check[(0 <= points_check[:, 0]) & (points_check[:, 0] < bound_i), :]
    points_check = points_check[(0 <= points_check[:, 1]) & (points_check[:, 1] < bound_j), :]
    return points_check

def get_is_low(inputs, i, j):
    points_check = get_adj(i, j, *inputs.shape)
    return (inputs[points_check[:, 0], points_check[:, 1]] > inputs[i, j]).sum() == points_check.shape[0]

def part_one():
    inputs = load_inputs("inputs/day9.txt")
    inputs = np.array(inputs)
    is_low = np.zeros_like(inputs).astype(bool)
    for i in range(inputs.shape[0]):
        for j in range(inputs.shape[1]): 
            is_low[i, j] = get_is_low(inputs, i, j)
    
    print(inputs[is_low].sum() + is_low.sum())
    
def get_children(inputs, i, j):
    points_check = get_adj(i, j, *inputs.shape)
    children = []
    for child_i, child_j in points_check:
        if inputs[child_i, child_j] != 9 and inputs[child_i, child_j] > inputs[i, j]:
            children.append((child_i, child_j))
            
    return children

def dfs(inputs, i, j):
    can_flow = [(i, j)] 
    visited = set(can_flow)
    while len(can_flow) != 0:
        parent = can_flow.pop()
        children = get_children(inputs, *parent)
        for child in children: 
            if child not in visited:
                can_flow.append(child)
                visited.add(child)
    return len(visited)
    
    

def part_two():
    inputs = load_inputs("inputs/day9.txt")
    inputs = np.array(inputs)
    is_low = np.zeros_like(inputs).astype(bool)
    for i in range(inputs.shape[0]):
        for j in range(inputs.shape[1]): 
            is_low[i, j] = get_is_low(inputs, i, j)
    
    basins = np.transpose(is_low.nonzero())
    values = {}
    # some kind of cursed DFS
    for i, j in basins:  
        values[(i, j)] = dfs(inputs, i, j)
        
    top_basins = sorted(list(values.values()))[-3:]
    print(top_basins[0] * top_basins[1] * top_basins[2])
    
    
if __name__ == "__main__": 
    part_one()
    part_two()