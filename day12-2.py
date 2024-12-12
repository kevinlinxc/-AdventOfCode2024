import fileinput
from dataclasses import dataclass

lines = [line.strip() for line in fileinput.input(files="inputs/12.txt")]

# find all the regions by flood filling with the current character
visited = set()


@dataclass
class Region:
    letter: str
    area: int
    num_sides: int
    initial_x: int
    initial_y: int


def pretty_print_fences(fences: set):
    fences = set([(int(fence[0] * 4), int(fence[1] * 4)) for fence in fences])
    # print grid, if there's a fence somewhere make it #, otherwise .
    max_x = max(fence[0] for fence in fences)
    min_x = min(fence[0] for fence in fences)
    max_y = max(fence[1] for fence in fences)
    min_y = min(fence[1] for fence in fences)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in fences:
                print("#", end="")
            else:
                print(".", end="")
        print()


regions = []
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if (x, y) in visited:
            continue
        # flood fill
        stack = [(x, y)]
        visited.add((x, y))
        area = 1
        num_sides = 0
        fences = set()
        initial_x = x
        initial_y = y
        while stack:
            ix, iy = stack.pop(0)
            print("Visiting ", ix, iy)
            # right and left checks:
            for dx, dy in [(-1, 0), (1, 0)]:
                direciton = "left" if dx == -1 else "right"
                # print(f"Looking at {direciton} of {ix}, {iy}")
                new_x, new_y = ix + dx, iy
                if 0 <= new_x < len(line):
                    if (new_x, new_y) not in visited and lines[new_y][new_x] == char:
                        stack.append((new_x, new_y))
                        visited.add((new_x, new_y))
                        area += 1
                    elif lines[new_y][new_x] != char:
                        fence_x = new_x + dx / 4
                        fence = (fence_x, iy)
                        print(f"Adding fence to the {direciton} of {new_x, new_y}")
                        fences.add(fence)
                        # top or bottom have a fence, then this is not a new side, add to side counter
                        if not (
                            (fence_x, iy + 1) in fences or (fence_x, iy - 1) in fences
                        ):
                            print(
                                f"Adding side {num_sides} to {'left' if dx == -1 else 'right'} of {ix}, {iy} "
                            )

                            num_sides += 1
                else:  # out of bounds, add a fence too:
                    fence_x = new_x + dx / 4
                    fence = (fence_x, iy)
                    print(f"Adding fence to the {direciton} of {new_x, new_y}")

                    fences.add(fence)
                    if not (
                        (fence_x, fence[1] + 1) in fences
                        or (fence_x, fence[1] - 1) in fences
                    ):
                        print(
                            f"Adding side {num_sides} to {'left' if dx == -1 else 'right'} of {ix}, {iy} "
                        )
                        num_sides += 1
            # up and down checks:
            for dx, dy in [(0, 1), (0, -1)]:
                direciton = "up" if dy == -1 else "down"
                # print(f"Looking at {direciton} of {ix}, {iy}")
                new_x, new_y = ix, iy + dy
                if 0 <= new_y < len(lines):
                    if (new_x, new_y) not in visited and lines[new_y][new_x] == char:
                        stack.append((new_x, new_y))
                        visited.add((new_x, new_y))
                        area += 1
                    elif lines[new_y][new_x] != char:
                        fence_y = new_y + dy / 4
                        fence = (ix, fence_y)
                        fences.add(fence)
                        print(f"Adding fence to the {direciton} of {new_x, new_y}")
                        if not (
                            (fence[0] + 1, fence_y) in fences
                            or (fence[0] - 1, fence_y) in fences
                        ):
                            print(
                                f"Adding side {num_sides} to {'top' if dy == -1 else 'bottom'} of {ix}, {iy} "
                            )
                            num_sides += 1
                else:
                    fence_y = new_y + dy / 4
                    fence = (ix, fence_y)
                    print(f"Adding fence to the {direciton} of {new_x, new_y}")

                    fences.add(fence)
                    if not (
                        (fence[0] + 1, fence_y) in fences
                        or (fence[0] - 1, fence_y) in fences
                    ):
                        print(
                            f"Adding side {num_sides} to {'top' if dy == -1 else 'bottom'} of {ix}, {iy} "
                        )

                        num_sides += 1
        regions.append(Region(char, area, num_sides, initial_x, initial_y))

total = 0
for region in regions:
    print(
        f"Region {region.letter}, area: {region.area}, num_sides: {region.num_sides}, {region.initial_x}, {region.initial_y}"
    )
    total += region.area * region.num_sides
print(total)
