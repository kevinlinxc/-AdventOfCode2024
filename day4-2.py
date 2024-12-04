import fileinput
from collections import defaultdict

lines = [line.strip() for line in fileinput.input(files="inputs/4.txt")]

# find every instance of xmas
width = len(lines[0])
height = len(lines)
print(width, height)


def is_xmas_at_a(lines, x, y):
    """
    Assumes there is an "X" at x, y
    Check all directions for "XMAS"

    :param x:
    :param y:
    :return:
    """
    # print(f"Checking at {x}, {y}")
    if x == 0 or x == width - 1 or y == 0 or y == height - 1:
        return 0
    freq = defaultdict(int)
    top_left = lines[y - 1][x - 1]
    top_right = lines[y - 1][x + 1]
    bottom_left = lines[y + 1][x - 1]
    bottom_right = lines[y + 1][x + 1]
    freq[top_left] += 1
    freq[top_right] += 1
    freq[bottom_left] += 1
    freq[bottom_right] += 1
    if freq["M"] == 2 and freq["S"] == 2 and top_left != bottom_right:
        print(f"Found at {x}, {y}:")
        print(
            f"""
{top_left}.{top_right}
.A.
{bottom_left}.{bottom_right}
        """
        )
        return 1
    return 0


total_xmas = 0

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "A":
            total_xmas += is_xmas_at_a(lines, x, y)

print(total_xmas)
