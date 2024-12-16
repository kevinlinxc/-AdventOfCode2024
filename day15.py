import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/15.txt")]


map = {}
moves = []
moves_flag = False

robot_x = 0
robot_y = 0

for y, line in enumerate(lines):
    for x, item in enumerate(line):
        if moves_flag:
            moves.append(item)
        else:
            if item == "@":
                robot_x = x
                robot_y = y
            map[(x, y)] = item
    if line == "":
        moves_flag = True
        continue


def calculate_gps_sum(map):
    sum = 0
    for key in map:
        if map[key] == "O":
            x, y = key
            sum += 100 * y + x
    return sum


# do every move, if the robot would hit a box, see if it can move it


def move_robot(map, robot_x, robot_y, move):
    diffs = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

    x, y = robot_x, robot_y
    new_x, new_y = x + diffs[move][0], y + diffs[move][1]
    occupant = map[(new_x, new_y)]
    if occupant == ".":
        # can easily move, move there
        map[(x, y)] = "."
        map[(new_x, new_y)] = "@"
        return new_x, new_y
    elif occupant == "#":
        # easy, can't move
        return x, y
    elif occupant == "O":

        # box exists, see if we can move
        to_move = [(new_x, new_y)]
        check_x = new_x
        check_y = new_y
        while True:
            check_x += diffs[move][0]
            check_y += diffs[move][1]
            occupant = map[(check_x, check_y)]
            if occupant == ".":
                can_move = True
                break
            elif occupant == "#":
                can_move = False
                break
            else:
                # box
                to_move.append((check_x, check_y))
        if can_move:
            for box in to_move:
                map[box[0] + diffs[move][0], box[1] + diffs[move][1]] = "O"
            map[(new_x, new_y)] = "@"
            map[(x, y)] = "."
            return new_x, new_y
        else:
            return x, y


for move in moves:
    robot_x, robot_y = move_robot(map, robot_x, robot_y, move)

print(calculate_gps_sum(map))
