import numpy as np


def load_inputs(path): 
    with open(path) as f:
        inputs = f.read()
        coords, instructions = inputs.split("\n\n")
    return [[int(i) for i in i.strip().split(",") if i != ""] for i in coords.split("\n")], instructions.split("\n")

def fold_y(paper, coord):
    copy = np.zeros((coord, paper.shape[1]))
    dist = paper.shape[0] - coord - 1
    copy[-dist:, :] = paper[coord-dist:coord, :] + np.flipud(paper[coord+1:, :])
    copy[:-dist, :] = paper[:coord-dist, :]
    return np.minimum(1, copy)

def fold_x(paper, coord):

    copy = np.zeros((paper.shape[0], coord))
    dist = paper.shape[1] - coord - 1 
    copy[:, -dist:] = paper[:, coord-dist:coord] + np.fliplr(paper[:, coord+1:])
    copy[:, :-dist] = paper[:, :coord-dist]
    return np.minimum(1, copy)


if __name__ == "__main__": 
    coords, instructions = load_inputs("inputs/day13.txt")
    coords = np.array(coords)
    paper = np.zeros((coords[:, 1].max()+1, coords[:, 0].max() + 1))
    paper[coords[:, 1], coords[:, 0]] = 1
    for i, instruction in enumerate(instructions):
        val = instruction.split(" ")[-1]
        pos, coord = val.split("=")
        coord = int(coord)
        if pos == "y": 
            paper = fold_y(paper, coord)
        else: 
            paper = fold_x(paper, coord)
        
        if i == 0: 
            # Part 1
            print(paper.sum())

    # Part 2
    paper = paper.astype(int).astype(str)
    total = ["".join(paper[i, :]) for i in range(paper.shape[0])]
    print("\n".join(total).replace("1", "#").replace("0", " "))
    