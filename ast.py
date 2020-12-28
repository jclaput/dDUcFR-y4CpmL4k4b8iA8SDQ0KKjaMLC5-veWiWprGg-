class AST:
    def __init__(self):
        pass


class InfOp(AST):
    def __init__(self, op, child):
        self.token = op
        self.op = op
        self.child = child
        self.value = None


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = op
        self.op = op
        self.right = right


class UnOp(AST):
    def __init__(self, operator, operand):
        self.token = operator
        self.operator = operator
        self.operand = operand


class VariableDeclaration(AST):
    def __init__(self, token, varObj, varValue):
        self.token = token
        self.varObj = varObj
        self.varValue = varValue


class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value


class IfElseStatement(AST):
    def __init__(self, token, trueCodeBlock, falseCodeBlock):
        self.token = token
        self.trueCodeBlock = trueCodeBlock
        self.falseCodeBlock = falseCodeBlock


class SwitchCaseStatement(AST):
    def __init__(self, token, codeBlockList):
        self.token = token
        self.codeBlockList = codeBlockList


class SwitchCaseCodeBlock(AST):
    def __init__(self, token, literalValue, codeBlockUnit):
        self.token = token
        self.literalValue = literalValue
        self.codeBlockUnit = codeBlockUnit

class BreakStatement(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Num:
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Bool:
    def __init__(self, token):
        self.token = token
        self.value = token.value


class String:
    def __init__(self, token):
        self.token = token
        self.value = token.value
