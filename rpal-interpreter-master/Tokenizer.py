from enum import Enum

# define punctuation characters
PUNCTION = ['(', ')', ';', ',']

# reserved keywords in RPAL
RESERVED_KEYWORDS = ['fn','where', 'let', 'aug', 'within' ,'in' ,'rec' ,'eq','gr','ge','ls','le','ne','or','@','not','&','true','false','nil','dummy','and','|']

# --classes--

# define token class
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

# define token types enumeration
class TokenType(Enum):
    RESERVED_KEYWORD = 'RESERVED_KEYWORD'

    ID = 'ID'
    COMMENT = 'COMMENT'
    INT = 'INT'
    COMMA = 'COMMA' # ,
    PLUS = 'PLUS'  # +
    MINUS = 'MINUS'  # -
    MUL = 'MUL'  # *
    DIV = 'DIV'  # /
    GREATER_THAN = 'GREATER_THAN'  # >
    LESSER_THAN = 'LESSER_THAN'  # <
    GREATER_THAN_OR_EQUAL = 'GREATER_THAN_OR_EQUAL' # >=
    LESSER_THAN_OR_EQUAL = 'LESSER_THAN_OR_EQUAL' # <=
    POWER = 'POWER' 
    AMPERSAND_OPERATOR = 'AMPERSAND_OPERATOR'  # &
    DOT_OPERATOR = 'DOT_OPERATOR'  # .
    AT_OPERATOR = 'AT_OPERATOR'  # @
    SEMICOLON = 'SEMICOLON'  # ;
    EQUAL = 'EQUAL'  # =
    CURL = 'CURL'  # ~
    SQUARE_OPEN_BRACKET = 'SQUARE_OPEN_BRACKET'  # [
    SQUARE_CLOSE_BRACKET = 'SQUARE_CLOSE_BRACKET'  # ]
    CURLY_OPEN_BRACKET = 'CURLY_OPEN_BRACKET' # {
    CURLY_CLOSE_BRACKET = 'CURLY_CLOSE_BRACKET' # }
    DOLLAR = 'DOLLAR'  # $
    EXCLAMATION_MARK = 'EXCLAMATION_MARK' # !
    HASH_TAG = 'HASH_TAG'
    MODULUS = 'MODULUS'
    CARROT = 'CARROT'
    BACK_TICK = 'BACK_TICK'
    DOUBLE_QUOTE = 'DOUBLE_QUOTE'
    QUESTION_MARK = 'QUESTION_MARK' # ?
    PUNCTION = 'PUNCTION'
    OR_OPERATOR = 'OR_OPERATOR'
    STRING = 'STRING'
    TERNARY_OPERATOR = 'TERNARY_OPERATOR'

    EOF = 'EOF'


# Define lexical state class
class LexicalState:
    def __init__(self):
        self.line_num = 0
        self.curr_char = None
        self.col_num = None

# Tokenizer class for tokenizing input text
class Tokenize:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.state = LexicalState()

        self.state.curr_char = self.text[self.pos]
        self.state.line_num = 1
        self.state.col_num = 1


    # Error handling method
    def ErrorHandler(self):
        raise Exception('Error : parsing input')

    # Move to the next character
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.state.curr_char = None  # Indicates end of input
        else:
            self.state.curr_char = self.text[self.pos]
            self.state.col_num += 1

    # Skip space characters
    def skip_space(self):
        while self.state.curr_char is not None and self.state.curr_char.isspace():
            if self.state.curr_char == '\n':
                self.state.line_num += 1
                self.state.col_num = 0
            self.advance()
            
    # Tokenize integera
    def integer(self):
        result = ''
        while self.state.curr_char is not None :
            if self.state.curr_char.isdigit():
                result += self.state.curr_char
                self.advance()
            elif self.state.curr_char.isalpha():
                self.error()
            else: break


        return int(result)
    
    
    # Tokenize identifiers
    def identifier(self):
        result = ''
        while self.state.curr_char is not None and (
                self.state.curr_char.isalpha() or self.state.curr_char.isdigit() or self.state.curr_char == '_'):
            result += self.state.curr_char
            self.advance()
        return result
    
