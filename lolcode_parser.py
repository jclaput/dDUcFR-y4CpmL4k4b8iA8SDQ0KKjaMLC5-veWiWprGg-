from ast import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.currentToken = self.tokens[self.pos]
        self.trees = []


    def advance(self):
        self.pos += 1
        self.currentToken = self.tokens[self.pos]

    def parse_sumOf(self):
        # <add> ::= SUM OF <expression> AN <expression>

        node = self.currentToken

        # point to the next token
        self.advance()

        if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
            left = Num(self.currentToken)
        elif self.currentToken.tag == "TT_ADD":
            left = self.parse_sumOf()
        else:
            print("ERROR: Expected an arithmetic expression")

        # point to the next token
        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUCTOR":
            print("ERROR: Expected AN")
            return

        # point to the next token
        self.advance()

        if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
            right = Num(self.currentToken)
        elif self.currentToken.tag == "TT_ADD":
            right = self.parse_sumOf()
        else:
            print("ERROR: Expected an arithmetic expression")
            return

        return BinOp(left, node, right)


    def run(self):
        while self.currentToken.tag != "TT_END_OF_FILE":
            if self.currentToken.tag == "TT_DELIMITER":
                self.advance()
                continue
            if self.currentToken.tag == "TT_ADD":
                self.trees.insert(0,self.parse_sumOf())

            self.advance()





