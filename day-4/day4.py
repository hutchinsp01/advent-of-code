count=0
for l in open("day4.txt").read().strip().split("\n"):
    elves = l.split(',')
    elf1 = [int(x) for x in elves[0].split("-")]
    elf2 = [int(x) for x in elves[1].split("-")]
    elf1r = range(elf1[0], elf1[1]+1)
    for i in elf1r:
        if i in range(elf2[0], elf2[1]+1):
            count += 1
            break

print(count)