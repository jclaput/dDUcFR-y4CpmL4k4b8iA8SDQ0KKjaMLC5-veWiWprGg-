from constants import *
from ast import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.currentToken = self.tokens[self.pos]
        self.trees = []

    def __call__(self):
        self.run()

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
            raise Exception(repr(self.currentToken) + " ERROR: Expected an arithmetic expression")

        # point to the next token
        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
            raise Exception(repr(self.currentToken) + " ERROR: Expected AN")

        # point to the next token
        self.advance()

        if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
            right = Num(self.currentToken)
        elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
            right = self.parseArithmeticBinaryOperation()
        elif self.currentToken.tag == "TT_IDENTIFIER":
            right = Variable(self.currentToken)
        else:
            raise Exception(repr(self.currentToken) + " ERROR: Expected an arithmetic expression")

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
            raise Exception(repr(self.currentToken) + " ERROR: Expected an boolean expression")

        # point to the next token
        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
            raise Exception(repr(self.currentToken) + " ERROR: Expected AN")

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
            raise Exception(repr(self.currentToken) + " ERROR: Expected an boolean expression")

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
            raise Exception(repr(self.currentToken) + " ERROR: Expected a valid expression")

        # point to the next token
        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
            raise Exception(repr(self.currentToken) + " ERROR: Expected AN")

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
            raise Exception(repr(self.currentToken) + " ERROR: Expected a valid expression")

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
        else:
            raise Exception(repr(self.currentToken) + " ERROR: Expected a valid expression")

        currentChild.child = InfOp(node, None)
        currentChild = currentChild.child

        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
            raise Exception(repr(self.currentToken) + " ERROR: Expected AN")

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
        else:
            raise Exception(repr(self.currentToken) + " ERROR: Expected a valid expression")

        self.advance()

        while self.currentToken.tag not in ("TT_DELIMITER, TT_MULT_ARITY_ENDER"):
            if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
                raise Exception(repr(self.currentToken) + " ERROR: Expected AN")

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
            else:
                raise Exception(repr(self.currentToken) + " ERROR: Expected a valid expression")

            self.advance()

        if self.currentToken.tag == "TT_DELIMITER":
            raise Exception(repr(self.currentToken) + " ERROR: Expected MKAY")

        if not currentChild.value:
            raise Exception(repr(self.currentToken) + " ERROR: Expected an valid expression")

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
        else:
            raise Exception(repr(self.currentToken) + " ERROR: Expected a valid expression")

        currentChild.child = InfOp(node, None)
        currentChild = currentChild.child

        self.advance()

        if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
            raise Exception(repr(self.currentToken) + " ERROR: Expected AN")

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
        else:
            raise Exception(repr(self.currentToken) + " ERROR: Expected a valid expression")

        self.advance()

        while self.currentToken.tag not in ("TT_DELIMITER, TT_MULT_ARITY_ENDER, TT_SINGLE_COMMENT"):
            if self.currentToken.tag != "TT_MULT_ARITY_CONJUNCTOR":
                raise Exception(repr(self.currentToken) + " ERROR: Expected AN")

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
            else:
                raise Exception(repr(self.currentToken) + " ERROR: Expected a valid expression")

            self.advance()

        if not currentChild.value:
            raise Exception(repr(self.currentToken) + " ERROR: Expected an valid expression")

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
            raise Exception(repr(self.currentToken) + " ERROR: Expected an boolean expression")

        return UnOp(node, operand)

    def parseVariableDeclaration(self):
        # <declaration> ::= I HAS A variadent | I HAS A variadent ITZ <expression>

        node = self.currentToken
        varObj = None
        varValue = None

        self.advance()

        if self.currentToken.tag != "TT_IDENTIFIER":
            raise Exception(repr(self.currentToken) + " ERROR: expected a variable identifier")

        varObj = Variable(self.currentToken)

        self.advance()

        if self.currentToken.tag != "TT_DELIMITER":
            if self.currentToken.tag != "TT_VAR_ASSIGNMENT":
                raise Exception(repr(self.currentToken) + " ERROR: expected ITZ")

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
            elif self.currentToken.tag in INFINITE_ARITY_OPERATIONS:
                varValue = self.parseAndOrInfiniteOperation()
            elif self.currentToken.tag in COMPARISON_OPERATIONS:
                varValue = self.parseComparisonBinaryOperation()
            elif self.currentToken.tag == "TT_NOT":
                varValue = self.parseNotUnaryOperation()
            elif self.currentToken.tag == "TT_IDENTIFIER":
                varValue = Variable(self.currentToken)
            else:
                raise Exception(repr(self.currentToken) + " ERROR: expected a valid expression")

        return VariableDeclaration(node, varObj, varValue)

    def parseVariable(self):
        # <assignment> ::= variadent R <expression>

        left = Variable(self.currentToken)
        self.advance()

        if self.currentToken.tag in ("TT_DELIMITER"):
            return left

        if self.currentToken.tag != "TT_ASSIGN_TO_VAR":
            raise Exception(repr(self.currentToken) + " ERROR: expected R")

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
        elif self.currentToken.tag in INFINITE_ARITY_OPERATIONS:
            right = self.parseAndOrInfiniteOperation()
        elif self.currentToken.tag in COMPARISON_OPERATIONS:
            right = self.parseComparisonBinaryOperation()
        elif self.currentToken.tag == "TT_NOT":
            right = self.parseNotUnaryOperation()
        elif self.currentToken.tag == "TT_IDENTIFIER":
            right = Variable(self.currentToken)
        else:
            raise Exception(repr(self.currentToken) + " ERROR: expected a valid expression")

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
                raise Exception(repr(self.currentToken) + " ERROR: expected YA RLY")
        
        if self.currentToken.tag != "TT_IF_BLOCK":
            raise Exception(repr(self.currentToken) + " ERROR: expected YA RLY")

        self.advance()

        while self.currentToken.tag == "TT_DELIMITER":
            self.advance()
            if self.currentToken.tag == "TT_END_OF_FILE":
                raise Exception(repr(self.currentToken) + " ERROR: expected a valid expression or statement")

        while self.currentToken.tag not in ("TT_IF_SWITCH_END", "TT_ELSE_BLOCK"):
            if self.currentToken.tag == "TT_DELIMITER":
                self.advance()
                continue

            if self.currentToken.tag == "TT_END_OF_FILE":
                raise Exception(repr(self.currentToken) + " ERROR: expected NO WAI or OIC")

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
            elif self.currentToken.tag == "TT_PRINT":
                trueCodeBlock.append(self.parseVisible())
            elif self.currentToken.tag == "TT_INPUT":
                trueCodeBlock.append(self.parseGimmeh())
            else:
                raise Exception(repr(self.currentToken) + " ERROR: expected a valid expression or statement")

            self.advance()

        if self.currentToken.tag == "TT_ELSE_BLOCK":
            self.advance()
            falseCodeBlock = []
            while self.currentToken.tag != "TT_IF_SWITCH_END":
                if self.currentToken.tag == "TT_DELIMITER":
                    self.advance()
                    continue

                if self.currentToken.tag == "TT_END_OF_FILE":
                    raise Exception(repr(self.currentToken) + " ERROR: expected OIC")

                if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
                    falseCodeBlock.append(Num(self.currentToken))
                elif self.currentToken.tag == "TT_TROOF":
                    falseCodeBlock.append(Bool(self.currentToken))
                elif self.currentToken.tag == "TT_YARN":
                    falseCodeBlock.append(String(self.currentToken))
                elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
                    falseCodeBlock.append(
                        self.parseArithmeticBinaryOperation())
                elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                    falseCodeBlock.append(self.parseBooleanBinaryOperation())
                elif self.currentToken.tag in COMPARISON_OPERATIONS:
                    falseCodeBlock.append(
                        self.parseComparisonBinaryOperation())
                elif self.currentToken.tag == "TT_NOT":
                    falseCodeBlock.append(self.parseNotUnaryOperation())
                elif self.currentToken.tag == "TT_IDENTIFIER":
                    falseCodeBlock.append(self.parseVariable())
                elif self.currentToken.tag == "TT_PRINT":
                    falseCodeBlock.append(self.parseVisible())
                elif self.currentToken.tag == "TT_INPUT":
                    falseCodeBlock.append(self.parseGimmeh())
                else:
                    raise Exception(repr(self.currentToken) + " ERROR: expected a valid expression or statement")

                self.advance()

            if not falseCodeBlock:
                raise Exception(repr(self.currentToken) + " ERROR: expected a valid expression or statement")

        return IfElseStatement(node, trueCodeBlock, falseCodeBlock)

    def parseSwitchCaseStatement(self):
        # <switch> ::= WTF? <linebreak> <case> <linebreak> OMGWTF <code_block> <linebreak> OIC

        node = self.currentToken
        hasDefaultCase = False
        codeBlockList = []
        self.advance()

        while self.currentToken.tag == "TT_DELIMITER":
            self.advance()

            if self.currentToken.tag == "TT_END_OF_FILE":
                raise Exception(repr(self.currentToken) + " ERROR: expected WTF?")

        while self.currentToken.tag != "TT_IF_SWITCH_END":
            if self.currentToken.tag == "TT_DELIMITER":
                self.advance()
                continue
            
            if self.currentToken.tag == "TT_END_OF_FILE":
                raise Exception(repr(self.currentToken) + " ERROR: expected OIC")

            if self.currentToken.tag in ("TT_SWITCH_BLOCK", "TT_DEFAULT_CASE_BLOCK"):
                if self.currentToken.tag == "TT_DEFAULT_CASE_BLOCK":
                    if hasDefaultCase:
                        raise Exception(repr(self.currentToken) + " ERROR: cannot have multiple default cases")

                    hasDefaultCase = True
                else:
                    if hasDefaultCase:
                        raise Exception(repr(self.currentToken) + " ERROR: default case cannot be followed by another case")

                codeBlockList.append(self.parseSwitchCaseCodeBlock())
            else:
                raise Exception(repr(self.currentToken) + " ERROR: expected OMG or OMGWTF")

        if not codeBlockList:
            raise Exception(repr(self.currentToken) + " ERROR: must have atleast one OMG <literal>")

        return SwitchCaseStatement(node, codeBlockList)

    def parseSwitchCaseCodeBlock(self):
        # <case> ::= OMG <literal> <linebreak> <code_block> <linebreak> GTFO <case> | OMG <literal> <linebreak> <code_block> <linebreak> <case> |
        # OMG <literal> <linebreak> <code_block> <linebreak> GTFO |
        # OMG <literal> <linebreak> <code_block> <linebreak>

        node = self.currentToken
        literalValue = None
        codeBlockUnit = []
        self.advance()

        if node.tag == "TT_SWITCH_BLOCK" and self.currentToken.tag not in DATA_TYPES:
            raise Exception(repr(self.currentToken) + " ERROR: expected a literal")

        if self.currentToken.tag in ("TT_NUMBR", "TT_NUMBAR"):
            literalValue = Num(self.currentToken)
        elif self.currentToken.tag == "TT_TROOF":
            literalValue = Bool(self.currentToken)
        elif self.currentToken.tag == "TT_YARN":
            literalValue = String(self.currentToken)

        self.advance()

        while self.currentToken.tag == "TT_DELIMITER":
            self.advance()
            if self.currentToken.tag == "TT_END_OF_FILE":
                raise Exception(repr(self.currentToken) + " ERROR: expected a valid statement or expression")

        while self.currentToken.tag not in ("TT_SWITCH_BLOCK", "TT_DEFAULT_CASE_BLOCK", "TT_IF_SWITCH_END"):
            if self.currentToken.tag == "TT_DELIMITER":
                self.advance()
                continue

            if self.currentToken.tag == "TT_END_OF_FILE":
                raise Exception(repr(self.currentToken) + " ERROR: expected a valid statement or expression")

            if self.currentToken.tag in ("TT_NUMBR, TT_NUMBAR"):
                codeBlockUnit.append(Num(self.currentToken))
            elif self.currentToken.tag == "TT_TROOF":
                codeBlockUnit.append(Bool(self.currentToken))
            elif self.currentToken.tag == "TT_YARN":
                codeBlockUnit.append(String(self.currentToken))
            elif self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
                codeBlockUnit.append(self.parseArithmeticBinaryOperation())
            elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                codeBlockUnit.append(self.parseBooleanBinaryOperation())
            elif self.currentToken.tag in COMPARISON_OPERATIONS:
                codeBlockUnit.append(self.parseComparisonBinaryOperation())
            elif self.currentToken.tag == "TT_NOT":
                codeBlockUnit.append(self.parseNotUnaryOperation())
            elif self.currentToken.tag == "TT_IDENTIFIER":
                codeBlockUnit.append(self.parseVariable())
            elif self.currentToken.tag == "TT_PRINT":
                codeBlockUnit.append(self.parseVisible())
            elif self.currentToken.tag == "TT_INPUT":
                codeBlockUnit.append(self.parseGimmeh())
            elif self.currentToken.tag == "TT_BREAK":
                codeBlockUnit.append(BreakStatement(self.currentToken))
            else:
                raise Exception(repr(self.currentToken) + " ERROR: expected a valid statement or expression")

            self.advance()

        if not codeBlockUnit:
            raise Exception(repr(self.currentToken) + " ERROR: expected a valid statement or expression")

        return SwitchCaseCodeBlock(node, literalValue, codeBlockUnit)

    def parseVisible(self):
        # <output> ::= VISIBLE <expression>
        node = self.currentToken
        operandList = []

        self.advance()

        while self.currentToken.tag != "TT_DELIMITER":
            if self.currentToken.tag == "TT_END_OF_FILE":
                raise Exception(repr(self.currentToken) + " ERROR: expected a valid expression")

            if self.currentToken.tag in ARITHMETIC_BINARY_OPERATIONS:
                operandList.append(self.parseArithmeticBinaryOperation())
            elif self.currentToken.tag in BOOLEAN_BINARY_OPERATIONS:
                operandList.append(self.parseBooleanBinaryOperation())
            elif self.currentToken.tag in COMPARISON_OPERATIONS:
                operandList.append(self.parseComparisonBinaryOperation())
            elif self.currentToken.tag == "TT_NOT":
                operandList.append(self.parseNotUnaryOperation())
            elif self.currentToken.tag in INFINITE_ARITY_OPERATIONS:
                operandList.append(self.parseAndOrInfiniteOperation())
            elif self.currentToken.tag == "TT_INFINITY_CONCAT":
                operandList.append(self.parseSmoosh())
            elif self.currentToken.tag == "TT_VAR_DECLARATION":
                operandList.append(self.parseVariableDeclaration())
            elif self.currentToken.tag == "TT_IDENTIFIER":
                operandList.append(Variable(self.currentToken))
            elif self.currentToken.tag in ("TT_NUMBR", "TT_NUMBAR"):
                operandList.append(Num(self.currentToken))
            elif self.currentToken.tag in ("TT_TROOF"):
                operandList.append(Bool(self.currentToken))
            elif self.currentToken.tag in ("TT_YARN"):
                operandList.append(String(self.currentToken))
            else:
                raise Exception(repr(self.currentToken) + " ERROR: expected a valid expression")

            self.advance()

        if not operandList:
            raise Exception(repr(self.currentToken) + " ERROR: expected a valid expression")
        return Visible(node, operandList)

    def parseGimmeh(self):
        node = self.currentToken
        self.advance()

        if self.currentToken.tag != "TT_IDENTIFIER":
            raise Exception(repr(self.currentToken) + " ERROR: expected a valid identifier")
        
        return Gimmeh(node, Variable(self.currentToken))

    def handleMultiLineComment(self):
        while self.currentToken.tag not in ("TT_MULT_COMMENT_END", "TT_END_OF_FILE"):
            self.advance()

        if self.currentToken.tag != "TT_MULT_COMMENT_END":
            raise Exception(repr(self.currentToken) + " ERROR: expected TLDR")

        self.advance()

        if self.currentToken.tag != "TT_DELIMITER":
            raise Exception(repr(self.currentToken) + " ERROR: expected newline")

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
            elif self.currentToken.tag == "TT_SWITCH_START":
                self.trees.append(self.parseSwitchCaseStatement())
            elif self.currentToken.tag == "TT_PRINT":
                self.trees.append(self.parseVisible())
            elif self.currentToken.tag == "TT_INPUT":
                self.trees.append(self.parseGimmeh())
            elif self.currentToken.tag in ("TT_NUMBR", "TT_NUMBAR"):
                self.trees.append(Num(self.currentToken))
            elif self.currentToken.tag in ("TT_TROOF"):
                self.trees.append(Bool(self.currentToken))
            elif self.currentToken.tag in ("TT_YARN"):
                self.trees.append(String(self.currentToken))
            elif self.currentToken.tag == "TT_MULT_COMMENT_START":
                self.handleMultiLineComment()
            else:
                raise Exception("ERROR: cannot parse %s" %
                      repr(self.currentToken))

            self.advance()
