import fileinput
from collections import defaultdict

lines = [line.strip() for line in fileinput.input(files="inputs/1.txt")]

left_nums = []
right_nums = defaultdict(int)

for line in lines:
    left, right = line.split("   ")
    left_nums.append(int(left))
    right_nums[int(right)] += 1

similarity_score = 0

for num in left_nums:
    similarity_score += num * right_nums[num]

print(similarity_score)
# 26859182
