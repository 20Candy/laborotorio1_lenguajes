from utils.set import Set
class Node:
    def __init__(self, symbol, left_child=None, right_child=None, number=None):
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child
        self.number = number
        self.nullable = False
        self.firstpos = Set()
        self.lastpos = Set()
        self.followpos = Set()

    def __str__(self):
        return self.symbol
    
    def is_leaf(self):
        return self.left_child is None and self.right_child is None
