import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/23.txt")]

"""
Each line of text in the network map represents a single connection; the line kh-tc represents a connection between the computer named kh and the computer named tc. Connections aren't directional; tc-kh would mean exactly the same thing.

LAN parties typically involve multiplayer games, so maybe you can locate it by finding groups of connected computers. Start by looking for sets of three computers where each computer in the set is connected to the other two computers.

In this example, there are 12 such sets of three inter-connected computers:

aq,cg,yn
aq,vc,wq
co,de,ka
co,de,ta
co,ka,ta
de,ka,ta
kh,qp,ub
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
ub,vc,wq

If the Chief Historian is here, and he's at the LAN party, it would be best to know that right away. You're pretty sure his computer's name starts with t, so consider only sets of three computers where at least one computer's name starts with t. That narrows the list down to 7 sets of three inter-connected computers:

co,de,ta
co,ka,ta
de,ka,ta
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn

Find all the sets of three inter-connected computers. How many contain at least one computer with a name that starts with t?
"""
from collections import defaultdict

connections = defaultdict(set)
all_computers = set()
for line in lines:
    a, b = line.split("-")
    a = a.strip()
    b = b.strip()
    connections[a].add(b)
    connections[b].add(a)
    all_computers.add(a)
    all_computers.add(b)

triple_sets = set()
for computer in all_computers:
    for computer2 in all_computers - set(computer):
        for computer3 in all_computers - set(computer) - set(computer2):
            if (
                computer2 in connections[computer]
                and computer3 in connections[computer]
                and computer3 in connections[computer2]
            ):
                triple_sets.add(tuple(sorted([computer, computer2, computer3])))
print(triple_sets)

total_triple_sets_with_t = 0
for triple_set in triple_sets:
    if any([computer.startswith("t") for computer in triple_set]):
        total_triple_sets_with_t += 1
print(total_triple_sets_with_t)
