import xml.etree.ElementTree as ET
from const import OP, TAG_KEYWORD, TAG_SYMBOL, TAG_IDENTIFIER, TAG_INTEGER_CONST, TAG_STRING_CONST
import pathlib
import fileinput


class ComplilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def sub_with_text(self, parent, child_tag, child_text):
        child = ET.SubElement(parent, child_tag)
        child.text = child_text

    def add_and_advance(self, parent, asserted_tag, advance=True):
        '''
        現在のトークンをツリーに追加し、advanceがTrueならトークンを進める
        なるべくadvance=Trueにする（読み取りと同時にトークンが進む、というパターンでトークンの進みを管理したいので）
        '''
        read = self.tokenizer.read_token()
        assert asserted_tag and read["tag"] == asserted_tag
        self.sub_with_text(parent, read["tag"], read["token"])

    def check_current_token(self):
        '''
        現在のトークンを返す。トークンを進めはしない
        '''
        return self.tokenizer.read_token(advance=False)["token"]

    def compile_class(self):
        root = ET.Element("class")
        self.root = root
        self.add_and_advance(root, TAG_KEYWORD)
        self.add_and_advance(root, TAG_IDENTIFIER)
        self.add_and_advance(root, TAG_SYMBOL)
        self.tokenizer.advance()
        while self.tokenizer.token in ("static", "field"):
            self.compile_class_var_dec(root)

    def get_type(self, root):
        if self.check_current_token() in ("int", "char", "boolean"):
            self.add_and_advance(root, TAG_KEYWORD)
        else:
            self.add_and_advance(root, TAG_IDENTIFIER)

    def compile_class_var_dec(self, root):
        '''
        complied pattern) ('static' | 'field') type varName (',' varname)* ';'
        ex) static int x, y;
        '''
        assert self.check_current_token() in ("static", "field")
        class_var_dec = ET.SubElement(root, "classVarDec")
        self.add_and_advance(class_var_dec, TAG_KEYWORD)
        self.get_type(class_var_dec)
        self.add_and_advance(class_var_dec, TAG_IDENTIFIER)
        while self.tokenizer.token == ",":
            self.add_and_advance(class_var_dec, TAG_SYMBOL)
            self.add_and_advance(class_var_dec, TAG_IDENTIFIER)
        assert self.tokenizer.token == ";"
        self.add_and_advance(class_var_dec, TAG_SYMBOL)
        return

    def compile_var_dec(self, parent):
        assert self.check_current_token() == "var"
        var_dec = ET.SubElement(parent, "varDec")
        self.add_and_advance(var_dec, TAG_KEYWORD)
        self.get_type(var_dec)
        self.add_and_advance(var_dec, TAG_IDENTIFIER)
        while self.check_current_token() == ",":
            self.add_and_advance(var_dec, TAG_SYMBOL)
            self.add_and_advance(var_dec, TAG_IDENTIFIER)
        assert self.check_current_token() == ";"
        self.add_and_advance(var_dec, TAG_SYMBOL)

    def compile_expression(self, parent):
        '''
        compiled pattern) term (op term)*
        '''
        expression = ET.SubElement(parent, "expression")
        self.compile_term(expression)
        while self.check_current_token() in OP:
            self.add_and_advance(expression, TAG_SYMBOL)
            self.compile_term(expression)

    def compile_term(self, parent):
        term = ET.SubElement(parent, "term")
        read = self.tokenizer.read_token(advance=False)
        if read["tag"] == TAG_INTEGER_CONST:
            self.add_and_advance(term, TAG_INTEGER_CONST)
        elif read["tag"] == TAG_STRING_CONST:
            self.sub_with_text(term, TAG_STRING_CONST, self.tokenizer.read_token()["token"][1:-1])
        elif read["tag"] == TAG_KEYWORD:
            assert read["token"] in ("true", "false", "null", "this")
            self.add_and_advance(term, TAG_KEYWORD)
        elif read["token"] == "(":
            self.add_and_advance(term, TAG_SYMBOL)
            self.compile_expression(term)
            assert self.check_current_token() == ")"
            self.add_and_advance(term, TAG_SYMBOL)
        elif read["token"] in ("-", "~"):
            self.add_and_advance(term, TAG_SYMBOL)
            self.compile_term(term)
        # 以下の場合は先読みが必要
        # ただし、最後のトークンだった場合は変数に決定
        # 配列
        elif self.tokenizer.has_more_tokens() and self.tokenizer.read_next_token()["token"] == "[":
            self.add_and_advance(term, TAG_IDENTIFIER)
            self.add_and_advance(term, TAG_SYMBOL)
            self.compile_expression(term)
            assert self.check_current_token() == "]"
            self.add_and_advance(term, TAG_SYMBOL)
        # サブルーチン呼び出し
        elif self.tokenizer.has_more_tokens() and self.tokenizer.read_next_token()["token"] in (".", "("):
            self.compile_subroutine_call(term)
        # 変数
        else:
            self.add_and_advance(term, TAG_IDENTIFIER)

    def compile_expression_list(self, parent):
        # ↓呼び出し元で、expression_listの両側が()で閉じられてることに依存したロジック
        expression_list = ET.SubElement(parent, "expressionList")
        if self.check_current_token() == ")":
            return
        while True:
            self.compile_expression(expression_list)
            if self.check_current_token() == ")":
                return
            assert self.check_current_token() == ","
            self.add_and_advance(expression_list, TAG_SYMBOL)

    def compile_subroutine_call(self, parent):
        '''
        <subRoutineCall>タグの出力はしない
        '''
        self.add_and_advance(parent, TAG_IDENTIFIER)
        # 外部クラスの関数だった場合は追加
        if self.check_current_token() == ".":
            self.add_and_advance(parent, TAG_SYMBOL)
            self.add_and_advance(parent, TAG_IDENTIFIER)
        assert self.check_current_token() == "("
        self.add_and_advance(parent, TAG_SYMBOL)
        self.compile_expression_list(parent)
        assert self.check_current_token() == ")"
        self.add_and_advance(parent, TAG_SYMBOL)

    def compile_return(self, parent):
        assert self.check_current_token() == "return"
        return_statement = ET.SubElement(parent, "returnStatement")
        self.add_and_advance(return_statement, TAG_KEYWORD)
        if self.check_current_token() != ";":
            self.compile_expression(return_statement)
        assert self.check_current_token() == ";"
        self.add_and_advance(return_statement, TAG_SYMBOL)

    def compile_do(self, parent):
        assert self.check_current_token() == "do"
        do_statement = ET.SubElement(parent, "doStatement")
        self.add_and_advance(do_statement, TAG_KEYWORD)
        self.compile_subroutine_call(do_statement)
        assert self.check_current_token() == ";"
        self.add_and_advance(do_statement, TAG_SYMBOL)

    def compile_let(self, parent):
        assert self.check_current_token() == "let"
        let_statement = ET.SubElement(parent, "letStatement")
        self.add_and_advance(let_statement, TAG_KEYWORD)
        self.add_and_advance(let_statement, TAG_IDENTIFIER)
        if self.check_current_token() == "[":
            self.add_and_advance(let_statement, TAG_SYMBOL)
            self.compile_expression(let_statement)
            assert self.check_current_token() == "]"
            self.add_and_advance(let_statement, TAG_SYMBOL)
        assert self.check_current_token() == "="
        self.add_and_advance(let_statement, TAG_SYMBOL)
        self.compile_expression(let_statement)
        assert self.check_current_token() == ";"
        self.add_and_advance(let_statement, TAG_SYMBOL)

    def compile_statements(self, parent):
        statements = ET.SubElement(parent, "statements")
        while True:
            if self.check_current_token() == "let":
                self.compile_let(statements)
            elif self.check_current_token() == "if":
                self.compile_if(statements)
            elif self.check_current_token() == "while":
                self.compile_while(statements)
            elif self.check_current_token() == "do":
                self.compile_do(statements)
            elif self.check_current_token() == "return":
                self.compile_return(statements)
            else:
                break

    def compile_if(self, parent):
        assert self.check_current_token() == "if"
        if_statement = ET.SubElement(parent, "ifStatement")
        self.add_and_advance(if_statement, TAG_KEYWORD)
        assert self.check_current_token() == "("
        self.add_and_advance(if_statement, TAG_SYMBOL)
        self.compile_expression(if_statement)
        assert self.check_current_token() == ")"
        self.add_and_advance(if_statement, TAG_SYMBOL)
        assert self.check_current_token() == "{"
        self.add_and_advance(if_statement, TAG_SYMBOL)
        self.compile_statements(if_statement)
        assert self.check_current_token() == "}"
        self.add_and_advance(if_statement, TAG_SYMBOL)
        if self.check_current_token() == "else":
            self.add_and_advance(if_statement, TAG_KEYWORD)
            assert self.check_current_token() == "{"
            self.add_and_advance(if_statement, TAG_SYMBOL)
            self.compile_statements(if_statement)
            assert self.check_current_token() == "}"
            self.add_and_advance(if_statement, TAG_SYMBOL)

    def compile_while(self, parent):
        assert self.check_current_token() == "while"
        while_statement = ET.SubElement(parent, "whileStatement")
        self.add_and_advance(while_statement, TAG_KEYWORD)
        assert self.check_current_token() == "("
        self.add_and_advance(while_statement, TAG_SYMBOL)
        self.compile_expression(while_statement)
        assert self.check_current_token() == ")"
        self.add_and_advance(while_statement, TAG_SYMBOL)
        assert self.check_current_token() == "{"
        self.add_and_advance(while_statement, TAG_SYMBOL)
        self.compile_statements(while_statement)
        assert self.check_current_token() == "}"
        self.add_and_advance(while_statement, TAG_SYMBOL)

    def output_xml(self, filepath, root):
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        path = str(pathlib.Path(__file__).parent) + "/" + filepath
        tree.write(path, encoding="utf-8", short_empty_elements=False)
        # 空要素のタグ間に改行を入れる（nand2tetrisのツールでの比較のため）
        for line in fileinput.input(path, inplace=True):
            print(line.replace("></", ">\n</"), end='')
