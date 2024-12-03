import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/1.txt")]

left_nums = []
right_nums = []
for line in lines:
    left, right = line.split("   ")
    left_nums.append(int(left))
    right_nums.append(int(right))

# sort them

left_nums.sort()
right_nums.sort()

# find difference of both numbers

diff = sum([abs(left - right) for left, right in zip(left_nums, right_nums)])
print(diff)
# 1320851
