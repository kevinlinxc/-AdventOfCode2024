import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/14.txt")]


# each line is like p=98,87 v=80,2, get the position and velocity
# determine quadrant it'll be in after n moves
def simulate(position, velocity, n, game_width, game_height):
    for i in range(n):
        position[0] += velocity[0]
        position[1] += velocity[1]
        position[0] = position[0] % game_width
        position[1] = position[1] % game_height
    if position[0] == game_width // 2 or position[1] == game_height // 2:
        return 0
    elif position[0] < game_width // 2 and position[1] < game_height // 2:
        return 1
    elif position[0] > game_width // 2 and position[1] < game_height // 2:
        return 2
    elif position[0] > game_width // 2 and position[1] > game_height // 2:
        return 3
    else:
        return 4


quadrants = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
for line in lines:
    left, right = line.split(" v=")
    p = left.split("p=")[1]
    p_x, p_y = p.split(",")
    p_x, p_y = int(p_x), int(p_y)
    v = right.split(",")
    v_x = v[0]
    v_y = v[1]
    v_x, v_y = int(v_x), int(v_y)
    quadrant = simulate([p_x, p_y], [v_x, v_y], 100, 101, 103)
    quadrants[quadrant] += 1


print(quadrants)
print(quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4])
