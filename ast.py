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
