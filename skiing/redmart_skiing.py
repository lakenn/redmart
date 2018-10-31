#http://geeks.redmart.com/2015/01/07/skiing-in-singapore-a-coding-diversion/

from collections import deque

GRAY, BLACK = 0, 1

def topological(graph):
    order, enter, state = deque(), set(graph), {}

    def dfs(node):
        state[node] = GRAY
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == GRAY:
                raise ValueError("cycle")
            if sk == BLACK:
                continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = BLACK

    while enter:
        dfs(enter.pop())
    return order

def build_dag(lines, columns, rows):
    grid = []
    for i in range(1, rows+1):
        line = lines[i]
        row = line.split()
        grid.append(list(map(int, row)))

    adj_list = {(y, x): [] for x in range(columns) for y in range(rows) }

    # build DAG
    for x, y in adj_list.keys():
        neighbors = [
            (x, y - 1),  # up
            (x, y + 1),  # down
            (x - 1, y),  # left
            (x + 1, y),  # right
        ]

        for xn, yn in neighbors:
            if xn < 0 or yn < 0:
                continue
            try:
                neighbor = grid[yn][xn]
            except IndexError:
                continue

            if neighbor < grid[y][x]:
                adj_list[(y,x)].append((yn, xn))

    return grid, adj_list

if __name__ == '__main__':
    with open('map.txt', 'r') as input_data_file:
        input_data = input_data_file.read()

    lines = input_data.split('\n')
    firstLine = lines[0].split()

    columns = int(firstLine[0])
    rows = int(firstLine[1])

    dist = {(y, x): 1 for x in range(columns) for y in range(rows)}
    #prev = {(y, x): -1 for x in range(columns) for y in range(rows)}

    grid, graph = build_dag(lines, columns, rows)
    prev_max = {(y, x): grid[y][x] for x in range(columns) for y in range(rows)}

    topological_order = topological(graph)

    for u in topological_order:
        for v in graph.get(u, ()):
            # find a larger dist path
            if dist[v] < dist[u] + 1:
                dist[v] = dist[u] + 1
                prev_max[v] = prev_max[u]
                #prev[v] = u
            elif dist[v] == dist[u] + 1 and prev_max[v] < prev_max[u]:
                prev_max[v] = prev_max[u]
                #prev[v] = u

    dest_node = max(dist, key=dist.get)
    max_dist = dist[dest_node]
    max_drop = prev_max[dest_node] - grid[dest_node[0]][dest_node[1]]

    # graph may not be fully connected
    # We need to get the max_drop one
    for start_node, d in dist.items():
        if d == max_dist:
            curr_drop = prev_max[start_node] - grid[start_node[0]][start_node[1]]
            if curr_drop > max_drop:
                max_drop = curr_drop

    print('{} {}'.format(max_dist, max_drop))