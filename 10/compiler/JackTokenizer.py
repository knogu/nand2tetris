import re
import xml.etree.ElementTree as ET

class JackTokenizer:
    SYMBOLS = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
    KEYWORDS = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",\
        "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}

    def __init__(self, file):
        with open(file) as f:
            s = f.read()
        s = self.remove_comments(s)
        s = re.sub('(^|(?<=\n))\t*\n', '', s)
        s = re.sub('\t', '', s)
        self.s = s
        self.init_tokens()
        self.token_i = 0
        self.token = self.tokens[self.token_i]

    def has_more_tokens(self):
        return self.token_i+1 < len(self.tokens)

    def advance(self):
        self.token_i += 1
        self.token = self.tokens[self.token_i]

    def token_type(self):
        if self.token in self.KEYWORDS:
            return "KEYWORD"
        elif self.token in self.SYMBOLS:
            return "SYMBOL"
        elif re.fullmatch(r'\d+', self.token):
            return "INT_CONST"
        elif self.is_str(self.token):
            return "STRING_CONST"
        else:
            return "IDENTIFIER"

    def token_tag(self):
        if self.token_type() == "KEYWORD":
            return "keyword"
        elif self.token_type() == "SYMBOL":
            return "symbol"
        elif self.token_type() == "INT_CONST":
            return "integerConstant"
        elif self.token_type() == "STRING_CONST":
            return "stringConstant"
        elif self.token_type() == "IDENTIFIER":
            return "identifier"
        else:
            raise

    def init_tokens(self):
        self.tokens = self.s.split("\n")
        self.tokens = self.serparate_str()
        self.tokens = self.separete_by_space()
        self.tokens = self.seperate_by_symbols()

    def is_str(self, s):
        return s[0] == s[-1] == "\""

    def serparate_str(self):
        new = []
        for token in self.tokens:
            groups = token.split("\"")
            for i, group in enumerate(groups):
                if i % 2 == 0:
                    new.append(group)
                else:
                    new.append("\"" + group + "\"")
        return new

    def separete_by_space(self):
        new = []
        for token in self.tokens:
            if len(token) == 0:
                continue
            if self.is_str(token):
                new.append(token)
                continue
            groups = token.split(" ")
            for group in groups:
                if len(group) > 0:
                    new.append(group)
        return new

    def seperate_by_symbols(self):
        new = []
        for token in self.tokens:
            word = []
            for s in token:
                if s in self.SYMBOLS:
                    if word:
                        new.append("".join(word))
                        word = []
                    new.append(s)
                else:
                    word.append(s)
            if word:
                new.append("".join(word))
        return new

    def remove_comments(self, s):
        s = re.sub('/\*[\s\S.]*?\*/', '', s)
        # 行先頭からの//コメント
        s = re.sub('(?:^|(?<=\n))//.*(?:$|(?=\n))', '', s)
        # 行途中からの//コメント
        pattern = re.compile(r'(?:^|(?<=\n))(.*)//.*(?:$|(?=\n))')
        s = pattern.sub(r'\1', s)
        return s

    def create_token_xml(self, filepath):
        root = ET.Element("tokens")
        while True:
            token_xml = ET.SubElement(root, self.token_tag())
            if self.token_type() == "STRING_CONST":
                token_xml.text = self.token[1:-1]
            else:
                token_xml.text = self.token
            if not self.has_more_tokens():
                break
            self.advance()
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(filepath)
