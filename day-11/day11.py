

class Monkey:
    def __init__(self, items, operation, test, true, false):
        self.items = items
        self.operation = operation
        self.test = test
        self.true = true
        self.false = false
        self.count = 0

    def action(self, monkey_list):
        self.count += len(self.items)
        self.do_inspections()
        # self.destress_items()
        self.test_items(monkey_list)

    def do_inspections(self):
        new_items = []
        for item in self.items:
            new_items.append(self.do_inspection(item))
        self.items = new_items

    def do_inspection(self, item):
        item = item % LCM
        if self.operation[1] == 'old':
            if self.operation[0] == '+':
                return item + item
            elif self.operation[0] == '*':
                return item * item
        else:
            if self.operation[0] == '+':
                return item + int(self.operation[1])
            elif self.operation[0] == '*':
                return item * int(self.operation[1])

    def destress_items(self):
        self.items = [item // 3 for item in self.items]

    def test_items(self, monkey_list):
        for item in self.items:
            if self.test_item(item):
                monkey_list[self.true].items.append(item)
            else:
                monkey_list[self.false].items.append(item)
        self.items = []

    def test_item(self, item):
        return item % self.test == 0

LCM = 1
monkey_list = []
f = open("day11.txt").read().split('\n\n')
for monkey in f:
    split = monkey.split('\n')
    items = operation = test = true = false = None
    for line in split:
        if line.startswith("  Starting items:"):
            items = [int(x) for x in line.replace("  Starting items: ", "").strip().split(', ')]
        if line.startswith('  Operation:'):
            op = line.replace('  Operation: new = old ', "").strip().split(' ')
            operand = op[0]
            operand_number = op[1]
            operation = (operand, operand_number)
        if line.startswith('  Test: '):
            test = int(line.replace("  Test: divisible by ", '').strip())
            LCM = LCM * test
        if line.startswith('    If true:'):
            true = int(line.replace("    If true: throw to monkey ", '').strip())
        if line.startswith('    If false:'):
            false = int(line.replace("    If false: throw to monkey ", '').strip())
    monkey_list.append(Monkey(items, operation, test, true, false))

def run_monkeys(monkey_list):
    for i in range(10000):
        for monkey in monkey_list:
            monkey.action(monkey_list)

    counts = [monkey.count for monkey in monkey_list]
    counts.sort()
    counts.reverse()
    print(counts[0] * counts[1])

run_monkeys(monkey_list)
