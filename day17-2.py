list = [2, 4, 1, 1, 7, 5, 0, 3, 4, 3, 1, 6, 5, 5, 3, 0]


def get_output(register_a_value, register_b_value, register_c_value, program):
    instruction_index = 0
    output = []
    while True:
        try:
            operation = program[instruction_index]
        except IndexError:
            break
        operand = program[instruction_index + 1]
        literal_operand = operand
        try:
            combo_operand = (
                operand
                if operand <= 3
                else [register_a_value, register_b_value, register_c_value][operand - 4]
            )
        except KeyError:
            print("KeyError: ", operand + "should be 7")
            break
        if operation == 0:
            # division
            # print(f"a = a // {2 ** combo_operand}")
            register_a_value = register_a_value // (2**combo_operand)
        elif operation == 1:
            # bitwise XOR
            # print(f"b = b ^ {literal_operand}")
            register_b_value = register_b_value ^ literal_operand
        elif operation == 2:
            # print(f"b = A % 8")
            register_b_value = combo_operand % 8
        elif operation == 3:
            if not register_a_value == 0:
                instruction_index = literal_operand
                continue
        elif operation == 4:
            # print(f"b = b ^ c")
            register_b_value = register_b_value ^ register_c_value

        elif operation == 5:
            # print(f"output B % 8)")
            output.append(combo_operand % 8)

        elif operation == 6:
            # print(f"b = a // {2 ** combo_operand}")
            register_b_value = register_a_value // (2**combo_operand)
        elif operation == 7:
            # print(f"c = a // ?2 ** b")
            register_c_value = register_a_value // (2**combo_operand)
        instruction_index += 2
    return output


works = [0]
# the program just takes the last octal bit/ the last 3 bits and then does shit to it. S
# o, work 3 bits at a time and build a solution. Sometimes there's multiple solutions so on the nth iteration
# check all things that worked for the n-1th
for output in list[::-1]:
    print("output", output)
    next_works = []
    for option in works:
        for i in range(8):
            candidate = option * 8 + i
            print("candidate", candidate)

            # see if the output results in output
            b = candidate % 8  # get last three digits
            b = b ^ 1  # flip last one
            c = (
                candidate // 2**b
            )  # shift a right by last 3 digits with flipped last one
            a = candidate // 8  # shift right by 3 digits

            b = b ^ c  # flip c digits
            b = b ^ 6  # flip 2 out of 3 digits
            if b % 8 == output:  # check last 3 digits
                next_works.append(candidate)
    works = next_works
print(works)
print(min(works))


print(get_output(min(works), 0, 0, list))
