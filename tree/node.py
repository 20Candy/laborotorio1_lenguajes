class Node:
    def __init__(self, symbol, left_child=None, right_child=None, number=None, nullable=None, firstpos=None, lastpos=None, followpos=None):
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child
        self.number = number
        self.nullable = nullable
        self.firstpos = firstpos
        self.lastpos = lastpos
        self.followpos = followpos

    def __str__(self):
        return self.symbol
    
    def is_leaf(self):
        return self.left_child is None and self.right_child is None
