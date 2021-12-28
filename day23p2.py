import networkx as nx 
import heapq 
from collections import defaultdict
from tqdm.auto import tqdm

COSTS = {
    "A": 1, 
    "B": 10,
    "C": 100,
    "D": 1000
}

ILLEGAL = [
    "HL2", "HL4", "HL6", "HL8",
]

def build_graph():
    G = nx.Graph()
    # Build the hallway
    for i, j in zip(range(11), range(1, 11)):
        G.add_edge(f"HL{i}", f"HL{j}")
    
    # Room 0 is the room connected to the hallway.
    for room in ["A", "B", "C", "D"]: 
        G.add_edge(f"R{room}0", f"R{room}1")
        G.add_edge(f"R{room}1", f"R{room}2")
        G.add_edge(f"R{room}2", f"R{room}3")
    
    G.add_edge("RA0", "HL2")
    G.add_edge("RB0", "HL4")
    G.add_edge("RC0", "HL6")
    G.add_edge("RD0", "HL8")
    
    return G

def build_state():
    state = {
        "A0": "RB3", 
        "A1": "RC2",
        "A2": "RC3",
        "A3": "RD1", 
        
        "B0": "RB2",
        "B1": "RC1", 
        "B2": "RD0", 
        "B3": "RD3", 
        
        "C0": "RA3", 
        "C1": "RB0", 
        "C2": "RB1", 
        "C3": "RD2",
        
        "D0": "RA0", 
        "D1": "RA1", 
        "D2": "RA2",
        "D3": "RC0"
    }
    
    return state

def check_finish(state):
    for amphipod, room in state.items():
        # Amphipod[0] is it's type, room[1] is the designation of the room.
        if amphipod[0] != room[1]:
            return False
    return True

def get_score(connections, start, end, type):
    
    return connections[start][end] * (COSTS[type])

def is_blocked(source, target, state, paths):
    path = paths[source][target]
    for room in state.values():
        if room in path[1:]: 
            return True 
        
    return False

def _amphipod_hallway(amphipod, room, state, connections, paths, score):
    type_ = amphipod[0]
    room_occupants = [(occupant, other_room) for occupant, other_room in state.items() if f"R{type_}" in other_room]
    room_empty = len(room_occupants) == 0
    room_full = len(room_occupants) == 4
    # Can't move in if room is full
    if room_full:
        return None
    
    # Can't move in if room occupant is not the same
    nums = []
    for occupant, other_room in room_occupants:
        nums.append(int(other_room[-1]))
        if occupant[0] != type_:
            return None
    
    room_num = min(nums) - 1 if not room_empty else 3
    new_room = f"R{type_}{room_num}"
    if is_blocked(room, new_room, state, paths):
        return None
    new_state = state.copy()
    new_state[amphipod] = new_room
    move_cost = score + get_score(connections, room, new_room, type_)
    return (move_cost, new_state, (amphipod, room, new_room))

def _amphipod_room(amphipod, room, state, connections, paths, score):
    # Handle amphipod in room 
    moves = []
    type_ = amphipod[0]
    # The people living below you
    room_occupants = {other_room: occupant for occupant, other_room in state.items() if room[:2] in other_room}
    # If everything below you is already OK, then we don't have to move
    room_ok = True
    for num in range(3, int(room[-1])-1, -1):
        checking = f"{room[:2]}{num}"
        # Occupant doesn't belong in this room
        if room_occupants[checking][0] != room[1]:
            room_ok = False
    if room_ok:
        return [] 
        
    for hallway in range(11):
        hallway = f"HL{hallway}"
        # Not an illegal place to move 
        if hallway not in ILLEGAL and not is_blocked(room, hallway, state, paths):
            new_state = state.copy()
            new_state[amphipod] = hallway
            move_cost = score + get_score(connections, room, hallway, type_)
            moves.append((move_cost, new_state, (amphipod, room, hallway)))
    return moves

def get_amphipod_moves(amphipod, room, state, connections, paths, score):
    moves = []
    if "HL" in room:
        # Handle amphipod in hallway 
        move = _amphipod_hallway(amphipod, room, state, connections, paths, score)
        if move is not None: 
            moves.append(move)
    else:
        # Handle amphipod in room 
       moves.extend(_amphipod_room(amphipod, room, state, connections, paths, score))
                
    return moves
    
    
def get_children(state, connections, paths, score):
    """
    Get all possible moves from this state.
    """
    children = []
    for amphipod, room in state.items():
        moves = get_amphipod_moves(amphipod, room, state, connections, paths, score)
        children.extend(moves)
    return children

def get_frozen(state):
    frozen = defaultdict(list)
    for amphipod, room in state.items():
        frozen[amphipod[0]].append(room)
    
    frozen = {k: frozenset(v) for k, v in frozen.items()}
    return tuple(frozen.items())

def uniform_cost_search(state, connections, paths):
    
    queue = []
    heapq.heappush(queue, (0, 0, state, []))
    # Stores the lowest score of all visited states. Useful for cycle checking. 
    visited = defaultdict(lambda: float("inf"))
    NUM = 1
    with tqdm() as pbar: 
        while queue:
            score, tiebreaker, state, move_history = heapq.heappop(queue)
            if check_finish(state):
                return score, move_history
            children = get_children(state, connections, paths, score)
            for new_score, new_state, move in children:
                frozen_state = get_frozen(new_state)
                # Update 
                if visited[frozen_state] > new_score:
                    heapq.heappush(queue, (new_score, NUM, new_state, move_history + [move]))
                    NUM += 1
                    visited[frozen_state] = new_score
            pbar.update(1)
        
    return None

if __name__ == "__main__":
    G = build_graph()
    # Dict of {source: {target: distance}}
    connections = dict(nx.all_pairs_shortest_path_length(G))
    paths = dict(nx.all_pairs_shortest_path(G))
    state = build_state()
    
    cheapest = uniform_cost_search(state, connections, paths)
    print(cheapest)