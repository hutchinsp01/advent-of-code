count=0
instructions=False
crates=True

d={}

for l in open("day5.txt").read().strip().split("\n"):
    if '1' in l:
        crates=False

    if crates:
        line = [l[i:i+4] for i in range(0, len(l), 4)]
        for count, crate in enumerate(line, start=1):
            if '[' in crate:
                if str(count) in d.keys():
                    d[str(count)].insert(0, crate[1])
                else:
                    d[str(count)]=[crate[1]]

    if 'move' in l:
        instructions=True
    removed = []
    if instructions:
        line = l.replace(' ', '').replace('move','').split('from')
        amn = int(line[0])
        f, t = line[1].split('to')

        # Part 1
        for i in range(amn):
            d[t].append(d[f].pop())

        # Part 2
        # for i in range(amn):
        #     removed.append(d[f].pop())

        # removed.reverse()

        # for i in removed:
        #     d[t].append(i)

        #################

print([d[str(x)][-1] for x in range(1, len(d) + 1)])
