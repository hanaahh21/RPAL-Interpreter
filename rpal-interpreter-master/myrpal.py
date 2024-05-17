# Importing Tokenizer module
import Tokenizer
# Importing Screener class from Tokenizer module
from Tokenizer import Screener
 # Importing controlStructure module
import controlStructure
# Importing CSE_Machine class from cseMachine module
from cseMachine import CSE_Machine
# Importing os module for operating system dependent functionality
import os
# Importing ASTNode class from ASTNode module
from ASTNode import ASTNode

# ANSI escape codes for text color
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'

RESET = '\033[0m' # Reset to standard terminal text color

# Reassigning color codes, potentially redundant
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems


# Definition of ASTParser class
class ASTParser:

    # Constructor method
    def __int__(self, tokens1):
        self.tokens = tokens1  # List of tokens
        self.curr_token = None  # Current token being processed
        self.index = 0  # Index to keep track of current token position

    # Method to read tokens
    def read(self):

        # Processing tokens based on their type
        if self.curr_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                       Tokenizer.TokenType.STRING] :

            # Creating ASTNode for terminal tokens
            terminal_nd = ASTNode( str(self.curr_token.type))
            terminal_nd.val= self.curr_token.val
            stack.append(terminal_nd)
            

        # Processing specific token values
        if self.curr_token.val in  ['true', 'false', 'nil', 'dummy']:
            
            terminal_nd = ASTNode(str(self.curr_token.type))
            terminal_nd.val = self.curr_token.val
            stack.append(terminal_nd)

        
        self.index += 1  # Moving to the next token


        if (self.index < len(self.tokens)):
            self.curr_token = self.tokens[self.index]  # Updating current token
        


    # Method to build AST tree
    def build_tree(self, token, ariness):
        global stack

        

        node = ASTNode(token)  # Creating ASTNode instance

        node.val = None
        node.source_LineNum = -1
        node.child = None
        node.sib = None
        node.prev = None

        # Building the tree based on the arity
        while ariness > 0:
            
            child = stack[-1]  # Taking the top element from the stack
            stack.pop()    # Removing the top element
            # Assuming pop() is a function that returns an ASTNode
            if node.child is not None:
                child.sib = node.child
                node.child.prev = child
                
            node.child = child

            node.source_LineNum = child.source_LineNum
            ariness -= 1
        

        stack.append(node)  # Appending the node to the stack
       
        for node in stack:
            pass
            

     # Method to process expression
    def procE(self):


        # Matching current token value
        match self.curr_token.val:

            case 'let':
                self.read()
                self.procD()

                if self.curr_token.val != 'in':
        
                    return

                self.read()
                self.procE()
                self.build_tree("let", 2)    # Building tree for let expression

            case 'fn':

                n = 0

                self.read()

                while self.curr_token.type == Tokenizer.TokenType.ID or self.curr_token.val == '(':
                    self.procVb()
                    n += 1

                if n == 0:
                    return

                if self.curr_token.val != '.':
                    return

                self.read()
                self.procE()
                self.build_tree("lambda", n+1)   # Building tree for lambda expression

            case _:  # Default case
                self.procEw()
    

    # Method to process extended expression
    def procEw(self):
        self.procT()
        if self.curr_token.val == 'where':
            self.read()
            self.procDr()
            self.build_tree("where", 2)  # Building tree for where expression

    # Method to process term
    def procT(self):
        self.procTa()

        n = 0
        while self.curr_token.val == ',':
            self.read()
            self.procTa()
            n += 1
        if n > 0:
            self.build_tree("tau", n + 1)
        else:
            pass

    # Method to process term augmentation
    def procTa(self):
        self.procTc()
        while self.curr_token.val == 'aug':
            self.read()
            self.procTc()

            self.build_tree("aug", 2)

    # Method to process type conversion
    def procTc(self):

        self.procB()
        if self.curr_token.type == Tokenizer.TokenType.TERNARY_OPERATOR:
            self.read()
            self.procTc()

            if self.curr_token.val != '|':
                print("Error: | is expected")
                return
            self.read()
            self.procTc()
            self.build_tree("->", 3)

    # Method to process boolean expression
    def procB(self):

        self.procBt()  # Process term
        while self.curr_token.val == 'or':    # While there are 'or' operators
            self.read()
            self.procBt()    # Process term
            self.build_tree("or", 2)    # Build tree for 'or' operation

    # Method to process boolean term
    def procBt(self):

        self.procBs() # Process simple boolean
        
        while self.curr_token.val == '&':  # While there are '&' operators
            self.read()
            self.procBs()  # Process simple boolean
           
            self.build_tree("&", 2)    # Build tree for '&' operation

    # Method to process simple boolean
    def procBs(self):
        

        if self.curr_token.val == 'not':  # If there's a 'not' operator
            self.read()
            self.procBp()  # Process boolean primary
            
            self.build_tree("not", 1)  # Build tree for 'not' operation
        else:
            self.procBp()  # Process boolean primary

            
    
    # Method to process boolean primary
    def procBp(self):
       

        self.procA()  # Process arithmetic expression
        

        ##  Bp -> A ( 'gr' | '>') A
        match self.curr_token.val:    # Matching current token value
            case '>' | 'gr ':   # greater than
                self.read()
                self.procA()
               
                self.build_tree("gr", 2)    # Building tree for comparison operations
            

            case 'ge' | '>=': # greater than or equal
                self.read()
                self.procA()
                
                self.build_tree("ge", 2)  # Building tree for comparison operations


            case '<' | 'ls':  # less than
                self.read()
                self.procA()
                
                self.build_tree("ls", 2)  # Building tree for comparison operations

            
            case '<=' | 'le': # less than or equal
                self.read()
                self.procA()
                
                self.build_tree("le", 2)  # Building tree for comparison operations


            case 'eq':  # equal
                self.read()
                self.procA()
                
                self.build_tree("eq", 2)  # Building tree for comparison operations

            case 'ne':  # not equal
                self.read()
                self.procA()
                
                self.build_tree("ne", 2)  # Building tree for comparison operations

            case _:  # Default case
                return
            
            
