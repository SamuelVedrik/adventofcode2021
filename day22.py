from collections import defaultdict
from itertools import product
import re
from tqdm.auto import tqdm

def load_inputs(path): 
    with open(path) as f: 
        inputs = f.readlines()
    
    parsed = []
    for input_ in inputs:
        state, coords = input_.split(" ")
        search = re.search(r"x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)", coords)
        x_val = int(search.group(1)), int(search.group(2))
        y_val = int(search.group(3)), int(search.group(4))
        z_val = int(search.group(5)), int(search.group(6))
        parsed.append((state, x_val, y_val, z_val))
    return parsed

def naive_part_one():
    inputs = load_inputs("inputs/day22.txt")
    # Naive way to store these 
    cube_states = defaultdict(lambda: False)
    # First 20 are within -50, 50
    for state, x_val, y_val, z_val in inputs[:20]:
        for x,y,z in product(range(x_val[0], x_val[1]+1), range(y_val[0], y_val[1]+1), range(z_val[0], z_val[1]+1)):
            cube_states[x,y,z] = (state == "on")
    
    print(sum(1 for coords, state in cube_states.items() if state == True))

def get_intersection(box1, box2):
    x11, x12, y11, y12, z11, z12 = box1
    x21, x22, y21, y22, z21, z22 = box2
    
    x1_int = max(x21, x11)
    x2_int = min(x22, x12)
    y1_int = max(y21, y11)
    y2_int = min(y22, y12)
    z1_int = max(z21, z11)
    z2_int = min(z22, z12)
    
    w = x2_int - x1_int + 1
    l = y2_int - y1_int + 1
    h = z2_int - z1_int + 1
    if all([w > 0, l > 0, h > 0]):
        return (x1_int, x2_int, y1_int, y2_int, z1_int, z2_int)
    return None

def get_volume(box):
    x11, x12, y11, y12, z11, z12 = box
    return (x12 - x11 + 1) * (y12 - y11 + 1) * (z12- z11 + 1)

def update_components(components, box):
    new = components.copy()
    for action, box_action in components: 
        box_intersect = get_intersection(box_action, box)
        if box_intersect is not None:
            if action == "add":
                # We double counted an addition, remove it 
                new.append(("remove", box_intersect))
            elif action == "remove":
                # We double counted a removal, add it back 
                new.append(("add", box_intersect))  
    return new
    
def prune_components(comps):
    new = []
    for action, box in comps:
        if action == "add":
            if ("remove", box) in new:
                new.remove(("remove", box))
            else:
                new.append(("add", box))
        else: 
            if ("add", box) in new:
                new.remove(("add", box))
            else: 
                new.append(("remove", box))
    return new
                
if __name__ == "__main__":
    inputs = load_inputs("inputs/day22.txt")
    components = []
    for state, x_val, y_val, z_val in tqdm(inputs):
        box = (*x_val, *y_val, *z_val)
        if state == "on":
            # Considering everything before 
            new_components = update_components(components, box)
            new_components.append(("add", box))
        if state == "off":
            new_components = update_components(components, box)    
        
        # Pruning is expensive, only do it if it's worth it (1.2 is chosen arbitarily)
        if len(new_components) > len(components) * 1.2:
            new_components = prune_components(new_components)
        components = new_components       

    total = 0
    for action, component in components:
        volume = get_volume(component)
        assert(volume > 0)
        if action == "add":
            total += volume
        elif action == "remove": 
            total -= volume
    
    print(total)