direction = ["N", "S", "W", "E"]


def check_north(elves_pos, pos):
    return (
        (pos - 1j) in elves_pos
        or (pos - 1j + 1) in elves_pos
        or (pos - 1j - 1) in elves_pos
    )


def check_south(elves_pos, pos):
    return (
        (pos + 1j) in elves_pos
        or (pos + 1j + 1) in elves_pos
        or (pos + 1j - 1) in elves_pos
    )


def check_east(elves_pos, pos):
    return (
        (pos + 1) in elves_pos
        or (pos + 1 + 1j) in elves_pos
        or (pos + 1 - 1j) in elves_pos
    )


def check_west(elves_pos, pos):
    return (
        (pos - 1) in elves_pos
        or (pos - 1 + 1j) in elves_pos
        or (pos - 1 - 1j) in elves_pos
    )


def check_surrounding(elves_pos, pos):
    return (
        check_north(elves_pos, pos)
        or check_south(elves_pos, pos)
        or check_east(elves_pos, pos)
        or check_west(elves_pos, pos)
    )


def get_next_elf_pos(elves_pos, pos, move):

    if check_surrounding(elves_pos, pos):
        for i in range(4):
            if direction[(move + i) % 4] == "N":
                if not check_north(elves_pos, pos):
                    return pos - 1j
            elif direction[(move + i) % 4] == "S":
                if not check_south(elves_pos, pos):
                    return pos + 1j
            elif direction[(move + i) % 4] == "E":
                if not check_east(elves_pos, pos):
                    return pos + 1
            elif direction[(move + i) % 4] == "W":
                if not check_west(elves_pos, pos):
                    return pos - 1
    else:
        return pos


def part2vis(file_name):
    f = open(file_name).read().splitlines()

    elves_pos = set()

    for i, line in enumerate(f):
        for j, char in enumerate(line):
            if char == "#":
                elves_pos.add((j + (i * 1j)))

    i = 0
    vis_list = []
    while True:
        proposals = set()
        for pos in elves_pos:
            proposals.add((pos, get_next_elf_pos(elves_pos, pos, i)))

        if all([x[0] == x[1] for x in proposals]):
            vis_list.append(elves_pos)
            return vis_list
        elves_pos = set()
        next_poses = [x[1] for x in proposals]
        for pos, next_pos in proposals:
            if next_poses.count(next_pos) == 1:
                elves_pos.add(next_pos)
            else:
                elves_pos.add(pos)

        vis_list.append(elves_pos)
        i += 1
