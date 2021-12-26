import xml.etree.ElementTree as ET


class ComplilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def add_xml_child(self, parent, child_tag, child_text):
        child = ET.SubElement(parent, child_tag)
        child.text = child_text

    def get_terminal(self, parent, tag, advance=True):
        read = self.tokenizer.read_token(advance)
        token, tag_by_tokenizer = read["token"], read["tag"]
        if tag_by_tokenizer != tag:
            raise Exception
        self.add_xml_child(parent, tag_by_tokenizer, token)

    def get_symbol(self, parent):
        self.tokenizer.advance()
        if self.tokenizer.token_type != "SYMBOL":
            raise Exception
        self.add_xml_child(parent, "symbol", self.token)

    def compile_class(self):
        root = ET.Element("class")
        self.root = root
        self.get_terminal(root, self.tokenizer.TAG_KEYWORD)
        self.get_terminal(root, self.tokenizer.TAG_IDENTFIER, advance=True)
        self.get_terminal(root, self.tokenizer.TAG_SYMBOL, advance=True)
        self.tokenizer.advance()
        while self.tokenizer.token in ("static", "field"):
            self.compile_class_var_dec(root)

    def get_type(self, root):
        if self.tokenizer.read_token(advance=False)["token"] in ("int", "char", "boolean"):
            self.get_terminal(root, self.tokenizer.TAG_KEYWORD)
        else:
            self.get_terminal(root, self.tokenizer.TAG_IDENTIFIER)

    def compile_class_var_dec(self, root):
        '''
        complied pattern) ('static' | 'field') type varName (',' varname)* ';'
        ex) static int x, y;
        '''
        if self.tokenizer.read_token(advance=False)["token"] not in ("static", "field"):
            raise Exception

        class_var_dec = ET.SubElement(root, "classVarDec")
        self.add_xml_child(class_var_dec, "keyword", self.tokenizer.read_token()["token"])
        self.get_type(class_var_dec)
        self.get_terminal(class_var_dec, self.tokenizer.TAG_IDENTIFIER)
        while self.tokenizer.token == ",":
            self.get_terminal(class_var_dec, self.tokenizer.TAG_SYMBOL)
            # get varname
            self.get_terminal(class_var_dec, self.tokenizer.TAG_IDENTIFIER)
        if self.tokenizer.token != ";":
            raise Exception
        self.get_terminal(class_var_dec, self.tokenizer.TAG_SYMBOL, advance=False)
        return

    def output_xml(self, filepath, root=None):
        print(root if root else self.root)
        tree = ET.ElementTree(root if root else self.root)
        ET.indent(tree, space="\t", level=0)
        print("path:", filepath)
        # ET.dump(root)
        tree.write(filepath, encoding="utf-8")
