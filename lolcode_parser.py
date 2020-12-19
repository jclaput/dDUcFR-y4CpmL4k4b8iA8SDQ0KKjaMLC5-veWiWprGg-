
class Parser:
    def __init__(self, tokens):
        self.index = 0
        self.tokens = tokens
        self.classificationFunctionTable = { "Addition Operator" : self.sumOf }

    def advance(self):
        self.index += 1
        return self.tokens[self.index]

    def run(self):
        if self.getCurrentToken().value != "HAI":
            print("Error: expected HAI")
            return

        self.advance()

        while self.getCurrentToken().classification != "End-Of-File":
            if self.getCurrentToken().classification in ("Linebreak", "Delimiter"):
                self.advance()
                continue

            result = self.classificationFunctionTable[self.getCurrentToken().classification]()

            print(result)

            if result is None:
                print("Parsing Failure")
                return

            self.advance()


    def getCurrentToken(self):
        return self.tokens[self.index]

    def sumOf(self):
        nextToken = self.advance()
        left = None
        right = None

        if nextToken.classification in ("YARN Literal", "TROOF Literal"):
            print("Error: expected NUMBR or NUMBAR data type")
            return
        elif nextToken.classification in ("NUMBR Literal", "NUMBAR Literal"):
            left = nextToken.value
        elif nextToken.classification in \
        ("Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator",
        "Max Operator", "Min Operator"):

            left = self.classificationFunctionTable[nextToken.classification]()
        else:
            print("Error: expected arithmetic expression after SUM OF")
            return

        nextToken = self.advance()

        if nextToken.value != "AN":
            print("Error: expected AN")
            return
        else:
            nextToken = self.advance()



        if nextToken.classification in ("YARN Literal", "TROOF Literal"):
            print("Error: expected NUMBR or NUMBAR data type")
            return
        elif nextToken.classification in ("NUMBR Literal", "NUMBAR Literal"):
            right = nextToken.value
        elif nextToken.classification in (
        "Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator",
        "Max Operator", "Min Operator"):
            right = self.classificationFunctionTable[right.value]()
        else:
            print("Error: expected arithmetic expression")
            return

        return int(left) + int(right)
