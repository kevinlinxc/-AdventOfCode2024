import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/2.txt")]


safe_count = 0


def is_safe(nums):
    all_decreasing = sorted(nums) == nums
    all_increasing = sorted(nums, reverse=True) == nums
    if not all_decreasing and not all_increasing:
        print("Not all decreasing or increasing")
        return False

    for index in range(1, len(nums)):
        difference_last = nums[index] - nums[index - 1]
        if abs(difference_last) < 1 or abs(difference_last) > 3:
            return False
    return True


for line in lines:
    nums = list(map(int, line.split(" ")))
    print(nums)
    if is_safe(nums):
        safe_count += 1

print(safe_count)
# 549
