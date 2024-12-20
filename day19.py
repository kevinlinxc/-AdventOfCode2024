import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/19.txt")]

patterns = lines[0]
messages = lines[2:]
patterns = patterns.split(", ")
for pattern in patterns:
    print(pattern)


def can_construct(pattern, substrings):
    def helper(remaining):
        if remaining == "":
            return True
        for sub in substrings:
            if remaining.startswith(sub):
                if helper(remaining[len(sub):]):
                    return True
        return False
    return helper(pattern)

possible = 0
for line in messages:
    if can_construct(line, patterns):
        possible += 1
print(possible)
