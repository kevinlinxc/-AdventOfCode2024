import fileinput
from collections import defaultdict

lines = [line.strip() for line in fileinput.input(files="inputs/10.txt")]

graph = defaultdict(list)

# encode as node #, and value
id = 0
id_to_height = {}
for y, line in enumerate(lines):
    for x, height in enumerate(line):
        height = int(height)
        id_to_height[id] = height
        id += 1
print(id_to_height)
trail_heads = []
trail_ends = []

id = 0
for y, line in enumerate(lines):
    for x, height in enumerate(line):
        height = int(height)
        if height == 0:
            trail_heads.append(id)
        if height == 9:
            trail_ends.append(id)
        # add neighbours of this id
        if x > 0:
            # check if left neighbour is one higher
            if id_to_height[id - 1] == (height + 1):
                graph[id].append(id - 1)
        if y > 0:
            # check if above neighbour is one higher
            if id_to_height[id - len(lines[0])] == (height + 1):
                graph[id].append(id - len(lines[0]))
        if x < len(lines[0]) - 1:
            # check
            if id_to_height[id + 1] == (height + 1):
                graph[id].append(id + 1)
        if y < len(lines) - 1:
            if id_to_height[id + len(lines[0])] == (height + 1):
                graph[id].append(id + len(lines[0]))
        id += 1

print(f"{trail_heads=}")
print(graph)


# for each trail head, do BFS and find out how many trail ends are reachable
def unique_paths_from_start_to_end(graph, start, end):
    return recursive_helper(graph, start, end, [], set())


def recursive_helper(graph, start, end, path, visited):
    if start == end:
        return 1
    visited.add(start)
    total = 0
    for neighbour in graph[start]:
        if neighbour not in visited:
            total += recursive_helper(
                graph, neighbour, end, path + [neighbour], visited
            )
    visited.remove(start)
    return total


total = 0
for trail_head in trail_heads:
    for trail_end in trail_ends:
        total += unique_paths_from_start_to_end(graph, trail_head, trail_end)
print(total)
