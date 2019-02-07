import unittest
import os
from lexer import Lexer, TokenKind
from parser import Parser

#access input file
dir_path = os.path.dirname(__file__)
file_name = 'input.txt'
file_path = os.path.join(dir_path, file_name)
f_str = ''
with open(file_path) as f:
    line = ''
    c = f.read(1)
    while c:
        f_str += c
        c = f.read(1)
    print('End of file')
    # f_str = f.read()

class Test(unittest.TestCase):
    def test(self):
        tokenlist = Lexer(f_str).tokenize()
        for token in tokenlist:
            print(token.kind)
        # parse_tree = Parser().parse(tokenlist)
        # some assertion goes here

if __name__ == '__main__':
    unittest.main()
