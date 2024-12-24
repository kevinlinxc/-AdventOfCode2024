from pyvis.network import Network
import fileinput
from tqdm import tqdm
from copy import deepcopy
from collections import defaultdict

lines = [line.strip() for line in fileinput.input(files="inputs/24.txt")]


cache = {}
gates = []
gates_now = False
related_gates = defaultdict(list)
class Gate:
    def __init__(self, gate_str):
        print(gate_str)
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
        # print(f"Evaluating  {self.output} = {cache_[self.gate_1]} {self.op} {cache_[self.gate_2]}", end="")
        if self.op == "AND":
            cache[self.output] = cache_[self.gate_1] & cache_[self.gate_2]
        elif self.op == "XOR":
            cache[self.output] = cache_[self.gate_1] ^ cache_[self.gate_2]
        elif self.op == "OR":
            cache[self.output] = cache_[self.gate_1] | cache_[self.gate_2]

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
# Define the nodes and edges
edges = [(gate.gate_1, gate.output, gate.op) for gate in gates] + [(gate.gate_2, gate.output, gate.op) for gate in gates]
    # Add the rest of the edges here...


# Initialize the PyVis Network
net = Network(notebook=True, height="750px", width="100%", directed=True)

# Add edges with labels
for source, target, label in edges:
    net.add_node(source, label=source)
    net.add_node(target, label=target)
    net.add_edge(source, target, label=label)

# Customize appearance
net.repulsion(node_distance=200, spring_length=100)
net.show_buttons(filter_=["physics"])

# Generate and display the graph
net.show("graph.html")
