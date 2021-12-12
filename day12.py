from collections import defaultdict, Counter
from tqdm.auto import tqdm

def load_inputs(path): 
    with open(path) as f: 
        inputs = f.readlines()
    return [input.strip().split("-") for input in inputs]

def build_graph(inputs):
    G = defaultdict(list)
    for start, end  in inputs:
        # end has no edges from it, start has no edges to it.
        if start != "end" and end != "start":
            G[start].append(end) 
        if end != "end" and start != "start":
            G[end].append(start)
    return G

def get_children(path, graph):
    curr = path[-1]
    if curr == "end": 
        return []
    children = []
    for explore in graph[curr]:
        if explore.islower(): 
            if explore not in path:
                children.append(path + [explore])
        else:
            children.append(path + [explore])
    
    return children

def get_children2(path, graph):
    curr = path[-1]
    if curr == "end": 
        return []
    children = []
    count = Counter(path)
    for explore in graph[curr]:
        if explore.islower(): 
            if explore not in path or (count[explore] == 1 and all(count[other] == 1 for other in path if not(other == explore or other.isupper()))):
                to_add = path + [explore]
                children.append(to_add)   
        else:
            children.append(path + [explore])
    return children
    

def dfs(graph, child_f):
    paths = [["start"]]
    complete_paths = []
    with tqdm() as pbar:
        while paths:
            path = paths.pop()
            if path[-1] == "end":
                complete_paths.append(path)
            else:
                to_explore = child_f(path, graph)
                paths.extend(to_explore)
            pbar.update(1)

    return len(complete_paths)
    
if __name__ == "__main__":
    inputs = load_inputs("inputs/day12.txt")
    graph = build_graph(inputs)
    part_one = dfs(graph, get_children)
    part_two = dfs(graph, get_children2)
    print(part_one)
    print(part_two)