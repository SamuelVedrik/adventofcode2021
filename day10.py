from collections import Counter
import numpy as np

PAIRS = {
    "(" : ")",
    "{" : "}", 
    "[" : "]",
    "<" : ">"
}

SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}
OPEN = set(PAIRS.keys())
CLOSE = set(PAIRS.values())

SCORES2 = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}
def load_inputs(path): 
    with open(path) as f: 
        inputs = f.readlines()
    return inputs

def process_is_corrupt(line):
    stack = []
    for bracket in line: 
        if bracket in OPEN: 
            stack.append(bracket)
        if bracket in CLOSE: 
            curr = stack.pop()
            if PAIRS[curr] != bracket: 
                return True, bracket
    return False, None

def part_one():
    inputs = load_inputs("inputs/day10.txt")
    per_line = []
    for line in inputs: 
        is_corrupt, value = process_is_corrupt(line)
        if is_corrupt: 
            per_line.append(value)
    nums = Counter(per_line)
    total = 0
    for bracket in SCORES:
        total += (SCORES[bracket] * nums[bracket])
    print(total)

def remove_corrupt(inputs):
    return [line for line in inputs if not process_is_corrupt(line)[0]]
    
def get_completion(line):
    stack = []
    for bracket in line: 
        if bracket in OPEN: 
            stack.append(bracket)
        if bracket in CLOSE: 
            curr = stack.pop()
    return [PAIRS[bracket] for bracket in stack[::-1]]
    
def calculate_score(completion): 
    score = 0
    for bracket in completion:
        score *= 5
        score += SCORES2[bracket]
    return score

def part_two():
    inputs = load_inputs("inputs/day10.txt")
    inputs = remove_corrupt(inputs)
    values = []
    for line in inputs: 
        completion = get_completion(line)
        values.append(calculate_score(completion))
    print(np.median(values))
    
    
if __name__ == "__main__":
    part_one()
    part_two()
