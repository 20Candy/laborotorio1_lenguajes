class Node:
    def __init__(self, symbol, left_child=None, right_child=None):
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self):
        return self.symbol