from ast import *

ARITHMETIC_BINARY_OPERATIONS = ("TT_ADD", "TT_SUB", "TT_MUL", "TT_DIV", "TT_MOD", "TT_MAX", "TT_MIN")
BOOLEAN_BINARY_OPERATIONS = ("TT_AND", "TT_OR", "TT_XOR")
COMPARISON_OPERATIONS = ("TT_EQUAL", "TT_NOT_EQUAL")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.currentToken = self.tokens[self.pos]
        self.trees = []

    def advance(self):
        self.pos += 1
        self.currentToken = self.tokens[self.pos]

    def parseArithmeticBinaryOperation(self):
        # <add> ::= SUM OF <expression> AN <expression>
        # <sub> ::= DIFF OF <expression> AN <expression>
        # <mul> ::= PRODUKT OF <expression> AN <expression>
        # <div> ::= QUOSHUNT OF <expression> AN <expression>
        # <mod> ::= MOD OF <expression> AN <expression>
        # <max> ::= BIGGR OF <expression> AN <expression>
        # <min> ::= SMALLR OF <expression> AN <expression>

        node = self.currentToken

        # point to the next token
        self.advance()

        if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
            left = Num(self.currentToken)
        elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
            left = self.parseArithmeticBinaryOperation()
        else:
            print("ERROR: Expected an arithmetic expression")
            return

        # point to the next token
        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUCTOR":
            print("ERROR: Expected AN")
            return

        # point to the next token
        self.advance()

        if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
            right = Num(self.currentToken)
        elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
            right = self.parseArithmeticBinaryOperation()
        else:
            print("ERROR: Expected an arithmetic expression")
            return

        return BinOp(left, node, right)


    def parseBooleanBinaryOperation(self):
        # <and> ::= BOTH OF <expression> AN <expression>
        # <or> ::= EITHER OF <expression> AN <expression>
        # <xor> ::= WON OF <expression> AN <expression>

        node = self.currentToken

        # point to the next token
        self.advance()

        if self.currentToken.tag == "TT_TROOF":
            left = Bool(self.currentToken)
        elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
            left = self.parseBooleanBinaryOperation()
        else:
            print("ERROR: Expected an boolean expression")
            return

        # point to the next token
        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUCTOR":
            print("ERROR: Expected AN")
            return

        # point to the next token
        self.advance()

        if self.currentToken.tag == "TT_TROOF":
            right = Bool(self.currentToken)
        elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
            right = self.parseBooleanBinaryOperation()
        else:
            print("ERROR: Expected an boolean expression")
            return


        return BinOp(left, node, right)

    def run(self):
        while self.currentToken.tag != "TT_END_OF_FILE":
            if self.currentToken.tag == "TT_DELIMITER":
                self.advance()
                continue
            if self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
                self.trees.insert(0, self.parseArithmeticBinaryOperation())
            elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                self.trees.insert(0, self.parseBooleanBinaryOperation())
            else:
                print("ERROR: cannot parse %s" % repr(self.currentToken))
                return

            self.advance()
