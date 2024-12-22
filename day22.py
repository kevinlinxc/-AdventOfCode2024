import fileinput
from tqdm import tqdm

lines = [line.strip() for line in fileinput.input(files="inputs/22.txt")]


def get_it_two_thousand(n):
    for i in range(2000):
        n = ((n * 64) ^ n) % 16777216
        n = ((n // 32) ^ n) % 16777216
        n = ((n * 2048) ^ n) % 16777216
    return n


sum = 0
for line in tqdm(lines):
    it_two_thousand = get_it_two_thousand(int(line))
    print(f"{line} created {it_two_thousand}")
    sum += it_two_thousand


print(sum)
