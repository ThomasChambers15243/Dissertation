from random import randrange

'''
Given the root parent node of an unsorted tree and the implementation of the nodes, 
find all duplicate nodes (if any) and remove them from the tree so all nodes hold unique data. 
The tree does not need to be sorted or balanced. 
'''


class Node():
    '''
    Implementation of each Node in the tree.
    '''

    def __init__(self, data=-1):
        self.data = data
        self.children = []

    def AddChild(self, node):
        self.children.append(node)

    def AddChildren(self, numChildren: int):
        for _ in range(numChildren):
            self.AddChild(Node(randrange(0, 10)))


def MakeTree(node: Node, numChildren: int, depth: int, level: int) -> bool:
    '''
    Makes the tree given the number of children per node and the desired depth of the tree
    '''
    if depth <= level:
        return True
    node.AddChildren(numChildren)
    level += 1
    for child in node.children:
        MakeTree(child, randrange(1, 10), depth, level)


# TODO
def Q5(root: Node) -> Node:
    raise NotImplementedError