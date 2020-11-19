import re
import sys
import pprint

# Declare all regex of the lexemes
# Read the input file (source code)
# Apply all regex to find lexeme, add the found lexeme to the symbol table with its corresponding type

pp = pprint.PrettyPrinter(indent=4)

# REGEX
NUMBR_LITERAL_REGEX = "\-?[0-9]+"
NUMBAR_LITERAL_REGEX = "\-?[0-9]+\.[0-9]+"
YARN_LITERAL_REGEX = "\"[^\"]*\""
TROOF_LITERAL_REGEX = "^(WIN|FAIL)\s{0,1}"
TYPE_LITERAL_REGEX = "^(YARN|NUMBR|NUMBAR|TROOF|NOOB)\s{0,1}"
HAI_REGEX = "^\s*HAI\s{0,1}$"
KTHXBYE_REGEX = "^\s*KTHXBYE\s{0,1}"
BTW_REGEX = "^\s*BTW\s{0,1}"
OBTW_REGEX = "^\s*OBTW\s{0,1}"
TLDR_REGEX = "^\s*TLDR\s{0,1}"
I_HAS_A_REGEX = "^\s*I HAS A\s{0,1}"
ITZ_REGEX = "^\s*ITZ\s{0,1}"
R_REGEX = "^\s*R\s{0,1}"
SUM_OF_REGEX = "^\s*SUM OF\s{0,1}"
DIFF_OF_REGEX = "^\s*DIFF OF\s{0,1}"
PRODUKT_OF_REGEX = "^\s*PRODUKT OF\s{0,1}"
QUOSHUNT_OF_REGEX = "^\s*QUOSHUNT OF\s{0,1}"
MOD_OF_REGEX = "^\s*MOD OF\s{0,1}"
BIGGR_OF_REGEX = "^\s*BIGGR OF\s{0,1}"
SMALLR_OF_REGEX = "^\s*SMALLR OF\s{0,1}"
BOTH_OF_REGEX = "^\s*BOTH OF\s{0,1}"
EITHER_OF_REGEX = "^\s*EITHER OF\s{0,1}"
WON_OF_REGEX = "^\s*WON OF\s{0,1}"
NOT_REGEX = "^\s*NOT\s{0,1}"
ANY_OF_REGEX = "^\s*ANY OF\s{0,1}"
ALL_OF_REGEX = "^\s*ALL OF\s{0,1}"
BOTH_SAEM_REGEX = "^\s*BOTH SAEM\s{0,1}"
DIFFRINT_REGEX = "^\s*DIFFRINT\s{0,1}"
SMOOSH_REGEX = "^\s*SMOOSH\s{0,1}"
MAEK_REGEX = "^\s*MAEK\s{0,1}"
AN_REGEX = "^\s*AN\s{0,1}$"
A_REGEX = "^\s*A\s{0,1}$"
MKAY_REGEX = "^\s*MKAY\s{0,1}"
IS_NOW_A_REGEX = "^\s*IS NOW A\s{0,1}"
VISIBLE_REGEX = "^\s*VISIBLE\s{0,1}"
GIMMEH_REGEX = "^\s*GIMMEH\s{0,1}"
O_RLY_REGEX = "\s*O RLY\?"
YA_RLY_REGEX = "^\s*YA RLY\s{0,1}"
MEBBE_REGEX = "^\s*MEBE\s{0,1}"
NO_WAI_REGEX = "^\s*NO WAI\s{0,1}"
OIC_REGEX = "^\s*OIC\s{0,1}"
WTF_REGEX = "\s*WTF\?"
OMG_REGEX = "^\s*OMG\s{0,1}"
OMGWTF_REGEX = "^\s*OMGWTF\s{0,1}"
VARIABLE_IDENTIFIER_REGEX = "^[A-Za-z][A-Za-z0-9_]*"

# keywords that have the chance to be expanded to its complete and valid form
incompleteKeywords = (
    "I",
    "I HAS",
    "SUM",
    "DIFF",
    "PRODUKT",
    "QUOSHUNT",
    "MOD",
    "BIGGR",
    "SMALLR",
    "BOTH",
    "EITHER",
    "WON",
    "ANY",
    "ALL",
    "BOTH",
    "IS",
    "IS NOW",
    "O",
    "O RLY",
    "YA",
    "NO"
)

