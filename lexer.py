import string
UPPER_CASE = set(string.ascii_uppercase)

class Location:
    def __init__(self, line, col):
        self.col = col
        self.line = line

class TokenKind:
    ID = 0   # identifier
    LPAR = 1 # (
    RPAR = 2 # )
    NOT = 3  # !
    AND = 4  # /\
    OR = 5   # \/
    IMPLIES = 6  # =>
    IFF = 7  # <=>
    COMMA = 8 # ,

class Token:
    def __init__(self, loc, kind, text):
        self.loc = loc
        self.kind = kind
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return '\'' + str(self) + '\''

class Lexer:
    def __init__(self, text, line):
        self.text = text
        self.line = line
        self.col = 1

    def tokenize(self):
        tokens = []
        invalid_tokens = []
        while self.col <= len(self.text):
            if self.text[self.col-1].isalpha() and self.text[self.col-1].isupper():
                if(len(tokens) > 0 and tokens[-1].kind == TokenKind.ID
                and self.text[self.col-2] != ' '):
                    tokens[-1].text += self.text[self.col-1]
                else:
                    tokens.append(Token(Location(self.line, self.col), TokenKind.ID, 'ID'))
            elif self.text[self.col-1] == '(':
                tokens.append(Token(Location(self.line, self.col), TokenKind.LPAR, 'LPAR'))
            elif self.text[self.col-1] == ')':
                tokens.append(Token(Location(self.line, self.col), TokenKind.RPAR, 'RPAR'))
            elif self.text[self.col-1] == '!':
                tokens.append(Token(Location(self.line, self.col), TokenKind.NOT, 'NOT'))
            elif self.text[self.col-1] == '/' and self.col <= len(self.text)-1 and self.text[self.col] == '\\':
                tokens.append(Token(Location(self.line, self.col), TokenKind.AND, 'AND'))
                self.col += 1
            elif self.text[self.col-1] == '\\' and self.col <= len(self.text)-1 and self.text[self.col] == '/':
                tokens.append(Token(Location(self.line, self.col), TokenKind.OR, 'OR'))
                self.col += 1
            elif self.text[self.col-1] == '=' and self.col <= len(self.text)-1 and self.text[self.col] == '>':
                tokens.append(Token(Location(self.line, self.col), TokenKind.IMPLIES, 'IMPLIES'))
                self.col += 1
            elif self.text[self.col-1] == '<' and self.col+1 <= len(self.text)-1 and self.text[self.col] == '=' and self.text[self.col+1] == '>':
                tokens.append(Token(Location(self.line, self.col), TokenKind.IFF, 'IFF'))
                self.col += 2
            elif self.text[self.col-1] == ',':
                tokens.append(Token(Location(self.line, self.col), TokenKind.COMMA, 'comma'))
            elif self.text[self.col-1] == '\\' or self.text[self.col-1] == '=' or self.text[self.col-1] == '<':
                invalid_tokens.append(Token(Location(self.line, self.col), None, self.text[self.col-1]))
            elif self.text[self.col-1] != ' ': # any other invalid character
                invalid_tokens.append(Token(Location(self.line, self.col), None, self.text[self.col-1]))
            self.col += 1

        if len(invalid_tokens) == 0:
            return tokens
        else:
            return invalid_tokens
