from functools import lru_cache
from itertools import combinations, permutations

POS_INF = 9999999
START = "AA"

f = open("day16.txt").read().splitlines()


class Valve:
    def __init__(self, name, flow_rate, tunnels):
        self.name = name
        self.flow_rate = int(flow_rate)
        self.tunnels = tunnels
        self.open = False


# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
valves_dict = {}
for line in f:
    line = line.replace("Valve ", "")
    line = line.replace(" has flow rate=", "|")
    line = line.replace("; tunnels lead to valves ", "|")
    line = line.replace("; tunnel leads to valve ", "|")
    name, flow_rate, tunnels = line.split("|")
    valves_dict[name] = Valve(name, flow_rate, tunnels.split(", "))


def floyd_warshalls(valves_dict):
    # Create a distance matrix
    distance_matrix = {}
    for valve in valves_dict:
        distance_matrix[valve] = {}
        for valve2 in valves_dict:
            distance_matrix[valve][valve2] = POS_INF
    for valve in valves_dict:
        distance_matrix[valve][valve] = 0
        for tunnel in valves_dict[valve].tunnels:
            distance_matrix[valve][tunnel] = 1

    for k in distance_matrix:
        for i in distance_matrix:
            for j in distance_matrix:
                distance_matrix[i][j] = min(
                    distance_matrix[i][j], distance_matrix[i][k] + distance_matrix[k][j]
                )

    # Remove valves that have 0 flow rate
    to_pop = []
    for valve in distance_matrix:
        if valves_dict[valve].flow_rate <= 0 and valve != "AA":
            to_pop.append(valve)
        else:
            for valve2 in distance_matrix:
                if valves_dict[valve2].flow_rate <= 0:
                    distance_matrix[valve].pop(valve2)
    for valve in to_pop:
        distance_matrix.pop(valve)

    # Add 1 to all valves so I dont have to care about opening
    for valves in distance_matrix:
        for valve in distance_matrix[valves]:
            distance_matrix[valves][valve] += 1

    return distance_matrix


def find_total_flow(
    distance_matrix,
    cur_valve=valves_dict[START],
    time=30,
    open_set=set(),
    elephant=False,
    cur_max=0,
):
    if time <= 0:
        return 0
    total = 0
    for valve in distance_matrix[cur_valve.name]:
        if valve not in open_set:
            new_open_set = open_set.copy()
            new_open_set.add(valve)
            new_time = time - distance_matrix[cur_valve.name][valve]
            new_total = (time - distance_matrix[cur_valve.name][valve]) * valves_dict[
                valve
            ].flow_rate
            if elephant:
                elephant_total = new_total + find_total_flow(
                    distance_matrix=distance_matrix,
                    time=26,
                    open_set=new_open_set,
                    elephant=False,
                    cur_max=cur_max,
                )
            new_total += find_total_flow(
                distance_matrix,
                valves_dict[valve],
                new_time,
                new_open_set,
                elephant,
                cur_max,
            )

            if new_total > total:
                total = new_total

            if elephant and elephant_total > total:
                total = elephant_total

    return total


def find_all_sets(distance_matrix, start_valve=valves_dict[START], time=30):
    all_valves = set()
    for valve in distance_matrix:
        all_valves.add(valve)

    all_sets = _filter_all_sets(
        permutations(all_valves), distance_matrix, start_valve, time
    )
    return all_sets


def _filter_all_sets(all_sets, distance_matrix, start_valve, time=30):
    filtered = filter(lambda x: x[0] == start_valve.name, all_sets)
    filtered1 = filter(
        lambda x: sum([distance_matrix[x[i]][x[i + 1]] for i in range(len(x) - 1)])
        <= time,
        filtered,
    )
    return filtered1


def find_unique_set_combos(all_sets):
    all_unique_combos = combinations(all_sets, 2)
    filtered = filter(
        lambda x: all([True for v in x[0] if v not in x[1]]), all_unique_combos
    )
    return filtered


def find_total_flow2(cur_valve=valves_dict[START], time=30):
    max_total = 0
    sets = find_all_sets(distance_matrix, cur_valve, time)
    for path in sets:
        new_time = time - distance_matrix[path[0]][path[1]]
        total = sum_path(path[1:], new_time)

        if total > max_total:
            max_total = total

    return max_total


def find_total_elephant_flow2(cur_valve=valves_dict[START], time=26):
    max_total = 0
    sets = find_unique_set_combos(find_all_sets(distance_matrix, cur_valve, time))
    for combo in sets:
        total = sum(
            map(lambda x: sum_path(x[1:], time - distance_matrix[x[0]][x[1]]), combo)
        )

        if total > max_total:
            max_total = total

    return max_total


@lru_cache(maxsize=None)
def sum_path(path, time):
    if len(path) == 0:
        return 0
    if len(path) == 1:
        return time * valves_dict[path[0]].flow_rate
    new_time = time - distance_matrix[path[0]][path[1]]
    return time * valves_dict[path[0]].flow_rate + sum_path(path[1:], new_time)


distance_matrix = floyd_warshalls(valves_dict)
print(find_total_flow(distance_matrix=floyd_warshalls(valves_dict)))
print(find_total_flow2())
print(find_total_elephant_flow2())
# print(
#     find_total_flow(
#         distance_matrix=floyd_warshalls(valves_dict), time=26, elephant=True
#     )
# )
