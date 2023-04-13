f = open("day20.txt").read().splitlines()

arr = []

for line in f:
    arr.append(int(line))


def move_arr(arr, j):
    cur_pos = j
    to_move = arr[j][1] % (len(arr) - 1)

    new_pos = cur_pos + to_move
    if new_pos >= len(arr):
        new_pos -= len(arr) - 1

    arr.insert(new_pos, arr.pop(cur_pos))
    return arr


def part1(arr):
    new_arr = []
    for i, x in enumerate(arr):
        new_arr.append((i, x))
    for i in range(len(new_arr)):
        for j in range(len(new_arr)):
            if new_arr[j][0] == i:
                new_arr = move_arr(new_arr, j)
                # print([x[1] for x in arr])
                break

    location0 = [x[1] for x in new_arr].index(0)
    total = (
        new_arr[(location0 + 1000) % len(new_arr)][1]
        + new_arr[(location0 + 2000) % len(new_arr)][1]
        + new_arr[(location0 + 3000) % len(new_arr)][1]
    )
    print(total)
    return


def mix(new_arr):
    for i in range(len(new_arr)):
        for j in range(len(new_arr)):
            if new_arr[j][0] == i:
                new_arr = move_arr(new_arr, j)
                break
    return new_arr


def part2(arr):
    for i, x in enumerate(arr):
        arr[i] = (i, x * 811589153)
    for _ in range(10):
        arr = mix(arr)
    location0 = [x[1] for x in arr].index(0)
    total = (
        arr[(location0 + 1000) % len(arr)][1]
        + arr[(location0 + 2000) % len(arr)][1]
        + arr[(location0 + 3000) % len(arr)][1]
    )
    print(total)
    return [x[1] for x in arr]


part1(arr)
part2(arr)
