import constraint as csp
import re
from tqdm.auto import tqdm

def load_inputs(path): 
    with open(path) as f:
        inputs = f.readlines()

    alphas = []
    betas = []
    gammas = []
    for i in range(14):
        regex = r"(-?\d+)"
        alphas.append(int(re.search(regex, inputs[5+(i*18)]).group(1)))
        betas.append(int(re.search(regex, inputs[4+(i*18)]).group(1)))
        gammas.append(int(re.search(regex, inputs[15+(i*18)]).group(1)))
    
    return alphas, betas, gammas

def get_links(betas):
    stack = []
    links = []
    for i, item in enumerate(betas):
        if item == 1:
            stack.append(i)
        else:
            first = stack.pop()
            links.append((first, i))
    return links     


def get_constraint(alphas, gammas, i, j):
    
    return lambda wi, wj: (wi + gammas[i] + alphas[j] == wj)

def get_num(sol): 
    num = ""
    for i in range(14):
        num += str(sol[i])
        
    return int(num)
if __name__ == "__main__": 
    alphas, betas, gammas = load_inputs("inputs/day24.txt")
    print("Alphas", alphas)
    print("Betas", betas)
    print("Gammas", gammas)
    links = get_links(betas)
    
    problem = csp.Problem()
    problem.addVariables(range(14), range(1, 10))
    
    
    for i, j in links:
        print(f"w{i} + {gammas[i]} + {alphas[j]} == w{j}")
        problem.addConstraint(get_constraint(alphas, gammas, i, j), [i, j])
    
    sol = problem.getSolution()
    max_ = -1
    min_ = float("inf")
    for sol in tqdm(problem.getSolutionIter()):
        num = get_num(sol)
        max_ = max(max_, num)
        min_ = min(min_, num)
    
    print(max_)
    print(min_)    
    