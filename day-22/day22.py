f = open("day22.txt").read()

grove, instructions = f.split("\n\n")
max_len = 0

directions = ["R", "D", "L", "U"]


class Grove:
    def __init__(self, groveParam, direction="R", fake_edges=None):
        self.grove = groveParam.splitlines()
        self.pos = self.find_start()
        self.direction = direction
        self.max_real = max([len(line) for line in self.grove])
        self.max_imag = len(self.grove)
        self.grove = [
            x + " " * (self.max_real - len(x)) for x in groveParam.splitlines()
        ]
        self.edges = fake_edges

    def find_start(self):
        start = self.grove[0].index(".")
        return 0j + start

    def new_move(self, n):
        next_pos = self.pos
        direction = self.direction
        for _ in range(n):
            rotated_pos, rotated_direction = self.new_rotate_pos(next_pos)
            if rotated_pos != self.pos:
                next_pos = rotated_pos
                direction = rotated_direction
            elif self.direction == "R":
                next_pos += 1
            elif self.direction == "L":
                next_pos -= 1
            elif self.direction == "U":
                next_pos -= 1j
            elif self.direction == "D":
                next_pos += 1j
            if self.lookup(next_pos) == "#":
                break
            self.pos = next_pos
            self.direction = direction

    def move(self, n):
        if self.direction == "R":
            self.move_right(n)
        elif self.direction == "L":
            self.move_left(n)
        elif self.direction == "U":
            self.move_up(n)
        elif self.direction == "D":
            self.move_down(n)

    def move_down(self, n):
        for _ in range(n):
            next_square = self.next_pos(self.pos + 1j)
            if self.lookup(next_square) == "#":
                break
            self.pos = next_square

    def move_up(self, n):
        for _ in range(n):
            next_square = self.next_pos(self.pos - 1j)
            if self.lookup(next_square) == "#":
                break
            self.pos = next_square

    def move_left(self, n):
        for _ in range(n):
            next_square = self.next_pos(self.pos - 1)
            if self.lookup(next_square) == "#":
                break
            self.pos = next_square

    def move_right(self, n):
        for _ in range(n):
            next_square = self.next_pos(self.pos + 1)
            if self.lookup(next_square) == "#":
                break
            self.pos = next_square

    def rotate(self, rotation):
        if rotation == "R":
            self.direction = directions[
                (directions.index(self.direction) + 1) % len(directions)
            ]
        elif rotation == "L":
            self.direction = directions[
                (directions.index(self.direction) - 1) % len(directions)
            ]

    def next_pos(self, pos):
        pos = self.mod_to_range(pos)
        next_pos = self.grove[int(pos.imag)][int(pos.real)]
        if next_pos not in ["#", "."]:
            if self.direction == "R":
                pos = self.next_pos(pos + 1)
            elif self.direction == "L":
                pos = self.next_pos(pos - 1)
            elif self.direction == "U":
                pos = self.next_pos(pos - 1j)
            elif self.direction == "D":
                pos = self.next_pos(pos + 1j)
        return pos

    def new_rotate_pos(self, pos):
        pos = self.pos
        direction = self.direction
        if self.direction == "U":
            if pos in self.edges["edge2a"]:
                pos = self.edges["edge2b"][self.edges["edge2a"].index(pos)]
                direction = "R"
            elif pos in self.edges["edge3a"]:
                pos = self.edges["edge3b"][self.edges["edge3a"].index(pos)]
                direction = "U"
            elif pos in self.edges["edge7b"]:
                pos = self.edges["edge7a"][self.edges["edge7b"].index(pos)]
                direction = "R"
        elif self.direction == "R":
            if pos in self.edges["edge4a"]:
                pos = self.edges["edge4b"][self.edges["edge4a"].index(pos)]
                direction = "L"
            elif pos in self.edges["edge4b"]:
                pos = self.edges["edge4a"][self.edges["edge4b"].index(pos)]
                direction = "L"
            elif pos in self.edges["edge5b"]:
                pos = self.edges["edge5a"][self.edges["edge5b"].index(pos)]
                direction = "U"
            elif pos in self.edges["edge6b"]:
                pos = self.edges["edge6a"][self.edges["edge6b"].index(pos)]
                direction = "U"
        elif self.direction == "D":
            if pos in self.edges["edge3b"]:
                pos = self.edges["edge3a"][self.edges["edge3b"].index(pos)]
                direction = "D"
            elif pos in self.edges["edge5a"]:
                pos = self.edges["edge5b"][self.edges["edge5a"].index(pos)]
                direction = "L"
            elif pos in self.edges["edge6a"]:
                pos = self.edges["edge6b"][self.edges["edge6a"].index(pos)]
                direction = "L"
        elif self.direction == "L":
            if pos in self.edges["edge1a"]:
                pos = self.edges["edge1b"][self.edges["edge1a"].index(pos)]
                direction = "R"
            elif pos in self.edges["edge1b"]:
                pos = self.edges["edge1a"][self.edges["edge1b"].index(pos)]
                direction = "R"
            elif pos in self.edges["edge2b"]:
                pos = self.edges["edge2a"][self.edges["edge2b"].index(pos)]
                direction = "D"
            elif pos in self.edges["edge7a"]:
                pos = self.edges["edge7b"][self.edges["edge7a"].index(pos)]
                direction = "D"
        return (pos, direction)

    def lookup(self, pos):
        pos = self.mod_to_range(pos)
        return self.grove[int(pos.imag)][int(pos.real)]

    def mod_to_range(self, pos):
        if pos.real < 0:
            pos = pos + self.max_real
        elif pos.real > self.max_real - 1:
            pos = pos - self.max_real

        if pos.imag < 0:
            pos = pos + (self.max_imag * 1j)
        elif pos.imag > self.max_imag - 1:
            pos = pos - (self.max_imag * 1j)

        return pos


