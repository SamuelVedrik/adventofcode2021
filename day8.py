import numpy as np 

def load_inputs(path): 
    with open(path) as file: 
        inputs = file.readlines()
    return [input_.split(" | ") for input_ in inputs] 

def part_one():
    inputs = load_inputs("inputs/day8.txt")
    inputs = [[len(i.strip()) for i in input_[1].split(" ")] for input_ in inputs]
    inputs = np.array(inputs)
    print(np.isin(inputs, [2, 3, 4, 7]).sum())
    
def get_encoding(codes):
    encoding = {str(i): None for i in range(10)}
    # Find the unique ones
    for code in codes: 
        if len(code) == 2:
            encoding["1"] = code
        elif len(code) == 3: 
            encoding["7"] = code
        elif len(code) == 4:
            encoding["4"] = code
        elif len(code) == 7: 
            encoding["8"] = code 
    
    # Differentiate the len 6s:
    for code in codes: 
        if len(code) == 6:
            if len(set(encoding["1"]) - set(code)) != 0: 
                encoding["6"] = code
            elif len(set(encoding["4"]) - set(code)) == 0:
                encoding["9"] = code
            elif len(set(encoding["4"]) - set(code)) != 0: 
                # Must be len(set(codes[1]) - set(code)) == 0 as well
                encoding["0"] = code
            
    # Find top right code
    top_right = (set(encoding ["1"]) - set(encoding["6"])).pop()
    # Differentiate the len 5s:
    for code in codes: 
        if len(code) == 5:
            if len(set(encoding["1"]) - set(code)) == 0:
                encoding["3"] = code
            elif top_right in code:
                encoding["2"] = code
            else:
                encoding["5"] = code
                
    return encoding

def part_two():
    inputs = load_inputs("inputs/day8.txt")
    inputs = [
        [[i.strip() for i in input_[0].split(" ")], [i.strip() for i in input_[1].split(" ")]] 
        for input_ in inputs]
    
    sum_ = 0
    for i, codes in enumerate(inputs):
        codes, output_codes = codes
        encoding = get_encoding(codes)
        encoding_r = {frozenset(v): k for k, v in encoding.items()}
        sum_ += int("".join([encoding_r[frozenset(code)] for code in output_codes]))
    
    print(sum_)
 

if __name__ == "__main__": 
    part_one()
    part_two()
        
    
    