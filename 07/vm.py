from parser import Parser
from code_writer import CodeWriter
import sys

path = sys.argv[1]
parser = Parser(path)
c_writer = CodeWriter(path)

while True:
    print('parser.tmp_line', parser.tmp_line())
    if parser.command_type() == "C_PUSH":
        print("parser.words_ls", parser.words_ls)
        c_writer.writePushPop(parser.command_type(), parser.arg1(), parser.arg2())
    if parser.command_type() == "C_ARITHMETIC":
        c_writer.writeArithmetic(parser.command())
    if not parser.has_more_commands():
        break
    parser.advance()

c_writer.close()
