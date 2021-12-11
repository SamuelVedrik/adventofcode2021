import numpy as np 


test = """
8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848
"""

def load_data(path): 
    with open(path) as f: 
        inputs = f.readlines()
    return np.array([[int(i) for i in input.strip()] for input in inputs])

def update_step(inputs): 
    return inputs + 1 

def get_adjacent(i, j): 
    return np.array([[i+di, j+dj]for dj in range(-1, 2) for di in range(-1, 2) if not ((dj == 0) and (di == 0))] )

def update_flashes(inputs): 
    has_flashed = np.zeros_like(inputs).astype(bool)
    inputs = inputs.copy()
    while (inputs[~has_flashed] > 9).sum():
        flashing = np.transpose(np.nonzero((inputs > 9) & (~has_flashed)))
        for i, j in flashing:
            to_update = get_adjacent(i, j)
            inputs[to_update[:, 0], to_update[:, 1]] += 1
            has_flashed[i, j] = True
    
    return inputs    

def single_day(inputs):
    inputs = inputs.copy()
    inputs = update_step(inputs) 
    inputs = update_flashes(inputs)
    has_flashed = inputs > 9
    inputs[has_flashed] = 0
    return inputs, has_flashed.sum()
        
def part_one():
    inputs = load_data("inputs/day11.txt")
    inputs = np.pad(inputs, 1, constant_values=-np.inf)
    total = 0
    for _ in range(0, 100):
        inputs, num_flashed = single_day(inputs)
        # print(num_flashed)
        total += num_flashed
    print(total)
        
def part_two():
    inputs = load_data("inputs/day11.txt")
    inputs = np.pad(inputs, 1, constant_values=-np.inf)
    day = 1
    while True:
        inputs, num_flashed = single_day(inputs)
        if num_flashed == 100: 
            print(day)
            break
        day += 1
    
    
if __name__ == "__main__": 
    part_one()
    part_two()
    
        
    
    
    