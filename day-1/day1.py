file = open("day1.txt", "r")

biggestElf1 = 0
biggestElf2 = 0
biggestElf3 = 0
currentElf = 0
for line in file.readlines():


    if not line.strip() :
        if currentElf > biggestElf1:
            biggestElf3 = biggestElf2
            biggestElf2 = biggestElf1
            biggestElf1 = currentElf
        elif currentElf > biggestElf2:
            biggestElf3 = biggestElf2
            biggestElf2 = currentElf
        elif currentElf > biggestElf3:
            biggestElf3 = currentElf
        currentElf = 0

    else:
        currentElf += int(line.split()[0])

if currentElf > biggestElf1:
    biggestElf3 = biggestElf2
    biggestElf2 = biggestElf1
    biggestElf1 = currentElf
elif currentElf > biggestElf2:
    biggestElf3 = biggestElf2
    biggestElf2 = currentElf
elif currentElf > biggestElf3:
    biggestElf3 = currentElf


print(biggestElf1 + biggestElf2 + biggestElf3)
