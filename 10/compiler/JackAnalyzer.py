from JackTokenizer import JackTokenizer
import sys

path = sys.argv[1]
tokenizer = JackTokenizer.construct_from_file(path)
if sys.argv[2] == "-t":
    tokenizer.create_token_xml(path[:-5] + "T_out" + "." + "xml")
