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
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "S":
            start = (x, y)
        elif c == "E":
            end = (x, y)
        elif c == "#":
            # only add if its not on the edge
            if x != 0 and x != width - 1 and y != 0 and y != height - 1:
                walls.append((x, y))
        map[(x, y)] = c


#
# given a map, find the length of the shortest path from start to end
def find_shortest_path(map_):
    graph = Graph()
    for key in map_:
        x, y = key
        if map_[key] == "." or map_[key] == "S" or map_[key] == "E":
            if map_.get((x + 1, y)) in [".", "S", "E"]:
                graph.add_edge(key, (key[0] + 1, key[1]), 1)
                # add reverse
                graph.add_edge((key[0] + 1, key[1]), key, 1)
            if map_.get((x - 1, y)) in [".", "S", "E"]:
                graph.add_edge(key, (key[0] - 1, key[1]), 1)
                graph.add_edge((key[0] - 1, key[1]), key, 1)
            if map_.get((x, y + 1)) in [".", "S", "E"]:
                graph.add_edge(key, (key[0], key[1] + 1), 1)
                graph.add_edge((key[0], key[1] + 1), key, 1)
            if map_.get((x, y - 1)) in [".", "S", "E"]:
                graph.add_edge(key, (key[0], key[1] - 1), 1)
                graph.add_edge((key[0], key[1] - 1), key, 1)
    return find_path(graph, start, end)


max_time = find_shortest_path(map).total_cost
print(max_time)

# def pretty_print_map(map_, one_location, two_location):
#     for y in range(height):
#         line = ""
#         for x in range(width):
#             if (x, y) == one_location:
#                 line += "1"
#             elif (x, y) == two_location:
#                 line += "2"
#             else:
#                 line += map_[(x, y)]
#         print(line)

# iterate through walls ,see how much they speed up the shortest path
time_save_dict = defaultdict(int)
for wall in tqdm(walls):
    # for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    # print(f"Trying wall {wall} and delta {delta}")
    map_copy = deepcopy(map)
    map_copy[wall] = "."
    # map_copy[(wall[0] + delta[0], wall[1] + delta[1])] = "."

    # if wall == (8, 1) and delta == (0, 1):
    # print("here")
    # pretty_print_map(map_copy, wall, (wall[0] + delta[0], wall[1] + delta[1]))
    path = find_shortest_path(map_copy)
    time_save = max_time - path.total_cost
    # print(f"Time save: {time_save}")
    time_save_dict[time_save] += 1

print(time_save_dict)
total_saves_100 = 0
for key in sorted(time_save_dict.keys()):
    print(key, time_save_dict[key])
    if key >= 100:
        total_saves_100 += time_save_dict[key]

print(total_saves_100)
print("\a")
