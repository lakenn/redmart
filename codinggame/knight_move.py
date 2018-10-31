#Problem Set:
# https://www.codingame.com/training/medium/shadows-of-the-knight-episode-1

import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.

# starting pos
x0, y0 = [int(i) for i in input().split()]

x_left_bound = 0
x_right_bound = w-1

y_left_bound = 0
y_right_bound = h-1

# game loop
while True:
    bomb_dir = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    if 'D' in bomb_dir:
        y_left_bound = y0+1
    elif 'U' in bomb_dir:
        y_right_bound = y0-1

    if 'R' in bomb_dir:
        x_left_bound = x0+1
    elif 'L' in bomb_dir:
        x_right_bound = x0-1

    x0 = int((x_left_bound + x_right_bound)/2)
    y0 = int((y_left_bound + y_right_bound)/2)

    # the location of the next window Batman should jump to.
    print("{} {}".format(x0, y0))