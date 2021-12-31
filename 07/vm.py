from parser import Parser
from code_writer import CodeWriter
import os
import sys

path = sys.argv[1]
vm_files = []  # 対象となるvmファイルの絶対パス、のリスト
if path[-3:] == ".vm":
    vm_files.append(path)
else:
    dir = path
    if dir[-1] != "/":
        dir = dir + "/"
    init_filename = "Sys.vm"
    is_init_file_found = False
    for filename in os.listdir(path):
        if filename == init_filename:
            is_init_file_found = True
            continue
        if filename[-3:] == ".vm":
            vm_files.append(dir + filename)
    if not is_init_file_found:
        print("init file not found")
        raise
    vm_files.append(dir + init_filename)
    vm_files = vm_files[::-1]
    print(vm_files)

for i, path in enumerate(vm_files):
    parser = Parser(path)
    c_writer = CodeWriter(
        path, sys.argv[2], True if i > 0 else False, True if i == 0 else False)

    while True:
        # print(parser.tmp_line())
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
        elif parser.command_type() == "C_CALL":
            c_writer.write_call(parser.arg1(), parser.arg2())
        elif parser.command_type() == "C_FUNCTION":
            c_writer.write_function(parser.arg1(), parser.arg2())
        elif parser.command_type() == "C_RETURN":
            c_writer.write_return()
        if not parser.has_more_commands():
            break
        parser.advance()

    c_writer.close()
