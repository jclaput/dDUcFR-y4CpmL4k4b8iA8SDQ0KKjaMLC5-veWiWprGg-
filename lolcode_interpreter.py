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
            # print(t)
            # print(t.token)
            result = self.visit(t)
            # print(result)
            
            if t.token.tag in EXPRESSIONS:
                self.symbolTable["IT"] = {
                    "varValue": result, "varType": self.getValueDataType(result)}

    def printTree(self, node):
        # For diagnostics or debugging
        if hasattr(node, 'left'):
            self.printTree(node.left)
        if hasattr(node, 'right'):
            self.printTree(node.right)
        print(repr(node.token))

    def visit(self, node):
        # Each AST node has a corresponding method when visited
        # eg. AST node of type Visible. Invoking self.visit(node) will call visit_Visible(self, node)
        methodName = 'visit_' + type(node).__name__
        visitor = getattr(self, methodName)
        return visitor(node)

    def visit_VariableDeclaration(self, node):
        val = None
        varType = "NOOB"

        if node.varObj.name == "IT":
            raise Exception("ERROR: cannot use implicit variable IT")

        if self.isExistingVariable(node.varObj.name):
            raise Exception("ERROR: variable %s already exists" % node.varObj.name)

        if node.varValue:  # Variable token has a value, meaning its data type is not NOOB
            val = self.visit(node.varValue)

            if val:
                varType = self.getValueDataType(val)

        self.symbolTable[node.varObj.name] = {
            "varValue": val, "varType": varType}

        return self.symbolTable[node.varObj.name]

    def visit_Variable(self, node):
        if not self.isExistingVariable(node.name):
            raise Exception("ERROR: variable %s does not exist" % node.name)

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
                # Check if correct data type usage
                if self.getValueDataType(self.visit(node.left)) not in ("NUMBR", "NUMBAR") or self.getValueDataType(self.visit(node.right)) not in ("NUMBR", "NUMBAR"):
                    raise TypeError

                result = self.visit(node.left) + self.visit(node.right)
                hasNumbar = False

                try:
                    # Check if atleast one of the operands is a NUMBAR
                    hasNumbar = self.getValueDataType(self.implicitCastNum(self.visit(node.left))) == "NUMBAR" or self.getValueDataType(self.implicitCastNum(self.visit(node.right))) == "NUMBAR"
                except:
                    print("")

                if hasNumbar == False:
                    result = int(result)
                    
                return result
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected NUMBR or NUMBAR for SUM OF")
            return
        if node.token.tag == "TT_SUB":
            try:
                # Check if correct data type usage
                if self.getValueDataType(self.visit(node.left)) not in ("NUMBR", "NUMBAR") or self.getValueDataType(self.visit(node.right)) not in ("NUMBR", "NUMBAR"):
                    raise TypeError

                result = self.visit(node.left) - self.visit(node.right)
                hasNumbar = False

                try:
                    # Check if atleast one of the operands is a NUMBAR
                    hasNumbar = self.getValueDataType(self.implicitCastNum(self.visit(node.left))) == "NUMBAR" or self.getValueDataType(self.implicitCastNum(self.visit(node.right))) == "NUMBAR"
                except:
                    print("")

                if hasNumbar == False:
                    result = int(result)
                return result
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected NUMBR or NUMBAR for DIFF OF")
            return
        if node.token.tag == "TT_MUL":
            try:
                # Check if correct data type usage
                if self.getValueDataType(self.visit(node.left)) not in ("NUMBR", "NUMBAR") or self.getValueDataType(self.visit(node.right)) not in ("NUMBR", "NUMBAR"):
                    raise TypeError

                result = self.visit(node.left) * self.visit(node.right)
                hasNumbar = False

                try:
                    # Check if atleast one of the operands is a NUMBAR
                    hasNumbar = self.getValueDataType(self.implicitCastNum(self.visit(node.left))) == "NUMBAR" or self.getValueDataType(self.implicitCastNum(self.visit(node.right))) == "NUMBAR"
                except:
                    print("")

                if hasNumbar == False:
                    result = int(result)
                return result
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected NUMBR or NUMBAR for PRODUKT OF")
            return
        if node.token.tag == "TT_DIV":
            try:
                # Check if correct data type usage
                if self.getValueDataType(self.visit(node.left)) not in ("NUMBR", "NUMBAR") or self.getValueDataType(self.visit(node.right)) not in ("NUMBR", "NUMBAR"):
                    raise TypeError
                result = self.visit(node.left) / self.visit(node.right)
                return result
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected NUMBR or NUMBAR for DIV OF")
            except ZeroDivisionError:
                raise Exception("ERROR: division by zero")

            return
        if node.token.tag == "TT_MOD":
            try:
                # Check if correct data type usage
                if self.getValueDataType(self.visit(node.left)) not in ("NUMBR", "NUMBAR") or self.getValueDataType(self.visit(node.right)) not in ("NUMBR", "NUMBAR"):
                    raise TypeError
                result = self.visit(node.left) % self.visit(node.right)
                return result
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected NUMBR or NUMBAR for MOD OF")

            return
        if node.token.tag == "TT_MAX":
            try:
                # Check if correct data type usage
                if self.getValueDataType(self.visit(node.left)) not in ("NUMBR", "NUMBAR") or self.getValueDataType(self.visit(node.right)) not in ("NUMBR", "NUMBAR"):
                    raise TypeError
                result = max(self.visit(node.left), self.visit(node.right))
                return result
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected NUMBR or NUMBAR for MAX OF")

            return

        if node.token.tag == "TT_MIN":
            try:
                # Check if correct data type usage
                if self.getValueDataType(self.visit(node.left)) not in ("NUMBR", "NUMBAR") or self.getValueDataType(self.visit(node.right)) not in ("NUMBR", "NUMBAR"):
                    raise TypeError
                result = min(self.visit(node.left), self.visit(node.right))
                return result
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected NUMBR or NUMBAR for MIN OF")

            return

        # Boolean Binary Operations
        if node.token.tag == "TT_AND":
            try:
                # Check if correct data type usage
                if self.getValueDataType(self.visit(node.left)) != "TROOF" or self.getValueDataType(self.visit(node.right)) != "TROOF":
                    raise TypeError
                return self.visit(node.left) and self.visit(node.right)
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected TROOF for BOTH OF")
            return
        if node.token.tag == "TT_XOR":
            try:
                # Check if correct data type usage
                if self.getValueDataType(self.visit(node.left)) != "TROOF" or self.getValueDataType(self.visit(node.right)) != "TROOF":
                    raise TypeError
                return self.visit(node.left) ^ self.visit(node.right)
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected TROOF for EITHER OF")
            return
        if node.token.tag == "TT_OR":
            try:
                # Check if correct data type usage
                if self.getValueDataType(self.visit(node.left)) != "TROOF" or self.getValueDataType(self.visit(node.right)) != "TROOF":
                    raise TypeError
                return self.visit(node.left) or self.visit(node.right)
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected TROOF for WON OF")
            return

        # Comparison Binary Operations
        if node.token.tag == "TT_EQUAL":
            try:
                return self.visit(node.left) == self.visit(node.right)
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected a valid expression for BOTH SAEM")
            return
        if node.token.tag == "TT_NOT_EQUAL":
            try:
                return self.visit(node.left) != self.visit(node.right)
            except TypeError:
                raise Exception("ERROR: Data type mismatch. Expected a valid expression for DIFFRINT")
            return

        # Variable Assignment Statement
        if node.token.tag == "TT_ASSIGN_TO_VAR":
            if not self.isExistingVariable(node.left.name):
                raise Exception("ERROR: variable %s does not exist" % node.left.name)

            val = self.visit(node.right)
            varType = "NOOB"

            if val:
                varType = self.getValueDataType(val)

            self.symbolTable[node.left.name] = {"varValue": val, "varType": varType}
            return self.symbolTable[node.left.name]

    def visit_InfOp(self, node):
        if node.token.tag == "TT_INFINITY_CONCAT":
            result = self.visit(node.value)

            if result == None:
                raise Exception("ERROR: cannot concatenate with a value of type NOOB")
            
            if self.getValueDataType(result) == "TROOF":
                result = self.pythonBoolToLolCode(result)

            # recursive call until it no longer has a child, meaning it has no more child to concatenate to
            if not node.child:
                return str(result)
            else:
                return str(result) + self.visit_InfOp(node.child)
        elif node.token.tag == "TT_INFINITY_OR":
            # recursive call until it no longer has a child, meaning it reached the last operand
            if not node.child:
                return self.visit(node.value)
            else:
                try:
                    return self.visit(node.value) or self.visit(node.child)
                except TypeError:
                    raise Exception("ERROR: Data type mismatch. Expected TROOF for ANY OF")
        elif node.token.tag == "TT_INFINITY_AND":
            # recursive call until it no longer has a child, meaning it reached the last operand
            if not node.child:
                return self.visit(node.value)
            else:
                try:
                    return self.visit(node.value) and self.visit(node.child)
                except TypeError:
                    raise Exception("ERROR: Data type mismatch. Expected TROOF for ALL OF")
        else:
            raise Exception("ERROR: %s is invalid" % node.token)

    def visit_IfElseStatement(self, node):
        whichCodeBlock = None
        
        if self.getValueDataType(self.symbolTable["IT"]["varValue"]) != "TROOF":
            raise Exception("ERROR: implicit IT variable must be in the form of TROOF to evaluate If-Else Statement")

        if self.symbolTable["IT"]["varValue"]:
            whichCodeBlock = node.trueCodeBlock
        else:
            whichCodeBlock = node.falseCodeBlock

        if not whichCodeBlock:
            raise Exception("ERROR: expected a codeblock")

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
                if self.visit_SwitchCaseCodeBlock(c) == False:
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
                raise Exception("ERROR: cannot print of type NOOB")

            if self.getValueDataType(result) == "TROOF":
                result = self.pythonBoolToLolCode(result)
            concatenated += str(result)
        
        if concatenated:
            print(concatenated)

    def visit_Gimmeh(self, node):
        if not self.isExistingVariable(node.variable.name):
            raise Exception("ERROR: uninitialized variable")
        
        newValue = simpledialog.askstring("Input", "GIMMEH encountered", parent=self.window)
        
        if newValue in ("WIN", "FAIL"):
            newValue = self.lolCodeBoolToPython(newValue)
        else:
            try:
                newValue = self.implicitCastNum(newValue)
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

    def implicitCastNum(self, value):
        newValue = float(value)
                
        if newValue.is_integer():
            newValue = int(newValue)
        
        return newValue

    def visit_String(self, node):
        return str(node.value).replace("\"", "")
