import fileinput
from itertools import combinations

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

There are still way too many results to go through them all. You'll have to find the LAN party another way and go there yourself.

Since it doesn't seem like any employees are around, you figure they must all be at the LAN party. If that's true, the LAN party will be the largest set of computers that are all connected to each other. That is, for each computer at the LAN party, that computer will have a connection to every other computer at the LAN party.

In the above example, the largest set of computers that are all connected to each other is made up of co, de, ka, and ta. Each computer in this set has a connection to every other computer in the set:

ka-co
ta-co
de-co
ta-ka
de-ta
ka-de

The LAN party posters say that the password to get into the LAN party is the name of every computer at the LAN party, sorted alphabetically, then joined together with commas. (The people running the LAN party are clearly a bunch of nerds.) In this example, the password would be co,de,ka,ta.

What is the password to get into the LAN party?
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

# find the biggest island of connected computers

# print the computer with the most connections
max_connections = 0
max_computer = None
for computer in all_computers:
    if len(connections[computer]) > max_connections:
        max_connections = len(connections[computer])
        max_computer = computer
print(max_computer, max_connections)

# iterate over all the connections of the computer with the most connections, see if they are all connected to each other
# if they are, print them


def all_connected(computers):
    for computer in set(computers):
        for other in computers - {computer}:
            if other not in connections[computer]:
                return False
    # print("All connected:", computers)
    return True


print(connections)
max_connected = 0
password = ""
for computer in all_computers:
    connection_count = len(connections[computer])
    for combination_size in range(connection_count, 1, -1):
        # import pdb; pdb.set_trace()
        all_computers = connections[computer].union({computer})
        # print(f"Checking {computer} with {all_computers}, combination size: {combination_size}")
        for combination in combinations(all_computers, combination_size):
            # print(f"Checking combination: {sorted(combination)}")
            if all_connected(set(combination)):
                num_connected = len(combination)
                if num_connected > max_connected:
                    max_connected = num_connected
                    print(f"New max: {max_connected}")
                    print(f"Password: {','.join(sorted(combination))}")
                    password = ",".join(sorted(combination))
print(password)
