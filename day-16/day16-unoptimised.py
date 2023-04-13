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
    for i in distance_matrix:
        for j in distance_matrix:
            if valves_dict[j].flow_rate <= 0:
                distance_matrix[i][j] = POS_INF
    return distance_matrix


def find_total_flow(
    distance_matrix,
    cur_valve=valves_dict[START],
    time=30,
    open_set=set(),
    elephant=False,
):
    if time <= 0:
        return 0
    total = 0
    for valve in distance_matrix[cur_valve.name]:
        if valve not in open_set and valves_dict[valve].flow_rate > 0:
            new_open_set = open_set.copy()
            new_open_set.add(valve)
            new_time = time - distance_matrix[cur_valve.name][valve] - 1
            new_total = (
                time - distance_matrix[cur_valve.name][valve] - 1
            ) * valves_dict[valve].flow_rate
            if elephant:
                elephant_total = new_total + find_total_flow(
                    distance_matrix=distance_matrix,
                    time=26,
                    open_set=new_open_set,
                    elephant=False,
                )
            new_total += find_total_flow(
                distance_matrix, valves_dict[valve], new_time, new_open_set, elephant
            )

            if new_total > total:
                total = new_total

            if elephant and elephant_total > total:
                total = elephant_total

    return total


print(find_total_flow(distance_matrix=floyd_warshalls(valves_dict)))
print(
    find_total_flow(
        distance_matrix=floyd_warshalls(valves_dict), time=26, elephant=True
    )
)
