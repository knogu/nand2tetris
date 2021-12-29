import xml.etree.ElementTree as ET
from const import OP
import pathlib
import fileinput


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
        self.get_terminal(root, self.tokenizer.TAG_IDENTIFIER, advance=True)
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
            self.get_terminal(class_var_dec, self.tokenizer.TAG_IDENTIFIER)
        if self.tokenizer.token != ";":
            raise Exception
        self.get_terminal(class_var_dec, self.tokenizer.TAG_SYMBOL, advance=False)
        return

    def compile_expression(self, parent):
        '''
        compiled pattern) term (op term)*
        '''
        expression = ET.SubElement(parent, "expression")
        self.compile_term(expression)
        while self.tokenizer.read_token(advance=False)["token"] in OP:
            self.add_xml_child(expression, self.tokenizer.TAG_SYMBOL, self.tokenizer.read_token()["token"])
            self.compile_term(expression)

    def compile_term(self, parent):
        term = ET.SubElement(parent, "term")
        read = self.tokenizer.read_token(advance=False)
        if read["tag"] == self.tokenizer.TAG_INTEGER_CONST:
            self.add_xml_child(term, self.tokenizer.TAG_INTEGER_CONST, self.tokenizer.read_token()["token"])
        elif read["tag"] == self.tokenizer.TAG_STRING_CONST:
            self.add_xml_child(term, self.tokenizer.TAG_STRING_CONST, self.tokenizer.read_token()["token"][1:-1])
        elif read["tag"] == self.tokenizer.TAG_KEYWORD:
            if read["token"] not in ("true", "false", "null", "this"):
                raise Exception
            self.add_xml_child(term, self.tokenizer.TAG_KEYWORD, self.tokenizer.read_token()["token"])
        elif read["token"] == "(":
            self.add_xml_child(term, self.tokenizer.TAG_SYMBOL, self.tokenizer.read_token()["token"])
            self.compile_expression(term)
            read_latter = self.tokenizer.read_token()
            if read_latter["token"] != ")":
                raise Exception
            self.add_xml_child(term, self.tokenizer.TAG_SYMBOL, read_latter["token"])
        elif read["token"] in ("-", "~"):
            self.add_xml_child(term, self.tokenizer.TAG_SYMBOL, self.tokenizer.read_token()["token"])
            self.compile_term(term)
        # 以下の場合は先読みが必要
        # ただし、最後のトークンだった場合は変数に決定
        # 配列
        elif self.tokenizer.has_more_tokens() and self.tokenizer.read_next_token()["token"] == "[":
            self.add_xml_child(term, self.tokenizer.TAG_IDENTIFIER, self.tokenizer.read_token()["token"])
            self.add_xml_child(term, self.tokenizer.TAG_SYMBOL, self.tokenizer.read_token()["token"])
            self.compile_expression(term)
            read_latter = self.tokenizer.read_token()
            if read_latter["token"] != "]":
                raise Exception
            self.add_xml_child(term, self.tokenizer.TAG_SYMBOL, read_latter["token"])
        # サブルーチン呼び出し
        elif self.tokenizer.has_more_tokens() and self.tokenizer.read_next_token()["token"] in (".", "("):
            self.compile_subroutine_call(term)
        # 変数
        else:
            self.add_xml_child(term, self.tokenizer.TAG_IDENTIFIER, self.tokenizer.read_token()["token"])

    def compile_expression_list(self, parent):
        # ↓呼び出し元で、expression_listの両側が()で閉じられてることに依存したロジック
        expression_list = ET.SubElement(parent, "expressionList")
        if self.tokenizer.read_token(advance=False)["token"] == ")":
            return
        while True:
            self.compile_expression(expression_list)
            if self.tokenizer.read_token(advance=False)["token"] == ")":
                return
            assert self.tokenizer.read_token(advance=False)["token"] == ","
            self.add_xml_child(expression_list, self.tokenizer.TAG_SYMBOL, self.tokenizer.read_token()["token"])

    def compile_subroutine_call(self, parent):
        '''
        <subRoutineCall>タグの出力はしない
        '''
        self.add_xml_child(parent, self.tokenizer.TAG_IDENTIFIER, self.tokenizer.read_token()["token"])
        # 外部クラスの関数だった場合は追加
        if self.tokenizer.read_token(advance=False)["token"] == ".":
            self.add_xml_child(parent, self.tokenizer.TAG_SYMBOL, self.tokenizer.read_token()["token"])
            self.add_xml_child(parent, self.tokenizer.TAG_IDENTIFIER, self.tokenizer.read_token()["token"])
        assert self.tokenizer.read_token(advance=False)["token"] == "("
        self.add_xml_child(parent, self.tokenizer.TAG_SYMBOL, self.tokenizer.read_token()["token"])
        self.compile_expression_list(parent)
        assert self.tokenizer.read_token(advance=False)["token"] == ")"
        self.add_xml_child(parent, self.tokenizer.TAG_SYMBOL, self.tokenizer.read_token()["token"])

    def compile_return(self, parent):
        assert self.tokenizer.read_token(advance=False)["token"] == "return"
        return_statement = ET.SubElement(parent, "returnStatement")
        self.add_xml_child(return_statement, self.tokenizer.TAG_KEYWORD, self.tokenizer.read_token()["token"])
        if self.tokenizer.read_token(advance=False)["token"] != ";":
            self.compile_expression(return_statement)
        assert self.tokenizer.read_token(advance=False)["token"] == ";"
        self.add_xml_child(return_statement, self.tokenizer.TAG_SYMBOL, self.tokenizer.read_token()["token"])

    def compile_do(self, parent):
        assert self.tokenizer.read_token(advance=False)["token"] == "do"
        do_statement = ET.SubElement(parent, "doStatement")
        self.add_xml_child(do_statement, self.tokenizer.TAG_KEYWORD, self.tokenizer.read_token()["token"])
        self.compile_subroutine_call(do_statement)
        assert self.tokenizer.read_token(advance=False)["token"] == ";"
        self.add_xml_child(do_statement, self.tokenizer.TAG_SYMBOL, self.tokenizer.read_token()["token"])

    def output_xml(self, filepath, root):
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        path = str(pathlib.Path(__file__).parent) + "/" + filepath
        tree.write(path, encoding="utf-8", short_empty_elements=False)
        # 空要素のタグ間に改行を入れる（nand2tetrisのツールでの比較のため）
        for line in fileinput.input(path, inplace=True):
            print(line.replace("></", ">\n</"), end='')
