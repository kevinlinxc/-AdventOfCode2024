import fileinput
from collections import defaultdict

lines = [line.strip() for line in fileinput.input(files="inputs/8.txt")]

antenna_locations = defaultdict(list)

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char != ".":
            antenna_locations[char[0]].append((x, y))


print(antenna_locations)


def check_spot(x, y):
    if 0 <= x < len(lines[0]) and 0 <= y < len(lines):
        return True


possible_antinodes = set()
for key in antenna_locations:
    # find all the antinodes created by every pair of antennas
    for i in range(len(antenna_locations[key])):
        for j in range(i + 1, len(antenna_locations[key])):
            x1, y1 = antenna_locations[key][i]
            x2, y2 = antenna_locations[key][j]

            dx = x2 - x1
            dy = y2 - y1

            spot_1 = (x1 - dx, y1 - dy)
            spot_2 = (x2 + dx, y2 + dy)
            if check_spot(*spot_1):
                possible_antinodes.add(spot_1)
            if check_spot(*spot_2):
                possible_antinodes.add(spot_2)

print(possible_antinodes)
print(len(possible_antinodes))


def draw_antinodes():
    for x, y in possible_antinodes:
        lines[y] = lines[y][:x] + "#" + lines[y][x + 1 :]
    for line in lines:
        print(line)


draw_antinodes()
