import re
import sys

class Parser:
    def __init__(self, file):
        with open(file) as f:
            self.lines = []
            for s in f.readlines():
                s = s.strip().replace(" ", "")
                s = re.sub('//.*', '', s)
                if s:
                    self.lines.append(s)
        self.tmp_idx = 0
        self.eq_idx = -1
        self.semicolon_idx = -1

    def reset(self):
        self.tmp_idx = 0
        self.reset_idx()

    def tmp_line(self):
        return self.lines[self.tmp_idx]

    def has_more_commands(self):
        return self.tmp_idx + 1 < len(self.lines)
    
    def reset_idx(self):
        self.eq_idx = -1
        self.semicolon_idx = -1

    def advance(self):
        if not self.has_more_commands():
            print('cannot advance anymore')
            raise
        self.tmp_idx += 1
        self.reset_idx()

    def command_type(self):
        if self.tmp_line()[0] == "@":
            type_ = "A"
        elif self.tmp_line()[0] == "(":
            type_ = "L"
        else:
            type_ = "C"
        return "{}_COMMAND".format(type_)

    def symbol(self):
        symbol_ = ""
        for s in self.tmp_line():
            if s not in ("@", "(", ")"):
                symbol_ += s
        return symbol_

    def detect(self):
        # 省略されていてもparseできるようにするための初期値
        self.eq_idx = 0
        self.semicolon_idx = len(self.lines[self.tmp_idx])
        for i, s in enumerate(self.tmp_line()):
            if s == "=":
                self.eq_idx = i
            elif s == ";":
                self.semicolon_idx = i
                break

    def is_detected(self):
        return self.eq_idx != -1 and self.semicolon_idx != -1

    def dest(self):
        if self.command_type() != "C_COMMAND":
            print('dest() cannot be called when command type is C')
            raise
        if not self.is_detected():
            self.detect()
        return self.tmp_line()[:self.eq_idx]

    def has_equal(self):
        if not self.is_detected():
            self.detect()
        return self.eq_idx > 0
    
    def comp(self):
        if self.command_type() != "C_COMMAND":
            print('comp() cannot be called when command type is C')
            raise
        if not self.is_detected():
            self.detect()
        start_idx = self.eq_idx + 1 if self.has_equal() else self.eq_idx
        return self.tmp_line()[start_idx : self.semicolon_idx]
    
    def jump(self):
        if self.command_type() != "C_COMMAND":
            print('jump() cannot be called when command type is C')
            raise
        if not self.is_detected():
            self.detect()
        return self.tmp_line()[self.semicolon_idx+1:]

class Code:
    def __init__(self):
        self.jump_table = {
            "": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }
        self.comp_table = {
            "":"",
            "0":"101010",
            "1":"111111",
            "-1":"111010",
            "D":"001100",
            "A":"110000",
            "!D":"001101",
            "!A":"110001",
            "-D":"001111",
            "-A":"110011",
            "D+1":"011111",
            "A+1":"110111",
            "D-1":"001110",
            "A-1":"110010",
            "D+A":"000010",
            "D-A":"010011",
            "A-D":"000111",
            "D&A":"000000",
            "D|A":"010101"
        }

    def dest(self, mnemonic):
        result = ["0"] * 3
        if "A" in mnemonic:
            result[0] = "1"
        if "D" in mnemonic:
            result[1] = "1"
        if "M" in mnemonic:
            result[2] = "1"
        return "".join(result)

    def jump(self, mnemonic):
        return self.jump_table[mnemonic]

    def comp(self, mnemonic):
        res = ["0"] * 7
        if "M" in mnemonic:
            res[0] = "1"
            mnemonic = mnemonic.replace("M", "A")
        res[1:] = self.comp_table[mnemonic]
        return "".join(res)

class SymbolTable:
    def __init__(self):
        # スクリプト中の処理で２進数に変換する
        # todo: 外側からのアクセスを禁止する
        self.table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576
        }
    def add_entry(self, symbol, address):
        self.table[symbol] = address

    def contains(self, symbol):
        for i in range(16):
            if symbol == "R{}".format(i):
                return True
        return symbol in self.table

    def get_address(self, symbol):
        # R0-R15のチェック
        for i in range(16):
            if symbol == "R{}".format(i):
                return i
        return self.table[symbol]

path = sys.argv[1]
parser = Parser(path)
code = Code()

# 最初のパス
table = SymbolTable()
address = 0
while True:
    if parser.command_type()[0] == "L":
        table.add_entry(parser.symbol(), address)
    else:
        address += 1
    if not parser.has_more_commands():
        break
    parser.advance()

parser.reset()
next_address = 16
with open(path[:-3] + "hack", mode='w') as f:
    while True:
        res = ["0"] * 16
        # print(parser.tmp_line())
        if parser.command_type()[0] == "A":
            symbol = parser.symbol()
            if symbol.isdigit():
                address = int(symbol)
            elif table.contains(symbol):
                address = table.get_address(symbol)
            else:
                address = next_address
                table.add_entry(symbol, address)
                next_address += 1
            res[1:] = "{:015b}".format(address)
            f.write("".join(res))
            f.write("\n")
        elif parser.command_type()[0] == "C":
            res[0:3] = "111"
            res[3:10] = code.comp(parser.comp())
            res[10:13] = code.dest(parser.dest())
            res[13:16] = code.jump(parser.jump())
            f.write("".join(res))
            f.write("\n")
        if not parser.has_more_commands():
            break
        parser.advance()
