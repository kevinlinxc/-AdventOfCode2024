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
def bfs_trail_ends(graph, start):
    visited = set()
    queue = []
    queue.append(start)
    trail_ends_found = set()
    while queue:
        node = queue.pop(0)
        if node not in visited:
            if node in trail_ends:
                trail_ends_found.add(node)
            visited.add(node)
            queue.extend(list(set(graph[node]) - visited))
    return len(trail_ends_found)


total = 0
for trail_head in trail_heads:
    paths_to_ends = bfs_trail_ends(graph, trail_head)
    print(f"Found {paths_to_ends} trail ends from {trail_head=}")
    total += paths_to_ends

print(total)
