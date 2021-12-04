import numpy as np 

def load_inputs(path, split_by="\n"): 
    with open(path) as file: 
        numbers_called = file.readline()
        file.readline()
        inputs = file.read().split(split_by)
    numbers_called = [int(num) for num in numbers_called.split(",")]
    # I hate this input reading
    result = [[[int(num) for num in line.split(" ") if num != ""] for line in input_.split("\n")] for input_ in inputs]
    return numbers_called, result

def calc_result(inputs, input_bingo, idx, number_winner):
    unmarked_sum = inputs[idx, ~input_bingo[idx].astype(bool)].sum()
    return unmarked_sum * number_winner

def part_one():
    numbers_called, inputs = load_inputs("inputs/day4.txt", split_by="\n\n")
    inputs = np.array(inputs)
    input_bingo = np.zeros_like(inputs)
    idx_winner = None
    number_winner = None
    for number in numbers_called: 
        input_bingo[inputs == number] = 1
        # Checks if anyone has all the columns filled up
        if (input_bingo.sum(axis=1) == 5).any():
            idx_winner = (input_bingo.sum(axis=1) == 5).argmax(axis=1).argmax()
            number_winner = number
            break
        # Checks if anyone has all the rows filled up
        if (input_bingo.sum(axis=2) == 5).any():
            idx_winner = (input_bingo.sum(axis=2) == 5).argmax(axis=1).argmax()
            number_winner = number
            break
    
    print(calc_result(inputs, input_bingo, idx_winner, number_winner))
    
def part_two():
    numbers_called, inputs = load_inputs("inputs/day4.txt", split_by="\n\n")
    inputs = np.array(inputs)
    input_bingo = np.zeros_like(inputs)
    last_winner = None
    number_last = None
    prev_wins = np.zeros((inputs.shape[0], 1))
    for number in numbers_called: 
        input_bingo[inputs == number] = 1
        col_wins = (input_bingo.sum(axis=1) == 5)
        row_wins = (input_bingo.sum(axis=2) == 5)
        has_row_win = (row_wins.sum(axis=1) >= 1)
        has_col_win = (col_wins.sum(axis=1) >= 1)
        has_win = (has_row_win | has_col_win)

        if has_win.all():
            # The last winner is the one that has 0 wins in the very last number called before they finally win. 
            last_winner = prev_wins.argmin()
            number_last = number
            break
            
        prev_wins = row_wins.sum(axis=1)  + col_wins.sum(axis=1)
        
    print(calc_result(inputs, input_bingo, last_winner, number_last))
    
if __name__ == "__main__": 
    part_one()
    part_two()
    
            
        
    