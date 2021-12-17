import numpy as np

def get_landing(y_ranges, velocity):
    
    # After some time the projectile drops to y=0 anyways. If y_velocity = 4 for example,
    # Then it would go -5, -11... 
    # The distance it moves is (end+1)(end)/2 - (velocity+1)(velocity)/2
    # Therefore, we can test all the values in the range and see if there is an integer that satisfies:
    # (end+1)(end)/2 - (velocity+1)(velocity)/2 = y_range
    # This defines a quadratic equation.
    values = []
    for target in range(y_ranges[1], y_ranges[0]-1, -1):
            alpha = (velocity * (velocity+1))/2
            beta = 2*(-target + alpha)
            root = (np.sqrt(1+(4*beta))-1)/2 
            if np.mod(root, 1) == 0: # checks is whole number
                values.append((root, target))
    if values:
        return values
    return None
    
def part_one():
    x_range = [209, 238]
    y_range = [-86, -59]
    
    curr_y = 0
    max_found = 0
    while curr_y < 10000:
        result = get_landing(y_range, curr_y)
        if result is not None:
            max_found = curr_y
        curr_y += 1
                
    max_y_height = ((max_found) * (max_found + 1))/2
    
    print("Max y velocity: ", max_found)
    print("Max Height achieved: ", max_y_height)
    
def part_two():
    x_range = [209, 238]
    y_range = [-86, -59]
    
    curr_y = 0 
    num_valid = 0
    while curr_y < 10000:
        results = get_landing(y_range, curr_y)
        if results is not None:
            root, final_dest = results[0] # first dist reached 
            num_pos = len(results)
            # 2y+1 is the number of steps required to reach 0
            # root is the ending velocity  when reaching target
            # root - curr_y is number of steps to reach that velocity from when we first got 0
            pos_y_steps = int(((2*curr_y) + 1) + (root - curr_y))
            
            # If y=4 works, then y=-5 also works. There are just less steps needed to reach target
            neg_y_steps = int(root - curr_y)
            
            # We only need at most x_range[1] speed.
            x_init_velocities = np.arange(0, x_range[1]+1)
            # I mean come on 200 should be plenty 
            distance_travelled = np.zeros((x_range[1]+1, 200))
            for i in range(1, 200):
                distance_travelled[:, i] = distance_travelled[:, i-1] + np.maximum(0, x_init_velocities - (i-1))
            
            is_within = (x_range[0] <= distance_travelled) & (distance_travelled <= x_range[1])
            
            num_valid += is_within[:, pos_y_steps:pos_y_steps+num_pos].any(axis=1).sum()
            num_valid += is_within[:, neg_y_steps:neg_y_steps+num_pos].any(axis=1).sum()
                     
            
        curr_y += 1      
    
    print(num_valid)
    
if __name__ == "__main__":

    part_one()
    part_two()
            
   
    