def part1(g, instructions):
    instructions = (
        instructions.strip().replace("L", ",L,").replace("R", ",R,").split(",")
    )
    grove = Grove(g)
    for instruction in instructions:
        if instruction in ["L", "R"]:
            grove.rotate(instruction)
        else:
            grove.move(int(instruction))

    return (
        (1000 * (grove.pos.imag + 1))
        + (4 * (grove.pos.real + 1))
        + directions.index(grove.direction)
    )


def make_fake_edges():
    edge1a = [50 + (1j * x) for x in range(50)]  # Left -> Right
    edge1b = [0 + (149j - (x * 1j)) for x in range(50)]  # Left -> Right

    edge2a = [50 + x + 0j for x in range(50)]  # Up -> Right
    edge2b = [0 + (150j + (x * 1j)) for x in range(50)]  # Left -> Down

    edge3a = [100 + x + 0j for x in range(50)]  # Up -> Up
    edge3b = [0 + x + 199j for x in range(50)]  # Down -> Down

    edge4a = [149 + (1j * x) for x in range(50)]  # Right -> Left
    edge4b = [99 + (149j - (x * 1j)) for x in range(50)]  # Right -> Left

    edge5a = [49j + 100 + x for x in range(50)]  # Down -> Left
    edge5b = [99 + (50j + x * 1j) for x in range(50)]  # Right -> Up

    edge6a = [50 + x + 149j for x in range(50)]  # Down -> Left
    edge6b = [49 + (150j + (1j * x)) for x in range(50)]  # Right -> Up

    edge7a = [50 + (50j + (x * 1j)) for x in range(50)]  # Left -> Down
    edge7b = [0 + x + 100j for x in range(50)]  # Up -> Right
    return {
        "edge1a": edge1a,
        "edge1b": edge1b,
        "edge2a": edge2a,
        "edge2b": edge2b,
        "edge3a": edge3a,
        "edge3b": edge3b,
        "edge4a": edge4a,
        "edge4b": edge4b,
        "edge5a": edge5a,
        "edge5b": edge5b,
        "edge6a": edge6a,
        "edge6b": edge6b,
        "edge7a": edge7a,
        "edge7b": edge7b,
    }


def part2(g, instructions):
    instructions = (
        instructions.strip().replace("L", ",L,").replace("R", ",R,").split(",")
    )
    fake_edges = make_fake_edges()
    grove = Grove(groveParam=g, fake_edges=fake_edges)
    for instruction in instructions:
        if instruction in ["L", "R"]:
            grove.rotate(instruction)
        else:
            grove.new_move(int(instruction))

    return (
        (1000 * (grove.pos.imag + 1))
        + (4 * (grove.pos.real + 1))
        + directions.index(grove.direction)
    )


print(part1(grove, instructions))

print(part2(grove, instructions))
