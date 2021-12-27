import unittest
from CompilationEngine import ComplilationEngine
from JackTokenizer import JackTokenizer
import xml.etree.ElementTree as ET
import subprocess


class TestComplilationEngine(unittest.TestCase):
    def set_up_compiler(self, input):
        self.root = ET.Element("root")
        tokenizer = JackTokenizer(input)
        compiler = ComplilationEngine(tokenizer)
        return compiler

    def check(self, compiler, output_file, asserted_file):
        compiler.output_xml(output_file, self.root)
        subprocess.run(["/Users/noguchikoutarou/nand2tetris/tools/TextComparer.sh",
                        output_file,
                        asserted_file
                        ])

    def test_compile_class_var_dec(self):
        s = '''
        static int a, b;
        '''
        compiler = self.set_up_compiler(s)
        compiler.compile_class_var_dec(self.root)
        self.check(compiler, "test_compile_class_var_dec.xml", "test_output/test1.xml")

    def test_compile_term(self):
        fixture = [
            # integerConstant
            {"input": "333", "asserted_file": "test_output/term/assertion/integer_constant.xml"},
        ]
        for i, test in enumerate(fixture):
            compiler = self.set_up_compiler(test["input"])
            compiler.compile_term(self.root)
            self.check(compiler, "test_output/term/actual/integer_constant_{}.xml".format(i), test["asserted_file"])


if __name__ == "__main__":
    unittest.main()
