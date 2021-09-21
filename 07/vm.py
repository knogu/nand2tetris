from parser import Parser
from code_writer import CodeWriter
import sys

path = sys.argv[1]
parser = Parser(path)
c_writer = CodeWriter(path)

while True:
    if parser.command_type() in ("C_PUSH", "C_POP"):
        c_writer.writePushPop(parser.command_type(),
                              parser.arg1(), parser.arg2())
    elif parser.command_type() == "C_ARITHMETIC":
        c_writer.writeArithmetic(parser.command())
    elif parser.command_type() == "C_LABEL":
        c_writer.write_label(parser.arg1())
    elif parser.command_type() == "C_GOTO":
        c_writer.write_goto(parser.arg1())
    elif parser.command_type() == "C_IF":
        c_writer.write_if(parser.arg1())
    if not parser.has_more_commands():
        break
    parser.advance()

c_writer.close()