keywordClassification = {
    "NUMBR": "NUMBR Literal",
    "NUMBAR": "NUMBAR Literal",
    "YARN": "YARN Literal",
    "TROOF": "TROOF Literal",
    "TYPE": "Data Type",
    "HAI": "Delimiter",
    "KTHXBYE": "Delimiter",
    "BTW": "Single-line Comment",
    "OBTW": "Multi-line Comment Start",
    "TLDR": "Multi-line Commend End",
    "I HAS A": "Variable Declaration",
    "ITZ": "Variable Assignment",
    "R": "Assign Value To Variable",
    "SUM OF": "Addition Operator",
    "DIFF OF": "Subtraction Operator",
    "PRODUKT OF": "Multiplication Operator",
    "QUOSHUNT OF": "Division Operator",
    "MOD OF": "Modulo Operator",
    "BIGGR OF": "Max Operator",
    "SMALLR OF": "Min Operator",
    "BOTH OF": "AND Logical Operator",
    "EITHER OF": "OR Logical Operator",
    "WON OF": "XOR Logical Operator",
    "NOT": "NOT Logical Operator",
    "ANY OF": "Infinite Arity OR Operator",
    "ALL OF": "Infinite Arity AND Operator",
    "BOTH SAEM": "Equal Comparison Logical Operator",
    "DIFFRINT": "Not Equal Comparison Logical Operator",
    "SMOOSH": "String Concatenation Operator",
    "MAEK": "Explicit Typecasting For Expression",
    "A": "Type Operator",
    "AN": "Multiple Arity Conjunctor",
    "MKAY": "Multiple Arity Conjunctor",
    "IS NOW A": "Explicit Typecasting for Variable",
    "VISIBLE": "Printing",
    "GIMMEH": "Input",
    "O RLY?": "If Statement Start",
    "YA RLY": "If True Block",
    "MEBBE": "Else If Block",
    "NO WAI": "Else Block",
    "OIC": "If And Switch Statement End",
    "WTF?": "Switch Case Start",
    "OMG": "Switch Case Block",
    "OMGWTF": "Default Case Block",
    "VARIADENT": "Variable Identifier",
    "UNKNOWN": "Unknown"
}


def keywordIsEmpty(keyword):
    if not keyword or keyword.isspace():
        return True
    return False

def keywordIsIncomplete(keyword):
    for w in incompleteKeywords:
        if re.match("^\s*" + w + "\s{0,1}", keyword):
            return True

    return False

def keywordHasDoubleQuote(keyword):
    return (re.match("^\"[^\"]*$", keyword))



