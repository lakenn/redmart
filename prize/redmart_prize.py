#http://geeks.redmart.com/2015/10/26/1000000th-customer-prize-another-programming-challenge/

#!/usr/bin/python
import csv
from functools import reduce

class Item:
    def __init__(self, index, id, value, weight, volume):
        self.index = index
        self.id = id
        self.value = value
        self.weight = weight
        self.volume = volume

class Node:
    def __init__(self, index, id, value, weight, room, estimate, path):
        self.index = index
        self.id = id
        self.value = value
        self.weight = weight
        self.room = room
        self.estimate = estimate
        self.path = path

def get_volume(dims):
    return reduce(lambda x, y: x * y, dims, 1)

# greedy approach for fractional knapsack
def calc_estimate(items, capacity, start_idx, max_tree_depth):
    volume = 0
    value = 0
    for idx in range(start_idx, max_tree_depth+1):
        if volume + items[idx].volume <= capacity:
            volume += items[idx].volume
            value += items[idx].value
        else:
            # last one
            return value + items[idx].ratio * (capacity - volume)
    return value

# return a child node of a node if flesible
def child_node(node, items, taken, best_node, max_tree_depth):
    item = items[node.index + 1]
    path = node.path
    path += " %d" % taken

    child = None

    # we want to take the item
    if taken:
        # check if we can take it
        if item.volume <= node.room:
            child = Node(node.index + 1, node.id, node.value + item.value, node.weight + item.weight, node.room - item.volume, node.estimate, path)
    else:
        # not taking the item
        new_estimate = node.value + calc_estimate(items, node.room, node.index + 2, max_tree_depth)

        # pruning
        if best_node and new_estimate < best_node.estimate:
            # print('pruning at node %s' % str(node.index+1))
            return None

        child = Node(node.index + 1, node.id, node.value, node.weight, node.room, new_estimate, path)

    return child

def branch_and_bound(items, tote_volume):
    # calc value per weight
    for item in items:
        item.ratio = item.value / item.volume

    # sort items by decreasing value of  Value/Volume
    sorted_items = sorted(items, key=lambda x: x.ratio, reverse=True)

    max_tree_depth = len(items)
    # find a best estimate value for pruning search space
    best_estimate = calc_estimate(sorted_items, tote_volume, 0, max_tree_depth)

    # for easier tree indexing only
    sorted_items.insert(0, 'dummy')
    stack = []

    best_node = Node(0, 0, 0, 0, tote_volume, 0, '')
    node_0 = Node(0, 0, 0, 0, tote_volume, best_estimate, '')
    stack.append(node_0)

    # DFS for best solution
    while (len(stack)):
        node = stack.pop()

        # reach leaf node
        if node.index == max_tree_depth:
            # see if we need to update best_node
            if node.estimate > best_node.estimate:
                best_node = node
            elif node.estimate == best_node.estimate and node.weight < best_node.weight:
                best_node = node
        else:
            # does the node has valid children ?
            # two cases: take or not to take
            for taken in [0, 1]:
                child = child_node(node, sorted_items, taken, best_node, max_tree_depth)

                if child:
                    stack.append(child)

    best_path = best_node.path.split(' ')
    # remove the dummy item
    sorted_items.pop(0)
    best_path.pop(0)

    for i, item in enumerate(sorted_items):
        item.select = best_path[i]

    result = 0
    for item in sorted_items:
        if item.select == '1':
            result += item.id
    return result

if __name__ == '__main__':

    # length, width, height
    tote_dims = [45,30,35]
    tote_volume = get_volume(tote_dims)
    items = []
    rejected = 0

    with open('products.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        index = 1
        for row in reader:
            item = [int(x) for x in row]
            item_dims = item[2:5]

            fit = all(x <= y for x,y in zip(item_dims, tote_dims))

            if fit:
                items.append(Item(index, item[0], item[1], item[5], get_volume(item_dims)))
                index += 1
            else:
                rejected +=1

        print("Number of items that do not fit the tote: {}".format(rejected))

        print(branch_and_bound(items, tote_volume))