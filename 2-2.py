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
        difference_last = nums[index] - nums[index-1]
        if abs(difference_last) < 1 or abs(difference_last) > 3:
            return False
    return True

for line in lines:
    nums = list(map(int, line.split(" ")))
    number_of_nums = len(nums)
    print(nums)
    if is_safe(nums):
        safe_count += 1
        continue
    for index in range(number_of_nums):
        # make copy with one element removed
        copy = nums.copy()
        copy.pop(index)
        if is_safe(copy):
            safe_count += 1
            break

print(safe_count)
# 589
