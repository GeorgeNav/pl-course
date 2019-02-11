import unittest
import os
from lexer import Lexer, TokenKind
from parser import Parser

#access input file
dir_path = os.path.dirname(__file__)
file_name = 'input.txt'
input_file_path = os.path.join(dir_path, file_name)
f_lines = ['']
with open(input_file_path) as f:
    c = f.read(1)
    i = 0
    while c:
        if c != '\n':
            f_lines[i] += c
        elif c == '\n':
            f_lines.append('')
            i += 1
        c = f.read(1)
    print('End of file')
    # f_str = f.read()

class Test(unittest.TestCase):
    def test(self):
        tokenlists = []
        for i, line in enumerate(f_lines):
            if line.strip():
                tokenlists.append(Lexer(line, i+1).tokenize())

        output_file_path = os.path.join(dir_path, 'output.txt')
        with open(output_file_path, 'w') as f:
            for i, tokens in enumerate(tokenlists):
                f.write('Input #' + str(i+1) + ':')
                f.write('\n---------')
                f.write('\nProposition\t\t\t: ')
                f.write(f_lines[i].replace('\'', ''))
                if tokens[0].kind != None:
                    f.write('\nLexer\t\t\t\t: ')
                    f.write(str(tokens).replace('\'', '').replace('[', '[ ').replace(']', ' ]'))
                    f.write('\nParser\t\t\t\t: ')
                    tokens = Parser(tokens).parse()
                    f.write(str(tokens).replace('\'', ''))
                else:
                    f.write('\nSyntaxError(s)\t\t: ')
                    for i, invalidToken in enumerate(tokens):
                        f.write(str(invalidToken) + ' (line ' + str(invalidToken.loc.line) + ', col '+ str(invalidToken.loc.col) + ')')
                        if i+1 != len(tokens):
                            f.write(' | ')
                f.write('\n\n')

if __name__ == '__main__':
    unittest.main()
