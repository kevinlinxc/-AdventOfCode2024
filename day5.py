import fileinput
from collections import defaultdict

lines = [line.strip() for line in fileinput.input(files="inputs/5.txt")]

rules = []
sequences = []

rules_mode = True

for line in lines:
    if not bool(line):
        rules_mode = False
    else:
        if rules_mode:
            rules.append(line)
        else:
            sequences.append(line)

print(f"{len(rules)=}")
print(f"{len(sequences)=}")

less_than = defaultdict(set)
greater_than = defaultdict(set)

for rule in rules:
    left, right = rule.split("|")
    left, right = int(left), int(right)
    print(f"Adding rule: {left} < {right}")
    less_than[right].add(left)
    greater_than[left].add(right)


def check_two_numbers(a, b):
    if a in less_than[b] or b in greater_than[a]:
        return True
    return False


# iterate through each sequence, for each pairwise number, call check_two_numbers
middle_total = 0
for sequence in sequences:
    numbers = list(map(int, sequence.split(",")))
    sequence_good = True
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if not check_two_numbers(numbers[i], numbers[j]):
                sequence_good = False
                print(
                    f"Bad sequence: {sequence}, rule failed: {numbers[i]}, {numbers[j]}"
                )
                break
        if not sequence_good:
            break
    if sequence_good:
        print(f"Good sequence: {sequence}")
        middle_total += numbers[len(numbers) // 2]

print(middle_total)
