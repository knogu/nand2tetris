import re

class JackTokenizer:
    SYMBOLS = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}

    def __init__(self, file):
        with open(file) as f:
            s = f.read()
        s = self.remove_comments(s)
        s = re.sub('(^|(?<=\n))\t*\n', '', s)
        s = re.sub('\t', '', s)
        self.s = s
        self.seperate()
    
    def seperate(self):
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
        s = re.sub('/\*.*\*/', '', s)
        pattern = re.compile(r'(?:^|(?<=\n))(.*)//.*(?:$|(?=\n))')
        s = pattern.sub(r'\1', s)
        return s
