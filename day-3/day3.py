total = 0
with open("day3.txt") as f:
    lines = f.read().strip().split("\n")

    for i in range(0, len(lines), 3):
        group = lines[i:i+3]

        for i in group[0]:
            if i in group[1] and i in group[2]:
                print(i)
                if i.isupper():
                    total += (ord(i) - 64 + 26)
                else:
                    total += (ord(i) - 96)

                break

print({1,2} & {2,3} & {2,4}) # {2}
print(total)