import xml.etree.ElementTree as ET
from const import OP, TAG_KEYWORD, TAG_SYMBOL, TAG_IDENTIFIER, TAG_INTEGER_CONST, TAG_STRING_CONST, CONSTANT,\
    ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP, OP_COMMAND, VAR, UNARY_OP
import pathlib
import fileinput
from vm_writer import VMWriter
from symbol_table import SymbolTable


class ComplilationEngine:
    def __init__(self, tokenizer, vm_out_path=None, symbol_table=None):
        self.tokenizer = tokenizer
        if vm_out_path:
            self.vm_writer = VMWriter(vm_out_path)
            if symbol_table:
                self.symbol_table = symbol_table
            else:
                self.symbol_table = SymbolTable()

    def sub_with_text(self, parent, child_tag, child_text):
        child = ET.SubElement(parent, child_tag)
        child.text = child_text

    def add_and_advance(self, parent, asserted_tag, asserted_token=None, advance=True):
        '''
        現在のトークンをツリーに追加し、advanceがTrueならトークンを進める
        なるべくadvance=Trueにする（読み取りと同時にトークンが進む、というパターンでトークンの進みを管理したいので）
        '''
        read = self.tokenizer.read_token()
        if asserted_tag:
            assert read["tag"] == asserted_tag
        if asserted_token:
            assert read["token"] == asserted_token
        self.sub_with_text(parent, read["tag"], read["token"])

    def check_current_token(self):
        '''
        現在のトークンを返す。トークンを進めはしない
        '''
        return self.tokenizer.read_token(advance=False)["token"]

    def compile_class(self):
        self.root = ET.Element("class")
        self.add_and_advance(self.root, TAG_KEYWORD)
        self.add_and_advance(self.root, TAG_IDENTIFIER)
        self.add_and_advance(self.root, TAG_SYMBOL, "{")
        while self.check_current_token() in ("static", "field"):
            self.compile_class_var_dec(self.root)
        while self.check_current_token() != "}":
            self.compile_subroutine_dec(self.root)
        self.add_and_advance(self.root, TAG_SYMBOL, "}")

    def output_class(self):
        class_name = self.root[1].text
        # TODO: class_var_dec
        for subroutine_dec in self.root.findall("subroutineDec"):
            self.output_subroutine_dec(subroutine_dec, class_name)
        return

    def output_subroutine_dec(self, subroutine_dec, class_name):
        subroutine_name = subroutine_dec[2].text
        # TODO: ローカル変数の個数を渡す（一旦0）
        self.vm_writer.write_func(class_name, subroutine_name, 0)
        # TODO: 引数の取得
        self.output_subroutine_body(subroutine_dec.find("subroutineBody"))
        return

    def output_subroutine_body(self, subroutine_body):
        var_dec_list = subroutine_body.findall("varDec")
        if var_dec_list:
            for var_dec in var_dec_list:
                self.output_var_dec(var_dec)
        self.output_statements(subroutine_body.find("statements"))
        return

    # TODO: クラスのインスタンスの対応
    def output_var_dec(self, var_dec):
        type = var_dec[1]
        for identifier in var_dec.findall("identifier"):
            symbol = self.symbol_table.define(identifier.text, type, VAR)
            # ローカル変数の初期化
            self.vm_writer.write_push(CONSTANT, 0)
            self.vm_writer.write_pop(LOCAL, symbol.number)

    def output_statements(self, statements):
        for statement in statements:
            if statement.tag == "doStatement":
                self.output_do(statement)
            elif statement.tag == "returnStatement":
                self.output_return(statement)
            elif statement.tag == "letStatement":
                self.output_let(statement)
            else:
                raise Exception
        return

    def output_return(self, statement):
        # TODO: 返り値
        self.vm_writer.write_return()

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
        self.add_and_advance(class_var_dec, TAG_SYMBOL, ";")
        return

    def compile_var_dec(self, parent):
        var_dec = ET.SubElement(parent, "varDec")
        self.add_and_advance(var_dec, TAG_KEYWORD, "var")
        self.get_type(var_dec)
        self.add_and_advance(var_dec, TAG_IDENTIFIER)
        while self.check_current_token() == ",":
            self.add_and_advance(var_dec, TAG_SYMBOL)
            self.add_and_advance(var_dec, TAG_IDENTIFIER)
        self.add_and_advance(var_dec, TAG_SYMBOL, ";")
        return var_dec

    def compile_expression(self, parent):
        '''
        compiled pattern) term (op term)*
        '''
        expression = ET.SubElement(parent, "expression")
        self.compile_term(expression)
        while self.check_current_token() in OP:
            self.add_and_advance(expression, TAG_SYMBOL)
            self.compile_term(expression)
        return expression

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
            self.add_and_advance(term, TAG_SYMBOL, ")")
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

    # TODO: ElementTreeの機能でリプレイスできないか？
    def bracket_is_included(self, parent: ET.Element):
        for child in parent:
            if child.text == "(" and child.tag == "symbol":
                return True
        return False

    # termをpushするvmプログラムを出力
    def output_term(self, term: ET.Element):
        if len(term) == 1:
            if term[0].tag == TAG_INTEGER_CONST:
                self.vm_writer.write_push(CONSTANT, int(term[0].text))
            elif term[0].tag == TAG_IDENTIFIER:
                symbol = self.symbol_table.symbol(term[0].text)
                self.vm_writer.write_push(symbol.segment(), symbol.number)
            else:
                raise Exception
        elif term[0].text == "(":
            self.output_expression(term[1])
        elif term[0].text in UNARY_OP:
            self.output_term(term[1])
            self.vm_writer.write_arithmetic(OP_COMMAND[term[0].text])
        # サブルーチン呼び出し←→term[0]が"("でなく（↑でカバー済）、かつ"("が含まれている、とする
        elif self.bracket_is_included(term):
            self.output_subroutine_call(term)
        else:
            raise Exception

    def output_op(self, op):
        self.vm_writer.write_arithmetic(OP_COMMAND[op.text])

    def create_expression(self, children: list[ET.Element]):
        expression = ET.Element("expression")
        for child in children:
            expression.append(child)
        return expression

    # expressionのノードをどう初期化するか、は要検討かも（とりあえず引数で受け取る）
    def output_expression(self, expression: ET.Element):
        # term (op term)* の形だから、childの数が偶数にはならない
        if len(expression) % 2 == 0:
            raise Exception
        self.output_term(expression[0])
        # 最初のtermの後に、op termが一度以上続く場合
        if len(expression) >= 3:
            self.output_expression(self.create_expression(expression[2:]))
            self.output_op(expression[1])

    def compile_expression_list(self, parent):
        # ↓呼び出し元で、expression_listの両側が()で閉じられてることに依存したロジック
        expression_list = ET.SubElement(parent, "expressionList")
        if self.check_current_token() == ")":
            return
        while True:
            self.compile_expression(expression_list)
            if self.check_current_token() == ")":
                return
            self.add_and_advance(expression_list, TAG_SYMBOL, ",")

    def compile_subroutine_call(self, parent):
        '''
        <subRoutineCall>タグの出力はしない
        '''
        self.add_and_advance(parent, TAG_IDENTIFIER)
        # 外部クラスの関数だった場合は追加
        if self.check_current_token() == ".":
            self.add_and_advance(parent, TAG_SYMBOL)
            self.add_and_advance(parent, TAG_IDENTIFIER)
        self.add_and_advance(parent, TAG_SYMBOL, "(")
        self.compile_expression_list(parent)
        self.add_and_advance(parent, TAG_SYMBOL, ")")

    # subroutine_call要素は、仕様によりxmlタグとして出力することはない
    # しかし、output_subroutine_callを呼ぶ上でsubroutine_call要素が存在したほうが実装しやすいので、呼ぶ前に作成する
    # subroutine_callはdoとtermしか子要素として持たず、それらの場合のsubroutine_call要素の作成は容易
    def output_subroutine_call(self, subroutine_call):
        func_name = ""
        for child in subroutine_call:
            if child.text == "(":
                break
            func_name += child.text

        # expression_list includes symbols
        expression_list = subroutine_call.find("expressionList")
        # 区切りのコンマに対しては何もしなくて良いはず
        expressions = expression_list.findall("expression")
        for expression in expressions:
            self.output_expression(expression)

        self.vm_writer.write_call(func_name, len(expressions))
        return

    def compile_return(self, parent):
        return_statement = ET.SubElement(parent, "returnStatement")
        self.add_and_advance(return_statement, TAG_KEYWORD, "return")
        if self.check_current_token() != ";":
            self.compile_expression(return_statement)
        self.add_and_advance(return_statement, TAG_SYMBOL, ";")

    def compile_do(self, parent):
        do_statement = ET.SubElement(parent, "doStatement")
        self.add_and_advance(do_statement, TAG_KEYWORD, "do")
        self.compile_subroutine_call(do_statement)
        self.add_and_advance(do_statement, TAG_SYMBOL, ";")
        return do_statement

    def output_do(self, do_statement: ET.Element):
        do_statement.remove(do_statement[0])
        do_statement.remove(do_statement[-1])
        self.output_subroutine_call(do_statement)

    def compile_let(self, parent):
        let_statement = ET.SubElement(parent, "letStatement")
        self.add_and_advance(let_statement, TAG_KEYWORD, "let")
        self.add_and_advance(let_statement, TAG_IDENTIFIER)
        if self.check_current_token() == "[":
            self.add_and_advance(let_statement, TAG_SYMBOL)
            self.compile_expression(let_statement)
            self.add_and_advance(let_statement, TAG_SYMBOL, "]")
        self.add_and_advance(let_statement, TAG_SYMBOL, "=")
        self.compile_expression(let_statement)
        self.add_and_advance(let_statement, TAG_SYMBOL, ";")
        return let_statement

    def output_let(self, let_statement):
        # まずlet式の右辺をpush
        assert let_statement[-2].tag == "expression"
        self.output_expression(let_statement[-2])
        assert let_statement[1].tag == TAG_IDENTIFIER
        symbol = self.symbol_table.symbol(let_statement[1].text)
        self.vm_writer.write_pop(symbol.segment(), symbol.number)

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
        if_statement = ET.SubElement(parent, "ifStatement")
        self.add_and_advance(if_statement, TAG_KEYWORD, "if")
        self.add_and_advance(if_statement, TAG_SYMBOL, "(")
        self.compile_expression(if_statement)
        self.add_and_advance(if_statement, TAG_SYMBOL, ")")
        self.add_and_advance(if_statement, TAG_SYMBOL, "{")
        self.compile_statements(if_statement)
        self.add_and_advance(if_statement, TAG_SYMBOL, "}")
        if self.check_current_token() == "else":
            self.add_and_advance(if_statement, TAG_KEYWORD)
            self.add_and_advance(if_statement, TAG_SYMBOL, "{")
            self.compile_statements(if_statement)
            self.add_and_advance(if_statement, TAG_SYMBOL, "}")

    def compile_while(self, parent):
        while_statement = ET.SubElement(parent, "whileStatement")
        self.add_and_advance(while_statement, TAG_KEYWORD, "while")
        self.add_and_advance(while_statement, TAG_SYMBOL, "(")
        self.compile_expression(while_statement)
        self.add_and_advance(while_statement, TAG_SYMBOL, ")")
        self.add_and_advance(while_statement, TAG_SYMBOL, "{")
        self.compile_statements(while_statement)
        self.add_and_advance(while_statement, TAG_SYMBOL, "}")

    def compile_subroutine_body(self, parent):
        subroutine_body = ET.SubElement(parent, "subroutineBody")
        self.add_and_advance(subroutine_body, TAG_SYMBOL, "{")
        while self.check_current_token() == "var":
            self.compile_var_dec(subroutine_body)
        self.compile_statements(subroutine_body)
        self.add_and_advance(subroutine_body, TAG_SYMBOL, "}")

    def compile_parameter_list(self, parent):
        parameter_list = ET.SubElement(parent, "parameterList")
        # 引数なしだった場合
        if self.check_current_token() == ")":
            return
        while True:
            self.get_type(parameter_list)
            self.add_and_advance(parameter_list, TAG_IDENTIFIER)
            if self.check_current_token() != ",":
                break
            self.add_and_advance(parameter_list, TAG_SYMBOL, ",")

    def compile_subroutine_dec(self, parent):
        subroutine_dec = ET.SubElement(parent, "subroutineDec")
        assert self.check_current_token() in ("constructor", "function", "method")
        self.add_and_advance(subroutine_dec, TAG_KEYWORD)
        if self.check_current_token() == "void":
            self.add_and_advance(subroutine_dec, TAG_KEYWORD)
        else:
            self.get_type(subroutine_dec)
        self.add_and_advance(subroutine_dec, TAG_IDENTIFIER)
        self.add_and_advance(subroutine_dec, TAG_SYMBOL, "(")
        self.compile_parameter_list(subroutine_dec)
        self.add_and_advance(subroutine_dec, TAG_SYMBOL, ")")
        self.compile_subroutine_body(subroutine_dec)

    def output_xml(self, filepath, root=None, abspath=False):
        tree = ET.ElementTree(root if root else self.root)
        ET.indent(tree, space="\t", level=0)
        path = filepath if abspath else str(pathlib.Path(__file__).parent) + "/" + filepath
        tree.write(path, encoding="utf-8", short_empty_elements=False)
        # 空要素のタグ間に改行を入れる（nand2tetrisのツールでの比較のため）
        for line in fileinput.input(path, inplace=True):
            print(line.replace("></", ">\n</"), end='')
