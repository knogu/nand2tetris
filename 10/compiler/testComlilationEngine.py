import unittest
from CompilationEngine import ComplilationEngine
from JackTokenizer import JackTokenizer
import xml.etree.ElementTree as ET
import subprocess


class TestComplilationEngine(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.root = ET.Element("root")

    def test_compile_class_var_dec(self):
        s = '''
        static int a, b;
        '''
        tokenizer = JackTokenizer(s)
        compiler = ComplilationEngine(tokenizer)
        compiler.compile_class_var_dec(self.root)
        compiler.output_xml("test_compile_class_var_dec.xml", self.root)
        subprocess.run(["/Users/noguchikoutarou/nand2tetris/tools/TextComparer.sh",
                        "test_compile_class_var_dec.xml",
                        "test_output/test1.xml"
                        ])


if __name__ == "__main__":
    unittest.main()
