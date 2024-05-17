from enum import Enum

# define punctuation characters
PUNCTION = ['(', ')', ';', ',']

# reserved keywords in RPAL
RESERVED_KEYWORDS = ['fn','where', 'let', 'aug', 'within' ,'in' ,'rec' ,'eq','gr','ge','ls','le','ne','or','@','not','&','true','false','nil','dummy','and','|']

# --classes--

# define token class to represent tokens in the input
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

# define token types enumeration using Enum for better type management
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


# Define lexical state class to keep track of the lexical analysis state
class LexicalState:
    def __init__(self):
        self.line_num = 0  # Current line number
        self.curr_char = None  # Current character
        self.col_num = None   # Current column number

# Define the Tokenize class to handle the tokenization of input text
class Tokenize:
    def __init__(self, text):
        self.text = text  # Input text to be tokenized
        self.pos = 0   # Current position in the input text
        self.state = LexicalState()   # Initialize lexical state

        # Set initial state values
        self.state.curr_char = self.text[self.pos]
        self.state.line_num = 1
        self.state.col_num = 1


    # Error handling method
    def ErrorHandler(self):
        raise Exception('Error : parsing input')

    # Move to the next character in the input text
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.state.curr_char = None  # Indicates end of input
        else:
            self.state.curr_char = self.text[self.pos]
            self.state.col_num += 1

    # Skip space characters in the input text
    def skip_space(self):
        while self.state.curr_char is not None and self.state.curr_char.isspace():
            if self.state.curr_char == '\n':
                self.state.line_num += 1
                self.state.col_num = 0
            self.advance()
            
    # Tokenize integer values
    def integer(self):
        result = ''
        while self.state.curr_char is not None :
            if self.state.curr_char.isdigit():
                result += self.state.curr_char
                self.advance()  # Move to the next character
            elif self.state.curr_char.isalpha():
                self.error()  # Raise an error if an alphabetic character is found in an integer
            else: break


        return int(result)   # Return the integer value
    
    
    # Tokenize identifiers (variable names, function names, etc.)
    def identifier(self):
        result = ''
        while self.state.curr_char is not None and (
                self.state.curr_char.isalpha() or self.state.curr_char.isdigit() or self.state.curr_char == '_'):
            result += self.state.curr_char
            self.advance()   # Move to the next character
        return result  # Return the identifier
    
#   Tokenize comments
    def comment(self):
        result = ''
        while self.state.curr_char is not None and self.state.curr_char != '\n':
            result += self.state.curr_char
            self.advance()  # Move to the next character
        return result  # Return the comment text
    
    # Check if the current character is a comment
    def isComment(self):
        if self.state.curr_char is not None and self.state.curr_char == '/':
            return True  # It is a comment
        else:
            return False  # It is not a comment

    # Tokenize strings
    def string(self):
        result = ''
        while self.state.curr_char is not None and self.state.curr_char != "'":
            result += self.state.curr_char
            self.advance()    # Move to the next character 
        self.advance()    # Move past the closing quote
        return result  # Return the string content
        
    # Get the next token from the input
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
                    self.advance()  # Skip the first '/'
                    self.advance()  # Skip the second '/'
                    return Token(TokenType.COMMENT, self.comment())

                else :
                    self.advance()
                    return Token(TokenType.DIV, '/')



            # tokenize string starting with a single quote - '
            elif self.state.curr_char == "'":
                self.advance()  # Skip the opening quote
                return Token(TokenType.STRING, self.string())


            # tokenize punctuation characters
            elif self.state.curr_char in PUNCTION:
                token = Token(TokenType.PUNCTION, self.state.curr_char)
                self.advance()  # Move to the next character
                return token

            # Tokenize single character tokens
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

            self.error()   # Raise an error if no valid token is found

        # Return EOF token at the end of the input
        return Token(TokenType.EOF, None)


# define screener class
class Screener:
    # Initialize the Screener object with a list of tokens
    def __init__(self,tokens):
        self.text = None
        self.tokens=tokens

     # Merge consecutive tokens based on specific patterns
    def mergeTok(self ):
        tokens=self.tokens

        for i in range(len(tokens)):
            # Merge '-' and '<' into '->'
            if i < len(tokens) and tokens[i].type == TokenType.MINUS and tokens[i + 1].type == TokenType.LESSER_THAN:
                tokens[i].value = '->'
                tokens[i].type = TokenType.TERNARY_OPERATOR
                tokens.pop(i + 1)  # Remove the next token after merging

            # Merge '>' and '=' into '>='
            if i < len(tokens) and tokens[i].type == TokenType.GREATER_THAN and tokens[i + 1].type == TokenType.EQUAL:
                tokens[i].value = '>='
                tokens[i].type = TokenType.GREATER_THAN_OR_EQUAL
                tokens.pop(i + 1)  # Remove the next token after merging

            # Merge '<' and '=' into '<='
            if i < len(tokens) and tokens[i].type == TokenType.LESSER_THAN and tokens[i + 1].type == TokenType.EQUAL:
                tokens[i].value = '<='
                tokens[i].type = TokenType.LESSER_THAN_OR_EQUAL
                tokens.pop(i + 1)  # Remove the next token after merging


            ## merge **
            if i < len(tokens) and tokens[i].type == TokenType.MUL and tokens[i + 1].type == TokenType.MUL:
                tokens[i].value = '**'
                tokens[i].type = TokenType.POWER
                tokens.pop(i + 1)   # Remove the next token after merging



        self.tokens=tokens  # Update the tokens list after merging

    # Remove comments from the tokens list
    def removeComments(self):
        tokens = self.tokens
        tokensToPop=[]
        # Identify tokens that are comments    
        for (i , token) in enumerate(tokens):
            if tokens[i].type == TokenType.COMMENT:
                tokensToPop.append(i)  # Add the index of the comment token
                
        # Remove comment tokens            
        for i in tokensToPop:
            tokens.pop(i)

        self.tokens = tokens  # Update the tokens list after removing comments

    
    # Identify and classify reserved keywords in the tokens list
    def screenReserved_Keywords(self):
        tokens=self.tokens

        # Check each token and update its type if it is a reserved keyword
        for i in range(len(tokens)):
            if tokens[i].value in RESERVED_KEYWORDS:
                tokens[i].type=TokenType.RESERVED_KEYWORD
        self.tokens=tokens  # Update the tokens list after screening for reserved keywords

    # Main method to screen the tokens
    def screen(self):
        self.mergeTok()  # Merge specific token patterns
        self.removeComments()  # Remove comments
        self.screenReserved_Keywords()  # Screen for reserved keywords
        return self.tokens  # Return the updated list of tokens

