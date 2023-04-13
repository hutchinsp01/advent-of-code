f = open("day18.txt").read().splitlines()


class Cube:
    def __init__(self, pos):
        self.pos = pos

    def count_adjacent(self, cubes):
        count = 0
        for cube in cubes:
            if cube != self:
                if cube.pos == (self.pos[0] + 1, self.pos[1], self.pos[2]):
                    count += 1
                if cube.pos == (self.pos[0] - 1, self.pos[1], self.pos[2]):
                    count += 1
                if cube.pos == (self.pos[0], self.pos[1] + 1, self.pos[2]):
                    count += 1
                if cube.pos == (self.pos[0], self.pos[1] - 1, self.pos[2]):
                    count += 1
                if cube.pos == (self.pos[0], self.pos[1], self.pos[2] + 1):
                    count += 1
                if cube.pos == (self.pos[0], self.pos[1], self.pos[2] - 1):
                    count += 1
        return 6 - count

    def adjacent_list(self):
        return [
            (self.pos[0] + 1, self.pos[1], self.pos[2]),
            (self.pos[0] - 1, self.pos[1], self.pos[2]),
            (self.pos[0], self.pos[1] + 1, self.pos[2]),
            (self.pos[0], self.pos[1] - 1, self.pos[2]),
            (self.pos[0], self.pos[1], self.pos[2] + 1),
            (self.pos[0], self.pos[1], self.pos[2] - 1),
        ]


cubes = []
min_x = 0
max_x = 0
min_y = 0
max_y = 0
min_z = 0
max_z = 0

for line in f:
    x, y, z = line.split(",")
    cubes.append(Cube((int(x), int(y), int(z))))
    if int(x) < min_x:
        min_x = int(x)
    if int(x) > max_x:
        max_x = int(x)
    if int(y) < min_y:
        min_y = int(y)
    if int(y) > max_y:
        max_y = int(y)
    if int(z) < min_z:
        min_z = int(z)
    if int(z) > max_z:
        max_z = int(z)


def part1():
    count = 0
    for cube in cubes:
        count += cube.count_adjacent(cubes)
    return count


def part2():
    x_range = range(min_x - 2, max_x + 2)
    y_range = range(min_y - 2, max_y + 2)
    z_range = range(min_z - 2, max_z + 2)
    cube_pos_list = [cube.pos for cube in cubes]
    checked_cubes = []
    to_check = [(min_x, min_y, min_z)]
    edges = 0
    while len(to_check) > 0:
        cube = Cube(to_check.pop(0))
        checked_cubes.append(cube.pos)
        for adj in cube.adjacent_list():
            if adj[0] in x_range and adj[1] in y_range and adj[2] in z_range:
                if adj not in checked_cubes:
                    if adj in cube_pos_list:
                        edges += 1
                    elif adj not in to_check:
                        to_check.append(adj)
    return edges


print(part1())

print(part2())
