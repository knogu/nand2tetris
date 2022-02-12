import unittest
from compilation_engine import ComplilationEngine
from jack_tokenizer import JackTokenizer
from symbol_table import SymbolTable
from const import *
import xml.etree.ElementTree as ET
import subprocess
import pathlib
import os


class TestComplilationEngine(unittest.TestCase):
    def set_up_compiler(self, input, vm_out=None, symbol_table=None):
        self.root = ET.Element("root")
        tokenizer = JackTokenizer(input)
        compiler = ComplilationEngine(tokenizer, vm_out, symbol_table)
        return compiler

    def check_xml(self, compiler, output_file, asserted_file):
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
            raise AssertionError

    def check_vm(self, output_file, asserted_file):
        try:
            out = subprocess.check_output(["/Users/noguchikoutarou/nand2tetris/tools/TextComparer.sh",
                                           output_file,
                                           str(pathlib.Path(__file__).parent) + "/" + asserted_file
                                           ])
            self.assertEqual(b'Comparison ended successfully\n', out)
            if b'Comparison ended successfully\n' != out:
                print(out)
        except Exception as e:
            print("\n", e)
            subprocess.run(["/Users/noguchikoutarou/nand2tetris/tools/TextComparer.sh",
                            output_file,
                            str(pathlib.Path(__file__).parent) + "/" + asserted_file
                            ])
            raise AssertionError

    def test_compile_class_var_dec(self):
        s = '''
        static int a, b;
        '''
        compiler = self.set_up_compiler(s)
        compiler.compile_class_var_dec(self.root)
        self.check_xml(compiler, "unit_tests/class_var_dec/actual/simple.xml",
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
                self.check_xml(compiler, "/unit_tests/expression/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_output_expression(self):
        fixture = [
            {"input": "1 + (2 * 3)", "asserted_file": "unit_tests/output_expression/asserted/one.vm"},
            # {"input": "x+g(2,y,-z)*5", "asserted_file": "unit_tests/output_expression/asserted/p259.vm"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                out_path = "/Users/noguchikoutarou/nand2tetris/projects/10/compiler/unit_tests/output_expression/actual/out_{}.vm".format(i)
                compiler = self.set_up_compiler(test["input"], out_path)
                exp = compiler.compile_expression(self.root)
                compiler.output_expression(exp)
                compiler.vm_writer.f.close()
                self.check_vm(out_path, test["asserted_file"])

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
                self.check_xml(compiler, "unit_tests/term/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_return(self):
        fixture = [
            {"input": "return;", "asserted_file": "unit_tests/return/asserted/return_none.xml"},
            {"input": "return x;", "asserted_file": "unit_tests/return/asserted/return_x.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_return(self.root)
                self.check_xml(compiler, "unit_tests/return/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_do(self):
        fixture = [
            {"input": "do draw();", "asserted_file": "unit_tests/do/asserted/simple.xml"},
            {"input": "do Memory.deAlloc(this);", "asserted_file": "unit_tests/do/asserted/external_with_arg.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_do(self.root)
                self.check_xml(compiler, "unit_tests/do/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_output_do(self):
        fixture = [
            {"input": "do Output.printInt(1 + (2 * 3));", "asserted_file": "unit_tests/output_do/asserted/seven.vm"},
            {"input": "do Main.fillMemory(8001, 16, -1);", "asserted_file": "unit_tests/output_do/asserted/fill_memory.vm"}
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                out_path = "/Users/noguchikoutarou/nand2tetris/projects/10/compiler/unit_tests/output_do/actual/out_{}.vm".format(i)
                compiler = self.set_up_compiler(test["input"], out_path)
                do_statement = compiler.compile_do(self.root)
                compiler.output_do(do_statement)
                compiler.vm_writer.f.close()
                self.check_vm(out_path, test["asserted_file"])

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
                self.check_xml(compiler, "unit_tests/do/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_output_let(self):
        fixture = [
            {"input": "let value = Memory.peek(8000); ", "asserted_file": "unit_tests/output_let/asserted/peek_memory.vm"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                out_path = "/Users/noguchikoutarou/nand2tetris/projects/10/compiler/unit_tests/output_let/actual/out_{}.vm".format(i)
                symbol_table = SymbolTable()
                symbol_table.define("value", "int", VAR)
                compiler = self.set_up_compiler(test["input"], out_path, symbol_table)
                do_statement = compiler.compile_let(self.root)
                compiler.output_let(do_statement)
                compiler.vm_writer.f.close()
                self.check_vm(out_path, test["asserted_file"])

    def test_compile_statements(self):
        fixture = [
            {"input": '''
                let sum = sum + a[i];
                let i = i + 1;
            ''',
             "asserted_file": "unit_tests/statements/asserted/one.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_statements(self.root)
                self.check_xml(compiler, "unit_tests/statements/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_while(self):
        fixture = [
            {"input": '''
                while (key) {
                    let key = key;
                    do moveSquare();
                }
            ''',
             "asserted_file": "unit_tests/while/asserted/one.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_while(self.root)
                self.check_xml(compiler, "unit_tests/while/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_if(self):
        fixture = [
            {"input": '''
                if ((x + size) < 510) {
                    do Screen.setColor(false);
                    do Screen.drawRectangle(x, y, x + 1, y + size);
                    let x = x + 2;
                    do Screen.setColor(true);
                    do Screen.drawRectangle((x + size) - 1, y, x + size, y + size);
                }
            ''',
             "asserted_file": "unit_tests/if/asserted/without_else.xml"},
            {"input": '''
                if (false) {
                    let s = "string constant";
                    let s = null;
                    let a[1] = a[2];
                }
                else {              // There is no else keyword in the Square files.
                    let i = i * (-j);
                    let j = j / (-2);   // note: unary negate constant 2
                    let i = i | j;
                }
            ''',
             "asserted_file": "unit_tests/if/asserted/with_else.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_if(self.root)
                self.check_xml(compiler, "unit_tests/if/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_var_dec(self):
        fixture = [
            {"input": "var SquareGame game;", "asserted_file": "unit_tests/var_dec/asserted/simple.xml"},
            {"input": "var int i, j;", "asserted_file": "unit_tests/var_dec/asserted/double.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_var_dec(self.root)
                self.check_xml(compiler, "unit_tests/var_dec/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_output_var_dec(self):
        fixture = [
            # {"input": "var SquareGame game;", "asserted_file": "unit_tests/var_dec/asserted/simple.xml"},
            {"input": "var int i, j;", "asserted_file": "unit_tests/output_var_dec/asserted/double_int.vm"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                out_path = "/Users/noguchikoutarou/nand2tetris/projects/10/compiler/unit_tests/output_var_dec/actual/out_{}.vm".format(i)
                compiler = self.set_up_compiler(test["input"], out_path)
                var_dec = compiler.compile_var_dec(self.root)
                compiler.output_var_dec(var_dec)
                compiler.vm_writer.f.close()
                self.check_vm(out_path, test["asserted_file"])

    def test_compile_subroutine_body(self):
        fixture = [
            {"input": '''{
                do Screen.setColor(true);
                do Screen.drawRectangle(x, y, x + size, y + size);
                return;
            }
            ''',
             "asserted_file": "unit_tests/subroutine_body/asserted/one.xml"},
            {"input": '''{
                var char key;  // the key currently pressed by the user
                var boolean exit;
                let exit = false;

                while (~exit) {
                    // waits for a key to be pressed
                    while (key = 0) {
                        let key = Keyboard.keyPressed();
                        do moveSquare();
                    }
                    if (key = 81)  { let exit = true; }     // q key
                    if (key = 90)  { do square.decSize(); } // z key
                    if (key = 88)  { do square.incSize(); } // x key
                    if (key = 131) { let direction = 1; }   // up arrow
                    if (key = 133) { let direction = 2; }   // down arrow
                    if (key = 130) { let direction = 3; }   // left arrow
                    if (key = 132) { let direction = 4; }   // right arrow

                    // waits for the key to be released
                    while (~(key = 0)) {
                        let key = Keyboard.keyPressed();
                        do moveSquare();
                    }
                } // while
                return;
            }
            ''',
             "asserted_file": "unit_tests/subroutine_body/asserted/with_var.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_subroutine_body(self.root)
                self.check_xml(compiler, "unit_tests/subroutine_body/actual/out_{}.xml".format(i),
                               test["asserted_file"])

    def test_compile_parameter_list(self):
        fixture = [
            {"input": "int Ax, int Ay, int Asize", "asserted_file": "unit_tests/parameter_list/asserted/simple.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_parameter_list(self.root)
                self.check_xml(compiler, "unit_tests/parameter_list/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_subroutine_dec(self):
        fixture = [
            {"input": '''
                method void dispose() {
                    do Memory.deAlloc(this);
                    return;
                }
            ''',
             "asserted_file": "unit_tests/subroutine_dec/asserted/simple.xml"},
            {"input": '''
                constructor Square new(int Ax, int Ay, int Asize) {
                    let x = Ax;
                    let y = Ay;
                    let size = Asize;
                    do draw();
                    return this;
                }
            ''',
             "asserted_file": "unit_tests/subroutine_dec/asserted/constructor.xml"},
        ]
        for i, test in enumerate(fixture):
            with self.subTest(input=test["input"], asserted_file=test["asserted_file"]):
                compiler = self.set_up_compiler(test["input"])
                compiler.compile_subroutine_dec(self.root)
                self.check_xml(compiler, "unit_tests/subroutine_dec/actual/out_{}.xml".format(i), test["asserted_file"])

    def test_compile_class(self):
        dirs = ["ArrayTest", "Square"]
        for dir in dirs:
            dirpath = str(pathlib.Path(__file__).parent.parent) + "/" + dir
            for i, file in enumerate(os.listdir(dirpath)):
                if file[-4:] != "jack":
                    continue
                input_path = dirpath + "/" + file
                tokenizer = JackTokenizer.construct_from_file(input_path)
                compiler = ComplilationEngine(tokenizer)
                compiler.compile_class()
                output_path = dirpath + "/out" + str(i) + ".xml"
                compiler.output_xml(output_path, abspath=True)
                out = subprocess.check_output(["/Users/noguchikoutarou/nand2tetris/tools/TextComparer.sh",
                                               output_path,
                                               input_path[:-4] + "xml"
                                               ])
                self.assertEqual(b'Comparison ended successfully\n', out)

    def test_output_class(self):
        dirs = [
            "/Users/noguchikoutarou/nand2tetris/projects/11/Seven",
            "/Users/noguchikoutarou/nand2tetris/projects/11/ConvertToBin",
            "/Users/noguchikoutarou/nand2tetris/projects/11/Square"
        ]
        for dirpath in dirs:
            for i, file in enumerate(os.listdir(dirpath)):
                if file[-4:] != "jack":
                    continue
                with self.subTest(dir=dirpath, file=file):
                    input_path = dirpath + "/" + file
                    tokenizer = JackTokenizer.construct_from_file(input_path)
                    output_path = dirpath + "/" + file[:-5] + ".vm"
                    print("out_path: ", output_path)
                    compiler = ComplilationEngine(tokenizer, output_path)
                    compiler.compile_class()
                    compiler.output_class()


if __name__ == "__main__":
    unittest.main()