# Method to process arithmetic expression
    def procA(self):
        

        if self.curr_token.val == '+':  # If current token is '+'
            self.read()
            self.procAt()   # Process arithmetic term
            

        elif self.curr_token.val == '-': # If current token is '-'
            self.read()
            self.procAt()   # Process arithmetic term
            
            self.build_tree("neg", 1)  # Build tree for 'neg' operation


        else:
            self.procAt()  # Process arithmetic term
           
        plus = '+'  # Initialize operation as addition
        while self.curr_token.val == '+' or self.curr_token.val == '-':  # While there are '+' or '-' operators

            if self.curr_token.val=='-':
                plus='-'  # If '-', set operation as subtraction

            self.read()
            self.procAt()  # Process arithmetic term
           
            self.build_tree(plus, 2)  # Build tree for addition or subtraction


    # Method to process arithmetic term
    def procAt(self):
        

        self.procAf()  # Process arithmetic factor
        # print('At->Af')
        while self.curr_token.val == '*' or self.curr_token.val == '/':  # While there are '*' or '/' operators
            self.read()
            self.read()
            self.procAf()  # Process arithmetic factor
            
            self.build_tree("*", 2)  # Build tree for multiplication or division


    # Method to process arithmetic factor
    def procAf(self):
        

        self.procAp()
        
        while self.curr_token.val == '**':
            self.read()
            self.procAf()  # Process arithmetic factor
            
            self.build_tree("**", 2)  # Build tree for exponentiation


    # Method to process arithmetic power
    def procAp(self):
        

        self.procR() # Process arithmetic root
        
        while self.curr_token.val == '@':  # While there are '@' operators
            self.read()
            self.procR()  # Process arithmetic root
            
            self.build_tree("@", 2)  # Build tree for root operation

    def procR(self):
        

        self.procRn()   # Process arithmetic negative
        

        while (self.curr_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,Tokenizer.TokenType.STRING] or self.curr_token.val in ['true', 'false','nil', 'dummy',"("]):
            if self.index >= len(self.tokens):
                break
            self.procRn()    # Process arithmetic negative
            
            self.build_tree("gamma", 2)  # Build tree for function application


    # Method to process arithmetic negative
    def procRn(self):
        
        # Check token type and value for identifiers, integers, and strings
        if self.curr_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,Tokenizer.TokenType.STRING]:

            self.read()  # Move to the next token

            

        # Check token value for true, false, nil, dummy
        elif self.curr_token.val in ['true', 'false', 'nil', 'dummy']:
           
            self.read()  # Move to the next token
            
        elif self.curr_token.val == '(':
            self.read()  # Move to the next token
            self.procE()   # Process expression inside parentheses
            if self.curr_token.val != ')':
               
                return   # Return if closing parenthesis is missing
            self.read()  # Move to the next token
            

    
