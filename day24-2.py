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



def get_dec_number(cache_, letter="z"):
    output = ""
    for key in sorted(cache_.keys()):
        if letter in key:
            output =  str(cache_[key]) + output

    return int(output, 2)



# print(gates)
# print(cache)
# print(get_dec_number(cache, "x"))
# print(get_dec_number(cache, "y"))
# expected = get_dec_number(cache,"x") + get_dec_number(cache, "y")
# print(f"Expected = {expected}")



# half adder for 0
# there should be x0 xor y0 = s0 and x0 and y0 = z1
assert gates_map["z00"].gate_1 == "x00" and gates_map["z00"].gate_2 == "y00" and gates_map["z00"].op == "XOR"
# carry one should come from x0 and y0 = z1
# carry_bit = related_gates['x00'][0].output

#carry_bit_0 and  a1 xor b1 should get xord to get s1
print(gates_map["z01"])
a1xorb1 = related_gates['x01'][0].output
# assert gates_map["z01"].gate_1 == carry_bit_0 and gates_map["z01"].gate_2 == "x01" and gates_map["z01"].op == "XOR"
#half adder seems ok

def find_gate(input1, input2, operation):
    for gate in gates:
        if gate.gate_1 in [input1, input2 ]and gate.gate_2 in [input1, input2] and gate.op == operation:
            return gate
            
    return None

sus_gates = set()
for i in range(1, 44):


    x = "x" + f"{str(i).zfill(2)}"
    y = "y" + f"{str(i).zfill(2)}"
    z = "z" + f"{str(i).zfill(2)}"
    x_next = "x" + f"{str(i+1).zfill(2)}"
    y_next = "y" + f"{str(i+1).zfill(2)}"
    z_next = "z" + f"{str(i+1).zfill(2)}"
    i_top_bit = None
    # find z gate with xor
    cand1 = None
    cand2 = None
    for gate in gates:
        if gate.output == z and gate.op == "XOR":
            # print(f"{z} comes from {gate}")
            cand_1 = gate.gate_1
            cand_2 = gate.gate_2
    
    # one of cand_1, cand_2 should come from xi xor yi
    xor1i = find_gate(x, y, "XOR")
    # find gate that takes xor1 as input and is xor, its output maybe is wrong
    for gate in gates:
        if (xor1i.output in [gate.gate_1, gate.gate_2]) and gate.op == "XOR":
            if gate.output != z:
                print(f"Gate {gate} takes {xor1i.output} as input but doesn't output z, output {gate.output} is sus")
                if z in ["z06","z15","z23","z39"]:
                    print("Ignoring because the z is probably wrong")
                else:
                    sus_gates.add(gate.output)

    if xor1i.output not in [cand_1, cand_2]:
        print(f"Gate {z} is sus because it doesn't have the right XOR gate: {xor1i} not in {[cand1, cand2]}!")
        sus_gates.add(z)
    
    # find the gate thats x and y
    xandy = find_gate(x, y, "AND").output
    # this should be used only for the carry out gate
    for gate in gates:
        if gate.gate_1 == xandy or gate.gate_2 == xandy:
            next_carry_bit = gate.output
    # next carry bit should be used in the next gate's sum
    next_xor1 = find_gate(x_next, y_next, "XOR").output
    next_other_xor2 = find_gate(next_carry_bit, next_xor1, "XOR")
    if not next_other_xor2 or next_other_xor2.output != z_next:
        print(f"Gate {next_carry_bit} is sus because its a carry bit and doesn't lead into {z_next}!")
        if z_next in ["z06","z15","z23","z39"]:
            print("Ignoring because the z is probably wrong")
        else:
            sus_gates.add(next_carry_bit)
    


    # output_gate_z = gates_map[z]
    # if carry_bit not in [output_gate_z.gate_1, output_gate_z.gate_2]:
    #     print(f"Gate {output_gate_z} is sus because it doesn't have the last carry bit: {carry_bit}!")

    # i_top_bit = find_gate(x, y, "XOR").output
    # i_middle_bit = find_gate(x, y, "AND").output
    # # i_bot_bit = find_gate(i_top_bit, carry_bit, "AND").output
    # print(f"Index {i} has intermediate bits {i_top_bit}, {i_middle_bit}, ")
    

    # # find the gates connected to x and y
    # # see if the don't  match the ones connected to z
    # x_gates = [gate for gate in gates if gate.gate_1 == x or gate.gate_2 == x]
    # y_gates = [gate for gate in gates if gate.gate_1 == y or gate.gate_2 == y]
    # z_gates = [gate for gate in gates if gate.output == z]
    # print(x_gates, y_gates, z_gates)
    # input()

print(",".join(sorted(list(sus_gates))))
    


