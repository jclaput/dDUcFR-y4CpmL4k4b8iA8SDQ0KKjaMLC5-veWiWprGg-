class AST:
    def __init__(self):
        pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = op
        self.op = op
        self.right = right


class Num:
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Bool:
    def __init__(self, token):
        self.token = token
        self.value = token.value
