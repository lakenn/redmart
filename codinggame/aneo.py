#Problem Set:
#https://www.codingame.com/training/medium/aneo

import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

speed = int(input())
light_count = int(input())

print("max speed...{}".format(speed), file=sys.stderr)
print("light count...{}".format(light_count), file=sys.stderr)

lights = []

for i in range(light_count):
    distance, duration = [int(j) for j in input().split()]
    print("Distance Info...{} {}".format(distance, duration), file=sys.stderr)
    lights.append((distance, duration))

# min speed
answer = 1
# only consider int velocity
for velocity in range(speed, 1, -1):

    def is_pass_green_light(speed, dist, duration):
        return int(dist * 36 / speed / 10 / duration % 2)


    result = 0
    for light in reversed(lights):
        dist = light[0]
        duration = light[1]
        success = is_pass_green_light(velocity, dist, duration)
        result += success

        print("Passing light...{} {} with speed: {}".format(distance, duration, velocity), file=sys.stderr)
        print("result is {}".format(success), file=sys.stderr)

        # early termination as it fails to pass a green light
        if result > 0:
            break

    if result == 0:
        answer = velocity
        break

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(answer)