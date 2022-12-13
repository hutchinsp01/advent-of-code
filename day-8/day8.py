f = [list(x) for x in open("day8-test.txt").read().strip().split("\n")]
height = len(f)
length = len(f[0])

total = (length * 2 + height * 2) - 4

def all_shorter_to_left(h, l, f):
    for k in range(l):
        if f[h][k] >= f[h][l]:
            return False
    return True

def all_shorter_to_right(h, l, f):
    for k in range(l + 1, length):
        if f[h][k] >= f[h][l]:
            return False
    return True

def all_shorter_above(h, l, f):
    for k in range(h):
        if f[k][l] >= f[h][l]:
            return False
    return True

def all_shorter_below(h, l, f):
    for k in range(h + 1, height):
        if f[k][l] >= f[h][l]:
            return False
    return True

for h in range(1, height - 1):
    for l in range(1, length - 1):
        if all_shorter_to_left(h, l, f) or all_shorter_to_right(h, l, f) or all_shorter_above(h, l, f) or all_shorter_below(h, l, f):
            total += 1
print(total)

def score_to_the_left(h,l,f):
    score = 0
    for k in reversed(range(l)):
        score += 1
        if f[h][k] >= f[h][l]:
            return score
    return score

def score_to_the_right(h,l,f):
    score = 0
    for k in range(l + 1, length):
        score += 1
        if f[h][k] >= f[h][l]:
            return score
    return score

def score_above(h,l,f):
    score = 0
    for k in reversed(range(h)):
        score += 1
        if f[k][l] >= f[h][l]:
            return score
    return score

def score_below(h,l,f):
    score = 0
    for k in range(h + 1, height):
        score += 1
        if f[k][l] >= f[h][l]:
            return score
    return score

new_total = [1]
for h in range(1, height - 1):
    for l in range(1, length - 1):
        score = score_to_the_left(h,l,f) * score_to_the_right(h,l,f) * score_above(h,l,f) * score_below(h,l,f)
        new_total.append(score)

print(max(new_total))
