from lexer import Location, Lexer, TokenKind
import sys

class VariableType:
    PROPOSITIONS = 0
    PROPOSITION = 1
    ATOMIC = 2
    MOREPROPOSITIONS = 3
    COMPOUND = 4
    CONNECTIVE = 5

class Parser:
    def __init__(self, tokenlist):
        self.loc = Location(0, 0)
        self.tokenlist = tokenlist
        self.parse_tree = []
        self.errors = []

    def parse(self):
        self.find_error()
        self.propositions()
        if len(self.errors) == 0:
            return str(self.parse_tree).replace('[', '[ ').replace(']', ' ]')
        else:
            raise SyntaxError(str(self.errors).replace('[', '').replace(']', '').replace(', ', ' | '))

    def find_error(self):
        wrappers = 0
        for i, token in enumerate(self.tokenlist):
            if token.kind == TokenKind.ID and i-1 >= 0 and self.tokenlist[i-1].kind == TokenKind.ID:
                self.error('invalid ID', token)
            elif token.kind == TokenKind.LPAR:
                wrappers -= 1
                if wrappers > 0:
                    self.error('invalid parentheses', token)
                elif i-1 >= 0 and self.tokenlist[i-1].kind != TokenKind.COMMA and not self.is_connective(self.tokenlist[i-1].kind): # here
                    self.error('expecting connective ', self.tokenlist[i-1])
            elif token.kind == TokenKind.RPAR:
                wrappers += 1
                if wrappers > 0:
                    self.error('invalid parentheses', token)
                elif len(self.tokenlist) > i+1 and self.tokenlist[i+1].kind != TokenKind.COMMA and not self.is_connective(self.tokenlist[i+1].kind): # here
                    self.error('expecting connective ', self.tokenlist[i+1])
            elif token.kind == TokenKind.NOT:
                if(i+1 == len(self.tokenlist) or
                i+1 < len(self.tokenlist)
                and self.tokenlist[i+1].kind != TokenKind.LPAR and self.tokenlist[i+1].kind != TokenKind.ID):
                    self.error('invalid NOT symbol', token)
        if wrappers != 0 and 'invalid parentheses' not in self.errors:
            self.error('invalid parenthesis', None)

    def propositions(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        self.proposition()
        self.more_propositions()

    def more_propositions(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        if self.is_empty():
            self.parse_tree.append('epsilon')
        elif self.top_kind() == TokenKind.COMMA:
            self.pop(TokenKind.COMMA) # comma
            self.propositions()

    def proposition(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        if not self.is_compound():
            self.atomic()
        else:
            self.compound()

    def atomic(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        self.pop(TokenKind.ID) # ID

    def compound(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        if self.top_kind() == TokenKind.ID:
            self.atomic() # ID or RPAR
            self.connective()
            self.proposition()
        elif self.is_connective(self.top_kind()):
            self.connective()
            self.proposition()
        elif self.top_kind() == TokenKind.LPAR:
            self.pop(TokenKind.LPAR) # LPAR
            self.proposition()
            self.pop(TokenKind.RPAR) # RPAR
        elif self.top_kind() == TokenKind.NOT:
            self.pop(TokenKind.NOT) # NOT
            self.proposition()

    def connective(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        self.pop(self.top_kind()) # Connective

    # add more methods if needed
    def is_connective(self, kind):
        if(kind == TokenKind.AND
        or kind == TokenKind.OR
        or kind == TokenKind.IMPLIES
        or kind == TokenKind.IFF):
            return True
        else:
            return False

    def is_compound(self):
        if(len(self.tokenlist) > 1 and self.is_connective(self.tokenlist[1].kind)
        or self.top_kind() == TokenKind.LPAR or self.top_kind() == TokenKind.NOT):
            return True
        else:
            return False

    def pop(self, kind):
        if not self.is_empty() and kind is self.top_kind():
            self.loc = self.tokenlist[0].loc
            self.parse_tree.append(str(self.tokenlist.pop(0)))
        else:
            self.errors.append('TokenType ' + self.str_kind(kind) + ' not found after line' + str(self.loc.line) + ',col' + str(self.loc.col))
    

    def is_empty(self):
        if len(self.tokenlist) == 0:
            return True
        else:
            return False

    def top_kind(self):
        if not self.is_empty():
            return self.tokenlist[0].kind
        else:
            return None
 
    def error(self, s, token):
        if token != None and s == None: # general location
            self.errors.append('(line' + str(token.loc.line) + ',col' + str(token.loc.col) + ')')
        elif s != None and token == None: # general type of error
            self.errors.append(s)
        elif token != None and s != None: # specific type and location of error
            self.errors.append(s + ' (line' + str(token.loc.line) + ',col' + str(token.loc.col) + ')')

    def str_kind(self, kind):
        if kind is TokenKind.ID:
            return 'ID'
        elif kind is TokenKind.RPAR:
            return 'RPAR'
        elif kind is TokenKind.RPAR:
            return 'LPAR'
        elif kind is TokenKind.NOT:
            return 'NOT'
        elif kind is TokenKind.AND or kind is TokenKind.OR or kind is TokenKind.IMPLIES or kind is TokenKind.IFF:
            return 'CONNECTIVE'
        elif kind is TokenKind.COMMA:
            return 'COMMA'
        elif kind is None:
            return 'INVALID_KIND'
