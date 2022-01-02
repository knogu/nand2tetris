from JackTokenizer import JackTokenizer
from CompilationEngine import ComplilationEngine
import sys

path = sys.argv[1]
tokenizer = JackTokenizer.construct_from_file(path)
if len(sys.argv) >= 3 and sys.argv[2] == "-t":
    tokenizer.create_token_xml(path[:-5] + "T_out" + "." + "xml")
else:
    compiler = ComplilationEngine(tokenizer)
    compiler.compile_class()
    output_path = path[:-4] + "xml"
    compiler.output_xml(output_path, abspath=True)
