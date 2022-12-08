
base = {}
directories = [base]
cur_dir = base
for l in open("input7.txt").read().strip().split("\n"):
    if l.startswith('$'):
        if l == '$ cd /':
            cur_dir = base
        elif l.startswith("$ cd .."):
            cur_dir = cur_dir['..']
        elif l.startswith("$ cd "):
            cur_dir = cur_dir[l.replace('$ cd ', '')]
        if l == '$ ls':
            continue

    elif l.startswith('dir'):
        cur_dir[l.replace('dir ', '')] = {'..': cur_dir}
        directories.append(cur_dir[l.replace('dir ', '')])

    else:
        size, file = l.split(' ')
        cur_dir.update({file: int(size)})

def remove_backtracks(d):
    d.pop('..', None)
    for k, v in d.items():
        if isinstance(v, dict):
            remove_backtracks(v)

def sum_nested_dictionary(d):
    total = 0
    for k, v in d.items():
        if isinstance(v, dict):
            total += sum_nested_dictionary(v)
        else:
            total += v

    return total


remove_backtracks(base)
directories_sum = [sum_nested_dictionary(d) for d in directories]
directories_sum.sort()
print(directories_sum)
print(sum(filter(lambda x: x <= 100000, directories_sum ))) # Part 1
print(next(x for x in directories_sum if x >= (sum_nested_dictionary(base) - 40000000))) # Part 2
