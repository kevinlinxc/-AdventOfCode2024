import fileinput
from enum import Enum

map = [line.strip() for line in fileinput.input(files="inputs/6.txt")]


class GuardDirection(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


visited = set()

guard_direction = GuardDirection.UP
guard_position = (0, 0)
for x, row in enumerate(map):
    for y, cell in enumerate(row):
        if cell == "^":
            guard_position = (x, y)
            visited.add(guard_position)

while (
    guard_position[0] >= 0
    and guard_position[0] < len(map)
    and guard_position[1] >= 0
    and guard_position[1] < len(map[0])
):
    if guard_direction == GuardDirection.UP:
        next_pos = (guard_position[0] - 1, guard_position[1])
        if next_pos[0] < 0:
            break
        if map[next_pos[0]][next_pos[1]] == "#":
            guard_direction = GuardDirection.RIGHT
        else:
            guard_position = next_pos
            visited.add(next_pos)
    elif guard_direction == GuardDirection.RIGHT:
        next_pos = (guard_position[0], guard_position[1] + 1)
        if next_pos[1] >= len(map[0]):
            break
        if map[next_pos[0]][next_pos[1]] == "#":
            guard_direction = GuardDirection.DOWN
        else:
            guard_position = next_pos
            visited.add(next_pos)
    elif guard_direction == GuardDirection.DOWN:
        next_pos = (guard_position[0] + 1, guard_position[1])
        if next_pos[0] >= len(map):
            break
        if map[next_pos[0]][next_pos[1]] == "#":
            guard_direction = GuardDirection.LEFT
        else:
            guard_position = next_pos
            visited.add(next_pos)
    elif guard_direction == GuardDirection.LEFT:
        next_pos = (guard_position[0], guard_position[1] - 1)
        if next_pos[1] < 0:
            break
        if map[next_pos[0]][next_pos[1]] == "#":
            guard_direction = GuardDirection.UP
        else:
            guard_position = next_pos
            visited.add(next_pos)
print(len(visited))
