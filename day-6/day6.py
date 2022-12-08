routine = open('day6-test.txt').readline().replace('\n', '')

for i in range(0, len(routine)-13):
    chord = routine[i:i+14]
    if len(set(chord)) == len(chord):
        print(chord)
        print(i+14)
        break
