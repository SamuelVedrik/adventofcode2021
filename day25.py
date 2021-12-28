from scipy.signal import correlate2d
import numpy as np
from tqdm.auto import tqdm

def load_inputs(path): 
    with open(path) as f: 
        inputs = f.read().splitlines()
        inputs = [list(input_) for input_ in inputs]
    
    return np.array(inputs)

def parse(inputs):
    inputs = np.where(inputs == "v", 1, inputs)
    inputs = np.where(inputs == ">", 2, inputs)
    inputs = np.where(inputs == ".", 0, inputs)
    return inputs

def reverse(inputs):
    inputs = np.where(inputs == 1, "v", inputs)
    inputs = np.where(inputs == "2.0", ">", inputs)
    inputs = np.where(inputs == "0.0", ".", inputs)
    return inputs
    

def single_step_right(floor):
    right_filter = np.zeros((3, 3))
    right_filter[1, 2] = 1
    right = correlate2d(floor, right_filter, mode="same", boundary="wrap")
    new = floor.copy()
    
    valid_move = (right == 0) & (floor == 2)
    ids = np.transpose(np.nonzero(valid_move))
    new[ids[:, 0], ids[:, 1]] = 0
    new[ids[:, 0], (ids[:, 1] + 1) % (floor.shape[1])] = 2
    return new
    
def single_step_bottom(floor):
    bottom_filter = np.zeros((3, 3))
    bottom_filter[2, 1] = 1
    bottom = correlate2d(floor, bottom_filter, mode="same", boundary="wrap")
    new = floor.copy()
    
    valid_move = (bottom == 0) & (floor == 1)
    ids = np.transpose(np.nonzero(valid_move))
    new[ids[:, 0], ids[:, 1]] = 0
    new[(ids[:, 0] + 1) %(floor.shape[0]), ids[:, 1]] = 1
    
    return new

def single_step(floor):
    floor = single_step_right(floor)
    floor = single_step_bottom(floor)
    return floor

if __name__ == "__main__": 
    inputs = load_inputs("inputs/day25.txt")
    inputs = parse(inputs).astype(np.float64)
    steps = 1
    with tqdm() as pbar:
        while True:
            new = single_step(inputs)
            if (new == inputs).all(): 
                break
            steps += 1
            inputs = new
            pbar.update(1)
    
    print(steps)
    