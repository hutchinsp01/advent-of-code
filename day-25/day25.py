f = open("day25-test.txt").read().splitlines()

SNAFU = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
revSNAFU = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}

count = 0
for line in f:
    value = 0
    index = 0

    for roman_digit in line[::-1]:
        value += pow(5, index) * SNAFU[roman_digit]
        index += 1

    count += value

SNAFUstring = ""
while count > 0:
    cur = count % 5
    if cur in revSNAFU:
        SNAFUstring = revSNAFU[cur] + SNAFUstring
        count -= cur
    else:
        SNAFUstring = revSNAFU[cur - 5] + SNAFUstring
        count += abs(cur - 5)
    count = count // 5


# 27210103880867
print(count)
print(SNAFUstring)
