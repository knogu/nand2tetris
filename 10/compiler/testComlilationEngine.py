import unittest
from CompilationEngine import ComplilationEngine
from JackTokenizer import JackTokenizer
import xml.etree.ElementTree as ET


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


if __name__ == "__main__":
    unittest.main()
