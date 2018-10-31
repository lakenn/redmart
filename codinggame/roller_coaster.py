import sys
import math
import fileinput
import sys

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# l -- l seats
# c -- number of times per day
# n -- number of groups

l, c, n = [int(i) for i in input().split()]
#l, c, n = 100000, 50000, 1000

print("l: {}, c: {} , n:{}".format(l, c, n), file=sys.stderr)

# for i in range(n):
#    pi = int(input())

groups = [int(input()) for i in range(n)]

'''
groups = []
with open('roller_coaster_input.txt') as f:
    lines = f.readlines()[1:]

    for line in lines:
        groups.append(int(line))

print("groups...{}".format(groups), file=sys.stderr)
'''

def effective_play_rc(l, groups, start, total_len):
    cum_sum = 0
    idx = start

    while True:

        if cum_sum + groups[idx] <= l:
            cum_sum += groups[idx]
            idx = (idx + 1) % total_len

            # circle !
            if idx == start:
                break

        else:
            break

    return cum_sum, idx

result_map = {}
ans = 0
start = 0
total_len = len(groups)

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
for i in range(c):
    record = result_map.get(start, None)
    if record is None:
        earn, end = effective_play_rc(l, groups, start, total_len)
        result_map[start] = (earn, end)
    else:
        earn, end = record

    start = end
    ans += earn

print(ans)