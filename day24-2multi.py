import fileinput
from tqdm import tqdm
from copy import deepcopy
from collections import defaultdict
import threading
from queue import Queue
from itertools import combinations
import concurrent.futures
import random

class Gate:
    def __init__(self, gate_str):
        if "AND" in gate_str:
            self.op = "AND"
        elif "XOR" in gate_str:
            self.op = "XOR"
        elif "OR" in gate_str:
            self.op = "OR"
        self.gate_1 = gate_str.split(" ")[0]
        self.gate_2 = gate_str.split(self.op)[1].split(" ")[1]
        self.output = gate_str.split("->")[1].strip()

    def __str__(self):
        return f"{self.gate_1} {self.op} {self.gate_2} -> {self.output}"

    def __repr__(self):
        return self.__str__()
    
    def can_evaluate(self, cache_):
        return self.gate_1 in cache_ and self.gate_2 in cache_
    
    def evaluate(self, cache_):
        if self.op == "AND":
            cache_[self.output] = cache_[self.gate_1] & cache_[self.gate_2]
        elif self.op == "XOR":
            cache_[self.output] = cache_[self.gate_1] ^ cache_[self.gate_2]
        elif self.op == "OR":
            cache_[self.output] = cache_[self.gate_1] | cache_[self.gate_2]

def get_dec_number(cache_, letter="z"):
    output = ""
    for key in sorted(cache_.keys()):
        if letter in key:
            output = str(cache_[key]) + output
    return int(output, 2)

def evaluate(cache_, gates_):
    while len(gates_) > 0:
        can_evaluate = []
        for gate in gates_:
            if gate.can_evaluate(cache_):
                can_evaluate.append(gate)
        if len(can_evaluate) == 0:
            return None
        for gate in can_evaluate:
            gate.evaluate(cache_)
            gates_.remove(gate)
    return get_dec_number(cache_, "z")

def process_combination(combination, gates, cache, expected, bad_zs):

    gate1, gate2, gate3, gate4 = combination
    cache_copy = deepcopy(cache)
    new_gates = []
    
    # Create mapping for gate swapping
    mapping = {
        gate1: "z06", 
        gate2: "z15", 
        gate3: "z23", 
        gate4: "z39"
    }
    mapping_inv = {v: k for k, v in mapping.items()}
    mapping.update(mapping_inv)
    
    # Create new gates with swapped values
    for gate in gates:
        gate_copy = deepcopy(gate)
        if gate_copy.output in mapping:
            gate_copy.output = mapping[gate_copy.output]
        new_gates.append(gate_copy)
    
    result = evaluate(cache_copy, new_gates)
    if result == expected:
        value = sorted([gate1, gate2, gate3, gate4, *list(bad_zs)])
        print(",".join(value))
        with open("day24ans.txt", "w") as f:
            f.write(",".join(value))
        return sorted([gate1, gate2, gate3, gate4, *list(bad_zs)])
    return None

def main():
    # Read input and initialize data structures
    lines = [line.strip() for line in fileinput.input(files="inputs/24.txt")]
    cache = {}
    gates = []
    gates_now = False
    related_gates = defaultdict(list)
    gates_map = {}
    all_gates = set()
    
    # Parse input
    for line in lines:
        if line == "":
            gates_now = True
            continue
        if gates_now:
            new_gate = Gate(line)
            gates.append(new_gate)
            gates_map[new_gate.output] = new_gate
            all_gates.add(new_gate.output)
            related_gates[new_gate.gate_1].append(new_gate)
            related_gates[new_gate.gate_2].append(new_gate)
        else:
            name, value = line.split(": ")
            cache[name] = int(value)
    
    # Calculate expected value
    expected = get_dec_number(cache, "x") + get_dec_number(cache, "y")
    
    # Remove unnecessary gates
    bad_zs = set(["z06", "z15", "z23", "z39"])
    valid_gates = all_gates - bad_zs - set(g for g in all_gates if g.startswith(('z', 'x', 'y')))
    
    # Generate combinations for parallel processing
    combinations_list = list(combinations(valid_gates, 4))
    
    # Process combinations in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(
                process_combination, 
                combo, 
                gates, 
                cache, 
                expected, 
                bad_zs
            )
            for combo in combinations_list
        ]
        
        # Use tqdm to show progress
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            result = future.result()
            if result:
                print("Found it!")
                print(",".join(result))
                executor.shutdown(wait=False)
                return

if __name__ == "__main__":
    main()