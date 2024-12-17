import fileinput

import dijkstar.algorithm
from dijkstar import Graph, find_path

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

graph = Graph()
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
        graph.add_node(f"{x}_{y}_{direction}")
        for neighbour in neighbour_dirs:
            graph.add_edge(f"{x}_{y}_{direction}", f"{x}_{y}_{neighbour}", 1000)

        dx, dy = deltas[direction]
        if map.get((x + dx, y + dy)) in [
            ".",
            "E",
            "S",
        ]:  # can move in that direction, add an edge
            graph.add_edge(f"{x}_{y}_{direction}", f"{x+dx}_{y+dy}_{direction}", 1)

# print(graph)
costs = []
for end_node in end_nodes:
    try:
        print(f"Start and end in graph: {start_node} -> {end_node}")
        path = find_path(graph, start_node, end_node)
        print(path.total_cost)
        costs.append(path.total_cost)
    except dijkstar.algorithm.NoPathError as e:
        print(e)
        pass

print(costs)
