import numpy

def load_inputs(path): 
    with open(path) as file: 
        input_ = file.readlines()
    return input_

def get_pos(inputs): 
    depth = 0
    hori = 0
    for instruction, value in inputs: 
        if instruction == "forward": 
            hori += value
        elif instruction == "down": 
            depth += value
        elif instruction == "up": 
            depth -= value
        else: 
            print("invalid value")
    return depth, hori

def get_pos_part2(inputs): 
    aim = 0
    hori = 0
    depth = 0
    for instruction, value in inputs: 
        if instruction == "forward": 
            hori += value 
            depth += (value * aim)
        elif instruction == "down": 
            aim += value
        elif instruction == "up": 
            aim -= value
        else: 
            print("invalid value")
    return depth, hori

def part_one():
    inputs = load_inputs("inputs/day2.txt")
    inputs_new = []
    for input_ in inputs: 
        instruction, value = input_.split(" ")
        inputs_new.append((instruction, int(value)))
    depth, hori = get_pos(inputs_new)
    print(depth * hori)
    
def part_two():
    inputs = load_inputs("inputs/day2.txt")
    inputs_new = []
    for input_ in inputs: 
        instruction, value = input_.split(" ")
        inputs_new.append((instruction, int(value)))
    depth, hori = get_pos_part2(inputs_new)
    print(depth * hori)

if __name__ == "__main__": 
    part_one()
    part_two()
    
