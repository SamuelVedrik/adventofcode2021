import numpy as np
from scipy.signal import correlate

def load_input(path): 
    with open(path) as file: 
        input_ = file.read()
    inputs = input_.split("\n")
    inputs = np.array([int(i) for i in inputs])
    return inputs

def part_one(inputs):
    sum_ = 0
    for prev, next_ in zip(inputs, inputs[1:]): 
        sum_ += next_ > prev
    return sum_

def numpy_part_one(inputs): 
    return ((inputs[1:] - inputs[:-1]) > 0).sum()
    
def part_two(inputs):
    values = inputs[:-2] + inputs[1:-1] + inputs[2:]
    sum_ = 0
    for prev, next_ in zip(values, values[1:]): 
        sum_ += next_ > prev
    return sum_

def numpy_part_two(inputs): 
    values = inputs[:-2] + inputs[1:-1] + inputs[2:]
    return ((values[1:] - values[:-1]) > 0).sum()

if __name__ == "__main__": 
    inputs = load_input("inputs/day1.txt")
    print(numpy_part_one(inputs))
    print(numpy_part_two(inputs))
    