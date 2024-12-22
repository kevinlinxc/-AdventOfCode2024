import fileinput
from dijkstar import Graph, find_path
from collections import defaultdict
from copy import deepcopy
from tqdm import tqdm

lines = [line.strip() for line in fileinput.input(files="inputs/20.txt")]
width = len(lines[0])
height = len(lines)
print(width, height)
# parse the map

map = {}

start = None
end = None
walls = []
not_walls = []
for y, line in enumerate(lines):
    for x, c in enumerate(line):

        if c == "S":
            start = (x, y)
            not_walls.append((x, y))
        elif c == "E":
            end = (x, y)
            not_walls.append((x, y))
        elif c == "#":
            # only add if its not on the edge
            if x != 0 and x != width - 1 and y != 0 and y != height - 1:
                walls.append((x, y))
        elif c == ".":
            not_walls.append((x, y))
        map[(x, y)] = c


#
# given a map, find the length of the shortest path from start to end
def build_base_graph(map_, wall_allow=None):
    graph = Graph()
    for key in map_:
        x, y = key
        if map_[key] in [".", "S", "E"] or key == wall_allow:
            if map_.get((x + 1, y)) in [".", "S", "E"]:
                graph.add_edge(key, (x + 1, y), 1)
                graph.add_edge((x + 1, y), key, 1)
            if map_.get((x - 1, y)) in [".", "S", "E"]:
                graph.add_edge(key, (x - 1, y), 1)
                graph.add_edge((x - 1, y), key, 1)
            if map_.get((x, y + 1)) in [".", "S", "E"]:
                graph.add_edge(key, (x, y + 1), 1)
                graph.add_edge((x, y + 1), key, 1)
            if map_.get((x, y - 1)) in [".", "S", "E"]:
                graph.add_edge(key, (x, y - 1), 1)
                graph.add_edge((x, y - 1), key, 1)
    return graph


base_graph = build_base_graph(map)

main_path = find_path(base_graph, start, end)

max_time = main_path.total_cost
path = main_path.nodes


print(max_time)


def street_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


good_shortcuts = 0
time_save_frequency = defaultdict(int)
for i in range(len(path)):
    for j in range(i + 1, len(path)):
        distance = street_distance(path[i], path[j])
        if distance <= 20:
            time_save = (j - i) - distance
            if time_save >= 100:
                good_shortcuts += 1
                time_save_frequency[time_save] += 1


for key in sorted(time_save_frequency):
    print(key, time_save_frequency[key])
print(good_shortcuts)
