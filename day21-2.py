import fileinput
from functools import lru_cache
from collections import deque, defaultdict

# Keep your original keypad layouts and graph definitions
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
numeric_position_to_key = {v: k for k, v in numeric_keypad_positions.items()}

directional_keypad_positions = {
    "A": (2, 1),
    "^": (1, 1),
    "<": (0, 0),
    "v": (1, 0),
    ">": (2, 0),
}

# Keep your original dir_keypad_moves
dir_keypad_moves = dict([(('A','^'),'<A'),
                        (('A','>'),'vA'),
                        (('A','v'),'<vA'),
                        (('A','<'),'v<<A'),
                        (('^','A'),'>A'),
                        (('^','>'),'v>A'),
                        (('^','<'),'v<A'),
                        (('^','v'),'vA'),
                        (('v','A'),'^>A'),
                        (('v','>'),'>A'),
                        (('v','<'),'<A'),
                        (('v','^'),'^A'),
                        (('>','A'),'^A'),
                        (('>','^'),'<^A'),
                        (('>','v'),'<A'),
                        (('>','<'),'<<A'),
                        (('<','A'),'>>^A'),
                        (('<','^'),'>^A'),
                        (('<','v'),'>A'),
                        (('<','>'),'>>A')])

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

@lru_cache(maxsize=None)
def fastest_directional_path(start, end):
    if start == end:
        return "A"
    return dir_keypad_moves[(start, end)]

def find_all_shortest_paths(graph, start, end):
    queue = deque([[start]])
    shortest_paths = []
    shortest_length = float("inf")
    
    while queue:
        path = queue.popleft()
        current_node = path[-1]
        
        if len(path) > shortest_length:
            continue
            
        if current_node == end:
            if len(path) < shortest_length:
                shortest_paths = [path]
                shortest_length = len(path)
            elif len(path) == shortest_length:
                shortest_paths.append(path)
            continue
            
        for neighbor in graph.get(current_node, []):
            if neighbor not in path:
                queue.append(path + [neighbor])
                
    outputs = []
    for path in shortest_paths:
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
        outputs.append(output)
    return outputs


def get_transition_frequencies(line):
    frequencies = defaultdict(int)
    current_char = "A"
    for char in line:
        transition = current_char + char
        frequencies[transition] += 1
        current_char = char
    return frequencies

def iterate_frequencies_next_robot(frequencies):
    new_frequencies = defaultdict(int)
    for key, value in frequencies.items():
        # move from the first char to the second char
        first = key[0]
        second = key[1]
        path = fastest_directional_path(first, second)
        frequencies = get_transition_frequencies(path)
        for key in frequencies:
            new_frequencies[key] += value * frequencies[key]
    return new_frequencies

@lru_cache(maxsize=None)
def get_min_path_length(start, end):
    """Get optimal sequence for numeric keypad transitions."""
    print(f"Getting min path length from {start} to {end}")
    if start == end:
        return ""
        
    paths = find_all_shortest_paths(graph_of_numpad, nums[start], nums[end])
    min_length = float("inf")
    
    for path in paths:
        path = path + "A"
        freq = get_transition_frequencies(path)
        for _ in range(25):
            freq = iterate_frequencies_next_robot(freq)
        total_length = 0
        for key in freq:
            total_length += freq[key] * len(key)
        min_length = min(min_length, total_length)         
    return min_length

def get_sequence_length(line):
    final_length = 0
    start_char = "A"

    for char in line:
        length = get_min_path_length(start_char, char)
        start_char = char
        final_length += length
    return final_length


def solve(lines):
    score = 0
    for line in lines:
        print(f"Solving {line}")
        sequence_len = get_sequence_length(line)
        numeric = int(line[:-1])
        print(f"This got a score of {sequence_len} * {numeric}")
        score += numeric * sequence_len
    return score//2  # /2 for some reason?!?

if __name__ == "__main__":
    lines = [line.strip() for line in fileinput.input(files="inputs/21.txt")]
    print(solve(lines))