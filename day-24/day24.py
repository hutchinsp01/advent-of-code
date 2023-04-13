f = open("day24.txt").read().splitlines()

moves = [-1j, 1j, 1, -1, 0]
start = 1
end = ((len(f) - 1) * 1j) + len(f[0]) - 2
max_x = len(f[0])
max_y = len(f)
blizzards = {"^": set(), "v": set(), ">": set(), "<": set()}
for i, line in enumerate(f):
    for j, char in enumerate(line):
        if char not in [".", "#"]:
            blizzards[char].add((j + (i * 1j)))


def update_blizzards(blizzards):
    new_blizzards = {"^": set(), "v": set(), ">": set(), "<": set()}
    for char in blizzards:
        for pos in blizzards[char]:
            if char == "^":
                if pos.imag == 1:
                    new_blizzards[char].add(pos.real + (max_y - 2) * 1j)
                else:
                    new_blizzards[char].add(pos - 1j)
            elif char == "v":
                if pos.imag == max_y - 2:
                    new_blizzards[char].add(pos.real + 1j)
                else:
                    new_blizzards[char].add(pos + 1j)
            elif char == ">":
                if pos.real == max_x - 2:
                    new_blizzards[char].add((pos.imag * 1j) + 1)
                else:
                    new_blizzards[char].add(pos + 1)
            elif char == "<":
                if pos.real == 1:
                    new_blizzards[char].add((pos.imag * 1j) + max_x - 2)
                else:
                    new_blizzards[char].add(pos - 1)
    return new_blizzards


def in_blizzards(pos, blizzards):
    if (
        pos.real <= 0
        or pos.real >= (max_x - 1)
        or pos.imag <= 0
        or pos.imag >= (max_y - 1)
    ):
        return True
    for char in blizzards:
        if pos in blizzards[char]:
            return True
    return False


def part1(blizzards, start, end):
    possible_positions = set()
    possible_positions.add(start)
    i = 0
    while end not in possible_positions:
        new_possible_positions = set()
        blizzards = update_blizzards(blizzards)
        # print_blizzard(blizzards)
        for pos in possible_positions:
            for move in moves:
                if (
                    not in_blizzards(pos + move, blizzards)
                    or pos + move == end
                    or pos + move == start
                ):
                    new_possible_positions.add(pos + move)
        possible_positions = new_possible_positions
        i += 1

    return (i, blizzards)


def part2(blizzards, start, end):
    i, blizzards = part1(blizzards, start, end)
    j, blizzards = part1(blizzards, end, start)
    k, blizzards = part1(blizzards, start, end)
    return i + j + k


def print_blizzard(blizzards):
    for i in range(max_y):
        for j in range(max_x):
            pchar = "."
            for char in blizzards:
                if (j + (i * 1j)) in blizzards[char]:
                    if pchar != ".":
                        pchar = "X"
                    else:
                        pchar = char
            print(pchar, end="")
        print()
    print()


print(part1(blizzards, start, end)[0])
print(part2(blizzards, start, end))
