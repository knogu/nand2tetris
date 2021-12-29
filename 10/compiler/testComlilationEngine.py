import unittest
from CompilationEngine import ComplilationEngine
from JackTokenizer import JackTokenizer
import xml.etree.ElementTree as ET
import subprocess
import pathlib


class TestComplilationEngine(unittest.TestCase):
    def set_up_compiler(self, input):
        self.root = ET.Element("root")
        tokenizer = JackTokenizer(input)
        compiler = ComplilationEngine(tokenizer)
        return compiler

    def check(self, compiler, output_file, asserted_file):
        compiler.output_xml(output_file, self.root)
        try:
            out = subprocess.check_output(["/Users/noguchikoutarou/nand2tetris/tools/TextComparer.sh",
                                           str(pathlib.Path(__file__).parent) + "/" + output_file,
                                           str(pathlib.Path(__file__).parent) + "/" + asserted_file
                                           ])
            self.assertEqual(b'Comparison ended successfully\n', out)
            if b'Comparison ended successfully\n' != out:
                print(out)
        except Exception as e:
            print("\n", e)
            subprocess.run(["/Users/noguchikoutarou/nand2tetris/tools/TextComparer.sh",
                           str(pathlib.Path(__file__).parent) + "/" + output_file,
                           str(pathlib.Path(__file__).parent) + "/" + asserted_file
                            ])

    def test_compile_class_var_dec(self):
        s = '''
        static int a, b;
        '''
        compiler = self.set_up_compiler(s)
        compiler.compile_class_var_dec(self.root)
        self.check(compiler, "unit_tests/class_var_dec/actual/simple.xml",
                             "unit_tests/class_var_dec/asserted/simple.xml")

    def test_compile_expression(self):
        fixture = [
            {"input": "\"string constant\"", "asserted_file": "unit_tests/expression/asserted/just_a_term.xml"},
            {"input": "i | j", "asserted_file": "unit_tests/expression/asserted/binomial.xml"},
            {"input": "(y + size) - 1", "asserted_file": "unit_tests/expression/asserted/trinomial.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_expression(self.root)
                self.check(compiler, "/unit_tests/expression/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_term(self):
        fixture = [
            # integerConstant
            {"input": "333", "asserted_file": "unit_tests/term/assertion/integer_constant.xml"},
            # stringConstant
            {"input": "\"this is test 333\"", "asserted_file": "unit_tests/term/assertion/string_constant.xml"},
            # keywordConstant
            {"input": "null", "asserted_file": "unit_tests/term/assertion/keyword_constant.xml"},
            # varname
            {"input": "x", "asserted_file": "unit_tests/term/assertion/varname.xml"},
            # 配列: varname[expression]
            {"input": "a[2]", "asserted_file": "unit_tests/term/assertion/list.xml"},
            # subroutineCall
            {"input": "draw()", "asserted_file": "unit_tests/term/assertion/self_subroutine_call.xml"},
            {"input": "Keyboard.keyPressed()", "asserted_file": "unit_tests/term/assertion/outer_subroutine_call.xml"},
            {"input": "Keyboard.readInt(\"HOW MANY NUMBERS? \", arg2)",
             "asserted_file": "unit_tests/term/assertion/outer_subroutine_call_with_arg.xml"},
            # (expression)
            {"input": "(333)", "asserted_file": "unit_tests/term/assertion/in_bracket.xml"},
            # unaryOp term
            {"input": "- j", "asserted_file": "unit_tests/term/assertion/unary_op.xml"}
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_term(self.root)
                self.check(compiler, "unit_tests/term/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_return(self):
        fixture = [
            {"input": "return;", "asserted_file": "unit_tests/return/asserted/return_none.xml"},
            {"input": "return x;", "asserted_file": "unit_tests/return/asserted/return_x.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_return(self.root)
                self.check(compiler, "unit_tests/return/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_do(self):
        fixture = [
            {"input": "do draw();", "asserted_file": "unit_tests/do/asserted/simple.xml"},
            {"input": "do Memory.deAlloc(this);", "asserted_file": "unit_tests/do/asserted/external_with_arg.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_do(self.root)
                self.check(compiler, "unit_tests/do/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_let(self):
        fixture = [
            {"input": "let key = key;", "asserted_file": "unit_tests/let/asserted/simple.xml"},
            {"input": "let a[i] = Keyboard.readInt(\"ENTER THE NEXT NUMBER: \");",
             "asserted_file": "unit_tests/let/asserted/list.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_let(self.root)
                self.check(compiler, "unit_tests/do/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_while(self):
        fixture = [
            {"input": '''
                while (key) {
                    let key = key;
                    do moveSquare();
                }
            ''',
             "asserted_file": "unit_tests/do/asserted/simple.xml"},
        ]


if __name__ == "__main__":
    unittest.main()
