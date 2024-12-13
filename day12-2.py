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


def get_num_sides_from_fences(fences: set):

    vertical_fences = set()
    horizontal_fences = set()
    for fence in fences:
        if fence[0] % 1 != 0:
            vertical_fences.add(fence)
        else:
            horizontal_fences.add(fence)
    # sort them so we can't possibly consider them incorrectly?
    vertical_fences = sorted(list(vertical_fences))
    horizontal_fences = sorted(list(horizontal_fences))
    visited_vertical = set()
    num_sides = 0
    for vertical_fence in vertical_fences:
        # get top and bottom, if neither are in visited, add a side
        top = (vertical_fence[0], vertical_fence[1] - 1)
        bottom = (vertical_fence[0], vertical_fence[1] + 1)
        if top not in visited_vertical and bottom not in visited_vertical:
            num_sides += 1
        visited_vertical.add(vertical_fence)
    visited_horizontal = set()
    for horizontal_fence in horizontal_fences:
        # get left and right, if neither are in visited, add a side
        left = (horizontal_fence[0] - 1, horizontal_fence[1])
        right = (horizontal_fence[0] + 1, horizontal_fence[1])
        if left not in visited_horizontal and right not in visited_horizontal:
            num_sides += 1
        visited_horizontal.add(horizontal_fence)
    return num_sides


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
                else:  # out of bounds, add a fence too:
                    fence_x = new_x + dx / 4
                    fence = (fence_x, iy)
                    print(f"Adding fence to the {direciton} of {new_x, new_y}")

                    fences.add(fence)

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
                else:
                    fence_y = new_y + dy / 4
                    fence = (ix, fence_y)
                    print(f"Adding fence to the {direciton} of {new_x, new_y}")

                    fences.add(fence)
        num_sides = get_num_sides_from_fences(fences)
        regions.append(Region(char, area, num_sides, initial_x, initial_y))

total = 0
for region in regions:
    print(
        f"Region {region.letter}, area: {region.area}, num_sides: {region.num_sides}, {region.initial_x}, {region.initial_y}"
    )
    total += region.area * region.num_sides
print(total)
