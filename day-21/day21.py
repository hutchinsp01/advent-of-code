f = open("day21.txt").read().splitlines()


class YellMonkey:
    def __init__(self, number):
        self.number = number


class WaitMonkey:
    def __init__(self, monkey1, monkey2, method):
        self.monkey1 = monkey1
        self.monkey2 = monkey2
        self.method = method


monkeys = {}
for line in f:
    if "+" in line or "-" in line or "/" in line or "*" in line:
        monkeys[line[0:4]] = WaitMonkey(line[6:10], line[13:17], line[11])
    else:
        monkeys[line[0:4]] = YellMonkey(int(line[6:]))


def explore(monkey, monkeys):
    if type(monkey) == YellMonkey:
        return monkey.number

    elif type(monkey) == WaitMonkey:
        return eval(
            f"{explore(monkeys[monkey.monkey1], monkeys)} {monkey.method} {explore(monkeys[monkey.monkey2], monkeys)}"
        )


def find_trend(monkeys):
    lhs = monkeys["root"].monkey1
    rhs = monkeys["root"].monkey2

    monkeys["humn"].number = 0
    lhstotal = explore(monkeys[lhs], monkeys)
    rhstotal = explore(monkeys[rhs], monkeys)
    cur_diff = lhstotal - rhstotal

    monkeys["humn"].number = 1000
    lhstotal = explore(monkeys[lhs], monkeys)
    rhstotal = explore(monkeys[rhs], monkeys)
    new_diff = lhstotal - rhstotal

    if new_diff >= cur_diff:
        return "down"

    elif new_diff < cur_diff:
        return "up"


def part1(monkeys):
    start = monkeys["root"]
    total = explore(start, monkeys)
    return total


def part2(monkeys):
    lhs = monkeys["root"].monkey1
    rhs = monkeys["root"].monkey2
    monkeys["humn"].number = 0
    lhstotal = explore(monkeys[lhs], monkeys)
    rhstotal = explore(monkeys[rhs], monkeys)
    trend = find_trend(monkeys)
    binary_diff = 100000000000
    while lhstotal != rhstotal:
        if trend == "up":
            if rhstotal > lhstotal:
                binary_diff /= 2
                monkeys["humn"].number -= binary_diff
            else:
                monkeys["humn"].number += binary_diff

        elif trend == "down":
            if rhstotal > lhstotal:
                binary_diff /= 2
                monkeys["humn"].number += binary_diff
            else:
                monkeys["humn"].number -= binary_diff

        lhstotal = explore(monkeys[lhs], monkeys)
        rhstotal = explore(monkeys[rhs], monkeys)

    return monkeys["humn"].number


print(part1(monkeys))
print(part2(monkeys))
