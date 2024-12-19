import fileinput
from dijkstar import Graph, find_path

lines = [line.strip() for line in fileinput.input(files="inputs/18.txt")]

# side length =
side_length = 71
map = {}
for x in range(side_length):
    for y in range(side_length):
        map[(x, y)] = "."

for i in range(1024):
    x, y = lines[i].split(",")
    x, y = int(x), int(y)
    map[(x, y)] = "#"


def print_map():
    for y in range(side_length):
        for x in range(side_length):
            print(map[(x, y)], end="")
        print()


print_map()

# find shortest path from 0, 0 to side_length, side_length
graph = Graph()
for x in range(side_length):
    for y in range(side_length):
        if map[(x, y)] == "#":
            continue
        for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if 0 <= x + dx < side_length and 0 <= y + dy < side_length:
                if map[(x + dx, y + dy)] != "#":
                    graph.add_edge((x, y), (x + dx, y + dy), 1)

print(find_path(graph, (0, 0), (side_length - 1, side_length - 1)))