#   Tokenize comments
    def comment(self):
        result = ''
        while self.state.curr_char is not None and self.state.curr_char != '\n':
            result += self.state.curr_char
            self.advance()
        return result
    
    # Check if the current character is a comment
    def isComment(self):
        if self.state.curr_char is not None and self.state.curr_char == '/':
            return True
        else:
            return False

    # Tokenize strings
    def string(self):
        result = ''
        while self.state.curr_char is not None and self.state.curr_char != "'":
            result += self.state.curr_char
            self.advance()
        self.advance()
        return result

    def getNextToken(self):
        while self.state.curr_char is not None:

            # skip whitespace characters
            if self.state.curr_char.isspace():
                self.skip_space()
                continue

            # tokenize digits
            elif self.state.curr_char.isdigit():
                return Token(TokenType.INT, self.integer())

            ## tokenize identifier
            elif self.state.curr_char.isalpha():
                return Token(TokenType.ID, self.identifier())


            # handle comments
            elif self.state.curr_char == '/':
                if self.text[self.pos + 1] == '/':
                    self.advance()
                    self.advance()
                    return Token(TokenType.COMMENT, self.comment())

                else :
                    self.advance()
                    return Token(TokenType.DIV, '/')



            # tokenize string starting with '
            elif self.state.curr_char == "'":
                self.advance()
                return Token(TokenType.STRING, self.string())


            # tokenize punctuation
            elif self.state.curr_char in PUNCTION:
                token = Token(TokenType.PUNCTION, self.state.curr_char)
                self.advance()
                return token

            # tokenize all single character tokens
            elif self.state.curr_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            elif self.state.curr_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            elif self.state.curr_char == '*':
                self.advance()
                return Token(TokenType.MUL, '*')

            elif self.state.curr_char == '<':
                self.advance()
                return Token(TokenType.GREATER_THAN, '<')

            elif self.state.curr_char == '>':
                self.advance()
                return Token(TokenType.LESSER_THAN, '>')

            elif self.state.curr_char == '&':
                self.advance()
                return Token(TokenType.AMPERSAND_OPERATOR, '&')

            elif self.state.curr_char == '.':
                self.advance()
                return Token(TokenType.DOT_OPERATOR, '.')

            elif self.state.curr_char == '@':
                self.advance()
                return Token(TokenType.AT_OPERATOR, '@')

            elif self.state.curr_char == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';')

            elif self.state.curr_char == '=':
                self.advance()
                return Token(TokenType.EQUAL, '=')

            elif self.state.curr_char == '~':
                self.advance()
                return Token(TokenType.CURL, '~')

            elif self.state.curr_char == '[':
                self.advance()
                return Token(TokenType.SQUARE_OPEN_BRACKET, '[')

            elif self.state.curr_char == ']':
                self.advance()
                return Token(TokenType.SQUARE_CLOSE_BRACKET, ']')

            elif self.state.curr_char == '$':
                self.advance()
                return Token(TokenType.DOLLAR, '$')

            elif self.state.curr_char == '!':
                self.advance()
                return Token(TokenType.EXCLAMATION_MARK, '!')

            elif self.state.curr_char == '#':
                self.advance()
                return Token(TokenType.HASH_TAG, '#')

            elif self.state.curr_char == '%':
                self.advance()
                return Token(TokenType.MODULUS, '%')

            elif self.state.curr_char == '^':
                self.advance()
                return Token(TokenType.CARROT, '^')

            elif self.state.curr_char == '{':
                self.advance()
                return Token(TokenType.CURLY_OPEN_BRACKET, '{')

            elif self.state.curr_char == '}':
                self.advance()
                return Token(TokenType.CURLY_CLOSE_BRACKET, '}')

            elif self.state.curr_char == '`':
                self.advance()
                return Token(TokenType.BACK_TICK, '`')

            elif self.state.curr_char == '\"':
                self.advance()
                return Token(TokenType.DOUBLE_QUOTE, '\"')

            elif self.state.curr_char == '?':
                self.advance()
                return Token(TokenType.QUESTION_MARK, '?')

            elif self.state.curr_char == '|':
                self.advance()
                return Token(TokenType.OR_OPERATOR, '|')

            self.error()

        # return EOF at the end of file
        return Token(TokenType.EOF, None)


# define screener class
class Screener:
    # initialize screeener object with tokens
    def __init__(self,tokens):
        self.text = None
        self.tokens=tokens

     # merge consecutive tokens with specific patterns
    def mergeTok(self ):
        tokens=self.tokens

        for i in range(len(tokens)):
            # Merge '-' and '<' into '->'
            if i < len(tokens) and tokens[i].type == TokenType.MINUS and tokens[i + 1].type == TokenType.LESSER_THAN:
                tokens[i].value = '->'
                tokens[i].type = TokenType.TERNARY_OPERATOR
                tokens.pop(i + 1)

            # Merge '>' and '=' into '>='
            if i < len(tokens) and tokens[i].type == TokenType.GREATER_THAN and tokens[i + 1].type == TokenType.EQUAL:
                tokens[i].value = '>='
                tokens[i].type = TokenType.GREATER_THAN_OR_EQUAL
                tokens.pop(i + 1)

            # Merge '<' and '=' into '<='
            if i < len(tokens) and tokens[i].type == TokenType.LESSER_THAN and tokens[i + 1].type == TokenType.EQUAL:
                tokens[i].value = '<='
                tokens[i].type = TokenType.LESSER_THAN_OR_EQUAL
                tokens.pop(i + 1)


            ## merge **
            if i < len(tokens) and tokens[i].type == TokenType.MUL and tokens[i + 1].type == TokenType.MUL:
                tokens[i].value = '**'
                tokens[i].type = TokenType.POWER
                tokens.pop(i + 1)



        self.tokens=tokens

    ## remove comments
    def removeComments(self):
        tokens = self.tokens
        tokensToPop=[]
        for (i , token) in enumerate(tokens):
            if tokens[i].type == TokenType.COMMENT:
                tokensToPop.append(i)
                
        for i in tokensToPop:
            tokens.pop(i)

        self.tokens = tokens

    

    def screenReserved_Keywords(self):
        tokens=self.tokens
        for i in range(len(tokens)):
            if tokens[i].value in RESERVED_KEYWORDS:
                tokens[i].type=TokenType.RESERVED_KEYWORD
        self.tokens=tokens

    def screen(self):
        self.mergeTok()
        self.removeComments()
        self.screenReserved_Keywords()
        return self.tokens

