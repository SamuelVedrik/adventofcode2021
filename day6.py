from collections import Counter

def load_inputs(path): 
    with open(path) as file:
        inputs = file.read()
    return [int(i) for i in inputs.split(",")]  
            
            
def calc_totals(inputs, num_days):
    fish_count = Counter(inputs)
    for _ in range(num_days):
        fish_count_copy = {days: 0 for days in range(9)} 
        for days in fish_count: 
            if days == 0:
                fish_count_copy[6] += fish_count[days]
                fish_count_copy[8] += fish_count[days]
            else: 
                fish_count_copy[days-1] += fish_count[days]
        fish_count = fish_count_copy
 
    print(sum([num for num in fish_count.values()]))
    
if __name__ == "__main__":
    inputs = load_inputs("inputs/day6.txt")
    calc_totals(inputs, 80)
    calc_totals(inputs, 256)
        