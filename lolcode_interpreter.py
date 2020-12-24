import pprint
import re

from lolcode_lexer import *
from lolcode_parser import *


pp = pprint.PrettyPrinter(indent=4)


class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def __call__(self):
        return self.visit(self.parser.trees[0])

    def printTree(self, node):
        if hasattr(node, 'left'):
            left = self.printTree(node.left)
        if hasattr(node, 'right'):
            right = self.printTree(node.right)
        print(repr(node.token))

    def visit(self, node):
        methodName = 'visit_' + type(node).__name__
        visitor = getattr(self, methodName)
        return visitor(node)

    def visit_UnOp(self, node):
        if node.token.tag == "TT_NOT":
            return not self.visit(node.operand)

    def visit_BinOp(self, node):
        # Arithmetic Binary Operations
        if node.token.tag == "TT_ADD":
            return self.visit(node.left) + self.visit(node.right)
        if node.token.tag == "TT_SUB":
            return self.visit(node.left) - self.visit(node.right)
        if node.token.tag == "TT_MUL":
            return self.visit(node.left) * self.visit(node.right)
        if node.token.tag == "TT_DIV":
            return self.visit(node.left) / self.visit(node.right)
        if node.token.tag == "TT_MOD":
            return self.visit(node.left) % self.visit(node.right)
        if node.token.tag == "TT_MAX":
            return max(self.visit(node.left), self.visit(node.right))
        if node.token.tag == "TT_MIN":
            return min(self.visit(node.left), self.visit(node.right))

        # Boolean Binary Operations
        if node.token.tag == "TT_AND":
            return self.visit(node.left) and self.visit(node.right)
        if node.token.tag == "TT_XOR":
            return self.visit(node.left) ^ self.visit(node.right)
        if node.token.tag == "TT_OR":
            return self.visit(node.left) or self.visit(node.right)

        # Comparison Binary Operations
        if node.token.tag == "TT_EQUAL":
            return self.visit(node.left) == self.visit(node.right)
        if node.token.tag == "TT_NOT_EQUAL":
            return self.visit(node.left) != self.visit(node.right)

    def visit_InfOp(self, node):
        if node.token.tag == "TT_INFINITY_CONCAT":
            if not node.child:
                return str(self.visit(node.value))
            else:
                return str(self.visit(node.value)) + self.visit_InfOp(node.child)
        elif node.token.tag == "TT_INFINITY_OR":
            if not node.child:
                return self.visit(node.value)
            else:
                return self.visit(node.value) or self.visit_InfOp(node.child)
        elif node.token.tag == "TT_INFINITY_AND":
            if not node.child:
                return self.visit(node.value)
            else:
                return self.visit(node.value) and self.visit_InfOp(node.child)


    def visit_Num(self, node):
        if node.token.tag == "TT_NUMBR":
            return int(node.value)
        elif node.token.tag == "TT_NUMBAR":
            return float(node.value)

    def visit_Bool(self, node):
        if node.value == "WIN":
            return True
        elif node.value == "FAIL":
            return False

    def visit_String(self, node):
        return str(node.value).replace("\"","")


symbolTable = dict()

tokens = lexer(readSourceCode("LOLCODE_example/bestcase.lol"))
# pp.pprint(tokens)

myParser = Parser(tokens)
myParser.run()

if myParser:
    myInterpreter = Interpreter(myParser)
    # print(tokens)

    # print(myParser.trees)

    print(myInterpreter())
