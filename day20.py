import numpy as np
from collections import defaultdict, Counter
from itertools import product
from tqdm.auto import tqdm

def load_inputs(path): 
    with open(path) as f:
        encoding, image = f.read().split("\n\n")
        image = image.split("\n")
    return encoding.strip(), image

def get_neighbors(i, j):
    return [(i+di, j+dj) for di in [-1, 0, 1] for dj in [-1, 0, 1]]

def get_index(string):
    binary = string.replace("#", "1").replace(".", "0")
    return int(binary, base=2)

def update_image(image, encoding, min_, max_, pad=1, step=1):
    
    # What is happening here?
    # Somewhere far away in the infinite plane, at t = 0, they all encode to item 0. (...|...|...). 
    # If encode[0] == ".", then we get (... | ... | ...) again in t=1.
    # If encode[0] == "#", then we get (### | ### | ###) in t = 1
    # So oscillations can occur.
    # Here we are setting the boundary to be what it will be in t=step.
     
    if encoding[0] == "#" and encoding[-1] == ".":
        # Oscillations occur
        output = defaultdict(lambda: ".") if step % 2 == 0 else defaultdict(lambda: "#")
    elif encoding[0] == ".":
        output = defaultdict(lambda: ".")
    elif encoding[1] == "#" and encoding[-1] == "#":
        output = defaultdict(lambda: ".") if step == 1 else defaultdict(lambda: "#")
        
    for i, j in product(range(min_-pad, max_+pad), repeat=2):
        neighbors = get_neighbors(i, j)
        string = ""
        for neighbor in neighbors:
            string += image[neighbor]
        idx = get_index(string)
        output[i, j] = encoding[idx]
        
    return output, min_-1, max_+1
    
def print_image(image_dict, min_, max_):
    image = np.empty([max_ - min_]*2).astype(str)
    for (i, j) in product(np.arange(image.shape[0]), repeat=2):
        image[i, j] = image_dict[i+min_, j+min_]
    
    total = ["".join(image[i, :]) for i in range(image.shape[0])]
    print("\n".join(total).replace("1", "#").replace("0", " "))
    
def count_lights(image_dict, min_, max_):
    image_dict = {key: value for key, value in image_dict.items() if (min_ <= key[0] <= max_) and (min_ <= key[1] <= max_)}
    return Counter(image_dict.values())["#"]
    
    
if __name__ == "__main__":
    encoding, image = load_inputs("inputs/day20.txt")
    image_dict = defaultdict(lambda: ".")
    image_arr = np.array([[i for i in line] for line in image])
    min_, max_ = 0, image_arr.shape[0]
    for i in range(image_arr.shape[0]):
        for j in range(image_arr.shape[1]):
            image_dict[i, j] = image_arr[i, j]
    
    for i in tqdm(range(50)):
        image_dict, min_, max_ = update_image(image_dict, encoding, min_, max_, step=i+1)
        if i == 1 or i == 49: print(count_lights(image_dict, min_, max_))
    
