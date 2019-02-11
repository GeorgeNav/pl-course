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
            print(self.parse_tree)
            return str(self.parse_tree).replace('[', '[ ').replace(']', ' ]')
        else:
            print(self.errors)
            return 'Error(s) -> ' + str(self.errors).replace('[', '[ ').replace(']', ' ]')

    def find_error(self):
        wrappers = 0
        for i, token in enumerate(self.tokenlist):
            if token.kind == TokenKind.ID and i-1 >= 0 and self.tokenlist[i-1].kind == TokenKind.ID:
                self.error('invalid ID', token)
            elif token.kind == TokenKind.LPAR:
                wrappers -= 1
            elif token.kind == TokenKind.RPAR:
                wrappers += 1
            elif token.kind == TokenKind.NOT:
                if(i+1 == len(self.tokenlist) or
                i+1 < len(self.tokenlist)
                and self.tokenlist[i+1].kind != TokenKind.LPAR and self.tokenlist[i+1].kind != TokenKind.ID):
                    self.error('invalid NOT symbol', token)
        if wrappers != 0:
            self.error('invalid set of parentheses', None)

    def propositions(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        self.proposition()
        self.more_propositions()

    def more_propositions(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        if self.isEmpty():
            self.parse_tree.append('epsilon')
        elif self.top() == TokenKind.COMMA:
            self.pop() # comma
            self.propositions()

    def proposition(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        if not self.isCompound():
            self.atomic()
        else:
            self.compound()

    def atomic(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        self.pop() # ID

    def compound(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        if self.top() == TokenKind.ID:
            self.atomic() # ID or RPAR
            self.connective()
            self.proposition()
        elif self.isConnective(self.top()):
            self.connective()
            self.proposition()
        elif self.top() == TokenKind.LPAR:
            self.pop() # LPAR
            self.proposition()
            if len(self.tokenlist) > 1 and self.isConnective(self.tokenlist[1].kind):
                self.pop()
                self.connective()
                self.proposition()
            else:
                self.pop() # RPAR
        elif self.top() == TokenKind.NOT:
            self.pop() # NOT
            self.proposition()

    def connective(self):
        self.parse_tree.append(sys._getframe().f_code.co_name) # prints function name
        self.pop() # Connective

    # add more methods if needed
    def isConnective(self, kind):
        if(kind == TokenKind.AND
        or kind == TokenKind.OR
        or kind == TokenKind.IMPLIES
        or kind == TokenKind.IFF):
            return True
        else:
            return False

    def isCompound(self):
        if(len(self.tokenlist) > 1 and self.isConnective(self.tokenlist[1].kind)
        or self.top() == TokenKind.LPAR or self.top() == TokenKind.NOT):
            return True
        else:
            return False

    def pop(self):
        if not self.isEmpty():
            self.parse_tree.append(str(self.tokenlist.pop(0)))
        else:
            self.errors.append('Missing value')


    def isEmpty(self):
        if len(self.tokenlist) == 0:
            return True
        else:
            return False

    def top(self):
        if not self.isEmpty():
            return self.tokenlist[0].kind
        else:
            return None
 
    def error(self, s, token):
        if token != None and s == None: # general location
            self.errors.append('(line ' + str(token.loc.line) + ', col ' + str(token.loc.col) + ')')
        elif s != None and token == None: # general type of error
            self.errors.append(s)
        elif token != None and s != None: # specific type and location of error
            self.errors.append(s + ' (line ' + str(token.loc.line) + ', col ' + str(token.loc.col) + ')')
