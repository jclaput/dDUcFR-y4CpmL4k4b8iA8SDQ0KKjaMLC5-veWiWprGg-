import re
import sys

from token import *
from constants import *


# Declare all regex of the lexemes
# Read the input file (source code)
# Apply all regex to find lexeme, add the found lexeme to the symbol table with its corresponding type

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


def lexemeIsEmpty(lexeme):
    if not lexeme or lexeme.isspace():
        return True
    return False


def lexemeIsIncomplete(lexeme):
    if lexeme in incompleteLexeme:
        return True

    return False


def lexemeHasDoubleQuote(lexeme):
    return (re.match("^\"[^\"]*$", lexeme))


def getLexemeClassification(lexeme):
    if re.match(NUMBAR_LITERAL_REGEX, lexeme):
        return "NUMBAR"
    elif re.match(NUMBR_LITERAL_REGEX, lexeme):
        return "NUMBR"
    elif re.match(YARN_LITERAL_REGEX, lexeme):
        return "YARN"
    elif re.match(TROOF_LITERAL_REGEX, lexeme):
        return "TROOF"
    elif re.match(TYPE_LITERAL_REGEX, lexeme):
        return "TYPE"
    elif re.match(HAI_REGEX, lexeme):
        return "HAI"
    elif re.match(KTHXBYE_REGEX, lexeme):
        return "KTHXBYE"
    elif re.match(BTW_REGEX, lexeme):
        return "BTW"
    elif re.match(OBTW_REGEX, lexeme):
        return "OBTW"
    elif re.match(TLDR_REGEX, lexeme):
        return "TLDR"
    elif re.match(I_HAS_A_REGEX, lexeme):
        return "I HAS A"
    elif re.match(ITZ_REGEX, lexeme):
        return "ITZ"
    elif re.match(R_REGEX, lexeme):
        return "R"
    elif re.match(SUM_OF_REGEX, lexeme):
        return "SUM OF"
    elif re.match(DIFF_OF_REGEX, lexeme):
        return "DIFF OF"
    elif re.match(SUM_OF_REGEX, lexeme):
        return "SUM OF"
    elif re.match(DIFF_OF_REGEX, lexeme):
        return "DIFF OF"
    elif re.match(PRODUKT_OF_REGEX, lexeme):
        return "PRODUKT OF"
    elif re.match(QUOSHUNT_OF_REGEX, lexeme):
        return "QUOSHUNT OF"
    elif re.match(MOD_OF_REGEX, lexeme):
        return "MOD OF"
    elif re.match(BIGGR_OF_REGEX, lexeme):
        return "BIGGR OF"
    elif re.match(SMALLR_OF_REGEX, lexeme):
        return "SMALLR OF"
    elif re.match(BOTH_OF_REGEX, lexeme):
        return "BOTH OF"
    elif re.match(EITHER_OF_REGEX, lexeme):
        return "EITHER OF"
    elif re.match(WON_OF_REGEX, lexeme):
        return "WON OF"
    elif re.match(NOT_REGEX, lexeme):
        return "NOT"
    elif re.match(ANY_OF_REGEX, lexeme):
        return "ANY OF"
    elif re.match(ALL_OF_REGEX, lexeme):
        return "ALL OF"
    elif re.match(BOTH_SAEM_REGEX, lexeme):
        return "BOTH SAEM"
    elif re.match(DIFFRINT_REGEX, lexeme):
        return "DIFFRINT"
    elif re.match(SMOOSH_REGEX, lexeme):
        return "SMOOSH"
    elif re.match(AN_REGEX, lexeme):
        return "AN"
    elif re.match(A_REGEX, lexeme):
        return "A"
    elif re.match(MKAY_REGEX, lexeme):
        return "MKAY"
    elif re.match(IS_NOW_A_REGEX, lexeme):
        return "IS NOW A"
    elif re.match(VISIBLE_REGEX, lexeme):
        return "VISIBLE"
    elif re.match(GIMMEH_REGEX, lexeme):
        return "GIMMEH"
    elif re.match(O_RLY_REGEX, lexeme):
        return "O RLY?"
    elif re.match(YA_RLY_REGEX, lexeme):
        return "YA RLY"
    elif re.match(NO_WAI_REGEX, lexeme):
        return "NO WAI"
    elif re.match(OIC_REGEX, lexeme):
        return "OIC"
    elif re.match(WTF_REGEX, lexeme):
        return "WTF?"
    elif re.match(OMG_REGEX, lexeme):
        return "OMG"
    elif re.match(OMGWTF_REGEX, lexeme):
        return "OMGWTF"
    elif re.match(GTFO_REGEX, lexeme):
        return "GTFO"
    else:
        return "UNKNOWN"


def lexer(sourceCodeString):
    lineList = []
    lexemeTable = []

    # replace all tabs in the source code with space to handle cases with '\t<keyword>'
    sourceCodeString = re.sub("\t", " ", sourceCodeString)

    # get list containing each line of the source code
    lineList = sourceCodeString.split("\n")

    for line in lineList:
        ENCOUNTERED_DOUBLE_QUOTE = False
        TO_APPEND_FLAG = False
        ENCOUNTERED_SINGLE_COMMENT = False
        currentWord = ""
        appendedKeyword = ""
        classification = ""

        # Split the line into words
        lexemeList = line.split(" ")

        # pp.pprint(lexemeList)

        # Look for lexemes for each word
        for lexeme in lexemeList:
            if getLexemeClassification(lexeme) == "BTW":
                break
            # To retain spaces inside a yarn literal, stop ignoring spaces when you encountered a double quote
            if lexemeIsEmpty(lexeme) == True and ENCOUNTERED_DOUBLE_QUOTE == False:
                continue

            # Needs to append incomplete lexeme with the next word
            if TO_APPEND_FLAG == True:
                currentWord = currentWord + " " + lexeme
            else:
                currentWord = lexeme

            # Tries to match the current word to all of the lexeme
            classification = getLexemeClassification(currentWord)

            # Valid lexeme so just add to the lexeme table
            if classification != "UNKNOWN":
                lexemeTable.append(
                    Token(currentWord, tokenTag[classification]))
                TO_APPEND_FLAG = False
                ENCOUNTERED_DOUBLE_QUOTE = False
                continue
            else:
                # if not matched as a lexeme, it might be an incomplete lexeme or a variable identifier
                # check if its an incomplete lexeme. else check if its a valid variable identifier
                if lexemeIsIncomplete(currentWord):
                    TO_APPEND_FLAG = True
                elif lexemeHasDoubleQuote(currentWord):
                    ENCOUNTERED_DOUBLE_QUOTE = True
                    TO_APPEND_FLAG = True
                elif re.match(VARIABLE_IDENTIFIER_REGEX, currentWord):
                    lexemeTable.append(Token(currentWord, "TT_IDENTIFIER"))
                    TO_APPEND_FLAG = False
                    ENCOUNTERED_DOUBLE_QUOTE = False
                else:
                    lexemeTable.append(Token(currentWord, "TT_UNKNOWN"))

        # Append newline after finishing getting tokens per line to denote linebreak or codeblock delimiter
        lexemeTable.append(Token("\n", "TT_DELIMITER"))

    lexemeTable.append(Token("EOF", "TT_END_OF_FILE"))

    return lexemeTable