# Method to process declarations
    def procD(self):
       

        self.procDa()   # Process declaration abstraction
        
        while self.curr_token.val == 'within':  # Check for 'within' keyword
            self.read()  # Move to the next token

            self.procD()  # Process nested declarations
           
            self.build_tree("within", 2)

    # Method to process declaration abstraction
    def procDa(self):
        

        self.procDr()  # Process declaration recursor
       
        n = 0  # Counter for 'and' clauses
        while self.curr_token.val == 'and':  # Check for 'and' keyword
            n += 1   # Increment 'and' clause counter
            self.read()  # Move to the next token
            self.procDa()  # Process subsequent declarations
            
        if n > 0:
            self.build_tree("and", n + 1)  # Build tree for 'and' clauses

    # Method to process declaration recursor
    def procDr(self):
        

        if self.curr_token.val == 'rec':
            self.read()  # Move to the next token
            self.procDb()  # Process declaration body recursively
            
            self.build_tree("rec", 1)  # Build tree for 'rec' declaration

        self.procDb()  # Process declaration body
        

    # Method to process declaration body
    def procDb(self):
        

        if self.curr_token.val == '(':  # Check for opening parenthesis
            self.read()  # Move to the next token
            self.procD()  # Process nested declaration
            if self.curr_token.val != ')':  # Check for closing parenthesis
                
                return
            self.read()  # Move to the next token
           
            self.build_tree("()", 1)

        elif self.curr_token.type == Tokenizer.TokenType.ID:  # Check for identifier
            self.read()  # Move to the next token

            if self.curr_token.type == Tokenizer.TokenType.COMMA:  # Check for comma
                # Db -> Vl '=' E => '='
                self.read()   # Move to the next token
                self.procVb()  # Process variable binding

                if self.curr_token.val != '=':  # Check for assignment operator
                    print("Error: = is expected")
                    return
                self.build_tree(",", 2)  # Build tree for comma
                self.read()  # Move to the next token
                self.procE()  # Process expression
                self.build_tree("=", 2) # Build tree for assignment
            else :
                if self.curr_token.val == '=':
                    self.read()  # Move to the next token
                    self.procE()  # Process expression
                    
                    self.build_tree("=", 2)  # Build tree for assignment

                else :

                    n = 0  # Counter for variable bindings
                    while self.curr_token.type == Tokenizer.TokenType.ID or self.curr_token.val == '(':
                        self.procVb()  # Process variable binding
                        n += 1  # Increment variable binding counter

                    if n == 0:
                        print("Error: ID or ( is expected")
                        return

                    if self.curr_token.val != '=':  # Check for assignment operator
                        print("Error: = is expected")
                        return
                    self.read()   # Move to the next token
                    self.procE()  # Process expression
                    
                    self.build_tree("function_form", n + 2)  # Build tree for function form

       

    # Method to process variable binding
    def procVb(self):
       
        if self.curr_token.type == Tokenizer.TokenType.ID:  # Check for identifier
            self.read()  # Move to the next token
            

        elif self.curr_token.val == '(':  # Check for opening parenthesis
            self.read()  # Move to the next token
            
            if self.curr_token.type == ')': # Check for closing parenthesis
               
                self.build_tree("()", 0)  # Build tree for empty parentheses
                self.read()  # Move to the next token
            else:
                self.procVL()  # Process variable list
               
                if self.curr_token.val != ')':  # Check for closing parenthesis
                    print("Error: ) is expected")
                    return
            self.read()  # Move to the next token

            

        else:
            print("Error: ID or ( is expected")
            return

    # Method to process variable list
    def procVL(self):
        

        if self.curr_token.type != Tokenizer.TokenType.ID:  # Check for identifier token type
            pass  # Placeholder for error handling
            # print("562 VL: Identifier expected")  # Replace with appropriate error handling
        else:
            pass
            # print('VL->' + self.curr_token.val)

            self.read()  # Move to the next token
            trees_to_pop = 0  # Counter for trees to be popped
            while self.curr_token.val == ',':  # Check for comma separator
                # Vl -> '<IDENTIFIER>' list ',' => ','?;
                self.read()
                if self.curr_token.type != Tokenizer.TokenType.ID:  # Check for identifier token type
                    print(" 572 VL: Identifier expected")  # Placeholder for error handling
                self.read()
               

                trees_to_pop += 1  # Increment tree counter for popping
           
            if trees_to_pop > 0:
                self.build_tree(',', trees_to_pop +1)  # Build tree for comma-separated identifiers





