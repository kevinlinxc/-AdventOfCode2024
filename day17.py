import fileinput

# The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.
#
# The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.
#
# The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.
#
# The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
#
# The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
#
# The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)
#
# The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)
#
# The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)
lines = [line.strip() for line in fileinput.input(files="inputs/17.txt")]

# e.g. Register A: 18427963
register_a_value = int(lines[0].split(":")[1].strip())
register_b_value = int(lines[1].split(":")[1].strip())
register_c_value = int(lines[2].split(":")[1].strip())
# Program: 2,4,1,1,7,5,0,3,4,3,1,6,5,5,3,0

program = [int(x) for x in (lines[4].split(" ")[1]).split(",")]

print(program)

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

        register_a_value = register_a_value // (2**combo_operand)
    elif operation == 1:
        # bitwise XOR
        register_b_value = register_b_value ^ literal_operand
    elif operation == 2:
        register_b_value = combo_operand % 8
    elif operation == 3:
        if not register_a_value == 0:
            instruction_index = literal_operand
            continue
    elif operation == 4:
        register_b_value = register_b_value ^ register_c_value

    elif operation == 5:
        output.append(combo_operand % 8)

    elif operation == 6:
        register_b_value = register_a_value // (2**combo_operand)
    elif operation == 7:
        register_c_value = register_a_value // (2**combo_operand)
    instruction_index += 2

print(",".join([str(x) for x in output]))