def getKeywordType(keyword):
    if re.match(NUMBR_LITERAL_REGEX, keyword):
        return "NUMBR"
    elif re.match(NUMBAR_LITERAL_REGEX, keyword):
        return "NUMBAR"
    elif re.match(YARN_LITERAL_REGEX, keyword):
        return "YARN"
    elif re.match(TROOF_LITERAL_REGEX, keyword):
        return "TROOF"
    elif re.match(TYPE_LITERAL_REGEX, keyword):
        return "TYPE"
    elif re.match(HAI_REGEX, keyword):
        return "HAI"
    elif re.match(KTHXBYE_REGEX, keyword):
        return "KTHXBYE"
    elif re.match(BTW_REGEX, keyword):
        return "BTW"
    elif re.match(OBTW_REGEX, keyword):
        return "OBTW"
    elif re.match(TLDR_REGEX, keyword):
        return "TLDR"
    elif re.match(I_HAS_A_REGEX, keyword):
        return "I HAS A"
    elif re.match(ITZ_REGEX, keyword):
        return "ITZ"
    elif re.match(R_REGEX, keyword):
        return "R"
    elif re.match(SUM_OF_REGEX, keyword):
        return "SUM OF"
    elif re.match(DIFF_OF_REGEX, keyword):
        return "DIFF OF"
    elif re.match(SUM_OF_REGEX, keyword):
        return "SUM OF"
    elif re.match(DIFF_OF_REGEX, keyword):
        return "DIFF OF"
    elif re.match(PRODUKT_OF_REGEX, keyword):
        return "PRODUKT OF"
    elif re.match(QUOSHUNT_OF_REGEX, keyword):
        return "QUOSHUNT OF"
    elif re.match(MOD_OF_REGEX, keyword):
        return "MOD OF"
    elif re.match(BIGGR_OF_REGEX, keyword):
        return "BIGGR OF"
    elif re.match(SMALLR_OF_REGEX, keyword):
        return "SMALLR OF"
    elif re.match(BOTH_OF_REGEX, keyword):
        return "BOTH OF"
    elif re.match(EITHER_OF_REGEX, keyword):
        return "EITHER OF"
    elif re.match(WON_OF_REGEX, keyword):
        return "WON OF"
    elif re.match(NOT_REGEX, keyword):
        return "NOT"
    elif re.match(ANY_OF_REGEX, keyword):
        return "ANY OF"
    elif re.match(ALL_OF_REGEX, keyword):
        return "ALL OF"
    elif re.match(BOTH_SAEM_REGEX, keyword):
        return "BOTH SAEM"
    elif re.match(DIFFRINT_REGEX, keyword):
        return "DIFFRINT"
    elif re.match(SMOOSH_REGEX, keyword):
        return "SMOOSH"
    elif re.match(MAEK_REGEX, keyword):
        return "MAEK"
    elif re.match(AN_REGEX, keyword):
        return "AN"
    elif re.match(A_REGEX, keyword):
        return "A"
    elif re.match(MKAY_REGEX, keyword):
        return "MKAY"
    elif re.match(IS_NOW_A_REGEX, keyword):
        return "IS NOW A"
    elif re.match(VISIBLE_REGEX, keyword):
        return "VISIBLE"
    elif re.match(GIMMEH_REGEX, keyword):
        return "GIMMEH"
    elif re.match(O_RLY_REGEX, keyword):
        return "O RLY?"
    elif re.match(YA_RLY_REGEX, keyword):
        return "YA RLY"
    elif re.match(MEBBE_REGEX, keyword):
        return "MEBBE"
    elif re.match(NO_WAI_REGEX, keyword):
        return "NO WAI"
    elif re.match(OIC_REGEX, keyword):
        return "OIC"
    elif re.match(WTF_REGEX, keyword):
        return "WTF?"
    elif re.match(OMG_REGEX, keyword):
        return "OMG"
    elif re.match(OMGWTF_REGEX, keyword):
        return "OMGWTF"
    else:
        return "UNKNOWN"




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


def lexer(sourceCodeString):
    lineList = []
    lexemeTable = []

    # sourceCodeString = readSourceCode("LOLCODE_example/bool.lol")

    # replace all tabs in the source code with space to handle cases with '\t<keyword>'
    sourceCodeString = re.sub("\t", " ", sourceCodeString)

    # get list containing each line of the source code
    lineList = sourceCodeString.split("\n")


    for line in lineList:
        ENCOUNTERED_DOUBLE_QUOTE = False
        TO_APPEND_FLAG = False
        currentWord = ""
        appendedKeyword = ""
        keywordType = ""

        # Split the line into words
        keywordList = line.split(" ")

        # pp.pprint(keywordList)

        # Look for lexemes for each word
        for keyword in keywordList:
            # To retain spaces inside a yarn literal, stop ignoring spaces when you encountered a double quote
            if keywordIsEmpty(keyword) == True and ENCOUNTERED_DOUBLE_QUOTE == False:
                continue

            # Needs to append incomplete keywords with the next word
            if TO_APPEND_FLAG == True:
                    currentWord = currentWord + " " + keyword
            else:
                currentWord = keyword

            # Tries to match the current word to all of the keywords
            keywordType = getKeywordType(currentWord)

            # Valid keyword so just add to the lexeme table
            if keywordType != "UNKNOWN":
                lexemeTable.append({"lexeme": currentWord, "classification": keywordClassification[keywordType]})
                TO_APPEND_FLAG = False
                ENCOUNTERED_DOUBLE_QUOTE = False
                continue
            else:
                # if not matched as a keyword, it might be an incomplete keyword or a variable identifier
                # check if its an incomplete keyword. else check if its a valid variable identifier

                if keywordIsIncomplete(currentWord):
                    TO_APPEND_FLAG = True
                elif keywordHasDoubleQuote(currentWord):
                    ENCOUNTERED_DOUBLE_QUOTE = True
                    TO_APPEND_FLAG = True
                elif re.match(VARIABLE_IDENTIFIER_REGEX, currentWord):
                    lexemeTable.append({"lexeme": currentWord, "classification": keywordClassification["VARIADENT"]})
                    TO_APPEND_FLAG = False
                    ENCOUNTERED_DOUBLE_QUOTE = False

                # Insert error handling here "Nothing matched"

    return lexemeTable
