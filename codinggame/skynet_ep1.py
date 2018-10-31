import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = 38, 79, 3

adj_matrix = [[0] * n for i in range(n)]

links = [(28, 36),
(0, 2),
(3, 34),
(29, 21),
(37, 35),
(28, 32),
(0, 10),
(37, 2),
(4, 5),
(13, 14),
(34, 35),
(27, 19),
(28, 34),
(30, 31),
(18, 26),
(0, 9),
(7, 8),
(18, 24),
(18, 23),
(0, 5),
(16, 17),
(29, 30),
(10, 11),
(0, 12),
(15, 16),
(0, 11),
(0, 17),
(18, 22),
(23, 24),
(0, 7),
(35, 23),
(22, 23),
(1, 2),
(0, 13),
(18, 27),
(25, 26),
(32, 33),
(28, 31),
(24, 25),
(28, 35),
(21, 22),
(4, 33),
(28, 29),
(36, 22),
(18, 25),
(37, 23),
(18, 21),
(5, 6),
(19, 20),
(0, 14),
(35, 36),
(9, 10),
(0, 6),
(20, 21),
(0, 3),
(33, 34),
(14, 15),
(28, 33),
(11, 12),
(12, 13),
(17, 1),
(18, 19),
(36, 29),
(0, 4),
(0, 15),
(0, 1),
(18, 20),
(2, 3),
(0, 16),
(8, 9),
(0, 8),
(26, 27),
(28, 30),
(3, 4),
(31, 32),
(6, 7),
(37, 1),
(37, 24),
(35, 2)
]

for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    for link in links:
        n1 = link[0]
        n2 = link[1]

        print("n1: {}, n2:{}".format(n1, n2), file=sys.stderr)

        adj_matrix[n1][n2] = 1
        adj_matrix[n2][n1] = 1

# for i in range(e):
#    ei = int(input())  # the index of a gateway node
print("link adj matrix: {}".format(adj_matrix), file=sys.stderr)

#exit_gates = [int(input()) for i in range(e)]
exit_gates = [0, 18, 28]
print("Gates: {}".format(exit_gates), file=sys.stderr)

# si = 37, 35, 2, 1
# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    d1 = d2 = None
    for gate in exit_gates:
        if adj_matrix[si][gate] == 1:
            d1 = si
            d2 = gate

            adj_matrix[gate][si] = 0
            adj_matrix[si][gate] = 0

            break

    cut = 0
    if d1 == None:
        for gate in exit_gates:
            for i in range(n):
                if adj_matrix[gate][i] == 1:
                    d1 = gate
                    d2 = i

                    adj_matrix[gate][i] = 0
                    adj_matrix[i][gate] = 0

                    cut = 1
                    break

            if cut:
                break
    # Example: 0 1 are the indices of the nodes you wish to sever the link between
    print("{} {}".format(d1, d2))