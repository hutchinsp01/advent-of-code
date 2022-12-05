d=dict(zip([x+y for x in 'ABC' for y in 'XYZ'],'+T&\x0b7cH\x1aC'))
f=[l[::2]for l in open('2')]
print(sum([ord(d[l]) % 10 for l in f]), sum([ord(d[l]) // 10 for l in f]))

# print(round(sum([ord(d[l])//10+ord(d[l])%10*1e-5 for l in),5))

# [ord(d[l])//10+ord(d[l])%10*1e-5 for l in[l[0::2]for l in open('2')]]
# [x//10+x%10*1e-5 for x in[ord(d[l])for l in[l[0::2]for l in open('2')]]]

# print(round(sum([x//10+x%10*1e-9 for x in[ord(dict(zip([x+y for x in'ABC'for y in'XYZ'],'+T&\x0b7cH\x1aC'))[l])for l in[l[0::2]for l in open('2')]]]),9))

print(*map(sum,zip(*[map(int,'456897312357492816'['AXBYCZAYBZCXAZBXCY'.index(r[::2])//2::9])for r in open('2')])))