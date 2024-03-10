'''
Given the first node of an unsorted linked list and implementation of the nodes,
sort the list so it is ordered, from smallest value to largest.
'''

class Node:
    def __init__(self, data : int):
        self.next = None
        self.data = data

#TODO
def Q4(node : Node) -> Node:
    values = []

    # Collect and sort values
    while node.next is not None:
        values.append(node.data)
        node = node.next
    values.append(node.data)
    values.sort()

    # Create sorted list
    node = Node(values[0])
    root = node
    for i in values[1:]:
        node.next = Node(i)
        node = node.next
    return root