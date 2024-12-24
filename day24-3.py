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



def get_dec_number(cache_, letter="z"):
    output = ""
    for key in sorted(cache_.keys()):
        if letter in key:
            output =  str(cache_[key]) + output

    return int(output, 2)


bad_zs = set(["z06", "z15", "z23","z39"])
# print(gates)
# print(cache)
print(get_dec_number(cache, "x"))
print(get_dec_number(cache, "y"))
expected = get_dec_number(cache,"x") + get_dec_number(cache, "y")

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

# subtract all gates that start with z from all_gates
for gate in all_gates.copy():
    if gate.startswith("z") or gate.startswith("x") or gate.startswith("y"):
        all_gates.remove(gate)

for gate1 in tqdm(all_gates - bad_zs):
    for gate2 in tqdm(all_gates - bad_zs - set([gate1])):
        for gate3 in all_gates - bad_zs - set([gate1, gate2]):
            for gate4 in all_gates - bad_zs - set([gate1, gate2, gate3]):
                # make a copy of gates and cache
                cache_copy = deepcopy(cache)
                new_gates = []
                # swap gate 1, 2 3 4 with bad_zs in gates_copy
                mapping = {gate1: "z06", gate2: "z15", gate3: "z23", gate4: "z39"}
                mapping_inv = {v: k for k, v in mapping.items()}
                mapping.update(mapping_inv)
                for gate in gates:
                    if gate.output in mapping:
                        gate.output = mapping[gate.output]
                    new_gates.append(gate)
                if evaluate(cache_copy, new_gates) == expected:
                    print("Found it")
                    print(",".join(sorted([gate1, gate2, gate3, gate4 , *list(bad_zs)])))
                    exit()
                
                    


    


