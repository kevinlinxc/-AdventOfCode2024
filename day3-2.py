import fileinput
import re

lines = [line.strip() for line in fileinput.input(files="inputs/3.txt")]
line = "".join(lines)
pattern = r"mul\(\d+\,\d+\)"


def get_muls_result(line):
    """
    Get muls from a line that we've prevalidated
    """
    total = 0

    match = re.findall(pattern, line)
    for mul_found in match:
        nums = mul_found[4:-1].split(",")
        result = int(nums[0]) * int(nums[1])
        total += result
    print("Adding total: ", total)
    return total


final_total = 0

# find first "don't"
dont_index = line.find("don't()")
until_first = line[:dont_index]
print(f"Valid segment from {0} to {dont_index}: {until_first}")
# truncate, go to the next do and repeat
final_total += get_muls_result(until_first)

line = line[dont_index:]
do_index = line.find("do()")
line = line[do_index:]
no_add_at_end = False
while "don't" in line:
    dont_index = line.find("don't")
    until_dont = line[:dont_index]
    print(f"Valid segment from {do_index} to {dont_index}: {until_dont}")
    final_total += get_muls_result(until_dont)
    line = line[dont_index:]
    do_index = line.find("do()")
    if do_index == -1:
        no_add_at_end = True
        break
    line = line[do_index:]
if not no_add_at_end:
    final_total += get_muls_result(line)

print(final_total)
# 113965544
