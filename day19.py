import numpy as np
import itertools
from collections import defaultdict

def rotations():
    # The basis vectors 
    x = np.array([1, 0, 0])
    y = np.array([0, 1, 0])
    z = np.array([0, 0, 1])
    matrices = []
    for x, y, z in itertools.permutations([x, y, z]):
        for coefx, coefy, coefz in itertools.product([1, -1], repeat=3):
            r_m = np.c_[coefx*x, coefy*y, coefz*z]
            if np.linalg.det(r_m) == 1:
                matrices.append(r_m)
            # Otherwise, the determinant is -1.0. (Logic is from reddit)
    return matrices
ROTATIONS = rotations()

def load_inputs(path):
    with open(path) as f:
        inputs = f.read().split("\n\n")
    parsed = []
    for input_ in inputs:
        scanner_coords = []
        for coords in input_.split("\n")[1:]:
            scanner_coords.append([int(x) for x in coords.strip().split(",")])
        parsed.append(scanner_coords)
    return parsed

def overlaps(report1, report2):
    # Strategy: CHoose a random point in r1. 
    # Assume that that point overlaps. -> We can determine the relative position of report2's beacon
    # If 11 other points agree on that location, then it overlaps. 
    # Otherwise, it does not overlap.
    
    for rotation in ROTATIONS:
        curr_r2 = report2 @ rotation.T 
        diff_matrix = np.empty((report1.shape[0], curr_r2.shape[0], 3))
        for i in range(report1.shape[0]): 
            for j in range(curr_r2.shape[0]):
                # if i == 9 and j == 0:
                    # print(report1[i, :] - curr_r2[j, :])
                    # print((report1[i, :] - curr_r2[j, :] == np.array([68,-1246,-43])).all())
                diff_matrix[i, j, :] = report1[i, :] - curr_r2[j, :]
        
        diffs = diff_matrix.reshape(-1, 3)
        diffs_list = [(diff[0], diff[1], diff[2]) for diff in diffs]
        uniques, counts = np.unique(diffs_list, axis=0, return_counts=True)
        if counts.max() >= 12:
            # displacement = (diffs == uniques[counts.argmax()]).all(axis=1)
            # to_remove_j = np.nonzero(displacement)[0] % curr_r2.shape[0]
            # return uniques[counts.argmax()], rotation, len(set(to_remove_j)), to_remove_j
            return uniques[counts.argmax()], rotation, counts.max()
            
    return None, None, 0

def get_path(graph, source, target):
    queue = [(source, )]
    while queue:
        curr = queue.pop(0)
        if curr[-1] == target: 
            return curr
        for child in graph[curr[-1]]:
            queue.append((curr) + (child, ))
    return None

def get_rotation_reldis(displacements, graph, source, target):
    path = get_path(graph, source, target)
    curr_dis = np.zeros(3)
    rot = np.eye(3)
    if path is not None:
        for s, t in zip(path[:-1], path[1:]):
            rot = rot @ displacements[s, t][1]
            curr_dis += (rot @ displacements[s, t][0])
    return curr_dis, rot

if __name__ == "__main__":
    inputs = load_inputs("inputs/day19.txt")
    inputs = [np.array(input_) for input_ in inputs]
    removal = defaultdict(set)
    # Key: Scanner i, scanner J 
    # Value: The displacement matrix before rotation, the rotation so that scanner J is in domain of scanner I. 
    displacements = defaultdict(lambda: None)
    total_points = sum(input_.shape[0] for input_ in inputs)
    total_overlap = 0
    graph = defaultdict(list)
    
    for i, scanner in enumerate(inputs):
        for j, other in enumerate(inputs[i+1:]):
            displacement, rotation, num_overlap = overlaps(scanner, other)
            if displacement is not None:
                print(f"Scanner {i} and Scanner {j+(i+1)} overlap, with {num_overlap} points.")
                total_overlap += num_overlap
                displacements[i, (j+i+1)] = np.linalg.inv(rotation) @ displacement, rotation
                displacements[(j+i+1), i] = -displacement, np.linalg.inv(rotation)
                graph[i].append((j+i+1))
                graph[(j+i+1)].append(i)

    
    
    # s0_1 = displacements[0, 1][1] @ displacements[0, 1][0]
    # s0_3 = displacements[0, 1][1] @ displacements[0, 1][0] + (displacements[0, 1][1] @ displacements[1, 3][1] @ displacements[1, 3][0])
    # s0_4 = displacements[0, 1][1] @ displacements[0, 1][0] + (displacements[0, 1][1] @ displacements[1, 4][1] @ displacements[1, 4][0])
    # s0_2 = s0_4 + (displacements[0, 1][1] @ displacements[1, 4][1] @ displacements[4, 2][1] @ displacements[4, 2][0])
    
    new_displacements = defaultdict(lambda: None)
    for scanner_num in range(len(inputs)):
        new_displacements[0, scanner_num] = get_rotation_reldis(displacements, graph, 0, scanner_num)
    
    values = [inputs[0]]
    for i, scanner in enumerate(inputs[1:]):
        scanner_num = i+1 
        displacement, rotation = new_displacements[0, scanner_num]
        
        values.append((scanner @ rotation.T) + (displacement))
    
    total = np.concatenate(values)
    new_arr = [tuple(row) for row in total]
    print(np.unique(new_arr, axis=0).shape)
    
    distances = np.empty((len(inputs), len(inputs)))
    for i in range(distances.shape[0]): 
        for j in range(distances.shape[0]):
            x = new_displacements[0, i][0]
            y = new_displacements[0, j][0]
            distances[i, j] = np.abs(x - y).sum()
    
    print(distances.max())
        
    
    