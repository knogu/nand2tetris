import re


class CodeWriter:
    def __init__(self, input_file_path):
        self.f = open(input_file_path[:-3] + ".asm", mode='w')
        m = re.match(r'.+/([^/]+).vm', input_file_path)
        # 拡張子なしのファイル名(用途: static変数のシンボル)
        self.vm_filename = m.groups()[0]
        self.label_cnt = 0
        # pushに用いる
        self.insertD = [
            "@SP",
            "A = M",
            "M = D",
        ]
        # pushに用いる
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
        ] + setM

        if command == "add":
            code_lines = code_for_binary_before_comp + \
                ["M = M + D"] + self.incSP
        elif command == "sub":
            code_lines = code_for_binary_before_comp + \
                ["M = M - D"] + self.incSP
        elif command == "and":
            code_lines = code_for_binary_before_comp + \
                ["M = M & D"] + self.incSP
        elif command == "or":
            code_lines = code_for_binary_before_comp + \
                ["M = M | D"] + self.incSP
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
        self.__write_code_lines(code_lines)

    def __write_pop_default(self, setAddressToD):
        '''
        setAddressToD: pop先のアドレスをDレジスタに代入するコード(文字列のリスト)
        実装内部でR13とR14を用いる
        '''
        # popされる値をR13に格納
        self.__write_code_lines([
            "@SP",
            "M = M - 1",
            "A = M",
            "D = M",
            "@R13",
            "M = D",
        ])
        self.__write_code_lines(setAddressToD)
        self.__write_code_lines([
            # pop先アドレスをR14に格納
            "@R14",
            "M = D",
            # 値を指定されたアドレスにセット
            "@R13",
            "D = M",
            "@R14",
            "A = M",
            "M = D",
        ])

    def writePushPop(self, command, segment, index):
        # segment が constant の場合のみを想定
        # print("command, segment, index", command, segment, index)
        if command == "C_PUSH":
            if segment == "constant":
                self.__write_push_const(index)
                return
            elif segment in ("local", "argument", "this", "that"):
                setPushedValueToD = [
                    "@{}".format(index),
                    "D = A",
                    "@{}".format(self.__register_name[segment]),
                    "A = M + D",
                    "D = M",
                ]
            elif segment in ("pointer", "temp"):
                self.__write_push_memory_value(
                    self.__base[segment] + int(index))
                return
            elif segment == "static":
                self.__write_push_memory_value(
                    "{}.{}".format(self.vm_filename, index))
                return
            code_lines = setPushedValueToD + self.insertD + self.incSP
            self.__write_code_lines(code_lines)
        else:
            if segment in ("local", "argument", "this", "that"):
                self.__write_pop_default([
                    "@{}".format(index),
                    "D = A",
                    "@{}".format(self.__register_name[segment]),
                    "D = M + D",
                ])
            elif segment in ("pointer", "temp"):
                self.__write_pop_default([
                    "@{}".format(self.__base[segment] + int(index)),
                    "D = A",
                ])
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
                self.__write_code_lines(code_lines)
            else:
                raise

    def write_label(self, label):
        self.__write_code_lines([
            "({})".format(label)
        ])

    def __write_code_lines(self, code_lines):
        self.f.write('\n'.join(code_lines))
        self.f.write('\n')

    def write_goto(self, label):
        self.__write_code_lines([
            "@{}".format(label),
            "0;JMP"
        ])

    def write_if(self, label):
        self.__write_code_lines([
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@{}".format(label),
            "D;JNE"
        ])

    def __write_push_memory_value(self, address):
        '''
        シンボルで参照できるレジスタ(ex. R0, LCL)、またはメモリに入っている値をpushする
        '''
        setPushedValueToD = [
            "@{}".format(address),
            "D = M"
        ]
        code_lines = setPushedValueToD + self.insertD + self.incSP
        self.__write_code_lines(code_lines)

    def __write_push_const(self, value):
        '''
        引数valueをAレジスタに代入した後pushする
        '''
        setPushedValueToD = [
            "@{}".format(value),
            "D = A",
        ]
        code_lines = setPushedValueToD + self.insertD + self.incSP
        self.__write_code_lines(code_lines)

    def write_call(self, func_name, arg_count):
        # TODO: 引数をスタックにpush
        return_address = self.label_cnt
        self.__write_push_const(return_address)
        self.label_cnt += 1

        self.__write_push_memory_value("LCL")
        self.__write_push_memory_value("ARG")
        self.__write_push_memory_value("THIS")
        self.__write_push_memory_value("THAT")

        self.__write_code_lines([
            # ARGを戻す
            "@SP",
            "D = M",
            "@{}".format(arg_count+5),
            "D = D - A",
            "@ARG",
            "M = D",
            # LCLを戻す
            "@SP",
            "D = M",
            "@LCL",
            "M = D",
        ])
        self.write_goto(func_name)
        self.write_label(return_address)

    def write_function(self, func_name, arg_count):
        self.write_label(func_name)
        self.__write_code_lines([
            "@counter",
            "M = arg_count",
            "@(loop{})".format(self.label_cnt),
        ])
        self.__write_push_const(0)
        self.__write_code_lines([
            # ループに戻るか、終了
            "@counter",
            "D = M - 1",
            "@(loop{})".format(self.label_cnt),
            "D;JGT"
        ])
        self.label_cnt += 1

    def write_return(self):
        self.__write_pop_default([
            # 一時変数FRAMEにLCLの値を代入
            "@LCL",
            "D = M",
            "@FRAME{}".format(self.label_cnt),
            "M = D",
        ])
        # 戻り値を移動
        self.__write_pop_default([
            "@ARG",
            "A = M",
            "D = M",
        ])
        self.__write_pop_default([
            # SPを戻す
            "@ARG",
            "D = M",
            "@SP",
            "M = D + 1",
            # THATを戻す
            "@FRAME{}".format(self.label_cnt),
            "M = M-1",
            "A = M",
            "D = M",
            "@THAT",
            "M = D",
            # THISを戻す
            "@FRAME{}".format(self.label_cnt),
            "M = M-1",
            "A = M",
            "D = M",
            "@THIS",
            "M = D",
            # ARGを戻す
            "@FRAME{}".format(self.label_cnt),
            "M = M-1",
            "A = M",
            "D = M",
            "@ARG",
            "M = D",
            # LCLを戻す
            "@FRAME{}".format(self.label_cnt),
            "M = M-1",
            "A = M",
            "D = M",
            "@LCL",
            "M = D",
            # リターンアドレスへ移動
            "@FRAME{}".format(self.label_cnt),
            "M = M-1",
            "A = M",
            "0;JMP"
        ])
        self.label_cnt += 1
