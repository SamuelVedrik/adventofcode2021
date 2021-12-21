import numpy as np
from collections import defaultdict
from tqdm.auto import tqdm

# The number of universes that has key total dice.

DICE_ROLLS = {3: 1,
              4: 3,
              5: 6,
              6: 7,
              7: 6,
              8: 3,
              9: 1}


def get_dice_roll(dice):
    return dice[:3].sum(), np.roll(dice, -3)
    
def update_turn(player_pos, player_score, dice):
    
    roll, new_dice = get_dice_roll(dice)
    player_pos = (player_pos + roll) % 10
    player_score += (player_pos + 1)
    return player_pos, player_score, new_dice

def part_one():
    p1_pos = 0 # 1
    p2_pos = 9 #10
    dice = np.arange(1, 101)
    p1_score = 0
    p2_score = 0
    turn = 0
    while p1_score < 1000 and p2_score < 1000:
        if turn % 2 == 0:
            p1_pos, p1_score, dice = update_turn(p1_pos, p1_score, dice)
            print("P1 scores: ", p1_score)
        else: 
            p2_pos, p2_score, dice = update_turn(p2_pos, p2_score, dice)
            print("P2 scores: ", p2_score)
        
        turn += 1

    if p1_score < p2_score:
        # p2 got >= 1000 first
        print(turn * p1_score * 3)
    else: 
        print(turn * p2_score * 3)
    

def update_turn_p2(pos, score, roll):
    pos = (pos + roll) % 10
    score += (pos + 1)
    return pos, score
    
def update_scores(initial, turn):
    """
    initial: 
    A dict with keys [p1_pos, p1_score, p2_pos, p2_score]
    and value with number of universes with that configuration. 
    
    Update initial after one dice roll.
    """
    new = defaultdict(lambda: 0)
    for p1_pos, p1_score, p2_pos, p2_score in initial:
        if (turn % 2) == 0:
            # Indexing @ 0, evens are p1 turn
            for roll, num_universe in DICE_ROLLS.items():
                new_p1_pos, new_p1_score = update_turn_p2(p1_pos, p1_score, roll)
                new[new_p1_pos, new_p1_score, p2_pos, p2_score] += initial[p1_pos, p1_score, p2_pos, p2_score] * num_universe
        else: 
            # Indexing @ 0, odds are p2 turn
            for roll, num_universe in DICE_ROLLS.items():
                new_p2_pos, new_p2_score = update_turn_p2(p2_pos, p2_score, roll)
                new[p1_pos, p1_score, new_p2_pos, new_p2_score] += initial[p1_pos, p1_score, p2_pos, p2_score] * num_universe
    
    return new

if __name__ == "__main__":

    scores= defaultdict(lambda: 0)
    scores[0, 0, 9, 0] = 1
    num_p1_win = 0
    num_p2_win = 0
    for t in range(50):
        scores = update_scores(scores, t)
        if (t % 2) == 0:
            num_p1_win += sum(num_uni for (p1_pos, p1_score, p2_pos, p2_score), num_uni  in scores.items() if (p1_score >= 21) and (p2_score < 21))
        else:
            num_p2_win += sum(num_uni for (p1_pos, p1_score, p2_pos, p2_score), num_uni  in scores.items() if (p2_score >= 21) and (p1_score < 21))

        # Prune games that are already finished 
        scores = {key: value for key, value in scores.items() if key[1] < 21 and key[3] < 21}
    print(num_p1_win)
    print(num_p2_win)
    print(num_p1_win > num_p2_win)
        
        
    


    
    
    