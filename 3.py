import fileinput
import re

lines = [line.strip() for line in fileinput.input(files="inputs/3.txt")]
pattern = r"mul\(\d+\,\d+\)"
total = 0

for line in lines:
    # print(line)
    match = re.findall(pattern, line)
    for mul_found in match:
        nums = mul_found[4:-1].split(",")
        result = int(nums[0]) * int(nums[1])
        total += result
print(total)
# 188192787
