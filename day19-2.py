import fileinput

lines = [line.strip() for line in fileinput.input(files="inputs/19.txt")]

patterns = lines[0]
messages = lines[2:]
patterns = patterns.split(", ")
for pattern in patterns:
    print(pattern)


def count_ways_to_construct(pattern, substrings):
    # Memoization dictionary to store results of subproblems
    memo = {}

    def helper(remaining):
        # If the remaining string is empty, we've successfully constructed the pattern
        if not remaining:
            return 1

        # If already computed for this substring, return the result
        if remaining in memo:
            return memo[remaining]

        # Initialize the count of ways to construct the remaining string
        total_ways = 0

        # Try every substring
        for sub in substrings:
            # Check if the substring matches the beginning of the remaining string
            if remaining.startswith(sub):
                # Recur with the rest of the string and add the result to total_ways
                total_ways += helper(remaining[len(sub) :])

        # Store the result in memo and return it
        memo[remaining] = total_ways
        return total_ways

    return helper(pattern)


possible = 0
for line in messages:
    possible += count_ways_to_construct(line, patterns)
print(possible)
