import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/9.txt")]

line = lines[0]
print(len(line))

memory = []

for i, val in enumerate(line):
    # undensify from files and free space into uncompressed
    num = int(val)
    index = i // 2
    if i % 2 == 0:
        memory.extend([index] * num)
    else:
        memory.extend(["."] * num)


# compress all the memory from the right to the left:

right_pointer = len(memory) - 1
left_pointer = 0
print(f"Uncompressed memory: {memory}")
print("Compressing")
while right_pointer > left_pointer:
    print(f"left_pointer: {left_pointer}, right_pointer: {right_pointer}")
    while memory[left_pointer] != ".":
        print(f"left_pointer: {left_pointer}, right_pointer: {right_pointer}")

        left_pointer += 1
    while memory[right_pointer] == "." and right_pointer > left_pointer:
        print(f"left_pointer: {left_pointer}, right_pointer: {right_pointer}")

        right_pointer -= 1
    # swap
    memory[left_pointer], memory[right_pointer] = (
        memory[right_pointer],
        memory[left_pointer],
    )

print(memory)

final_sum = 0
for index, val in enumerate(memory):
    if val != ".":
        final_sum += index * val
print(final_sum)
