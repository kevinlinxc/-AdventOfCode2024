import fileinput
import numpy as np

lines = [line.strip() for line in fileinput.input(files="inputs/13.txt")]

a_cost = 3
b_cost = 1

# parse groups of lines like this:
"""
Button A: X+92, Y+24
Button B: X+13, Y+94
Prize: X=8901, Y=8574

"""
cost = 0
for i in range(len(lines[::4])):
    a_line = lines[i * 4]
    b_line = lines[i * 4 + 1]
    prize_line = lines[i * 4 + 2]

    a_x = int(a_line.split(",")[0].split("+")[1])
    a_y = int(a_line.split(",")[1].split("+")[1])
    b_x = int(b_line.split(",")[0].split("+")[1])
    b_y = int(b_line.split(",")[1].split("+")[1])
    prize_x = int(prize_line.split(",")[0].split("=")[1]) + 10000000000000
    prize_y = int(prize_line.split(",")[1].split("=")[1]) + 10000000000000
    # calculate linear combination of [ a_x, a_y ] and [ b_x, b_y ] to get [ prize_x, prize_y ]
    two_by_two = np.array([[a_x, b_x], [a_y, b_y]])
    result = np.array([prize_x, prize_y])
    try:
        solution = np.linalg.solve(two_by_two, result)

    except np.linalg.LinAlgError:
        print("No solution")
        continue
    if (
        abs(float(round(solution[0])) - solution[0]) < 0.001
        and abs(float(round(solution[1])) - solution[1]) < 0.001
    ):
        a_count = round(solution[0])
        b_count = round(solution[1])
        print(f"Solution: {solution[0]}, {solution[1]}: YES")
        cost += a_count * a_cost + b_count * b_cost
    else:
        print(f"Solution: {solution[0]}, {solution[1]}: NO")
        # print(f"{abs(float(round(solution[0])) - solution[0])} > 0.00001 or {abs(float(round(solution[1])) - solution[1])} > 0.00001")
        continue

print(f"Total cost: {cost}")
