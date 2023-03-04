from tree.node import Node
from graphviz import Digraph

class Tree:
    def __init__(self, expression):
        self.expression = expression
        self.node = None
        self.stack = []
    
    def BuildTree(self, filename="arbol"):
        for symbol in self.expression:
            if symbol == '*':
                self.create_node(symbol)
            elif symbol == '+':
                self.create_node(symbol)
            elif symbol == '?':
                self.create_node(symbol)
            elif symbol == '.':
                self.create_node(symbol)
            elif symbol == '|':
                self.create_node(symbol)
            else:
                self.create_node(symbol)

        self.node = self.stack.pop()
        self.toGraph(self.node, filename)

    def create_node(self, symbol):

        if symbol == '*':
            node = Node(symbol)
            node.left_child = self.stack.pop()
            self.stack.append(node)
        elif symbol == '+':
            node = Node(symbol)
            node.left_child = self.stack.pop()
            self.stack.append(node)
        elif symbol == '?':
            node = Node(symbol)
            node.left_child = self.stack.pop()
            self.stack.append(node)
        elif symbol == '.':
            node = Node(symbol)
            node.right_child = self.stack.pop()
            node.left_child = self.stack.pop()
            self.stack.append(node)
        elif symbol == '|':
            node = Node(symbol)
            node.right_child = self.stack.pop()
            node.left_child = self.stack.pop()
            self.stack.append(node)
        else:
            node = Node(symbol)
            self.stack.append(node)

    def toGraph(self, node, filename="arbol"):
        dot = Digraph(comment='Tree')
        self.GraphNode(node, dot)
        dot.render(filename, view=True)

    def GraphNode(self, node, dot):
        if node is None:
            return

        dot.node(str(id(node)), label=node.symbol)

        if node.left_child is not None:
            self.GraphNode(node.left_child, dot)
            dot.edge(str(id(node)), str(id(node.left_child)))

        if node.right_child is not None:
            self.GraphNode(node.right_child, dot)
            dot.edge(str(id(node)), str(id(node.right_child)))    
