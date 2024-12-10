import fileinput
from dataclasses import dataclass

lines = [line.strip() for line in fileinput.input(files="inputs/9.txt")]

line = lines[0]
print(len(line))

# files are 0, 2, 4, 6
# free space is 1, 3, 5, 7
files = []
free_space = []


@dataclass
class File:
    index: int
    size: int
    address: int


@dataclass
class FreeSpace:
    size: int
    address: int


# calculate the starting memory:
memory = []

for i, val in enumerate(line):
    # undensify from files and free space into uncompressed
    num = int(val)
    index = i // 2
    if i % 2 == 0:
        start_address = len(memory)
        file = File(index, num, start_address)
        files.append(file)
        memory.extend([index] * num)

    else:
        start_address = len(memory)
        free = FreeSpace(num, start_address)
        free_space.append(free)
        memory.extend(["."] * num)

print(f"{memory=}")


print(f"{files=}")
print(f"{free_space=}")
# start at the last value of the line, work backwards skipping an index of free space


for file in files[::-1]:
    file_size = file.size
    # find earliest free space that can fit the file
    for free in free_space:
        if free.address > file.address:
            break  # don't modify the file location, no good location can be found
        if free.size >= file_size:
            # insert the file into the free space
            for i in range(file_size):
                memory[free.address + i] = file.index
            # delete the file from original position
            for i in range(file_size):
                memory[file.address + i] = "."
            # reduce the free space
            free.size -= file_size
            free.address += file_size
            break
        # if the file and free size are equal, insert the file and delete the free space

print(memory)

final_sum = 0
for index, val in enumerate(memory):
    if val != ".":
        final_sum += index * val
print(final_sum)
