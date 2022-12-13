import json
from functools import cmp_to_key


def compare(left, right):
    maxIndex = max(len(left), len(right))
    for index in range(maxIndex):
        if index == len(left) and index < len(right):
            return 1
        if index < len(left) and index == len(right):
            return -1

        leftcmp, rightcmp = left[index], right[index]

        match leftcmp, rightcmp:
            case int(), int():
                if leftcmp < rightcmp:
                    return 1
                if leftcmp > rightcmp:
                    return -1
            case int(), list():
                cmpresult = compare([leftcmp], rightcmp)
                if cmpresult != 0:
                    return cmpresult
            case list(), int():
                cmpresult = compare(leftcmp, [rightcmp])
                if cmpresult != 0:
                    return cmpresult
            case list(), list():
                cmpresult = compare(leftcmp, rightcmp)
                if cmpresult != 0:
                    return cmpresult

    return 0


f = open("day13.txt").read().split("\n\n")
total = 0
for i, pair in enumerate(f, 1):
    left, right = pair.split("\n")
    left, right = json.loads(left), json.loads(right)
    if compare(left, right) == 1:
        total += i

print(total)

# part 2
f = open("day13.txt").read().replace("\n\n", "\n").split("\n")
f.append("[[2]]")
f.append("[[6]]")
lines = [json.loads(line) for line in f]
lines.sort(key=cmp_to_key(compare))
lines.reverse()
print((lines.index([[2]]) + 1) * (lines.index([[6]]) + 1))
