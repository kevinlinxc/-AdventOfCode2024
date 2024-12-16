import fileinput
import time
from matplotlib import pyplot as plt
import numpy as np
import cv2

lines = [line.strip() for line in fileinput.input(files="inputs/14.txt")]

# each line is like p=98,87 v=80,2, get the position and velocity
# determine quadrant it'll be in after n moves


def move(position, velocity, game_width, game_height):
    position[0] += velocity[0]
    position[1] += velocity[1]
    position[0] = position[0] % game_width
    position[1] = position[1] % game_height
    return position


quadrants = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
robots = []
for line in lines:
    left, right = line.split(" v=")
    p = left.split("p=")[1]
    p_x, p_y = p.split(",")
    p_x, p_y = int(p_x), int(p_y)
    v = right.split(",")
    v_x = v[0]
    v_y = v[1]
    v_x, v_y = int(v_x), int(v_y)
    robots.append([p_x, p_y, v_x, v_y])


def pretty_print(robots):
    # grid of 101x103 dots, for each robot we increment the count of a dot by 1
    grid = [["." for _ in range(101)] for _ in range(103)]
    for robot in robots:
        spot = grid[robot[1]][robot[0]]
        if spot == ".":
            grid[robot[1]] = (
                grid[robot[1]][: robot[0]] + [1] + grid[robot[1]][robot[0] + 1 :]
            )
        else:
            grid[robot[1]] = (
                grid[robot[1]][: robot[0]]
                + [int(spot) + 1]
                + grid[robot[1]][robot[0] + 1 :]
            )
    for row in grid:
        print(row)


def save_robots_to_image(robots, filename):
    # make scatterplot with robot positions

    blank = np.ndarray((103, 101, 1), dtype=np.uint8)
    blank.fill(255)
    for robot in robots:
        blank[robot[1], robot[0]] = 0
    cv2.imwrite(filename, blank)


def get_quadrant_count(robots):
    quadrants = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    game_width = 101
    game_height = 103
    for robot in robots:
        position = [robot[0], robot[1]]
        if position[0] == game_width // 2 or position[1] == game_height // 2:
            quadrants[0] += 1
        elif position[0] < game_width // 2 and position[1] < game_height // 2:
            quadrants[1] += 1
        elif position[0] > game_width // 2 and position[1] < game_height // 2:
            quadrants[2] += 1
        elif position[0] > game_width // 2 and position[1] > game_height // 2:
            quadrants[3] += 1
        else:
            quadrants[4] += 1
    return quadrants


for i in range(10000):
    print(f"Time: {i}")
    robots_new = []
    for robot in robots:
        new_robot_x, new_robot_y = move(
            [robot[0], robot[1]], [robot[2], robot[3]], 101, 103
        )
        robots_new.append([new_robot_x, new_robot_y, robot[2], robot[3]])

    robots = robots_new
    save_robots_to_image(robots, f"images/{i}.png")
# just look through the manually and find the tree
