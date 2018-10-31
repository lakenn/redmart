#Problem Set:
#https://www.codingame.com/ide/puzzle/stock-exchange-losses

import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

best_buy = -1
best_sell = -1
potential_buy = -1

n = int(input())
for i in input().split():
    v = int(i)

    # the 1st point
    if best_buy == -1:
        best_buy = v
        best_sell = v
        potential_buy = v

    # find a better sell point
    if v < best_sell:
        best_sell = v

    # potentially better buy point
    if v > potential_buy:
        potential_buy = v

    # find a bigger max_dradown
    # update it
    if v - potential_buy < best_sell - best_buy:
        best_buy = potential_buy
        best_sell = v

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(best_sell - best_buy)