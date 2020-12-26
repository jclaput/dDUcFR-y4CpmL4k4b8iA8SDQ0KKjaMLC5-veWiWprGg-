from constants import *
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
        elif self.currentToken.tag == "TT_IDENTIFIER":
            left = Variable(self.currentToken)
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
        elif self.currentToken.tag == "TT_IDENTIFIER":
            right = Variable(self.currentToken)
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
            left = self.parseNotUnaryOperation()
        elif self.currentToken.tag == "TT_IDENTIFIER":
            left = Variable(self.currentToken) 
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
            right = self.parseNotUnaryOperation()
        elif self.currentToken.tag == "TT_IDENTIFIER":
            right = Variable(self.currentToken) 
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
        elif self.currentToken.tag == "TT_IDENTIFIER":
            left = Variable(self.currentToken) 
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
        elif self.currentToken.tag == "TT_IDENTIFIER":
            right = Variable(self.currentToken) 
        else:
            print("ERROR: Expected a valid expression")
            return

        return BinOp(left, node, right)

    def parseAndOrInfiniteOperation(self):
        # <all_of> ::= ALL OF <expression> AN <mult_expression> MKAY
        # <any_of> ::= ANY OF <expression> AN <mult_expression> MKAY

        node = self.currentToken
        result = InfOp(node, None)
        currentChild = result

        node = self.currentToken
        result = InfOp(node, None)
        currentChild = result

        self.advance()

        if self.currentToken.tag == "TT_TROOF":
            currentChild.value = Bool(self.currentToken)
        elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
            currentChild.value = self.parseBooleanBinaryOperation()
        elif self.currentToken.tag in COMPARISON_OPERATIONS:
            currentChild.value = self.parseComparisonBinaryOperation()
        elif self.currentToken.tag == "TT_NOT":
            currentChild.value = self.parseNotUnaryOperation()
        elif self.currentToken.tag == "TT_IDENTIFIER":
            currentChild.value = Variable(self.currentToken) 


        currentChild.child = InfOp(node, None)
        currentChild = currentChild.child

        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
            print("ERROR: Expected AN")
            return

        self.advance()

        if self.currentToken.tag == "TT_TROOF":
            currentChild.value = Bool(self.currentToken)
        elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
            currentChild.value = self.parseBooleanBinaryOperation()
        elif self.currentToken.tag in COMPARISON_OPERATIONS:
            currentChild.value = self.parseComparisonBinaryOperation()
        elif self.currentToken.tag == "TT_NOT":
            currentChild.value = self.parseNotUnaryOperation()
        elif self.currentToken.tag == "TT_IDENTIFIER":
            currentChild.value = Variable(self.currentToken) 


        self.advance()

        while self.currentToken.tag not in ("TT_DELIMITER, TT_MULT_ARITY_ENDER"):
            if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
                print("ERROR: Expected AN")
                return

            self.advance()

            currentChild.child = InfOp(node, None)
            currentChild = currentChild.child

            if self.currentToken.tag == "TT_TROOF":
                currentChild.value = Bool(self.currentToken)
            elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                currentChild.value = self.parseBooleanBinaryOperation()
            elif self.currentToken.tag in COMPARISON_OPERATIONS:
                currentChild.value = self.parseComparisonBinaryOperation()
            elif self.currentToken.tag == "TT_NOT":
                currentChild.value = self.parseNotUnaryOperation()
            elif self.currentToken.tag == "TT_IDENTIFIER":
                currentChild.value = Variable(self.currentToken) 


            self.advance()

        if self.currentToken.tag == "TT_DELIMITER":
            print("ERROR: Expected MKAY")
            return

        if not currentChild.value:
            print("ERROR: Expected an valid expression")
            return

        return result

    def parseSmoosh(self):
        # <concatenation> ::=
        #   SMOOSH <expression> AN <mult_expression> | SMOOSH <expression> AN <mult_expression> MKAY |
        #   SMOOSH <expression> | SMOOSH <expression> MKAY

        node = self.currentToken
        result = InfOp(node, None)
        currentChild = result

        self.advance()

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
        elif self.currentToken.tag == "TT_IDENTIFIER":
            currentChild.value = Variable(self.currentToken) 


        currentChild.child = InfOp(node, None)
        currentChild = currentChild.child

        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
            print("ERROR: Expected AN")
            return

        self.advance()

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
        elif self.currentToken.tag == "TT_IDENTIFIER":
            currentChild.value = Variable(self.currentToken) 

        self.advance()

        while self.currentToken.tag not in ("TT_DELIMITER, TT_MULT_ARITY_ENDER"):
            if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
                print("ERROR: Expected AN")
                return

            self.advance()

            currentChild.child = InfOp(node, None)
            currentChild = currentChild.child

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
            elif self.currentToken.tag == "TT_IDENTIFIER":
                currentChild.value = Variable(self.currentToken) 

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
        elif self.currentToken.tag == "TT_IDENTIFIER":
            operand = Variable(self.currentToken) 
        else:
            print("ERROR: Expected an boolean expression")
            return

        return UnOp(node, operand)

    def parseVariableDeclaration(self):
        # <declaration> ::= I HAS A variadent | I HAS A variadent ITZ <expression>

        node = self.currentToken
        varObj = None
        varValue = None

        self.advance()

        if self.currentToken.tag != "TT_IDENTIFIER":
            print("ERROR: expected a variable identifier")
            return

        varObj = Variable(self.currentToken)

        self.advance()

        if self.currentToken.tag != "TT_DELIMITER":
            if self.currentToken.tag != "TT_VAR_ASSIGNMENT":
                print("ERROR: expected ITZ")
                return

            self.advance()

            if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
                varValue = Num(self.currentToken)
            elif self.currentToken.tag == "TT_TROOF":
                varValue = Bool(self.currentToken)
            elif self.currentToken.tag == "TT_YARN":
                varValue = String(self.currentToken)
            elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
                varValue = self.parseArithmeticBinaryOperation()
            elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                varValue = self.parseBooleanBinaryOperation()
            elif self.currentToken.tag in COMPARISON_OPERATIONS:
                varValue = self.parseComparisonBinaryOperation()
            elif self.currentToken.tag == "TT_NOT":
                varValue = self.parseNotUnaryOperation()
            elif self.currentToken.tag == "TT_IDENTIFIER":
                varValue = Variable(self.currentToken)
            else:
                print("ERROR: expected a valid expression")
                return

        return VariableDeclaration(node, varObj, varValue)

    def parseVariable(self):
        # <assignment> ::= variadent R <expression>

        left = Variable(self.currentToken)
        self.advance()

        if self.currentToken.tag == "TT_DELIMITER":
            return left

        if self.currentToken.tag != "TT_ASSIGN_TO_VAR":
            print("ERROR: expected R")
            return

        node = self.currentToken

        self.advance()

        if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
            right = Num(self.currentToken)
        elif self.currentToken.tag == "TT_TROOF":
            right = Bool(self.currentToken)
        elif self.currentToken.tag == "TT_YARN":
            right = String(self.currentToken)
        elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
            right = self.parseArithmeticBinaryOperation()
        elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
            right = self.parseBooleanBinaryOperation()
        elif self.currentToken.tag in COMPARISON_OPERATIONS:
            right = self.parseComparisonBinaryOperation()
        elif self.currentToken.tag == "TT_NOT":
            right = self.parseNotUnaryOperation()
        elif self.currentToken.tag == "TT_IDENTIFIER":
            right = Variable(self.currentToken)
        else:
            print("ERROR: expected a valid expression")
            return

        return BinOp(left, node, right)

    def parseIfElseStatement(self):
        # <if_then_statement> ::= O RLY? <linebreak> YA RLY <linebreak> <code_block> <linebreak> OIC | O RLY? <linebreak> YA RLY <linebreak> <code_block> <linebreak> <else_statement> <linebreak> OIC
        node = self.currentToken
        trueCodeBlock = []
        falseCodeBlock = None

        self.advance()
        

        while self.currentToken.tag == "TT_DELIMITER":
            self.advance()
            if self.currentToken.tag == "TT_END_OF_FILE":
                print("ERROR: expected YA RLY")
                return

        if self.currentToken.tag != "TT_IF_BLOCK":
            print("ERROR: expected YA RLY")
            return
        
        self.advance()

        while self.currentToken.tag == "TT_DELIMITER":
            self.advance()
            if self.currentToken.tag == "TT_END_OF_FILE":
                print("ERROR: expected a valid expression or statement")
                return

        while self.currentToken.tag not in ("TT_IF_SWITCH_END", "TT_ELSE_BLOCK"):
            if self.currentToken.tag == "TT_DELIMITER":
                self.advance()
                continue

            if self.currentToken.tag == "TT_END_OF_FILE":
                print("ERROR: expected NO WAI or OIC")
                return

            if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
                trueCodeBlock.append(Num(self.currentToken))
            elif self.currentToken.tag == "TT_TROOF":
                trueCodeBlock.append(Bool(self.currentToken))
            elif self.currentToken.tag == "TT_YARN":
                trueCodeBlock.append(String(self.currentToken))
            elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
                trueCodeBlock.append(self.parseArithmeticBinaryOperation())
            elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                trueCodeBlock.append(self.parseBooleanBinaryOperation())
            elif self.currentToken.tag in COMPARISON_OPERATIONS:
                trueCodeBlock.append(self.parseComparisonBinaryOperation())
            elif self.currentToken.tag == "TT_NOT":
                trueCodeBlock.append(self.parseNotUnaryOperation())
            elif self.currentToken.tag == "TT_IDENTIFIER":
                trueCodeBlock.append(self.parseVariable())
            else:
                print("ERROR: expected a valid expression or statement")
                return
        
            self.advance()


        if self.currentToken.tag == "TT_ELSE_BLOCK":
            self.advance()
            falseCodeBlock = []
            while self.currentToken.tag != "TT_IF_SWITCH_END":
                if self.currentToken.tag == "TT_DELIMITER":
                    self.advance()
                    continue

                if self.currentToken.tag == "TT_END_OF_FILE":
                    print("ERROR: expected OIC")
                    return

                if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
                    falseCodeBlock.append(Num(self.currentToken))
                elif self.currentToken.tag == "TT_TROOF":
                    falseCodeBlock.append(Bool(self.currentToken))
                elif self.currentToken.tag == "TT_YARN":
                    falseCodeBlock.append(String(self.currentToken))
                elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
                    falseCodeBlock.append(self.parseArithmeticBinaryOperation())
                elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                    falseCodeBlock.append(self.parseBooleanBinaryOperation())
                elif self.currentToken.tag in COMPARISON_OPERATIONS:
                    falseCodeBlock.append(self.parseComparisonBinaryOperation())
                elif self.currentToken.tag == "TT_NOT":
                    falseCodeBlock.append(self.parseNotUnaryOperation())
                elif self.currentToken.tag == "TT_IDENTIFIER":
                    falseCodeBlock.append(self.parseVariable())
                else:
                    print("ERROR: expected a valid expression or statement")
                    return
        
                self.advance()
            
            if not falseCodeBlock:
                print("ERROR: expected a valid expression or statement")
                return
        
        return IfElseStatement(node, trueCodeBlock, falseCodeBlock)

        
    def run(self):
        while self.currentToken.tag != "TT_END_OF_FILE":
            if self.currentToken.tag == "TT_DELIMITER":
                self.advance()
                continue
            if self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
                self.trees.append(self.parseArithmeticBinaryOperation())
            elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                self.trees.append(self.parseBooleanBinaryOperation())
            elif self.currentToken.tag in COMPARISON_OPERATIONS:
                self.trees.append(self.parseComparisonBinaryOperation())
            elif self.currentToken.tag == "TT_NOT":
                self.trees.append(self.parseNotUnaryOperation())
            elif self.currentToken.tag in INFINITE_ARITY_OPERATIONS:
                self.trees.append(self.parseAndOrInfiniteOperation())
            elif self.currentToken.tag == "TT_INFINITY_CONCAT":
                self.trees.append(self.parseSmoosh())
            elif self.currentToken.tag == "TT_VAR_DECLARATION":
                self.trees.append(self.parseVariableDeclaration())
            elif self.currentToken.tag == "TT_IDENTIFIER":
                self.trees.append(self.parseVariable())
            elif self.currentToken.tag == "TT_IF_START":
                self.trees.append(self.parseIfElseStatement())
            else:
                print("ERROR: cannot parse %s" % repr(self.currentToken))
                return

            self.advance()
