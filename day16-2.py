import fileinput

import heapq
from collections import defaultdict

lines = [line.strip() for line in fileinput.input(files="inputs/16.txt")]
# moving cost 1 point
# rotating costs 1000 points

# parse map
start = None
map = {}
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "S":
            start = (x, y)
        elif char == "E":
            end = (x, y)
        map[(x, y)] = char


# iterate over the keys. For each position that isn't a wall, create 4 graph nodes separated for each direction
# if they can move forward in that direction, add the position to the graph as well

graph = defaultdict(list)
start_node = f"{start[0]}_{start[1]}_E"
end_nodes = [f"{end[0]}_{end[1]}_E", f"{end[0]}_{end[1]}_N"]

for key in map:
    x, y = key
    if map[key] == "#":
        continue
    # its S, E or .
    # add one node for each direction
    deltas = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    neighbour_dirs = {
        "N": ["E", "W"],
        "E": ["N", "S"],
        "S": ["E", "W"],
        "W": ["N", "S"],
    }
    for direction in ["N", "E", "S", "W"]:
        graph[f"{x}_{y}_{direction}"] = []
        for neighbour in neighbour_dirs:
            graph[f"{x}_{y}_{direction}"].append((f"{x}_{y}_{neighbour}", 1000))

        dx, dy = deltas[direction]
        if map.get((x + dx, y + dy)) in [
            ".",
            "E",
            "S",
        ]:  # can move in that direction, add an edge
            graph[f"{x}_{y}_{direction}"].append((f"{x+dx}_{y+dy}_{direction}", 1))


def find_all_shortest_paths(graph, start, end):
    # Min-heap for Dijkstra's algorithm
    heap = [(0, start, [start])]  # (cost, current_node, path)
    # To store the minimum cost to reach each node
    min_cost = defaultdict(lambda: float("inf"))
    min_cost[start] = 0
    # To store all shortest paths
    shortest_paths = []
    shortest_cost = float("inf")

    while heap:
        cost, current_node, path = heapq.heappop(heap)

        # If we reach the end node and it's the shortest cost, add the path
        if current_node == end:
            if cost < shortest_cost:
                shortest_cost = cost
                shortest_paths = [path]
            elif cost == shortest_cost:
                shortest_paths.append(path)
            continue

        # Explore neighbors
        for neighbor, edge_cost in graph[current_node]:
            new_cost = cost + edge_cost
            if new_cost <= min_cost[neighbor]:
                min_cost[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor, path + [neighbor]))

    return shortest_paths, shortest_cost


# find all shortest paths from start_node to end_nodes
shortest_paths = []
shortest_cost = float("inf")
for end_node in end_nodes:
    paths, cost = find_all_shortest_paths(graph, start_node, end_node)
    if cost < shortest_cost:
        print(f"New shortest cost: {cost}")
        shortest_cost = cost
        shortest_paths = paths
    elif cost == shortest_cost:
        print(f"Same shortest cost: {cost}")
        shortest_paths.extend(paths)

print(shortest_paths)

all_nodes = set()
for shortest_path in shortest_paths:
    for tile in shortest_path:
        # truncate to remove direction
        all_nodes.add(tile[:-2])
print(len(all_nodes))
