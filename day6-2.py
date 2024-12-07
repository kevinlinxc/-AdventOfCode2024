import fileinput
from enum import Enum
from copy import deepcopy

map = [line.strip() for line in fileinput.input(files="inputs/6.txt")]


def pretty_print(map):
    for row in map:
        print(row)


class GuardDirection(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


guard_position = (0, 0)
for y, row in enumerate(map):
    for x, cell in enumerate(row):
        if cell == "^":
            guard_position = (x, y)


starting_guard_position = guard_position
num_good_obtruction_locations = 0


def causes_loop(map):
    # print("Checking map:")
    # pretty_print(map)
    # print("\n")
    guard_position = starting_guard_position
    guard_direction = GuardDirection.UP
    visited = set()
    path = []
    visited.add(starting_guard_position)
    path.append(starting_guard_position)
    # print(f"Start {visited}")
    while True:
        if guard_direction == GuardDirection.UP:
            next_pos = (guard_position[0], guard_position[1] - 1)
            if next_pos[1] < 0:
                break
            if map[next_pos[1]][next_pos[0]] in ["#", "O"]:
                guard_direction = GuardDirection.RIGHT
            else:
                if next_pos in visited:
                    # print(f"Already visited {next_pos} in {visited}")
                    # check if our previous position on the path was the same as the one before the index where next_pos first appeared in path
                    index_of_next_pos = path.index(next_pos)
                    if (
                        path[-1] == path[index_of_next_pos - 1]
                        and index_of_next_pos > 0
                    ):
                        # print(f"Loop found! {path[-1]} -> {next_pos} == {path[index_of_next_pos - 1]} -> {path[index_of_next_pos]}, {path=}, {index_of_next_pos=}")
                        return True
                guard_position = next_pos
                # print("Moving to ", guard_position)
                visited.add(next_pos)
                path.append(next_pos)
        elif guard_direction == GuardDirection.RIGHT:
            next_pos = (guard_position[0] + 1, guard_position[1])
            if next_pos[0] >= len(map[0]):
                break
            if map[next_pos[1]][next_pos[0]] in ["#", "O"]:
                guard_direction = GuardDirection.DOWN
            else:
                if next_pos in visited:
                    # print(f"Already visited {next_pos} in {visited}")
                    # check if our previous position on the path was the same as the one before the index where next_pos first appeared in path
                    index_of_next_pos = path.index(next_pos)
                    if (
                        path[-1] == path[index_of_next_pos - 1]
                        and index_of_next_pos > 0
                    ):
                        # print(f"Loop found! {path[-1]} -> {next_pos} == {path[index_of_next_pos - 1]} -> {path[index_of_next_pos]}, {path=}, {index_of_next_pos=}")
                        return True
                guard_position = next_pos
                # print("Moving to ", guard_position)
                visited.add(next_pos)
                path.append(next_pos)
        elif guard_direction == GuardDirection.DOWN:
            next_pos = (guard_position[0], guard_position[1] + 1)
            if next_pos[1] >= len(map):
                break
            if map[next_pos[1]][next_pos[0]] in ["#", "O"]:
                guard_direction = GuardDirection.LEFT
            else:
                if next_pos in visited:
                    # print(f"Already visited {next_pos} in {visited}")
                    # check if our previous position on the path was the same as the one before the index where next_pos first appeared in path
                    index_of_next_pos = path.index(next_pos)
                    if (
                        path[-1] == path[index_of_next_pos - 1]
                        and index_of_next_pos > 0
                    ):
                        # print(f"Loop found! {path[-1]} -> {next_pos} == {path[index_of_next_pos - 1]} -> {path[index_of_next_pos]}, {path=}, {index_of_next_pos=}")
                        return True

                guard_position = next_pos
                # print("Moving to ", guard_position)
                visited.add(next_pos)
                path.append(next_pos)
        elif guard_direction == GuardDirection.LEFT:
            next_pos = (guard_position[0] - 1, guard_position[1])
            if next_pos[0] < 0:
                break
            if map[next_pos[1]][next_pos[0]] in ["#", "O"]:
                guard_direction = GuardDirection.UP
            else:
                if next_pos in visited:
                    # print(f"Already visited {next_pos} in {visited}")
                    # check if our previous position on the path was the same as the one before the index where next_pos first appeared in path
                    index_of_next_pos = path.index(next_pos)
                    if (
                        path[-1] == path[index_of_next_pos - 1]
                        and index_of_next_pos > 0
                    ):
                        # print(f"Loop found! {path[-1]} -> {next_pos} == {path[index_of_next_pos - 1]} -> {path[index_of_next_pos]}, {path=}, {index_of_next_pos=}")
                        return True
                guard_position = next_pos
                # print("Moving to ", guard_position)
                visited.add(next_pos)
                path.append(next_pos)
    # print(f"No loop found!\n")
    return False


loop_causers = []
for y, row in enumerate(map):
    for x, cell in enumerate(row):
        print(f"Checking {x}, {y}")
        map_copy = deepcopy(map)
        if map_copy[y][x] == ".":
            # replace the y th row with a row where the xth column is a #
            original = map_copy[y]
            map_copy[y] = original[:x] + "O" + original[x + 1 :]
        else:
            continue
        # print(f"Checking map {x}, {y}")
        if causes_loop(map_copy):
            print(f"{x}, {y}, causes loop")
            num_good_obtruction_locations += 1
            loop_causers.append((x, y))


print(num_good_obtruction_locations)
print(f"{loop_causers}")
