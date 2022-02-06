OP = {"+", "-", "*", "/", "&", "|", "<", ">", "="}
UNARY_OP = {"-", "~"}
TAG_KEYWORD = "keyword"
TAG_SYMBOL = "symbol"
TAG_IDENTIFIER = "identifier"
TAG_INTEGER_CONST = "integerConstant"
TAG_STRING_CONST = "stringConstant"

# memory segment
CONSTANT = "constant"
ARG = "arg"
LOCAL = "local"
STATIC = "static"
THIS = "this"
THAT = "that"
POINTER = "pointer"
TEMP = "temp"

# symbol type (for symbol table)
FIELD = "field"
VAR = "var"

# 演算
OP_COMMAND = {"+": "add", "*": "call Math.multiply 2", "-": "neg", "~": "not"}
