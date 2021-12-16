from functools import lru_cache
from math import ceil
import numpy as np

def load_inputs(path): 
    with open(path) as f: 
        input_ = f.read()
    return input_

def convert_hex_to_b(input_):
    value = int(input_, base=16)
    binary = bin(value)[2:]
    final_length = ceil(len(binary)/4)*4
    return binary.rjust(final_length, "0")


def parse_literal(binary):
    num_bits = len(binary) // 5
    total = ""
    for i in range(num_bits):
        consider = binary[i*5:(i+1)*5]
        total += consider[1:]
    return int(total, base=2)

def parse_head(binary):
    version = int(binary[:3], base=2)
    type_id = int(binary[3:6], base=2)
    return version, type_id
    
@lru_cache(maxsize=None)
def get_literal_length(binary):
    working = binary[6:]
    i = 6
    while True:
        i += 5
        if working[0] == "0": 
            break
        else:
            working = working[5:]
    return i

@lru_cache(maxsize=None)
def get_operator_length(binary):
    version, type_id = parse_head(binary[:6])
    length_type_id = binary[6]
    if length_type_id == "0":
        children_length = int(binary[7:22], base=2)
        return 22 + children_length
    else:
        children = get_children(binary[6:])
        children_length = 0 
        for child in children:
            children_length += get_length(child)
        return 18 + children_length

@lru_cache(maxsize=None)
def get_length(binary):
    """
    Binary includes all data (head and all)
    """
    version, type_id = parse_head(binary[:6])
    if type_id == 4: 
        length = get_literal_length(binary)
    else: 
        length = get_operator_length(binary)
    return length 
  
@lru_cache(maxsize=None)
def get_children_bits(binary): 
    """
    Binary is bit operator, does not include the head
    returns list of binary children
    """
    total_length = int(binary[1:16], base=2)
    working = binary[16:]
    curr_length = 0
    children = []
    while curr_length < total_length:
        length = get_length(working)
        children.append(working[:length])
        curr_length += length
        working = working[length:]
    return children

@lru_cache(maxsize=None)
def get_children_num_packets(binary):
    total_children = int(binary[1:12], base=2)
    working = binary[12:]
    children = []
    while len(children) < total_children:
        length = get_length(working)
        children.append(working[:length])
        working = working[length:]
    return children    

@lru_cache(maxsize=None)
def get_children(binary):
    """
    Binary is operator packet, does not contain the head
    """
    length_type_id = binary[0]
    if length_type_id == "0":
        return get_children_bits(binary)
    else:
        return get_children_num_packets(binary)
    
@lru_cache(maxsize=None)
def parse_input(binary):
    version, type_id = parse_head(binary)
    if type_id == 4:
        value = parse_literal(binary[6:])
    else: 
       children = get_children(binary[6:])
       value = [parse_input(child) for child in children]
    return version, type_id, value

def get_total_version(tree):
    version, type_id, children = tree
    if isinstance(children, int):
        return version
    else:
        total = version
        for child in children:
            total += get_total_version(child)
        return total

def parse_tree(tree):
    version, type_id, children = tree
    if type_id == 4: 
        return children
    elif type_id == 0:
        return sum(parse_tree(child) for child in children)
    elif type_id == 1:
        return np.prod([parse_tree(child) for child in children])
    elif type_id == 2:
        return np.min([parse_tree(child) for child in children])
    elif type_id == 3:
        return np.max([parse_tree(child) for child in children])
    elif type_id == 5: 
        return int(parse_tree(children[0]) > parse_tree(children[1]))
    elif type_id == 6:
        return int(parse_tree(children[0]) < parse_tree(children[1]))
    elif type_id == 7:
        return int(parse_tree(children[0]) == parse_tree(children[1]))
    
if __name__ == "__main__": 
    inputs = load_inputs("inputs/day16.txt")
    inputs = convert_hex_to_b(inputs)
    tree = parse_input(inputs)
    print(get_total_version(tree))
    print(parse_tree(tree))
    