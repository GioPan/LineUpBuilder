from player import Player


class Node:
    counter = 0
    def __init__(self,parent=None,childrenNumber=None):
        self.id = Node.counter
        self.parent = parent
        self.childrenNumber = childrenNumber
        Node.counter = Node.counter + 1
        self.last = False
        self.branchingConstraints = []
        
# def __eq__(self, other):
#         return self.id == other.id
