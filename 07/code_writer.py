import re

class CodeWriter:
    def __init__(self, input_file_path):
        self.f = open(input_file_path[:-3] + ".asm", mode='w')
        m = re.match(r'.+/([^/]+).vm', input_file_path)
        # 拡張子なしのファイル名(用途: static変数のシンボル)
        self.vm_filename = m.groups()[0]
        self.label_cnt = 0
        self.incSP = [
            "@SP",
            "M = M+1"
        ]
        # todo: メモリアクセス直接指定が良いかも
        self.__register_name = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }
        self.__base = {
            "pointer": 3,
            "temp": 5
        }
    
    def close(self):
        self.f.close()

    def writeArithmetic(self, command):
        setM = [
            "@SP",
            "M = M-1",
            "A = M",
        ]
        code_for_binary_before_comp = [
            "@SP",
            "M = M-1",
            "A = M",
            "D = M",
            "M = 0",    # いらないかも
        ] + setM
        
        if command == "add":
            code_lines = code_for_binary_before_comp + ["M = M + D"] + self.incSP
        elif command == "sub":
            code_lines = code_for_binary_before_comp + ["M = M - D"] + self.incSP
        elif command == "and":
            code_lines = code_for_binary_before_comp + ["M = M & D"] + self.incSP
        elif command == "or":
            code_lines = code_for_binary_before_comp + ["M = M | D"] + self.incSP
        elif command == "eq":
            code_lines = code_for_binary_before_comp + [
                "D = M - D",
                "@label{}".format(self.label_cnt),
                "D;JEQ",
                "@SP",
                "A = M",
                "M = 0",    # falseの場合のみ
                "@label{}".format(self.label_cnt+1),
                "0;JMP",    # trueの場合の処理をスキップ
                "(label{})".format(self.label_cnt),
                "@SP",
                "A = M",
                "M = -1",
                "(label{})".format(self.label_cnt+1),
            ] + self.incSP
            self.label_cnt += 2
        elif command == "gt":
            code_lines = code_for_binary_before_comp + [
                "D = M - D",
                "@label{}".format(self.label_cnt),
                "D;JGT",
                "@SP",
                "A = M",
                "M = 0",    # falseの場合のみ
                "@label{}".format(self.label_cnt+1),
                "0;JMP",    # trueの場合の処理をスキップ
                "(label{})".format(self.label_cnt),
                "@SP",
                "A = M",
                "M = -1",
                "(label{})".format(self.label_cnt+1),
            ] + self.incSP
            self.label_cnt += 2
        elif command == "lt":
            code_lines = code_for_binary_before_comp + [
                "D = M - D",
                "@label{}".format(self.label_cnt),
                "D;JLT",
                "@SP",
                "A = M",
                "M = 0",    # falseの場合のみ
                "@label{}".format(self.label_cnt+1),
                "0;JMP",    # trueの場合の処理をスキップ
                "(label{})".format(self.label_cnt),
                "@SP",
                "A = M",
                "M = -1",
                "(label{})".format(self.label_cnt+1),
            ] + self.incSP
            self.label_cnt += 2
        elif command == "not":
            code_lines = setM + ["M = !M"] + self.incSP
        elif command == "neg":
            code_lines = setM + ["M = -M"] + self.incSP
        self.f.write('\n'.join(code_lines))
        self.f.write('\n')

    def writePushPop(self, command, segment, index):
        # segment が constant の場合のみを想定
        # print("command, segment, index", command, segment, index)
        if command == "C_PUSH":
            if segment == "constant":
                setPushedValueToD = [
                    "@{}".format(index),
                    "D = A",
                ]
            elif segment in ("local", "argument", "this", "that"):
                setPushedValueToD = [
                    "@{}".format(index),
                    "D = A",
                    "@{}".format(self.__register_name[segment]),
                    "A = M + D",
                    "D = M",
                ]
            elif segment in ("pointer", "temp"):
                setPushedValueToD = [
                    "@{}".format(self.__base[segment] + int(index)),
                    "D = M"
                ]
            elif segment == "static":
                setPushedValueToD = [
                    "@{}.{}".format(self.vm_filename, index),
                    "D = M"
                ]
            insertD = [
                "@SP",
                "A = M",
                "M = D",
            ]
            code_lines = setPushedValueToD + insertD + self.incSP
            self.f.write('\n'.join(code_lines))
            self.f.write('\n')
        else:
            popToR13 = [
                "@SP",
                "M = M - 1",
                "A = M",
                "D = M",
                "@R13",
                "M = D",
            ]
            setValue = [
                "@R13",
                "D = M",
                "@R14",
                "A = M",
                "M = D",
            ]
            if segment in ("local", "argument", "this", "that"):
                setAddressToR14 = [
                    "@{}".format(index),
                    "D = A",
                    "@{}".format(self.__register_name[segment]),
                    "D = M + D",
                    "@R14",
                    "M = D"
                ]
                code_lines = popToR13 + setAddressToR14 + setValue
            elif segment in ("pointer", "temp"):
                setAddressToR14 = [
                    "@{}".format(self.__base[segment] + int(index)),
                    "D = A",
                    "@R14",
                    "M = D",
                ]
                code_lines = popToR13 + setAddressToR14 + setValue
            elif segment == "static":
                code_lines = [
                    # Dにpopped valueを格納
                    "@SP",
                    "M = M - 1",
                    "A = M",
                    "D = M",
                    "@{}.{}".format(self.vm_filename, index),
                    "M = D",
                ]
            self.f.write('\n'.join(code_lines))
            self.f.write('\n')
