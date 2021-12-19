import math 
from itertools import combinations
from tqdm.auto import tqdm

class Tree:
    """
    Leaves have a value and no children
    Other nodes have no value and left and right children 
    """
    def __init__(self, initial=None, parent=None, depth=0):
        """
        initial: List representation of this tree.
        parent: A pointer to the parent of this tree. If the tree is the root, parent is None. 
        """
        self.depth = depth 
        self.parent = parent
        if isinstance(initial, int):
            self.value = initial
            self.left = None 
            self.right = None
        elif isinstance(initial, list):
            self.value = None
            self.left = Tree(initial[0], parent=self, depth=self.depth+1)
            self.right = Tree(initial[1], parent=self, depth=self.depth+1)
        else: 
            self.value = None 
            self.left = None
            self.right = None
    
    def __repr__(self):
        if self.value is not None:
            return f"T{self.value}"
        else:
            return f"T[{self.left.__repr__()}, {self.right.__repr__()}]"
    
    def __str__(self):
        if self.value is not None:
            return f"{self.value}"
        else:
            return f"[{self.left.__str__()}, {self.right.__str__()}]"
        
    def is_leaf(self):
        return self.value is not None
    
    def find_right(self):
        is_parent_right = True
        # First such ancestor s.t this tree is in left of it
        ancestor = self.parent
        check = self
        while is_parent_right and ancestor is not None:
            if ancestor.left == check:
                is_parent_right = False
            else:
                check = check.parent
                ancestor = ancestor.parent
        
        if ancestor is None: 
            return None 
        leaf = ancestor.right
        while not leaf.is_leaf():
            leaf = leaf.left
        return leaf
    
    def find_left(self): 
        is_parent_left = True 
        ancestor = self.parent
        check = self
        while is_parent_left and ancestor is not None:
            if ancestor.right == check: 
                is_parent_left = False 
            else: 
                check = check.parent
                ancestor = ancestor.parent
        
        if ancestor is None: 
            return None
        leaf= ancestor.left  
        while not leaf.is_leaf():
            leaf = leaf.right
        return leaf
    
    def explode(self):
        if self.is_leaf(): 
            raise ValueError(f"This is a leaf with value {self}")
        if not (self.left.is_leaf() and self.right.is_leaf()):
            raise ValueError(f"This node's children are not leaves. f{self}")
        if self.parent is None:
            raise ValueError("This is the root node dummy.")
            
        left = self.find_left()
        right = self.find_right()
        
        if left is not None:
            left.value += self.left.value   
        if right is not None:
            right.value += self.right.value 
            
        if self.parent.left == self:
            self.parent.left = Tree(0, self.parent, self.depth)
        elif self.parent.right == self:
            self.parent.right = Tree(0, self.parent, self.depth)
            
    def split(self):
        if not self.is_leaf(): 
            raise ValueError("You cannot split a non-leaf.")
        
        self.left = Tree(math.floor(self.value/2), parent=self, depth=self.depth+1)
        self.right = Tree(math.ceil(self.value/2), parent=self, depth=self.depth+1)
        self.value = None
        
    def _increase_depth(self):
        self.depth += 1
        if not self.is_leaf():
            self.left._increase_depth()
            self.right._increase_depth()
        
    def __add__(self, other):
        if self.parent is not None: 
            raise ValueError(f"Left is a non root tree.")
        if other.parent is not None: 
            raise ValueError(f"Right is a non root tree.")
        
        parent = Tree()
        self._increase_depth()
        other._increase_depth()
        self.parent = parent
        other.parent = parent
        
        parent.left = self
        parent.right = other
        
        return parent
        
        
    def __getitem__(self, idx):
        if not self.is_leaf():
            if idx == 0: 
                return self.left 
            elif idx == 1: 
                return self.right
            else: 
                raise IndexError
        raise IndexError("f{self} is a leaf node!")

def load_inputs(path): 
    with open(path) as f:
        lines = f.readlines()
    return [eval(line.strip()) for line in lines]

def reduction(tree):
    considering = [tree]
    while considering:
        curr = considering.pop()
        if curr.depth == 4 and not curr.is_leaf():
            curr.explode()
            reduction(tree)
            return
        if not curr.is_leaf():
            considering.append(curr.right)
            # Always consider left most first 
            considering.append(curr.left)
            
    considering = [tree]
    while considering:
        curr = considering.pop()
        if curr.is_leaf() and curr.value >= 10:
            curr.split()
            reduction(tree)
            return
        if not curr.is_leaf():
            considering.append(curr.right)
            # Always consider left most first 
            considering.append(curr.left)
            
def calc_magnitude(tree):
    if tree.is_leaf():
        return tree.value
    else: 
        return 3*calc_magnitude(tree.left) + 2*calc_magnitude(tree.right)       

def part_one():
    inputs = load_inputs("inputs/day18.txt")
    curr = Tree(inputs[0])
    for input_ in inputs[1:]:
        curr = curr + Tree(input_)
        reduction(curr)
    
    print(calc_magnitude(curr))
    
def part_two(): 
    inputs = load_inputs("inputs/day18.txt")
    max_ = -1
    for i1, i2 in tqdm(combinations(inputs, r=2)):
        tree1 = Tree(i1) + Tree(i2)
        tree2 = Tree(i2) + Tree(i1)
        reduction(tree1)
        reduction(tree2)
        max_ = max(max_, calc_magnitude(tree1), calc_magnitude(tree2))
    print(max_)
    
    
if __name__ == "__main__":
    part_one()
    part_two()
    
