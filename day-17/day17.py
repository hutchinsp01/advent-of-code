from functools import lru_cache

ROCKS = 1000000000000
CAVERN_WIDTH = 7

f = open("day17.txt").read().strip()


rocks = [
    ["..####."],
    ["...#...", "..###..", "...#..."],
    ["....#..", "....#..", "..###.."],
    ["..#....", "..#....", "..#....", "..#...."],
    ["..##...", "..##..."],
]


class GoodException(Exception):
    pass


class StopException(Exception):
    pass


def count_empty_cavern_rows(cavern):
    empty_rows = 0
    for row in cavern:
        if row == "." * CAVERN_WIDTH:
            empty_rows += 1
        else:
            break
    return empty_rows


def find_full_row(cavern):
    for row in range(len(cavern)):
        if cavern[row] == "@" * CAVERN_WIDTH:
            return row
    return -1


def add_rock_to_cavern(rock, cavern):
    for i in range(len(rock)):
        cavern[i] = rock[i]


def count_rock_size(rock):
    count = 0
    for row in rock:
        count += row.count("#")
    return count


def replace_str_index(text, index=0, replacement=""):
    return "%s%s%s" % (text[:index], replacement, text[index + 1 :])


def move_with_wind(cavern, wind, rock):
    check_count = 0
    rock_size = count_rock_size(rock)
    windint = 1 if wind == ">" else -1
    rows_needed = 0
    try:
        for row in range(len(cavern)):
            rows_needed += 1
            for col in range(CAVERN_WIDTH):
                if cavern[row][col] == "#":
                    if not CAVERN_WIDTH > col + windint >= 0:
                        raise Exception("Out of bounds")
                    if cavern[row][col + windint] not in ["#", "."]:
                        raise Exception("Collision")
                    check_count += 1
                if check_count == rock_size:
                    raise GoodException("Rock can move")
    except GoodException:
        ## Move rock Refactor later
        for row in range(rows_needed):
            row2 = cavern[row]
            for col in range(CAVERN_WIDTH):
                if row2[col] == "#":
                    if (
                        not CAVERN_WIDTH > col - windint >= 0
                        or CAVERN_WIDTH > col - windint >= 0
                        and row2[col - windint] != "#"
                    ):
                        cavern[row] = replace_str_index(cavern[row], col, ".")
                    cavern[row] = replace_str_index(cavern[row], col + windint, "#")

    except Exception:
        pass

    return cavern


def move_rock_down(cavern, rock):
    valid = True
    check_count = 0
    rock_size = count_rock_size(rock)
    try:
        for row in range(len(cavern)):
            for col in range(CAVERN_WIDTH):
                if cavern[row][col] == "#":
                    if row == len(cavern) - 1:
                        raise StopException("Rock hit bottom")
                    if cavern[row + 1][col] not in ["#", "."]:
                        raise StopException("Collision")
                    check_count += 1
                if check_count == rock_size:
                    raise GoodException("Rock can move")

    except GoodException:
        ## find lowest row
        check_count = 0
        lowest_row = 0
        for row in range(len(cavern)):
            for col in range(CAVERN_WIDTH):
                if cavern[row][col] == "#":
                    lowest_row = row
                    check_count += 1
            if check_count == rock_size:
                break

        ## Move rock
        for row in range(lowest_row, -1, -1):
            for col in range(CAVERN_WIDTH):
                if cavern[row][col] == "#":
                    cavern[row] = replace_str_index(cavern[row], col, ".")
                    cavern[row + 1] = replace_str_index(cavern[row + 1], col, "#")

    except StopException:
        valid = False
        check_count = 0
        for row in range(len(cavern)):
            for col in range(CAVERN_WIDTH):
                if cavern[row][col] == "#":
                    cavern[row] = replace_str_index(cavern[row], col, "@")
                    check_count += 1
            if check_count == rock_size:
                break
    return cavern, valid


def part1(number_of_rocks):
    cavern = ["." * CAVERN_WIDTH for _ in range(3)]

    move_count = 0
    cavern_len = 0
    hash_hit = False

    hash_map = {}

    i = 0
    while i < number_of_rocks:

        if len(cavern) > 40:
            cavern_len += len(cavern) - 40
            cavern = cavern[:40]

        if (
            i % len(rocks),
            move_count % len(f),
            tuple(cavern),
        ) in hash_map and not hash_hit:
            hash_hit = True
            hash_cavern_len, hash_i = hash_map[
                (i % len(rocks), move_count % len(f), tuple(cavern))
            ]
            i_diff = i - hash_i
            cavern_len_diff = cavern_len - hash_cavern_len
            cavern_len += cavern_len_diff * ((number_of_rocks - i) // i_diff)
            i = i + i_diff * ((number_of_rocks - i) // i_diff)

        hash_map[(i % len(rocks), move_count % len(f), tuple(cavern))] = (
            cavern_len,
            i,
        )

        rock = rocks[i % len(rocks)]
        rock_height = len(rock)
        empty_rows = count_empty_cavern_rows(cavern)
        if empty_rows - rock_height > 3:
            cavern = cavern[empty_rows - rock_height - 3 :]
        while empty_rows - rock_height < 3:
            cavern = ["." * CAVERN_WIDTH] + cavern
            empty_rows += 1
        add_rock_to_cavern(rock, cavern)

        while True:
            cavern = move_with_wind(cavern, f[move_count % len(f)], rock)
            cavern, valid = move_rock_down(cavern, rock)
            move_count += 1
            if not valid:
                break
        i += 1

    print((cavern_len + len(cavern)) - count_empty_cavern_rows(cavern))


part1(2022)
part1(1000000000000)
