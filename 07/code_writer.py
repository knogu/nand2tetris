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
    
    def close(self):
        self.f.close()

    def writeArithmetic(self, command):
        if command == "add":
            code_lines = [
                "@SP",
                "M = M-1",
                "A = M",
                "D = M",
                "M = 0",
                "@SP",
                "M = M-1",
                "A = M",
                "D = D + M",
                "@SP",
                "A = M",
                "M = D",
                "@SP",
                "M = M+1"
            ]
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
