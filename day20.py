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

def update_image(image, encoding, min_, max_, PAD=100):
    output = defaultdict(lambda: ".")
    for i, j in product(range(min_-PAD, max_+PAD), repeat=2):
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
        image_dict, min_, max_ = update_image(image_dict, encoding, min_, max_)
        if i == 1:
            print(count_lights(image_dict, min_, max_))
        if i == 49:
            print(count_lights(image_dict, min_, max_))
    