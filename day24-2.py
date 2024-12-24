import fileinput
from tqdm import tqdm
from copy import deepcopy
from collections import defaultdict
import graphviz
lines = [line.strip() for line in fileinput.input(files="inputs/24.txt")]
dot = graphviz.Digraph(comment="AOC 2024 Day 24", engine="dot")
cache = {}
gates = []
gates_now = False
related_gates = defaultdict(list)

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
            cache[self.output] = cache_[self.gate_1] & cache_[self.gate_2]
        elif self.op == "XOR":
            cache[self.output] = cache_[self.gate_1] ^ cache_[self.gate_2]
        elif self.op == "OR":
            cache[self.output] = cache_[self.gate_1] | cache_[self.gate_2]

# Parse input
gates_map = {}
all_gates = set()
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

def find_gate(input1, input2, operation):
    for gate in gates:
        if gate.gate_1 in [input1, input2] and gate.gate_2 in [input1, input2] and gate.op == operation:
            return gate
    return None

def get_gates_using_output(output):
    return [gate for gate in gates if gate.gate_1 == output or gate.gate_2 == output]



# iterate through the gates and give them apt names
aliases = {"rfg": "carry0"}
for i in range(1, 45):
    x = f"x{str(i).zfill(2)}"
    y = f"y{str(i).zfill(2)}"
    z = f"z{str(i).zfill(2)}"
    xxory1 = find_gate(x, y, "XOR")
    if xxory1 is None:
        print("sus: no xor for ", x, y)
    else:
        xor1output = xxory1.output
        aliases[xor1output] = f"xxory_{i}"
        # should be input to an and gate
        for gate in gates:
            if xor1output in [gate.gate_1, gate.gate_2]:
                if gate.op == "AND":
                    xorandcarry1 = gate.output
                    aliases[xorandcarry1] = f"xorandcarry_{i}"
        # should be input to an xor gate too
        for gate in gates:
            if xor1output in [gate.gate_1, gate.gate_2]:
                if gate.op == "XOR":
                    xor2output = gate.output
                    aliases[xor2output] = f"sum_{i}"

    xandy = find_gate(x, y, "AND")
    if xandy is None:
        print("sus: no and for ", x, y)
    else:
        andoutput1 = xandy.output
        aliases[andoutput1] = f"xandy_{i}"
    
    if xorandcarry1 and andoutput1:
        # should be input to an or gate for the next carry
        carry_gate = find_gate(xorandcarry1, andoutput1, "OR")
        if carry_gate is None:
            print("sus: no or for ", xorandcarry1, andoutput1)
        else:
            oroutput1 = carry_gate.output
            aliases[oroutput1] = f"carry_or_{i}"
print(aliases)
print(len(aliases))
for key, value in aliases.items():
    value = value + "(" + key + ")"
    aliases[key] = value

for gate in gates:
    gate_1_name = aliases.get(gate.gate_1, gate.gate_1)
    gate_2_name = aliases.get(gate.gate_2, gate.gate_2)
    output_name = aliases.get(gate.output, gate.output)
    dot.node(gate_1_name, gate_1_name)
    dot.node(gate_2_name, gate_2_name)
    dot.node(output_name, output_name)
    dot.edge(gate_1_name, output_name)
    dot.edge(gate_2_name, output_name)

dot.render("gates.gv", view=True)

# found these manually from the graphviz output
gates_to_swap = {"fdv": "dbp",
                 "dbp": "fdv",
                 "z15": "ckj",
                    "ckj": "z15",
                    "kdf": "z23",
                    "z23": "kdf",
                    "z39": "rpp",
                    "rpp": "z39"
                 }

for gate in gates:
    if gate.output in gates_to_swap:
        gate.output = gates_to_swap[gate.output]
        print(f"Swapping {gate.output}")

print("Evaluating")

def get_dec_number(cache_, letter="z"):
    output = ""
    for key in sorted(cache_.keys()):
        if letter in key:
            output =  str(cache_[key]) + output

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

finalz = evaluate(cache, gates)
print(f"Final z after swaps: {finalz}")
expected = get_dec_number(cache,"x") + get_dec_number(cache, "y")
assert finalz == expected, f"Expected {expected}, got {finalz}"

print(",".join(sorted(list(gates_to_swap.keys()))))
