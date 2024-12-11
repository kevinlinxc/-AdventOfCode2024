import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/11.txt")]


def blink(sequence: list[int]):
    new_list = []
    for item in sequence:
        if int(item) == 0:
            new_list.append(1)
        elif len(str(item)) % 2 == 0:
            # split it into left and right
            left = str(item)[: len(str(item)) // 2]
            right = str(item)[len(str(item)) // 2 :]
            new_list.append(int(left))
            new_list.append(int(right))
        else:
            new_list.append(int(item) * 2024)
    return new_list


start_list = lines[0].split(" ")
print(start_list)
for i in range(25):
    start_list = blink(start_list)
    print(start_list)

print(len(start_list))
