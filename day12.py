import fileinput
from dataclasses import dataclass

lines = [line.strip() for line in fileinput.input(files="inputs/12.txt")]

# find all the regions by flood filling with the current character
visited = set()


@dataclass
class Region:
    letter: str
    area: int
    perimeter: int
    initial_x: int
    initial_y: int


regions = []
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if (x, y) in visited:
            continue
        # flood fill
        stack = [(x, y)]
        visited.add((x, y))
        area = 1
        perimeter = 0
        initial_x = x
        initial_y = y
        while stack:
            ix, iy = stack.pop()
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x, new_y = ix + dx, iy + dy
                if 0 <= new_x < len(line) and 0 <= new_y < len(lines):
                    if (new_x, new_y) not in visited and lines[new_y][new_x] == char:
                        stack.append((new_x, new_y))
                        visited.add((new_x, new_y))
                        area += 1
                    elif lines[new_y][new_x] != char:
                        perimeter += 1
                else:
                    perimeter += 1
        regions.append(Region(char, area, perimeter, initial_x, initial_y))

total = 0
for region in regions:
    print(
        f"Region {region.letter}, area: {region.area}, perimeter: {region.perimeter}, {region.initial_x}, {region.initial_y}"
    )
    total += region.area * region.perimeter
print(total)
