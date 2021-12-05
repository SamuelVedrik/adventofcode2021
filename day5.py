import numpy as np 

def load_inputs(path): 
    with open(path) as file: 
        inputs = file.readlines()
    inputs = [input_.replace(" -> ", ",") for input_ in inputs]
    inputs = [[int(num) for num in input_.split(",")] for input_ in inputs]
    return inputs

def get_span(coords):
    """
    coords is in the form [x1, y1, x2, y2]
    """
    dir_vector = coords[2:] - coords[:2]
    # Normalize so for 1 change in x 
    if dir_vector[0] == 0:
        dir_vector = dir_vector / abs(dir_vector[1])
        distance_spanned = abs(coords[3] - coords[1]) + 1
    else:
        dir_vector = dir_vector / abs(dir_vector[0])
        distance_spanned = abs(coords[2] - coords[0]) + 1
    
    span = []
    for t in range(distance_spanned): 
        span.append((coords[:2] + (t*dir_vector)).astype(int))
    return np.stack(span)

def part_one():
    inputs = load_inputs("inputs/day5.txt")
    inputs = np.array(inputs)
    grid = np.zeros((inputs[:, [0, 2]].max()+1, inputs[:, [1, 3]].max()+1))
    for line in inputs:
        x1, y1, x2, y2 = line
        if x2 == x1 or y2 == y1:
            points_covered = get_span(line)
            grid[points_covered[:, 0], points_covered[:, 1]] += 1
    
    print((grid >= 2).sum())
    
def part_two():
    inputs = load_inputs("inputs/day5.txt")
    inputs = np.array(inputs)
    grid = np.zeros((inputs[:, [0, 2]].max()+1, inputs[:, [1, 3]].max()+1))
    for line in inputs:
        points_covered = get_span(line)
        grid[points_covered[:, 0], points_covered[:, 1]] += 1
        
    print((grid >= 2).sum())
    
if __name__ == "__main__": 
    part_one()
    part_two()