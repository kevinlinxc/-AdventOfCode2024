import fileinput
import cv2
import numpy as np
import tqdm

lines = [line.strip() for line in fileinput.input(files="inputs/15.txt")]


width = len(lines[0]) * 2

map = {}
moves = []
moves_flag = False

robot_x = 0
robot_y = 0

# double up everything
for y, line in enumerate(lines):
    for x, item in enumerate(line):
        if moves_flag:
            moves.append(item)
        else:
            if item == "@":
                robot_x = 2 * x
                robot_y = y
                map[(2 * x, y)] = "@"
                map[(2 * x + 1, y)] = "."
            elif item == ".":
                map[(2 * x, y)] = item
                map[(2 * x + 1, y)] = item
            elif item == "O":
                map[(2 * x, y)] = "["
                map[(2 * x + 1, y)] = "]"
            else:
                map[(2 * x, y)] = "#"
                map[(2 * x + 1, y)] = "#"
    if line == "":
        height = y
        moves_flag = True
        continue
print(f"height: {height}, width: {width}")


def map_to_image(map, file_number, next_move):
    filename = f"day15/{file_number}.png"
    # scale everything by 10
    blank = np.ndarray((height * 10, width * 10, 3), dtype=np.uint8)
    blank.fill(255)
    for key in map:
        x, y = key
        if map[key] == ".":
            blank[y * 10 : y * 10 + 10, x * 10 : x * 10 + 10] = (255, 255, 255)
        elif map[key] == "[" or map[key] == "]":
            blank[y * 10 : y * 10 + 10, x * 10 : x * 10 + 10] = [0, 255, 0]
        elif map[key] == "#":
            blank[y * 10 : y * 10 + 10, x * 10 : x * 10 + 10] = [255, 0, 0]
        elif map[key] == "@":
            blank[y * 10 : y * 10 + 10, x * 10 : x * 10 + 10] = [0, 0, 255]
            cv2.putText(
                blank,
                next_move,
                (x * 10, y * 10 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 0, 0),
                1,
            )
            cv2.putText(
                blank,
                str(file_number),
                (0, 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 255, 255),
                1,
            )
    cv2.imwrite(filename, blank)


def calculate_gps_sum(map):
    sum = 0
    for key in map:
        if map[key] == "[":
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
    elif occupant == "[" or occupant == "]":
        other_pos = (new_x + 1, new_y) if occupant == "[" else (new_x - 1, new_y)
        other = "]" if occupant == "[" else "["
        to_move = {(new_x, new_y): occupant, other_pos: other}
        check_x = new_x
        check_y = new_y
        if move == "<" or move == ">":
            # simpler, don't have cascading boxes
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
                    # box, [ or ]
                    to_move[(check_x, check_y)] = occupant
        else:
            # moving up or down, need to worry about cascading boxes
            columns_to_check = {new_x, other_pos[0]}
            while True:
                above = []
                check_y += diffs[move][1]
                for column in list(columns_to_check):
                    occupant = map[(column, check_y)]
                    if occupant == ".":
                        above.append(".")
                        columns_to_check.remove(column)
                    elif occupant == "#":
                        above.append("#")
                        break
                    else:
                        # box, [ or ]
                        above.append(occupant)
                        to_move[(column, check_y)] = occupant
                        if occupant == "[":
                            columns_to_check.add(column + 1)
                            to_move[(column + 1, check_y)] = "]"
                        else:
                            columns_to_check.add(column - 1)
                            to_move[(column - 1, check_y)] = "["
                if all([spot == "." for spot in above]):
                    can_move = True
                    break
                elif "#" in above:
                    can_move = False
                    break
                # otherwise we keep iterating

        if can_move:
            for box in list(to_move.keys()):
                occupant = to_move[box]
                map[(box[0] + diffs[move][0], box[1] + diffs[move][1])] = occupant
                if (box[0] - diffs[move][0], box[1] - diffs[move][1]) not in to_move:
                    map[(box[0], box[1])] = "."
            map[(new_x, new_y)] = "@"
            map[(x, y)] = "."
            return new_x, new_y
        else:
            return x, y
    else:
        print(f"wtf: {occupant}")


files = []
for i, move in enumerate(tqdm.tqdm(moves)):
    robot_x, robot_y = move_robot(map, robot_x, robot_y, move)

    map_to_image(map, i, moves[i + 1] if i + 1 < len(moves) else "END")
    files.append(f"day15/{i}.png")

# print(calculate_gps_sum(map))
video_writer = cv2.VideoWriter(
    "day15.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (width * 10, height * 10)
)
for file in files:
    image = cv2.imread(file)
    video_writer.write(image)
video_writer.release()
