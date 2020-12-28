from tkinter import simpledialog
from constants import *


class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.symbolTable = {"IT": {"varValue": None, "varType": "NOOB"}}
        self.errorOccured = False
        self.window = None

    def __call__(self, window):
        self.window = window
        for t in self.parser.trees:
            result = self.visit(t)
            # print(result)
            if t.token.tag in EXPRESSIONS:
                self.symbolTable["IT"] = {
                    "varValue": result, "varType": self.getValueDataType(result)}

    def printTree(self, node):
        if hasattr(node, 'left'):
            self.printTree(node.left)
        if hasattr(node, 'right'):
            self.printTree(node.right)
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
                varType = self.getValueDataType(val)

        self.symbolTable[node.varObj.name] = {
            "varValue": val, "varType": varType}

        return self.symbolTable[node.varObj.name]

    def visit_Variable(self, node):
        if not self.isExistingVariable(node.name):
            print("ERROR: variable does not exist")
            return

        return self.symbolTable[node.name]["varValue"]

    def getValueDataType(self, val):
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
                varType = self.getValueDataType(val)

            self.symbolTable[node.left.name] = {
                "varValue": val, "varType": varType}
            return self.symbolTable[node.left.name]

    def visit_InfOp(self, node):
        if node.token.tag == "TT_INFINITY_CONCAT":
            if not node.child:
                result = self.visit(node.value)
                if self.getValueDataType(result) == "TROOF":
                    result = self.pythonBoolToLolCode(result)

                return str(result)
            else:
                result = self.visit(node.value)
                if self.getValueDataType(result) == "TROOF":
                    result = self.pythonBoolToLolCode(result)

                return result + self.visit_InfOp(node.child)
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
                    "varValue": result, "varType": self.getValueDataType(result)}

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
                    "varValue": result, "varType": self.getValueDataType(result)}
        return True

    def visit_Visible(self, node):
        concatenated = ""
        for o in node.operandList:
            result = self.visit(o)

            if result == None:
                continue

            if self.getValueDataType(result) == "TROOF":
                result = self.pythonBoolToLolCode(result)
            concatenated += str(result)
        
        if concatenated:
            print(concatenated)

    def visit_Gimmeh(self, node):
        if not self.isExistingVariable(node.variable.name):
            print("ERROR: uninitialized variable")
            return
        
        newValue = simpledialog.askstring("Input", "GIMMEH encountered", parent=self.window)
        
        if newValue in ("WIN", "FAIL"):
            newValue = self.lolCodeBoolToPython(newValue)
        else:
            try:
                newValue = float(newValue)
                if newValue.is_integer():
                    newValue = int(newValue)
            except:
                print("")
    
        self.symbolTable[node.variable.name] = {"varValue": newValue, "varType": self.getValueDataType(newValue)}
 
    def visit_NoneType(self, node):
        return

    def visit_Num(self, node):
        if node.token.tag == "TT_NUMBR":
            return int(node.value)
        elif node.token.tag == "TT_NUMBAR":
            return float(node.value)

    def visit_Bool(self, node):
        return self.lolCodeBoolToPython(node.value)

    def pythonBoolToLolCode(self, value):
        if value == True:
            return "WIN"
        elif value == False:
            return "FAIL"

    def lolCodeBoolToPython(self, value):
        if value == "WIN":
            return True
        elif value == "FAIL":
            return False

    def visit_String(self, node):
        return str(node.value).replace("\"", "")
