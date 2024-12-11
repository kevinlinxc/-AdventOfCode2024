import fileinput
from collections import defaultdict
from copy import deepcopy


lines = [line.strip() for line in fileinput.input(files="inputs/11.txt")]


def blink(sequence: dict[int:int]):
    new_frequency = deepcopy(sequence)
    for item in sequence.keys():
        frequency = sequence[item]
        new_frequency[item] -= frequency
        print("Checking item", item)
        if new_frequency[item] == 0:
            del new_frequency[item]
        if int(item) == 0:
            print("Is 0")
            new_frequency[1] += frequency
        elif len(str(item)) % 2 == 0:
            print("Splitting")
            # split it into left and right
            left = str(item)[: len(str(item)) // 2]
            right = str(item)[len(str(item)) // 2 :]
            new_frequency[int(left)] += frequency
            new_frequency[int(right)] += frequency
        else:
            print("Multiplying")
            new_frequency[int(item) * 2024] += frequency

    return new_frequency


start_list = lines[0].split(" ")
frequency = defaultdict(int)
for item in start_list:
    frequency[int(item)] += 1

for i in range(75):
    print(i)

    frequency = blink(frequency)

total = 0
for key in frequency.keys():
    total += frequency[key]
print(total)
