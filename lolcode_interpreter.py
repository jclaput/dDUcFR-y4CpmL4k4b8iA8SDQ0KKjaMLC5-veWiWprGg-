from constants import *
from lolcode_lexer import *
from lolcode_parser import *


class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.symbolTable = {"IT": {"varValue": None, "varType": "NOOB"}}
        self.errorOccured = False

    def __call__(self):
        for t in self.parser.trees:
            result = self.visit(t)
            # print(result)
            if t.token.tag in EXPRESSIONS:
                self.symbolTable["IT"] = {
                    "varValue": result, "varType": self.getVariableDataType(result)}

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

    def visit_VariableDeclaration(self, node):
        val = None
        varType = "NOOB"

        if node.varObj.name == "IT":
            print("ERROR: cannot use implicit variable IT")
            return

        if self.isExistingVariable(node.varObj.name):
            print("ERROR: variable already exists")
            return

        if node.varValue:  # Variable token has a value, meaning its data type is not NOOB
            val = self.visit(node.varValue)

            if val:
                varType = self.getVariableDataType(val)

        self.symbolTable[node.varObj.name] = {
            "varValue": val, "varType": varType}

        return self.symbolTable[node.varObj.name]

    def visit_Variable(self, node):
        if not self.isExistingVariable(node.name):
            print("ERROR: variable does not exist")
            return

        return self.symbolTable[node.name]["varValue"]

    def getVariableDataType(self, val):
        varType = "NOOB"

        if type(val) == int:
            varType = "NUMBR"
        elif type(val) == float:
            varType = "NUMBAR"
        elif type(val) == bool:
            varType = "TROOF"
        elif type(val) == str:
            varType = "YARN"

        return varType

    def isExistingVariable(self, name):
        if name in self.symbolTable:
            return True
        return False

    def visit_UnOp(self, node):
        if node.token.tag == "TT_NOT":
            return not self.visit(node.operand)

    def visit_BinOp(self, node):
        # Arithmetic Binary Operations
        if node.token.tag == "TT_ADD":
            try:
                result = self.visit(node.left) + self.visit(node.right)
                if node.left.token.tag == "TT_NUMBAR" or node.right.token.tag == "TT_NUMBAR":
                    result = float(result)
                else:
                    result = int(result)
                return result
            except TypeError:
                print("ERROR: variable datatype")
            return
        if node.token.tag == "TT_SUB":
            try:
                result = self.visit(node.left) - self.visit(node.right)
                if node.left.token.tag == "TT_NUMBAR" or node.right.token.tag == "TT_NUMBAR":
                    result = float(result)
                else:
                    result = int(result)
                return result
            except TypeError:
                print("ERROR: variable datatype")
            return
        if node.token.tag == "TT_MUL":
            try:
                result = self.visit(node.left) * self.visit(node.right)
                if node.left.token.tag == "TT_NUMBAR" or node.right.token.tag == "TT_NUMBAR":
                    result = float(result)
                else:
                    result = int(result)
                return result
            except TypeError:
                print("ERROR: variable datatype")
            return
        if node.token.tag == "TT_DIV":
            try:
                result = self.visit(node.left) / self.visit(node.right)
                if node.left.token.tag == "TT_NUMBAR" or node.right.token.tag == "TT_NUMBAR":
                    result = float(result)
                else:
                    result = int(result)
                return result
            except TypeError:
                print("ERROR: variable datatype")
            except ZeroDivisionError:
                print("ERROR: division by zero")

            return
        if node.token.tag == "TT_MOD":
            try:
                result = self.visit(node.left) % self.visit(node.right)
                if node.left.token.tag == "TT_NUMBAR" or node.right.token.tag == "TT_NUMBAR":
                    result = float(result)
                else:
                    result = int(result)
                return result
            except TypeError:
                print("ERROR: variable datatype")

            return
        if node.token.tag == "TT_MAX":
            try:
                result = max(self.visit(node.left), self.visit(node.right))
                if node.left.token.tag == "TT_NUMBAR" or node.right.token.tag == "TT_NUMBAR":
                    result = float(result)
                else:
                    result = int(result)
                return result
            except TypeError:
                print("ERROR: variable datatype")

            return

        if node.token.tag == "TT_MIN":
            try:
                result = min(self.visit(node.left), self.visit(node.right))
                if node.left.token.tag == "TT_NUMBAR" or node.right.token.tag == "TT_NUMBAR":
                    result = float(result)
                else:
                    result = int(result)
                return result
            except TypeError:
                print("ERROR: variable datatype")

            return

        # Boolean Binary Operations
        if node.token.tag == "TT_AND":
            try:
                return self.visit(node.left) and self.visit(node.right)
            except TypeError:
                print("ERROR: variable datatype")
            return
        if node.token.tag == "TT_XOR":
            try:
                return self.visit(node.left) ^ self.visit(node.right)
            except TypeError:
                print("ERROR: variable datatype")
            return
        if node.token.tag == "TT_OR":
            try:
                return self.visit(node.left) or self.visit(node.right)
            except TypeError:
                print("ERROR: variable datatype")
            return

        # Comparison Binary Operations
        if node.token.tag == "TT_EQUAL":
            try:
                return self.visit(node.left) == self.visit(node.right)
            except TypeError:
                print("ERROR: variable datatype")
            return
        if node.token.tag == "TT_NOT_EQUAL":
            try:
                return self.visit(node.left) != self.visit(node.right)
            except TypeError:
                print("ERROR: variable datatype")
            return

        # Variable Assignment Statement
        if node.token.tag == "TT_ASSIGN_TO_VAR":
            if not self.isExistingVariable(node.left.name):
                print("ERROR: variable does not exist")
                return

            val = self.visit(node.right)
            varType = "NOOB"

            if val:
                varType = self.getVariableDataType(val)

            self.symbolTable[node.left.name] = {
                "varValue": val, "varType": varType}
            return self.symbolTable[node.left.name]

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

    def visit_IfElseStatement(self, node):
        whichCodeBlock = None
        if self.symbolTable["IT"]["varValue"]:
            whichCodeBlock = node.trueCodeBlock
        else:
            whichCodeBlock = node.falseCodeBlock

        if not whichCodeBlock:
            return

        for t in whichCodeBlock:
            result = self.visit(t)
            # print(result)
            if t.token.tag in EXPRESSIONS:
                self.symbolTable["IT"] = {
                    "varValue": result, "varType": self.getVariableDataType(result)}

        return

    def visit_SwitchCaseStatement(self, node):
        for c in node.codeBlockList:
            if c.token.tag == "TT_DEFAULT_CASE_BLOCK" or self.symbolTable["IT"]["varValue"] == self.visit(c.literalValue):
                if not self.visit_SwitchCaseCodeBlock(c):
                    break

    def visit_SwitchCaseCodeBlock(self, node):
        for c in node.codeBlockUnit:
            if c.token.tag == "TT_BREAK":
                return False
            result = self.visit(c)
            # print(result)
            if c.token.tag in EXPRESSIONS:
                self.symbolTable["IT"] = {
                    "varValue": result, "varType": self.getVariableDataType(result)}
        return True
    
    def visit_Visible(self, node):
        concatenated = ""
        for o in node.operandList:
            concatenated += str(self.visit(o))
        print(concatenated)

    def visit_NoneType(self, node):
        return

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
        return str(node.value).replace("\"", "")


tokens = lexer(readSourceCode("LOLCODE_example/bestcase.lol"))
# pp.pprint(tokens)

myParser = Parser(tokens)
myParser.run()

if myParser:
    myInterpreter = Interpreter(myParser)
    # print(tokens)

    # pp.pprint(myParser.trees)

    myInterpreter()
    # pp.pprint(myInterpreter.symbolTable)
