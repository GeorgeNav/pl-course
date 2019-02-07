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
    def __init__(self, loc, kind):
        self.loc = loc
        self.kind = kind

    def __str__(self):
        return str(self.kind)
    

class Lexer:
    def __init__(self, text):
        self.text = text
        self.line = 1
        self.col = 1
        self.tokens = []

    def tokenize(self):
        while self.col <= len(self.text):
            if self.text[self.col-1].isalpha() and self.text[self.col-1].isupper():
                self.tokens.append(Token(Location(self.col, self.line), TokenKind.ID))
            elif self.text[self.col-1] == '(':
                self.tokens.append(Token(Location(self.col, self.line), TokenKind.LPAR))
            elif self.text[self.col-1] == ')':
                self.tokens.append(Token(Location(self.col, self.line), TokenKind.RPAR))
            elif self.text[self.col-1] == '!':
                self.tokens.append(Token(Location(self.col, self.line), TokenKind.NOT))
            elif self.text[self.col-1] == '/' and self.col <= len(self.text)-1 and self.text[self.col] == '\\':
                self.tokens.append(Token(Location(self.col, self.line), TokenKind.AND))
                self.col += 1
            elif self.text[self.col-1] == '\\' and self.col <= len(self.text)-1 and self.text[self.col] == '/':
                self.tokens.append(Token(Location(self.col, self.line), TokenKind.OR))
                self.col += 1
            elif self.text[self.col-1] == '=' and self.col <= len(self.text)-1 and self.text[self.col] == '>':
                self.tokens.append(Token(Location(self.col, self.line), TokenKind.IMPLIES))
                self.col += 1
            elif self.text[self.col-1] == '<' and self.col+1 <= len(self.text)-1 and self.text[self.col] == '=' and self.text[self.col+1] == '>':
                self.tokens.append(Token(Location(self.col, self.line), TokenKind.IFF))
                self.col += 2
            elif self.text[self.col-1] == '\n':
                self.line += 1
            else: # any other invalid character
                raise NotImplementedError
            self.col += 1
        if len(self.tokens) >= 1:
            return self.tokens
        else:
            raise NotImplementedError
