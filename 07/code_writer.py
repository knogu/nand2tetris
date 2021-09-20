class CodeWriter:
    def __init__(self, input_file_path):
        self.f = open(input_file_path[:-2] + "asm", mode='w')
        # code_lines = [
        #     "@256",
        #     "D = A",
        #     "@SP",
        #     "M = D",
        # ]
        # self.f.write('\n'.join(code_lines))
        # self.f.write('\n')
        self.label_cnt = 0
    
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
        incSP = [
            "@SP",
            "M = M+1"
        ]
        
        if command == "add":
            code_lines = code_for_binary_before_comp + ["M = M + D"] + incSP
        elif command == "sub":
            code_lines = code_for_binary_before_comp + ["M = M - D"] + incSP
        elif command == "and":
            code_lines = code_for_binary_before_comp + ["M = M & D"] + incSP
        elif command == "or":
            code_lines = code_for_binary_before_comp + ["M = M | D"] + incSP
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
            ] + incSP
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
            ] + incSP
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
            ] + incSP
            self.label_cnt += 2
        elif command == "not":
            code_lines = setM + ["M = !M"] + incSP
        elif command == "neg":
            code_lines = setM + ["M = -M"] + incSP
        self.f.write('\n'.join(code_lines))
        self.f.write('\n')

    def writePushPop(self, command, segment, index):
        # segment が constant の場合のみを想定
        if command == "C_PUSH":
            print("push called")
            code_lines = [
                "@{}".format(index),
                "D = A",
                "@SP",
                "A = M",
                "M = D",
                "@SP",
                "M = M+1",
            ]
            self.f.write('\n'.join(code_lines))
            self.f.write('\n')
