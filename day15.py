import heapq 
import numpy as np 
from collections import defaultdict
from tqdm.auto import tqdm

def load_input(path):
    with open(path) as f: 
        inputs = f.readlines()
    return [[int(i) for i in input.strip() if input != ""] for input in inputs]

def get_adj(i, j, bound_i, bound_j): 
    points_check = np.array([[i-1, j], [i+1, j], [i, j-1], [i, j+1]])
    points_check = points_check[(0 <= points_check[:, 0]) & (points_check[:, 0] < bound_i), :]
    points_check = points_check[(0 <= points_check[:, 1]) & (points_check[:, 1] < bound_j), :]
    return points_check
    


    
def min_cost_bfs(inputs):
    current = []
    heapq.heappush(current, (inputs[0, 0], [(0, 0)]))
    visited_cheapest = defaultdict(lambda: np.inf)
    
    with tqdm() as pbar:
        while current:
            path_val, current_path = heapq.heappop(current)
            i, j = current_path[-1]
            if current_path[-1] == (inputs.shape[0]-1, inputs.shape[1]-1):
                return path_val, current_path
            children = get_adj(i, j, *inputs.shape)
            for child in children:
                (child_i, child_j) = child 
                value = inputs[child_i, child_j]
                total_path_value = path_val + value
                if (child_i, child_j) not in set(current_path):
                    if total_path_value < visited_cheapest[(child_i, child_j)]: 
                        heapq.heappush(current, (total_path_value, current_path + [(child_i, child_j)]))   
                        visited_cheapest[(child_i, child_j)] = total_path_value
            pbar.update(1)            
                   

def part_one():
    inputs = np.array(load_input("inputs/day15.txt"))
    path_val, path = min_cost_bfs(inputs)
    print(path_val - inputs[0, 0])
    
def build_full_size(inputs):
    
    single_row = [inputs]
    for _ in range(4):
        row = single_row[-1] + 1
        row = np.where(row == 10, 1, row)
        single_row.append(row)
    
    single_row = np.concatenate(single_row, axis=1)
    
    columns = [single_row]
    for _ in range(4):
        col = columns[-1] + 1
        col = np.where(col == 10, 1, col)
        columns.append(col)
    

    return np.concatenate(columns, axis=0)
        

if __name__ == "__main__": 
    inputs = np.array(load_input("inputs/day15.txt"))
    inputs = build_full_size(inputs)
    path_val, path = min_cost_bfs(inputs)
    print(path_val - inputs[0, 0])
    