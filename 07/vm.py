from parser import Parser
from code_writer import CodeWriter
import sys

path = sys.argv[1]
parser = Parser(path)
c_writer = CodeWriter(path)

while True:
    if parser.command_type() in ("C_PUSH", "C_POP"):
        c_writer.writePushPop(parser.command_type(), parser.arg1(), parser.arg2())
    if parser.command_type() == "C_ARITHMETIC":
        c_writer.writeArithmetic(parser.command())
    if not parser.has_more_commands():
        break
    parser.advance()

c_writer.close()
