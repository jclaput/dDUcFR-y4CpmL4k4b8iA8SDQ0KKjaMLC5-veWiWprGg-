import pprint

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
OMG_REGEX = "^\s*OMG\s{0,1}$"
OMGWTF_REGEX = "^\s*OMGWTF\s{0,1}$"
GTFO_REGEX = "^\s*GTFO\s{0,1}"
VARIABLE_IDENTIFIER_REGEX = "^[A-Za-z][A-Za-z0-9_]*"

# LEXEMES
# keywords that have the chance to be expanded to its complete and valid form
incompleteLexeme = (
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

lexemeDescription = {
    "TT_NUMBR": "NUMBR Literal",
    "TT_NUMBAR": "NUMBAR Literal",
    "TT_YARN": "YARN Literal",
    "TT_TROOF": "TROOF Literal",
    "TT_DATA_TYPE": "Data Type",
    "TT_DELIMITER": "Delimiter",
    "TT_SINGLE_COMMENT": "Single-line Comment",
    "TT_MULT_COMMENT_START": "Multi-line Comment Start",
    "TT_MULT_COMMENT_END": "Multi-line Commend End",
    "TT_VAR_DECLARATION": "Variable Declaration",
    "TT_VAR_ASSIGNMENT": "Variable Assignment",
    "TT_ASSIGN_TO_VAR": "Assign Value To Variable",
    "TT_ADD": "Addition Operator",
    "TT_SUB": "Subtraction Operator",
    "TT_MUL": "Multiplication Operator",
    "TT_DIV": "Division Operator",
    "TT_MOD": "Modulo Operator",
    "TT_MAX": "Max Operator",
    "TT_MIN": "Min Operator",
    "TT_AND": "AND Logical Operator",
    "TT_OR": "OR Logical Operator",
    "TT_XOR": "XOR Logical Operator",
    "TT_NOT": "NOT Logical Operator",
    "TT_INFINITY_OR": "Infinite Arity OR Operator",
    "TT_INFINITY_AND": "Infinite Arity AND Operator",
    "TT_INFINITY_CONCAT": "String Concatenation Operator",
    "TT_EQUAL": "Equal Comparison Logical Operator",
    "TT_NOT_EQUAL": "Not Equal Comparison Logical Operator",
    "TT_TYPE_OPERATOR": "Type Operator",
    "TT_MULT_ARITY_CONJUNCTOR": "Multiple Arity Conjunctor",
    "TT_MULT_ARITY_ENDER": "Multiple Arity Ender",
    "TT_PRINT": "Printing",
    "TT_INPUT": "Input",
    "TT_IF_START": "If Statement Start",
    "TT_IF_BLOCK": "If True Block",
    "TT_ELSE_BLOCK": "Else Block",
    "TT_IF_SWITCH_END": "If And Switch Statement End",
    "TT_SWITCH_START": "Switch Case Start",
    "TT_SWITCH_BLOCK": "Switch Case Block",
    "TT_DEFAULT_CASE_BLOCK": "Default Case Block",
    "TT_BREAK": "Break Statement",
    "TT_IDENTIFIER": "Variable Identifier",
    "TT_UNKNOWN": "Unknown",
    "TT_END_OF_FILE" : "End Of File"
}

tokenTag = {
    "NUMBR": "TT_NUMBR",
    "NUMBAR": "TT_NUMBAR",
    "YARN": "TT_YARN",
    "TROOF": "TT_TROOF",
    "TYPE": "TT_DATA_TYPE",
    "HAI": "TT_DELIMITER",
    "KTHXBYE": "TT_DELIMITER",
    "BTW": "TT_SINGLE_COMMENT",
    "OBTW": "TT_MULT_COMMENT_START",
    "TLDR": "TT_MULT_COMMENT_END",
    "I HAS A": "TT_VAR_DECLARATION",
    "ITZ": "TT_VAR_ASSIGNMENT",
    "R": "TT_ASSIGN_TO_VAR",
    "SUM OF": "TT_ADD",
    "DIFF OF": "TT_SUB",
    "PRODUKT OF": "TT_MUL",
    "QUOSHUNT OF": "TT_DIV",
    "MOD OF": "TT_MOD",
    "BIGGR OF": "TT_MAX",
    "SMALLR OF": "TT_MIN",
    "BOTH OF": "TT_AND",
    "EITHER OF": "TT_OR",
    "WON OF": "TT_XOR",
    "NOT": "TT_NOT",
    "ANY OF": "TT_INFINITY_OR",
    "ALL OF": "TT_INFINITY_AND",
    "SMOOSH": "TT_INFINITY_CONCAT",
    "BOTH SAEM": "TT_EQUAL",
    "DIFFRINT": "TT_NOT_EQUAL",
    "A": "TT_TYPE_OPERATOR",
    "AN": "TT_MULT_ARITY_CONJUNCTOR",
    "MKAY": "TT_MULT_ARITY_ENDER",
    "VISIBLE": "TT_PRINT",
    "GIMMEH": "TT_INPUT",
    "O RLY?": "TT_IF_START",
    "YA RLY": "TT_IF_BLOCK",
    "NO WAI": "TT_ELSE_BLOCK",
    "OIC": "TT_IF_SWITCH_END",
    "WTF?": "TT_SWITCH_START",
    "OMG": "TT_SWITCH_BLOCK",
    "OMGWTF": "TT_DEFAULT_CASE_BLOCK",
    "GTFO": "TT_BREAK",
    "VARIADENT": "TT_IDENTIFIER",
    "\n": "TT_DELIMITER",
}

ARITHMETIC_BINARY_OPERATIONS = (
    "TT_ADD", "TT_SUB", "TT_MUL", "TT_DIV", "TT_MOD", "TT_MAX", "TT_MIN")
BOOLEAN_BINARY_OPERATIONS = ("TT_AND", "TT_OR", "TT_XOR")
COMPARISON_OPERATIONS = ("TT_EQUAL", "TT_NOT_EQUAL")
INFINITE_ARITY_OPERATIONS = ("TT_INFINITY_OR", "TT_INFINITY_AND")
DATA_TYPES = ("TT_NUMBR", "TT_NUMBAR", "TT_TROOF", "TT_YARN")
EXPRESSIONS = (("TT_IDENTIFIER", "TT_NOT") + DATA_TYPES + ARITHMETIC_BINARY_OPERATIONS +
               BOOLEAN_BINARY_OPERATIONS + COMPARISON_OPERATIONS + INFINITE_ARITY_OPERATIONS)
