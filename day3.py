import numpy as np 

def load_inputs(path, split_by="\n"): 
    with open(path) as file: 
        inputs = file.read().split(split_by)
    return [[int(input_bit) for input_bit in input_] for input_ in inputs]

def get_most_common(inputs):
    return(inputs.sum(axis=0) >= inputs.shape[0]/2).astype(int)

def binary_to_int(arr): 
    arr = str(arr).strip("[]").replace(" ", "")
    return int(arr, base=2)

def part_one(): 
    inputs = load_inputs("inputs/day3.txt")
    inputs = np.array(inputs)
    gamma = binary_to_int(get_most_common(inputs))
    epsilon = binary_to_int(1-get_most_common(inputs))
    print(gamma, epsilon)
    print(gamma * epsilon)

def part_two():
    inputs = load_inputs("inputs/day3.txt")
    inputs = np.array(inputs)
    current_considering = inputs.copy()
    oxygen = None
    for i in range(inputs.shape[0]):
        curr_bit = get_most_common(current_considering)[i]
        current_considering = current_considering[current_considering[:, i] == curr_bit]
        if current_considering.shape[0] == 1:
            oxygen = binary_to_int(current_considering[0])
            break
        
    co2 = None
    current_considering = inputs.copy()
    for i in range(inputs.shape[0]):
        curr_bit = 1 - get_most_common(current_considering)[i]
        current_considering = current_considering[current_considering[:, i] == curr_bit]
        if current_considering.shape[0] == 1:
            co2 = binary_to_int(current_considering[0])
            break
    print(oxygen, co2)
    print(oxygen * co2)

    
if __name__ == "__main__": 
    part_one()
    part_two()
    
    
    
        