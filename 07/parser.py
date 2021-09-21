import re


class Parser:
    def __init__(self, file):
        with open(file) as f:
            self.__lines = []
            for s in f.readlines():
                # s = s.strip().replace(" ", "")
                s = re.sub('^\s+$', '', s)
                s = re.sub('//.*', '', s)
                if len(s) > 1:
                    # print("added line", s)
                    # print("len(s)", len(s))
                    self.__lines.append(s)
        self.tmp_idx = 0
        self.words_ls = list(self.tmp_line().split())
        self.command_type_dict = {
            "push": "C_PUSH",
            "pop": "C_POP",
            "label": "C_LABEL",
            "goto": "C_GOTO",
            "if-goto": "C_IF",
            "function": "C_FUNCTION",
            "return": "C_RETURN",
            "call": "C_CALL",
        }
        arithmetic_commands = ["add", "sub", "neg",
                               "eq", "gt", "lt", "and", "or", "not"]
        for command in arithmetic_commands:
            self.command_type_dict[command] = "C_ARITHMETIC"

    def tmp_line(self):
        return self.__lines[self.tmp_idx]

    def has_more_commands(self):
        return self.tmp_idx + 1 < len(self.__lines)

    def advance(self):
        if not self.has_more_commands():
            print('cannot advance anymore')
            raise
        self.tmp_idx += 1
        self.split_tmp_line()

    def split_tmp_line(self):
        self.words_ls = list(self.tmp_line().split())

    def command(self):
        return self.words_ls[0]

    def command_type(self):
        return self.command_type_dict[self.command()]

    def arg1(self):
        return self.words_ls[1]

    def arg2(self):
        if not self.command_type() in ("C_PUSH", "C_POP", "C_FUNCTION", "C_RETURN"):
            print("arg2 can't be called when command type is {}",
                  self.command_type())
            raise
        return self.words_ls[2]
