import numpy as np
import functools
from tqdm.auto import tqdm
from collections import defaultdict, Counter

def load_inputs(path): 
    with open(path) as f:
        template, instructions = f.read().split("\n\n")
        instructions = instructions.split("\n")
        instr_dict = {}
        for instruction in instructions:
            k, v = instruction.strip().split(" -> ")
            instr_dict[k] = v
    return template, instr_dict
        
def naive(input_, instructions):
    build = ""
    for (first, second) in tqdm(zip(input_, input_[1:])):
        to_add = f"{first}{second}"
        if to_add in instructions:
            build += f"{first}{instructions[to_add]}"
        else: 
            build += first
                
    return build + input_[-1]

# A sad attempt at making this fast. It's actually still O(n) lol
def recursive_builder(input_, instructions):
    if len(input_) == 1: 
        return input_
    mid = len(input_) // 2
    left = recursive_builder(input_[:mid], instructions)
    right = recursive_builder(input_[mid:], instructions)
    connect = f"{left[-1]}{right[0]}"
    join = instructions.get(connect, "")
    return left + join + right
    
def naive_part_one():
    template, instructions = load_inputs("inputs/day14.txt")
    input_ = template
    for _ in range(10): 
        input_ = recursive_builder(input_, instructions)
        
    unique, counts = np.unique(list(input_), return_counts=True)
    print(counts.max() - counts.min())
    
def build_counters(input_):
    char_counter = Counter(input_)
    bigram_counter = defaultdict(int)
    for first, second in zip(input_, input_[1:]):
        bigram_counter[f"{first}{second}"] += 1
    return char_counter, bigram_counter
     
def counter(char_counter, bigram_counter, instructions):
    
    bigram_copy = defaultdict(int)
    char_copy = defaultdict(int)
    for bigram in bigram_counter:
        if bigram in instructions:
            left, right = bigram
            connect = instructions[bigram]
            bigram_copy[f"{left}{connect}"] += bigram_counter[bigram]
            bigram_copy[f"{connect}{right}"] += bigram_counter[bigram]
            char_copy[connect] += bigram_counter[bigram]
        else: 
            bigram_copy[bigram] += bigram_counter[bigram]
    
    for char, num in char_counter.items():
        char_copy[char] += num
    return char_copy, bigram_copy

if __name__ == "__main__": 
    
    template, instructions = load_inputs("inputs/day14.txt")
    char_counter, bigram_counter = build_counters(template)
    for _ in range(40): #10 for part 1
        char_counter, bigram_counter = counter(char_counter, bigram_counter, instructions)
    
    print(max(char_counter.values()) - min(char_counter.values()))
    
    
    
    