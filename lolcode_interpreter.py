import pprint
from lolcode_lexer import *
from lolcode_parser import *

def readSourceCode(filePath):
    try:
        sourceCode = open(filePath, "r")
    except FileNotFoundError:
        print("File Not Found Error!")
        sys.exit()

    sourceCodeString = sourceCode.read()
    sourceCode.close()

    # source code to string then return
    return sourceCodeString

pp = pprint.PrettyPrinter(indent = 4)

tokens = lexer(readSourceCode("LOLCODE_example/bestcase.lol"))
myParser = Parser(tokens)
myParser.run()