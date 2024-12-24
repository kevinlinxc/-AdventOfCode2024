import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/24.txt")]


cache = {}
gates = []
gates_now = False
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
    
    def can_evaluate(self):
        return self.gate_1 in cache and self.gate_2 in cache
    
    def evaluate(self):
        print(f"Evaluating  {self.output} = {cache[self.gate_1]} {self.op} {cache[self.gate_2]}", end="")
        if self.op == "AND":
            cache[self.output] = cache[self.gate_1] & cache[self.gate_2]
        elif self.op == "XOR":
            cache[self.output] = cache[self.gate_1] ^ cache[self.gate_2]
        elif self.op == "OR":
            cache[self.output] = cache[self.gate_1] | cache[self.gate_2]
        print(f" = {cache[self.output]}")

for line in lines:
    if line == "":
        gates_now = True
        continue
    if gates_now:
        gates.append(Gate(line))
    else:
        name, value = line.split(": ")
        cache[name] = int(value)

print(gates)
print(cache)
while len(gates) > 0:
    can_evaluate = []
    for gate in gates:
        if gate.can_evaluate():
            can_evaluate.append(gate)
    for gate in can_evaluate:
        print(f"Evaluating {gate}")
        gate.evaluate()
        gates.remove(gate)
    print("Round done AAA")

output = ""
for key in sorted(cache.keys()):
    if "z" in key:
        print(key, cache[key])
        output =  str(cache[key]) + output


# evaluate binary to decimal
print(int(output, 2))