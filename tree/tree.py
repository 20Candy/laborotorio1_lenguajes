from tree.node import Node
from graphviz import Digraph
import re

class Tree:
    def __init__(self, expression):
        self.expression = expression
        self.node = None
        self.stack = []
        self.connections = []
    
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
            symbol_to_add = self.stack[-1]
        
            node = Node("•")
            node.left_child = symbol_to_add
            node.right_child = Node("*")
            node.right_child.left_child = self.stack.pop()
            
            self.stack.append(node)
        elif symbol == '?':
            symbol_to_add = self.stack.pop()

            node = Node("|")
            node.left_child = symbol_to_add
            node.right_child = Node("ε")

            self.stack.append(node)
        elif symbol == '•':
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
            node = Node(chr(int(symbol)))
            self.stack.append(node)

    def toGraph(self, node, filename="arbol"):
        dot = Digraph(comment='Tree')
        self.GraphNode(node, dot)
        dot.render(filename, view=True)

    def GraphNode(self, node, dot):
        if node is None:
            return

        if(node.symbol == "|" or node.symbol == "•" or node.symbol == "*" or node.symbol == "+" or node.symbol == "?"):
            dot.node(str(id(node)), label=node.symbol)
        else:
            dot.node(str(id(node)), label=(node.symbol))


        if node.left_child is not None:
            self.GraphNode(node.left_child, dot)
            if (str(id(node)), str(id(node.left_child))) not in self.connections:
                dot.edge(str(id(node)), str(id(node.left_child)))
                self.connections.append((str(id(node)), str(id(node.left_child))))

        if node.right_child is not None:
            self.GraphNode(node.right_child, dot)
            if (str(id(node)), str(id(node.right_child))) not in self.connections:
                dot.edge(str(id(node)), str(id(node.right_child)))
                self.connections.append((str(id(node)), str(id(node.right_child))))


