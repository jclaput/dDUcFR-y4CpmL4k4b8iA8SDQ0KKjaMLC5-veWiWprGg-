from ast import *

ARITHMETIC_BINARY_OPERATIONS = ("TT_ADD", "TT_SUB", "TT_MUL", "TT_DIV", "TT_MOD", "TT_MAX", "TT_MIN")
BOOLEAN_BINARY_OPERATIONS = ("TT_AND", "TT_OR", "TT_XOR")
COMPARISON_OPERATIONS = ("TT_EQUAL", "TT_NOT_EQUAL")
INFINITE_ARITY_OPERATIONS = ("TT_INFINITY_OR", "TT_INFINITY_AND")

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




        if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
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
        elif self.currentToken.tag == "TT_NOT":
            left = self.parseNotUnaryOperation() # check if this will work
        else:
            print("ERROR: Expected an boolean expression")
            return

        # point to the next token
        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
            print("ERROR: Expected AN")
            return

        # point to the next token
        self.advance()

        if self.currentToken.tag == "TT_TROOF":
            right = Bool(self.currentToken)
        elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
            right = self.parseBooleanBinaryOperation()
        elif self.currentToken.tag == "TT_NOT":
            right = self.parseNotUnaryOperation() # check if this will work
        else:
            print("ERROR: Expected an boolean expression")
            return

        return BinOp(left, node, right)

    def parseComparisonBinaryOperation(self):
        # <is_equal> ::= BOTH SAEM <expression> AN <expression>
        # <is_not_equal> ::= DIFFRINT <expression> AN <expression>

        node = self.currentToken

        # point to the next token
        self.advance()

        if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
            left = Num(self.currentToken)
        elif self.currentToken.tag == "TT_TROOF":
            left = Bool(self.currentToken)
        elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
            left = self.parseArithmeticBinaryOperation()
        elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
            left = self.parseBooleanBinaryOperation()
        elif self.currentToken.tag in COMPARISON_OPERATIONS:
            left = self.parseComparisonBinaryOperation()
        elif self.currentToken.tag == "TT_NOT":
            left = self.parseNotUnaryOperation()
        else:
            print("ERROR: Expected a valid expression")
            return

        # point to the next token
        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
            print("ERROR: Expected AN")
            return

        # point to the next token
        self.advance()

        if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
            right = Num(self.currentToken)
        elif self.currentToken.tag == "TT_TROOF":
            right = Bool(self.currentToken)
        elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
            right = self.parseArithmeticBinaryOperation()
        elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
            right = self.parseBooleanBinaryOperation()
        elif self.currentToken.tag in COMPARISON_OPERATIONS:
            right = self.parseComparisonBinaryOperation()
        elif self.currentToken.tag == "TT_NOT":
            right = self.parseNotUnaryOperation()
        else:
            print("ERROR: Expected a valid expression")
            return

        return BinOp(left, node, right)

    def parseSmoosh(self):
        # <concatenation> ::= SMOOSH <expression> AN <mult_expression> | SMOOSH <expression> AN <mult_expression> MKAY

        node = self.currentToken
        result = InfOp(node, None)
        currentChild = result

        self.advance()


        while True:
            if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
                currentChild.value = Num(self.currentToken)
            elif self.currentToken.tag == "TT_TROOF":
                currentChild.value = Bool(self.currentToken)
            elif self.currentToken.tag == "TT_YARN":
                currentChild.value = String(self.currentToken)
            elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
                currentChild.value = self.parseArithmeticBinaryOperation()
            elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                currentChild.value = self.parseBooleanBinaryOperation()
            elif self.currentToken.tag in COMPARISON_OPERATIONS:
                currentChild.value = self.parseComparisonBinaryOperation()
            elif self.currentToken.tag == "TT_NOT":
                currentChild.value = self.parseNotUnaryOperation()

            self.advance()

            if self.currentToken.tag in ("TT_DELIMITER, TT_MULT_ARITY_ENDER"):
                break

            if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
                print("ERROR: Expected AN")
                return

            currentChild.child = InfOp(node, None)
            currentChild = currentChild.child

            self.advance()

        if not currentChild.value:
            print("ERROR: Expected an valid expression")
            return

        return result


    def parseNotUnaryOperation(self):
        # <not> ::= NOT <expression>

        node = self.currentToken
        self.advance()

        if self.currentToken.tag == "TT_TROOF":
            operand = Bool(self.currentToken)
        elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
            operand = self.parseBooleanBinaryOperation()
        elif self.currentToken.tag == "TT_NOT":
            operand = self.parseNotUnaryOperation()
        else:
            print("ERROR: Expected an boolean expression")
            return

        return UnOp(node, operand)

    def run(self):
        while self.currentToken.tag != "TT_END_OF_FILE":
            if self.currentToken.tag == "TT_DELIMITER":
                self.advance()
                continue
            if self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
                self.trees.insert(0, self.parseArithmeticBinaryOperation())
            elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                self.trees.insert(0, self.parseBooleanBinaryOperation())
            elif self.currentToken.tag in COMPARISON_OPERATIONS:
                self.trees.insert(0, self.parseComparisonBinaryOperation())
            elif self.currentToken.tag == "TT_NOT":
                self.trees.insert(0, self.parseNotUnaryOperation())
            elif self.currentToken.tag == "TT_INFINITY_CONCAT":
                self.trees.insert(0, self.parseSmoosh())
            else:
                print("ERROR: cannot parse %s" % repr(self.currentToken))
                return

            self.advance()
