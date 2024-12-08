import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/7.txt")]


def recursive_check(target, operands, operator):
    if len(operands) == 2:
        if operator == "*":
            return operands[0] * operands[1] == target
        else:
            return operands[0] + operands[1] == target
    # more than 2 operands, go down the two cases
    first_two = operands[:2]
    if operator == "*":
        result = first_two[0] * first_two[1]
    else:
        result = first_two[0] + first_two[1]

    return recursive_check(target, [result] + operands[2:], "*") or recursive_check(
        target, [result] + operands[2:], "+"
    )


def can_reach_target(target, operands):
    # function that checks if adding + or * between operands can reach target
    return recursive_check(target, operands, "*") or recursive_check(
        target, operands, "+"
    )


sum_of_possible = 0
for line in lines:
    before, after = line.split(":")
    target = int(before)
    operands = [int(x) for x in after.split()]
    print(f"Trying to reach {target} with {operands}")
    if can_reach_target(target, operands):
        print("operands can reach target")
        sum_of_possible += target
    else:
        print("operands cannot reach target")

print(sum_of_possible)
