# gave up, didnt work

import fileinput
from functools import lru_cache
from tqdm import tqdm

lines = [line.strip() for line in fileinput.input(files="inputs/21.txt")]

score = 0

numeric_keypad_positions = {
    "A": (2, 0),
    "0": (1, 0),
    "1": (0, 1),
    "2": (1, 1),
    "3": (2, 1),
    "4": (0, 2),
    "5": (1, 2),
    "6": (2, 2),
    "7": (0, 3),
    "8": (1, 3),
    "9": (2, 3),
}

nums = numeric_keypad_positions

directional_keypad_positions = {
    "A": (2, 1),
    "^": (1, 1),
    "<": (0, 0),
    "v": (1, 0),
    ">": (2, 0),
}


@lru_cache(maxsize=None)
def fastest_directional_path(start, end):
    if start == end:
        return ""
    if start == "A":
        if end == ">":
            return "v"
        elif end == "v":
            return "<v"
        elif end == "<":
            return "v<<"
        elif end == "^":
            return "<"
    if start == ">":
        if end == "A":
            return "^"
        elif end == "v":
            return "<"
        elif end == "<":
            return "<<"
        elif end == "^":
            return "<^"
    if start == "^":
        if end == "A":
            return ">"
        elif end == ">":
            return "v>"
        elif end == "v":
            return "v"
        elif end == "<":
            return "v<"
    if start == "v":
        if end == "A":
            return ">^"
        elif end == ">":
            return ">"
        elif end == "^":
            return "^"
        elif end == "<":
            return "<"
    elif start == "<":
        if end == "A":
            return ">>^"
        elif end == ">":
            return ">>"
        elif end == "^":
            return ">^"
        elif end == "v":
            return ">"


graph_of_numpad = {
    nums["7"]: [nums["8"], nums["4"]],
    nums["8"]: [nums["9"], nums["5"], nums["7"]],
    nums["9"]: [nums["6"], nums["8"]],
    nums["4"]: [nums["5"], nums["1"], nums["7"]],
    nums["5"]: [nums["6"], nums["2"], nums["8"], nums["4"]],
    nums["6"]: [nums["3"], nums["5"], nums["9"]],
    nums["1"]: [nums["2"], nums["4"]],
    nums["2"]: [nums["3"], nums["5"], nums["1"], nums["0"]],
    nums["3"]: [nums["6"], nums["2"], nums["A"]],
    nums["A"]: [nums["3"], nums["0"]],
    nums["0"]: [nums["2"], nums["A"]],
}


from collections import deque


def find_all_shortest_paths(graph, start, end):
    # Initialize a queue for BFS: each element is a tuple (current_path, current_node)
    queue = deque([[start]])
    shortest_paths = []
    shortest_length = float("inf")

    while queue:
        # Get the current path from the queue
        path = queue.popleft()
        current_node = path[-1]

        # If the current path exceeds the shortest length, skip further exploration
        if len(path) > shortest_length:
            continue

        # If the end node is reached
        if current_node == end:
            if len(path) < shortest_length:
                # Found a shorter path, reset shortest paths
                shortest_paths = [path]
                shortest_length = len(path)
            elif len(path) == shortest_length:
                # Found another shortest path, add it to the list
                shortest_paths.append(path)
            continue

        # Explore neighbors
        for neighbor in graph.get(current_node, []):
            if neighbor not in path:  # Avoid cycles
                queue.append(path + [neighbor])

    return shortest_paths


@lru_cache(maxsize=None)
def fastest_keypad_path(start, end):
    # test out all the possible paths from start to end, return the one with
    # lowest get_second_robot_input(sequence)
    if start == end:
        return ""
    paths = find_all_shortest_paths(graph_of_numpad, nums[start], nums[end])
    min_length = float("inf")
    min_path = None
    for path in paths:
        # convert path into a string of directions
        output = ""
        for i in range(len(path) - 1):
            current = path[i]
            next = path[i + 1]
            if current[0] < next[0]:
                output += ">"
            elif current[0] > next[0]:
                output += "<"
            elif current[1] < next[1]:
                output += "^"
            elif current[1] > next[1]:
                output += "v"
        third_robot = get_second_robot_input(get_second_robot_input(output + "A"))
        if len(third_robot) < min_length:
            min_length = len(third_robot)
            min_path = output
    return min_path


def get_first_robot_input(line):
    # get list of inputs that would work for the first robot to get from

    current_char = "A"
    output = ""
    for c in line:
        output += fastest_keypad_path(current_char, c)
        output += "A"
        current_char = c
    return output


def get_second_robot_input(line):
    # starting at A
    current_char = "A"
    output = ""
    for c in line:
        output += fastest_directional_path(current_char, c)
        output += "A"
        current_char = c
    return output


def get_sequence(line):
    # first robot has to type the stuff in line using
    # a stupid keypad, starting at A
    first_robot_input = get_first_robot_input(line)
    print(first_robot_input)
    # second robot has to type the stuff for the first_robot_input
    # using a keypad starting at A
    # for each transition from character i to character i+1, calculate the number of steps in the 25th cycle.
    # # use caching so it gets memoized
    # for i in range(len(first_robot_input)-1):
    #     get_second_robot_input(first_robot_input[:i]
    # second_robot_input = get_second_robot_input(first_robot_input)
    # for i in tqdm(range(24)):
    #     second_robot_input = get_second_robot_input(second_robot_input)
    # return second_robot_input
    return ""


for line in lines:
    # get the correct sequnce for the user
    sequence = get_sequence(line)
    # numeric part of this sequence
    numeric = int(line[:-1])
    print(f"This got a score of {len(sequence)} * {numeric}")
    score += numeric * len(sequence)

print(score)
