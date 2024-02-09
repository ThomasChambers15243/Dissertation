'''
Given the first node of an unsorted linked list and implementation of the nodes,
sort the list so it is ordered, from smallest value to largest.
'''

class Node:
    def __init__(self, data : int):
        self.next : Node
        self.data = data

#TODO
def Q4(node : Node) -> Node:
    raise NotImplementedError

from random import randrange

def MakeList(node: Node, amount, current):
    if current < amount:
        node.next = Node(randrange(0,1000))
        MakeList(node.next,amount,current+1)
    return

node = Node(0)
MakeList(node,10,0)
print("Stop")
