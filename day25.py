import fileinput
from collections import defaultdict

lines = [line.strip() for line in fileinput.input(files="inputs/25.txt")]

# split by \n
class Key:
    def __init__(self, key_lines):
        self.column_count = {i: 0 for i in range(len(key_lines[0]))}
        for line in key_lines:
            for i, char in enumerate(line):
                if char == "#":
                    self.column_count[i] += 1
    def can_unlock(self, lock):
        for i in range(len(self.column_count)):
            if self.column_count[i] + lock.column_count[i] >= 6:
                print(f"{self} can't unlock {lock} because {self.column_count[i]} + {lock.column_count[i]} >= 6")
                return False
        print(f"{self} can unlock {lock}")
        return True
    
    def __repr__(self):
        return str([self.column_count[i] for i in range(len(self.column_count))])

class Lock:
    def __init__(self, lock_lines):
        self.column_count = {i: 0 for i in range(len(lock_lines[0]))}
        for line in lock_lines:
            for i, char in enumerate(line):
                if char == "#":
                    self.column_count[i] += 1
    def __repr__(self):
        return str([self.column_count[i] for i in range(len(self.column_count))])


locks = []
keys = []
for i in range(len(lines)//8 +1):
    relevant = lines[i*8:i*8+7]
    if relevant[0] == "#####":
        print("Lock!")
        locks.append(Lock(relevant[1:]))
    elif relevant[-1] == "#####":
        print("Key!")
        keys.append(Key(relevant[:-1]))

total_unlock = 0
for lock in locks:
    for key in keys:
        if key.can_unlock(lock):
            total_unlock += 1

print(locks)
print(keys)
print(total_unlock)