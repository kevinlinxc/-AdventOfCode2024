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

sus_gates = defaultdict(int)
for i in range(1, 44):
    x = f"x{str(i).zfill(2)}"
    y = f"y{str(i).zfill(2)}"
    z = f"z{str(i).zfill(2)}"
    x_prev = f"x{str(i-1).zfill(2)}"
    y_prev = f"y{str(i-1).zfill(2)}"
    x_next = f"x{str(i+1).zfill(2)}"
    y_next = f"y{str(i+1).zfill(2)}"
    z_next = f"z{str(i+1).zfill(2)}"

    # Rule 1: Check XOR gates
    xor1i = find_gate(x, y, "XOR")
    xandy = find_gate(x, y, "AND")

    if xor1i:
        for gate in gates:
            if (xor1i.output in [gate.gate_1, gate.gate_2]):
                if gate.op == "XOR":
                    if gate.output != z:
                        print(f"Adding {gate.output} because xor1i: {xor1i} -> {gate} should go to {z}")
                        other_gate = gate.gate_1 if gate.gate_2 == xor1i.output else gate.gate_2
                        # print(f"Other gate should be the carry in: {other_gate}")
                        # check if the carry in comes from an or gate
                        other_gate_source = gates_map[other_gate]
                        # print(f"Other gate: {other_gate_source}")
                        # print(f"Check backprop indexes: {gates_map[other_gate_source.gate_1]} {gates_map[other_gate_source.gate_2]}")
                        # looks good, so 
                        sus_gates[z] += 1
                        sus_gates[gate.output] += 1
                elif gate.op == "AND":
                    # make sure it goes into an OR gate, the carry gate
                    print("This exists AHHH")
                    carry_next = find_gate(gate.output, xandy, "OR")
                    if not carry_next:
                        sus_gates[gate.output] += 1
                        print(f"Adding {gate.output} because xor1i: {xor1i} -> {gate} should go to an AND gate that goes to an OR gate")



    # Rule 2: Check carry chain
    if xandy:
        and_users = get_gates_using_output(xandy.output)
        if len(and_users) != 1:
            print(f"Adding {xandy.output} because {x} and {y}: {xandy} should only have one user, has {len(and_users)}")
            sus_gates[xandy.output] += 1
        else:
            for gate in and_users:
                if gate.op != "OR":
                    # suspect because the only thing and should feed into is or
                    print(f"Adding {gate.output} because {x} and {y} -> {xandy} should go to an OR gate")
                    sus_gates[gate.output] += 1

    

    # # Rule 3: Check OR gates in carry propagation
    # prev_carry = find_gate(x_prev, y_prev, "AND")
    # if prev_carry:
    #     or_gates = [g for g in gates if g.op == "OR" and 
    #                (prev_carry.output in [g.gate_1, g.gate_2] or 
    #                 xandy.output in [g.gate_1, g.gate_2])]
    #     for or_gate in or_gates:
    #         carry_users = get_gates_using_output(or_gate.output)
    #         if not any(g.output == z_next for g in carry_users if g.op == "XOR"):
    #             if z_next not in ["z06","z15","z23","z39"]:
    #                 sus_gates.add(or_gate.output)

    # # Rule 4: Check intermediate carry propagation
    # for gate in gates:
    #     if gate.op == "AND":
    #         if (gate.gate_1.startswith(('x', 'y')) and 
    #             gate.gate_2.startswith(('x', 'y'))):
    #             carry_users = get_gates_using_output(gate.output)
    #             if not any(g.op == "OR" or (g.op == "XOR" and g.output.startswith('z')) 
    #                       for g in carry_users):
    #                 sus_gates.add(gate.output)

    # Rule 5: Validate carry-save structure
    # if xor1i and xandy:
    #     carry_save_gates = [g for g in gates if g.op in ["XOR", "AND"] and 
    #                       xor1i.output in [g.gate_1, g.gate_2]]
    #     for gate in carry_save_gates:
    #         if not any(g.output.startswith('z') for g in get_gates_using_output(gate.output)):
    #             sus_gates.add(gate.output)

print(sus_gates)


print(",".join(sorted(list(sus_gates))))