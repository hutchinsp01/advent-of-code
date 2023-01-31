f = open("day14.txt").read().splitlines()
sand_start = (500, 0)
max_depth = 0
cave_dict = {}

# [['498,4', '498,6', '496,6'], ['503,4', '502,4', '502,9', '494,9']]
rock = [x.split(" -> ") for x in f]

for i, path in enumerate(rock):
    for tuple in path:
        x, y = tuple.split(",")
        rock[i][path.index(tuple)] = (int(x), int(y))
        if int(y) > max_depth:
            max_depth = int(y)

# Fill in the rock
for path in rock:
    for i in range(len(path) - 1):
        start, end = path[i], path[i + 1]
        if start[0] == end[0]:
            if start[1] > end[1]:
                start, end = end, start
            for y in range(start[1], end[1] + 1):
                cave_dict[(start[0], y)] = "#"
        else:
            if start[0] > end[0]:
                start, end = end, start
            for x in range(start[0], end[0] + 1):
                cave_dict[(x, start[1])] = "#"


def flow_sand(cave_dict):
    cave_dict = cave_dict.copy()
    total = 0
    new_sand = True
    sand = sand_start
    while True:
        new_sand = True
        if sand[1] > max_depth:
            return total
        for check_sand in sand_movement(sand):
            if check_sand not in cave_dict:
                sand = check_sand
                new_sand = False
                break
        if new_sand:
            cave_dict[sand] = "o"
            sand = sand_start
            total += 1


def flow_sand2(cave_dict):
    cave_dict = cave_dict.copy()
    total = 1
    new_sand = True
    sand = sand_start
    check_start = False
    while True:
        new_sand = True
        for check_sand in sand_movement(sand):
            if check_sand not in cave_dict and check_sand[1] <= max_depth + 1:
                sand = check_sand
                new_sand = False
                break
        if sand == sand_start and check_start:
            return total
        check_start = True
        if new_sand:
            if sand == sand_start:
                return total
            cave_dict[sand] = "o"
            sand = sand_start
            total += 1
            check_start = False


def sand_movement(sand):
    return [
        (sand[0], sand[1] + 1),
        (sand[0] - 1, sand[1] + 1),
        (sand[0] + 1, sand[1] + 1),
    ]


# print(cave_dict)
print(flow_sand(cave_dict))
print(flow_sand2(cave_dict))
