import sys
import re
import rpn
from collections import deque

class Node:
    def __init__(self, key, expr):
        self.key = key
        self.parents = set()
        self.children = set()
        self.orig_expr = expr
        self.expr = expr
        self.value = None
        self.dirty = True

    def add_child(self, who):
        self.children.add(who)

    def add_parent(self, who):
        self.parents.add(who)

    def set_value(self, value):
        if self.value != value:
            self.value = value
            self.notify()

    def eval(self):
        if not self.dirty:
            return self.value

        expr = self.orig_expr
        for ancestor in self.parents:
            if ancestor.dirty:
                raise RuntimeError('Evaluating node %s before all parents are evaluated' % self.key)

            expr = re.sub(ancestor.key, str(ancestor.value), expr)


        self.value = rpn.eval_expression(expr.split())
        self.dirty = False

        # only evaluate when all parents have been assigned a value
        #if all(DAG[node].dirty == False for node in self.parents):
        #matches = re.findall(r'([A-Z])(\d+)', self.expr)
        #if len(matches) == 0:
        #    self.value = rpn.eval_expression(self.expr.split())
        #    self.dirty = False

    def update(self):
        self.dirty = True

    def notify(self):
        for child in self.children:
            child.update(self.key, self.value)

    def __repr__(self):
        return self.key + '(' + self.expr +')'

GRAY, BLACK = 0, 1

# BLACK -- visited

def topological(graph):
    order, enter, state = deque(), set(graph), {}

    def dfs(node):
        state[node] = GRAY
        node_obj = graph.get(node)
        for neighbour in node_obj.children:
            sk = state.get(neighbour.key, None)
            if sk == GRAY:
                raise ValueError("cycle")

            # visited
            if sk == BLACK:
                continue
            enter.discard(neighbour.key)
            dfs(neighbour.key)
        order.appendleft(node)
        state[node] = BLACK

    while enter:
        dfs(enter.pop())
    return order


if __name__ == '__main__':

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()

            # parse the input
            lines = input_data.split('\n')

            firstLine = lines[0].split()
            width, height = int(firstLine[0]), int(firstLine[1])

            total_num_of_items = width * height

            sheet = {}

            counter = 1
            for j in range(1, height + 1):
                for i in range(1, width + 1):
                    row_idx = chr(64 + j)
                    col_idx = str(i)

                    expr = lines[counter]
                    sheet.setdefault(row_idx + col_idx, Node(row_idx + col_idx, expr))
                    counter += 1

            # build DAG
            for i in range(1, width+1):
                for j in range(1, height+1):
                    j = chr(64 + j)
                    node = sheet.get(j + str(i), None)
                    matches = re.findall(r'([A-Z])(\d+)', node.expr)

                    # has parents
                    if len(matches):
                        for match in matches:
                            row = match[0]
                            col = match[1]

                            p_node = sheet.get(row + col, None)

                            p_node.add_child(node)
                            node.add_parent(p_node)

            try:
                eval_orders = topological(sheet)

            except ValueError:
                exit(-1)

            for key in eval_orders:
                node = sheet.get(key)
                node.eval()

            for j in range(1, height+1):
                j = chr(64 + j)
                for i in range(1, width+1):
                    node = sheet.get(j + str(i), None)
                    print('%.5f' % node.value)

    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
