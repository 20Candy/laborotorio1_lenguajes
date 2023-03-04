from automaton.automaton import Automaton
from tree.tree import Tree
from utils.set import Set


class Direct():
    def __init__(self):
        self.counter = 1
        self.table = []

    def Direct(self, postfix_expression):

        postfix_expression = postfix_expression + "#."
        tree = Tree(postfix_expression)
        tree.BuildTree("arbol_direct")
               
        direct = self.directAfd(tree.node)
        # direct.toString()
        # direct.toGraph(direct, "Direct")

        return direct
    
    def directAfd(self, node):
        automata = Automaton()

        self.numberNodes(node)
        self.checkNullable(node)
        self.checkFirstPos(node)
        self.checkLastPos(node)

        self.followPos(node)
        print("FollowPos: ", node.followPos)

    def numberNodes(self, node):

        if node.is_leaf():
            if node.symbol != 'ε':
                node.number = self.counter
                self.counter += 1
        else:
            if (node.left_child != None):
                self.numberNodes(node.left_child)
            if (node.right_child != None):
                self.numberNodes(node.right_child)

    def checkNullable(self, node):
        if node.is_leaf():
            node.nullable = node.symbol == 'ε'
        else:
            if node.symbol == '*':
                self.checkNullable(node.left_child)
                node.nullable = True
                
            elif node.symbol == '+':
                self.checkNullable(node.left_child)
                node.nullable = True
                
            elif node.symbol == '?':
                self.checkNullable(node.left_child)
                node.nullable = True
                
            elif node.symbol == '.':
                self.checkNullable(node.left_child)
                self.checkNullable(node.right_child)

                if node.left_child.nullable and node.right_child.nullable:
                    node.nullable = True
                else:
                    node.nullable = False

            elif node.symbol == '|':
                self.checkNullable(node.left_child)
                self.checkNullable(node.right_child)

                if node.left_child.nullable or node.right_child.nullable:
                    node.nullable = True
                else:
                    node.nullable = False

    def checkFirstPos(self, node):
        if node.is_leaf():
            if node.symbol == 'ε':
                node.firstpos = Set()
            else:
                node.firstpos = Set()
                node.firstpos.AddItem(node.number)

        else:
            if node.symbol == '*':
                self.checkFirstPos(node.left_child)
                node.firstpos = node.left_child.firstpos
                
            elif node.symbol == '+':
                self.checkFirstPos(node.left_child)
                node.firstpos = node.left_child.firstpos
            
            elif node.symbol == '?':
                self.checkFirstPos(node.left_child)
                node.firstpos = node.left_child.firstpos

            elif node.symbol == '.':
                self.checkFirstPos(node.left_child)
                self.checkFirstPos(node.right_child)

                if node.left_child.nullable:
                    node.firstpos = node.left_child.firstpos.Union(node.right_child.firstpos)
                else:
                    node.firstpos = node.left_child.firstpos
            elif node.symbol == '|':
                self.checkFirstPos(node.left_child)
                self.checkFirstPos(node.right_child)

                node.firstpos = node.left_child.firstpos.Union(node.right_child.firstpos)

    def checkLastPos(self, node):
        if node.is_leaf():
            if node.symbol == 'ε':
                node.lastpos = Set()
            else:
                node.lastpos = Set()
                node.lastpos.AddItem(node.number)
        else:
            if node.symbol == '*':
                self.checkLastPos(node.left_child)
                node.lastpos = node.left_child.lastpos

            elif node.symbol == '+':
                self.checkLastPos(node.left_child)
                node.lastpos = node.left_child.lastpos

            elif node.symbol == '?':
                self.checkLastPos(node.left_child)
                node.lastpos = node.left_child.lastpos

            elif node.symbol == '.':
                self.checkLastPos(node.left_child)
                self.checkLastPos(node.right_child)

                if node.right_child.nullable:
                    node.lastpos = node.left_child.lastpos.Union(node.right_child.lastpos)
                else:
                    node.lastpos = node.right_child.lastpos
            elif node.symbol == '|':
                self.checkLastPos(node.left_child)
                self.checkLastPos(node.right_child)

                node.lastpos = node.left_child.lastpos.Union(node.right_child.lastpos)

    def followPos(self, node):
        if node.is_leaf():
            if node.symbol != 'ε':
                self.table.append((node.number, node.symbol, Set()))

        else:
            if node.symbol == '*':
                self.followPos(node.left_child)

            elif node.symbol == '+':
                self.followPos(node.left_child)

            elif node.symbol == '?':
                self.followPos(node.left_child)

            elif node.symbol == '.':
                self.followPos(node.left_child)
                self.followPos(node.right_child)

                for i in node.left_child.lastpos:
                    for j in node.right_child.firstpos:
                        self.table.append((i, node.symbol, Set(j)))

            elif node.symbol == '|':
                self.followPos(node.left_child)
                self.followPos(node.right_child)
           
                        