if __name__ == "__main__":
    import sys

     # Check if command-line arguments are provided
    if len(sys.argv) > 1:
        argv_idx = 1  # Index of file name in argv
        ast_flag = 0  # Flag to check if AST or ST is to be printed

        # Check if AST or ST flag is provided as a command-line argument
        if len(sys.argv) == 3:  # Check if AST or ST flag is present
            argv_idx = 2
            if sys.argv[2] == "-ast":  # Check if AST flag is present
                ast_flag = 1

            input_path = sys.argv[1]  # Get input file path from command-line arguments
        else:
           
            input_path = sys.argv[1]

    with open(input_path) as file:
        program = file.read();   # Read the content of the input file

    stack = []  # Initialize stack for AST nodes
    tokens = []   # Initialize list of tokens

    # tokenize input
    Tokenize = Tokenizer.Tokenize(program)
    token = Tokenize.getNextToken()  # Get the next token
    while token.type != Tokenizer.TokenType.EOF:   # Continue until end of file token is encountered
        tokens.append(token)  # Append token to the list
        token = Tokenize.getNextToken()  # Get the next token

    # screeen tokens
    screener = Screener(tokens)
    tokens = screener.screen()  # Screen the tokens

    parser = ASTParser()  # Initialize AST parser
    parser.tokens = tokens  # Set tokens for parsing
    parser.curr_token = tokens[0]  # Set current token to the first token
    parser.index = 0

    parser.procE()  # Process the expression
    
    root = stack[0]  # Get the root node of the AST
   

     # Write AST to a file
    with open("output_files/" + input_path.split("\\")[-1], "w") as file:
        root.indentation = 0
        root.Tree_to_file(file)
        if ast_flag == 1: root.Tree_to_cmd()  # Print AST to command line if AST flag is set

    # If AST flag is not set, perform further processing
    if ast_flag == 0:
        ASTStandardizer = ASTNode("ASTStandardizer")
        root = ASTStandardizer.standardize(root)

        # Write standardized AST to a file
        with open( "output_files/"+input_path.split("\\")[-1] + "__standarized_output", "w") as file:
            root.indentation = 0
            root.Tree_to_file(file)

        ctrlStructGen = controlStructure.ControlStructureGenerator()  # Initialize control structure generator
        ctr_structs = ctrlStructGen.generate_ctrlStructs(root)  # Generate control structures
        

        # Initialize CSE machine
        cseMachine = CSE_Machine(ctr_structs, input_path)
        # Execute the CSE machine
        result = cseMachine.execute()
        

