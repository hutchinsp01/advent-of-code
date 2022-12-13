

f = open("day12-test.txt").read().splitlines()

mymap = [[square for square in line] for line in f]
width = len(mymap[0])
height = len(mymap)

def find_start_in_map(mymap):
    for y in range(height):
        for x in range(width):
            if mymap[y][x] == "S":
                return (x, y)

def find_end_in_map(mymap):
    for y in range(height):
        for x in range(width):
            if mymap[y][x] == "E":
                return (x, y)

def character_ascii_difference(char1, char2):
    return ord(char1) - ord(char2)

def get_adjacent_squares(mymap, tile):
    x, y = tile
    cur_tile_value = mymap[y][x]
    adjacent_squares = [(x,y) for (x,y) in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)] if 0 <= x < width and 0 <= y < height]
    return adjacent_squares

def djikstras(mymap, start, end):
    visited = set()
    queue = [(0, start)]
    mymap[start[1]][start[0]] = 'a'
    mymap[end[1]][end[0]] = 'z'
    while queue:
        (cost, (x, y)) = queue.pop(0)
        if (x, y) == end:
            return cost
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for (x2, y2) in get_adjacent_squares(mymap, (x, y)):
            if (x2, y2) not in visited and ord(mymap[y2][x2]) - ord(mymap[y][x]) <= 1:
                queue.append((cost + 1, (x2, y2)))
    return -1

def get_all_starts(mymap):
    return [(x, y) for y in range(height) for x in range(width) if mymap[y][x] in ['S', 'a']]

end = find_end_in_map(mymap)
print(djikstras(mymap, find_start_in_map(mymap), end))
print(min([x for x in [djikstras(mymap, start, end) for start in get_all_starts(mymap)] if x > 25]))
