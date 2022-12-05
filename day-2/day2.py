op_dict = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}
my_dict = {'X': 'rock', 'Y': 'paper', 'Z': 'scissors'}
my_swap = {'X': 'A', 'Y': 'B', 'Z': 'C'}
op_swap = {'A': 'X', 'B': 'Y', 'C': 'Z'}
score_dict = {'rock': 1, 'paper': 2, 'scissors': 3}


outcome_dict = {'X': -1, 'Y': 0, 'Z': 1}

def get_score(op, me):
    game_score = 0
    if op_dict[op] == my_dict[me]:
        game_score += 3
    elif my_dict[me] == 'paper' and op_dict[op] == 'rock':
        game_score += 6
    elif my_dict[me] == 'scissors' and op_dict[op] == 'paper':
        game_score += 6
    elif my_dict[me] == 'rock' and op_dict[op] == 'scissors':
        game_score += 6

    game_score += score_dict[my_dict[me]]

    return game_score

def get_score2(op, outcome):
    game_score = 0
    outcome = outcome_dict[outcome]
    if outcome == -1:
        for key, value in my_dict.items():
            if get_score(op, key) < get_score(my_swap[key], op_swap[op]):
                return get_score(op, key)

    if outcome == 0:
        for key, value in my_dict.items():
            if get_score(op, key) == get_score(my_swap[key], op_swap[op]):
                return get_score(op, key)

    if outcome == 1:
        for key, value in my_dict.items():
            if get_score(op, key) > get_score(my_swap[key], op_swap[op]):
                return get_score(op, key)

    return 0




with open("2") as f:
    rps_rounds = [get_score(gameround.split(" ")[0], gameround.split(" ")[1]) for gameround in f.read().strip().split("\n")]
    print(sum(rps_rounds))

    # Part 2

    rps_rounds = [get_score2(gameround.split(" ")[0], gameround.split(" ")[1]) for gameround in f.read().strip().split("\n")]
    print(sum(rps_rounds))
