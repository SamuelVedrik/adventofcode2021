import numpy as np

def load_input(path): 
    with open(path) as file: 
        input_ = file.read()
    return input_.split("\n")

def part_one():
    inputs = load_input("inputs/day1.txt")
    inputs = [int(i) for i in inputs]
    sum_ = 0
    for prev, next_ in zip(inputs[:-1], inputs[1:]): 
        sum_ += 1 if next_ > prev else 0
    print(sum_)
    
def part_two():
    inputs = load_input("inputs/day1.txt")
    inputs = [int(i) for i in inputs]
    arr = np.array(inputs)
    values = arr[:-2] + arr[1:-1] + arr[2:]
    sum_ = 0
    for prev, next_ in zip(values[:-1], values[1:]): 
        sum_ += 1 if next_ > prev else 0
    print(sum_)
    

if __name__ == "__main__": 
    part_one()
    part_two()
    