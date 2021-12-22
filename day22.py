from collections import defaultdict
from itertools import product, combinations
import re

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

def part_one():
    inputs = load_inputs("inputs/day22.txt")
    # Naive way to store these 
    cube_states = defaultdict(lambda: False)
    # First 20 are within -50, 50
    for state, x_val, y_val, z_val in inputs[:NUM_CON]:
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
    intersection = max(w * l * h, 0)
    if intersection > 0:
        return (x1_int, x2_int, y1_int, y2_int, z1_int, z2_int)
    return None

def get_volume(box):
    x11, x12, y11, y12, z11, z12 = box
    return (x12 - x11 + 1) * (y12 - y11 + 1) * (z12- z11 + 1)

if __name__ == "__main__":
    inputs = load_inputs("inputs/day22.txt")
    components = []
    NUM_CON = 13
    
    #TODO: Bug report: At this stage, I'm adding something that I shouldn't have.
    # In this case, adding multiple things.
    
    # First 20 are within -50, 50
    for i, state, x_val, y_val, z_val in inputs[:NUM_CON]:
        box = (*x_val, *y_val, *z_val)
        if state == "on":
            components.append(("add", box))
            # Considering everything before 
            for action, box_action in components.copy()[:-1]: 
                box_intersect = get_intersection(box_action, box)
                if box_intersect is not None:
                    if action == "add":
                        # I double counted a portion, so remove that bit.
                        components.append(("remove", box_intersect))
                    elif action == "remove":
                        # I double removed a portion, so add that bit 
                        components.append(("add", box_intersect))
        
        if state == "off":
            for action, box_action in components.copy(): 
                box_intersect = get_intersection(box_action, box)
                if box_intersect is not None:
                    if action == "add":
                        components.append(("remove", box_intersect))
                    elif action == "remove":
                        components.append(("add", box_intersect))               
    

    total = 0
    for action, component in components:
        volume = get_volume(component)
        if volume == 13257:
            print(action, component)
        assert(volume > 0)
        if action == "add":
            total += volume
        elif action == "remove": 
            total -= volume
    
    print(total)
    part_one()