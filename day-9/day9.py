f = open("day9.txt").read().splitlines()

def valid_tailpos(h, t):
    if max(abs(t[0] - h[0]), abs(t[1] - h[1])) <= 1:
        return True
    return False


def move_head(h, direction):
    if direction == 'R':
        return (h[0] + 1, h[1])
    if direction == 'L':
        return (h[0] - 1, h[1])
    if direction == 'U':
        return (h[0], h[1] + 1)
    if direction == 'D':
        return (h[0], h[1] - 1)


def move_tail(t, h, direction):
    if h[0] == t[0] or h[1] == t[1]:
        if h[0] != t[0]:
            if h[0] > t[0]:
                return (t[0] + 1, t[1])
            if h[0] <= t[0]:
                return (t[0] - 1, t[1])
        if h[1] != t[1]:
            if h[1] > t[1]:
                return (t[0], t[1] + 1)
            if h[0] <= t[0]:
                return (t[0], t[1] - 1)

    else:
        return (t[0] + 1 if h[0] > t[0] else t[0] - 1, t[1] + 1 if h[1] > t[1] else t[1] - 1)

tailposlist = [((0,0),(0,0))]
ropelist= [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
for l in f:
    direction, amount = l.split(' ')
    for i in range(0, int(amount)):
        ropelist[0] = move_head(ropelist[0], direction)
        for i in range(len(ropelist) - 1):
            if not valid_tailpos(ropelist[i], ropelist[i + 1]):
                ropelist[i+1] = move_tail(ropelist[i + 1], ropelist[i], direction)
        tailposlist.append((ropelist[1], ropelist[9]))


[print(len(set(x))) for x in zip(*tailposlist)]
