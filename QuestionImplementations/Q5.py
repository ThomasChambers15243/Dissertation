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

    def AddChildren(self, numChildren : int, childrenData : list[int]):
        for child in range(numChildren):
            self.AddChild(Node(childrenData[child]))


#TODO
def Q5(root : Node) -> Node:
    raise NotImplementedError