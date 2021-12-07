import numpy as np

def load_inputs(path): 
    with open(path) as file: 
        inputs = file.read()
    return [int(i) for i in inputs.split(",")]

def part_one():
    inputs = load_inputs("inputs/day7.txt")
    inputs = np.array(inputs)
    align = np.arange(0, np.max(inputs))
    values = abs(inputs.reshape(-1, 1) - align.reshape(1, -1))
    print(values.sum(axis=0).min())
    
def part_two():
    inputs = load_inputs("inputs/day7.txt")
    inputs = np.array(inputs)
    align = np.arange(0, np.max(inputs))
    values = abs(inputs.reshape(-1, 1) - align.reshape(1, -1))
    values = (values * (values + 1)) /2 
    print(values.sum(axis=0).min())

if __name__ == "__main__": 
    part_one()
    part_two()