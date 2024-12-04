import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/4.txt")]

# find every instance of xmas
width = len(lines[0])
height = len(lines)


def how_many_xmas_from_x(lines, x, y):
    """
    Assumes there is an "X" at x, y
    Check all directions for "XMAS"

    :param x:
    :param y:
    :return:
    """
    print(f"Checking at {x}, {y}")
    correct_xmas = 0
    if x - 3 >= 0:
        # can check left
        if lines[y][x - 1] == "M" and lines[y][x - 2] == "A" and lines[y][x - 3] == "S":
            correct_xmas += 1
        if y - 3 >= 0:
            # can check top left
            if (
                lines[y - 1][x - 1] == "M"
                and lines[y - 2][x - 2] == "A"
                and lines[y - 3][x - 3] == "S"
            ):
                correct_xmas += 1
        if y + 3 < height:
            # can check bottom left
            if (
                lines[y + 1][x - 1] == "M"
                and lines[y + 2][x - 2] == "A"
                and lines[y + 3][x - 3] == "S"
            ):
                correct_xmas += 1
    if x + 3 < width:
        # can check right
        if lines[y][x + 1] == "M" and lines[y][x + 2] == "A" and lines[y][x + 3] == "S":
            correct_xmas += 1
        if y - 3 >= 0:
            # can check top right
            if (
                lines[y - 1][x + 1] == "M"
                and lines[y - 2][x + 2] == "A"
                and lines[y - 3][x + 3] == "S"
            ):
                correct_xmas += 1
        if y + 3 < height:
            # can check bottom right
            if (
                lines[y + 1][x + 1] == "M"
                and lines[y + 2][x + 2] == "A"
                and lines[y + 3][x + 3] == "S"
            ):
                correct_xmas += 1
    if y - 3 >= 0:
        # can check top
        if lines[y - 1][x] == "M" and lines[y - 2][x] == "A" and lines[y - 3][x] == "S":
            correct_xmas += 1
    if y + 3 < height:
        # can check bottom
        if lines[y + 1][x] == "M" and lines[y + 2][x] == "A" and lines[y + 3][x] == "S":
            correct_xmas += 1
    return correct_xmas


total_xmas = 0

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "X":
            total_xmas += how_many_xmas_from_x(lines, x, y)

print(total_xmas)
