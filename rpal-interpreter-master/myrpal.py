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
            # #print stack
            # #print("stack content after reading")
            # for node in stack:
            #     #print(node.data)

        # Processing specific token values
        if self.curr_token.val in  ['true', 'false', 'nil', 'dummy']:
            # stack.append(ASTNode(self.curr_token.val))
            terminal_nd = ASTNode(str(self.curr_token.type))
            terminal_nd.val = self.curr_token.val
            stack.append(terminal_nd)

        #print("reading : " + str(self.curr_token.val))
        self.index += 1  # Moving to the next token


        if (self.index < len(self.tokens)):
            self.curr_token = self.tokens[self.index]  # Updating current token
        # elif self.index  >=len(self.tokens):



    # Method to build AST tree
    def build_tree(self, token, ariness):
        global stack

        #print("stack content before ")
        # for node in stack:
        #     node.Tree_to_cmd()




        # #print("building tree")

        node = ASTNode(token)  # Creating ASTNode instance

        node.val = None
        node.source_LineNum = -1
        node.child = None
        node.sib = None
        node.prev = None

        # Building the tree based on the arity
        while ariness > 0:
            # #print("error in while loop")
            child = stack[-1]  # Taking the top element from the stack
            stack.pop()    # Removing the top element
            # Assuming pop() is a function that returns an ASTNode
            if node.child is not None:
                child.sib = node.child
                node.child.prev = child
                # node.prev = child
            node.child = child

            node.source_LineNum = child.source_LineNum
            ariness -= 1
        # node.Tree()

        stack.append(node)  # Appending the node to the stack
        # #print("stack content after")
        for node in stack:
            pass
            # #print(node.type)

     # Method to process expression
    def procE(self):
        #print('procE')


        # Matching current token value
        match self.curr_token.val:

            case 'let':
                self.read()
                self.procD()

                if self.curr_token.val != 'in':
                    # #print("Error: in is expected")
                    return

                self.read()
                #print("E->let D in E #####")
                self.procE()
                #print("E->let D in E #")

                # #print('E->let D in E')
                self.build_tree("let", 2)    # Building tree for let expression

            case 'fn':

                n = 0

                self.read()

                while self.curr_token.type == Tokenizer.TokenType.ID or self.curr_token.val == '(':
                    self.procVb()
                    n += 1

                if n == 0:
                    #print("E: at least one 'Vb' expected\n")
                    return

                if self.curr_token.val != '.':
                    #print("Error: . is expected")
                    return

                self.read()
                self.procE()
                # #print('E->fn Vb . E')
                self.build_tree("lambda", n+1)   # Building tree for lambda expression

            case _:  # Default case
                self.procEw()
                # #print('E->Ew')
    

    # Method to process extended expression
    def procEw(self):
        #print('procEw')
        self.procT()
        # #print('Ew->T')
        if self.curr_token.val == 'where':
            self.read()
            self.procDr()
            # #print('Ew->T where Dr')
            self.build_tree("where", 2)  # Building tree for where expression

    # Method to process term
    def procT(self):
        # print('procT')
        self.procTa()
        # print('T->Ta')

        n = 0
        while self.curr_token.val == ',':
            self.read()
            self.procTa()
            n += 1
            # print('T->Ta , Ta')
        if n > 0:
            self.build_tree("tau", n + 1)
        else:
            pass
            # print('T->Ta')

    # Method to process term augmentation
    def procTa(self):
        # print('procTa')
        self.procTc()
        # print('Ta->Tc')
        while self.curr_token.val == 'aug':
            self.read()
            self.procTc()
            # print('Ta->Tc aug Tc')

            self.build_tree("aug", 2)

    # Method to process type conversion
    def procTc(self):
        # print('procTc')

        self.procB()
        # print('Tc->B')
        if self.curr_token.type == Tokenizer.TokenType.TERNARY_OPERATOR:
            self.read()
            self.procTc()

            if self.curr_token.val != '|':
                print("Error: | is expected")
                return
            self.read()
            self.procTc()
            # print('Tc->B -> Tc | Tc')
            self.build_tree("->", 3)

    # Method to process boolean expression
    def procB(self):
        # print('procB')

        self.procBt()  # Process term
        # print('B->Bt')
        while self.curr_token.val == 'or':    # While there are 'or' operators
            self.read()
            self.procBt()    # Process term
            # print('B->B or B')
            self.build_tree("or", 2)    # Build tree for 'or' operation

    # Method to process boolean term
    def procBt(self):
        # print('procBt')

        self.procBs() # Process simple boolean
        # print('Bt->Bs')
        while self.curr_token.val == '&':  # While there are '&' operators
            self.read()
            self.procBs()  # Process simple boolean
            # print('Bt->Bs & Bs')
            self.build_tree("&", 2)    # Build tree for '&' operation

    # Method to process simple boolean
    def procBs(self):
        # print('procBs')

        if self.curr_token.val == 'not':  # If there's a 'not' operator
            self.read()
            self.procBp()  # Process boolean primary
            # print('Bs->not Bp')
            self.build_tree("not", 1)  # Build tree for 'not' operation
        else:
            self.procBp()  # Process boolean primary

            # print('Bs->Bp')
    
    # Method to process boolean primary
    def procBp(self):
        # print('procBp')

        self.procA()  # Process arithmetic expression
        # print('Bp->A')
        # print(self.curr_token.val+"######")

        ##  Bp -> A ( 'gr' | '>') A
        match self.curr_token.val:    # Matching current token value
            case '>':
                self.read()
                self.procA()
                # print('Bp->A gr A')
                self.build_tree("gr", 2)    # Building tree for comparison operations
            case 'gr':
                self.read()
                self.procA()
                # print('Bp->A gr A')
                self.build_tree("gr", 2)  # Building tree for comparison operations

            case 'ge':
                self.read()
                self.procA()
                # print('Bp->A ge A')
                self.build_tree("ge", 2)  # Building tree for comparison operations

            case '>=':
                self.read()
                self.procA()
                # print('Bp->A ge A')
                self.build_tree("ge", 2)  # Building tree for comparison operations



            case '<':
                self.read()
                self.procA()
                # print('Bp->A ls A')
                self.build_tree("ls", 2)  # Building tree for comparison operations

            case 'ls':
                self.read()
                self.procA()
                # print('Bp->A ls A')
                self.build_tree("ls", 2)  # Building tree for comparison operations

            case '<=':
                self.read()
                self.procA()
                # print('Bp->A le A')
                self.build_tree("le", 2)  # Building tree for comparison operations

            case 'le':
                self.read()
                self.procA()
                # print('Bp->A le A')
                self.build_tree("le", 2)  # Building tree for comparison operations

            case 'eq':
                self.read()
                self.procA()
                # print('Bp->A eq A')
                self.build_tree("eq", 2)  # Building tree for comparison operations

            case 'ne':
                self.read()
                self.procA()
                # print('Bp->A ne A')
                self.build_tree("ne", 2)  # Building tree for comparison operations

            case _:  # Default case
                return
# Method to process arithmetic expression
    def procA(self):
        # print('procA')

        if self.curr_token.val == '+':  # If current token is '+'
            self.read()
            self.procAt()   # Process arithmetic term
            # print('A->+ At')
            # self.build_tree("+", 1)

        elif self.curr_token.val == '-': # If current token is '-'
            self.read()
            self.procAt()   # Process arithmetic term
            # print('A->- At')
            self.build_tree("neg", 1)  # Build tree for 'neg' operation


        else:
            self.procAt()  # Process arithmetic term
            # print('A->At')
        plus = '+'  # Initialize operation as addition
        while self.curr_token.val == '+' or self.curr_token.val == '-':  # While there are '+' or '-' operators

            if self.curr_token.val=='-':
                plus='-'  # If '-', set operation as subtraction

            self.read()
            self.procAt()  # Process arithmetic term
            # print('A->A + / -At')
            # print(self.curr_token.val)
            self.build_tree(plus, 2)  # Build tree for addition or subtraction


    # Method to process arithmetic term
    def procAt(self):
        # print('procAt')

        self.procAf()  # Process arithmetic factor
        # print('At->Af')
        while self.curr_token.val == '*' or self.curr_token.val == '/':  # While there are '*' or '/' operators
        self.read()
            self.read()
            self.procAf()  # Process arithmetic factor
            # print('At->Af * Af')
            # print("curr token val " + self.curr_token.val)
            self.build_tree("*", 2)  # Build tree for multiplication or division


    # Method to process arithmetic factor
    def procAf(self):
        # print('procAf')

        self.procAp()
        # print('Af->Ap')
        while self.curr_token.val == '**':
            self.read()
            self.procAf()  # Process arithmetic factor
            # print('Af->Ap ** Af')
            self.build_tree("**", 2)  # Build tree for exponentiation


    # Method to process arithmetic power
    def procAp(self):
        # print('procAp')

        self.procR() # Process arithmetic root
        # print('Ap->R')
        while self.curr_token.val == '@':  # While there are '@' operators
            self.read()
            self.procR()  # Process arithmetic root
            # print('Ap->R @ R')
            self.build_tree("@", 2)  # Build tree for root operation

    def procR(self):
        # print('procR')

        self.procRn()   # Process arithmetic negative
        # print('R->Rn')
        # self.read()

        while (self.curr_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                           Tokenizer.TokenType.STRING] or self.curr_token.val in ['true', 'false',
                                                                                                        'nil', 'dummy',
                                                                                                        "("]):
            if self.index >= len(self.tokens):
                break
            self.procRn()    # Process arithmetic negative
            # print('R->R Rn')
            self.build_tree("gamma", 2)  # Build tree for function application

            # self.read()

    # Method to process arithmetic negative
    def procRn(self):
        # print("procRn")
        # Check token type and value for identifiers, integers, and strings
        if self.curr_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                       Tokenizer.TokenType.STRING]:

            # print('Rn->' + str(self.curr_token.val))

            self.read()  # Move to the next token

            # self.read()
            # self.build_tree("id", 0)

        # Check token value for true, false, nil, dummy
        elif self.curr_token.val in ['true', 'false', 'nil', 'dummy']:
            # print('Rn->' + self.curr_token.val)
            self.read()  # Move to the next token
            # print("self.curr_token.val" , self.curr_token.val)
            # self.build_tree(self.curr_token.val, 0)
        elif self.curr_token.val == '(':
            self.read()  # Move to the next token
            self.procE()   # Process expression inside parentheses
            if self.curr_token.val != ')':
                # print("Error: ) is expected")
                return   # Return if closing parenthesis is missing
            self.read()  # Move to the next token
            # print('Rn->( E )')
            # self.build_tree("()", 1)

    
# Method to process declarations
    def procD(self):
        # print('procD')

        self.procDa()   # Process declaration abstraction
        # print('D->Da')
        while self.curr_token.val == 'within':  # Check for 'within' keyword
            self.read()  # Move to the next token

            self.procD()  # Process nested declarations
            # print('D->Da within D')
            self.build_tree("within", 2)

    # Method to process declaration abstraction
    def procDa(self):
        # print('procDa')

        self.procDr()  # Process declaration recursor
        # print('Da->Dr')
        n = 0  # Counter for 'and' clauses
        while self.curr_token.val == 'and':  # Check for 'and' keyword
            n += 1   # Increment 'and' clause counter
            self.read()  # Move to the next token
            self.procDa()  # Process subsequent declarations
            # print('Da->and Dr')
        # if n == 0:
        #     print("Error")
        #     return
        if n > 0:
            self.build_tree("and", n + 1)  # Build tree for 'and' clauses

    # Method to process declaration recursor
    def procDr(self):
        # print('procDr')

        if self.curr_token.val == 'rec':
            self.read()  # Move to the next token
            self.procDb()  # Process declaration body recursively
            # print('Dr->rec Db')
            self.build_tree("rec", 1)  # Build tree for 'rec' declaration

        self.procDb()  # Process declaration body
        # print('Dr->Db')

    # Method to process declaration body
    def procDb(self):
        # print('procDb')

        if self.curr_token.val == '(':  # Check for opening parenthesis
            self.read()  # Move to the next token
            self.procD()  # Process nested declaration
            if self.curr_token.val != ')':  # Check for closing parenthesis
                # print("Error: ) is expected")
                return
            self.read()  # Move to the next token
            # print('Db->( D )')
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
                    # print('Db->id = E')
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
                    # print('Db->identifier Vb+ = E')
                    self.build_tree("function_form", n + 2)  # Build tree for function form

        # else:
        #     self.procVL()
        #     print(self.curr_token.val)
        #     if self.curr_token.val != '=':
        #         print("Error: = is expected")
        #         return
        #     self.read()
        #     self.procE()
        #     print('Db->Vl = E')
        #     self.build_tree("=", 2)

    # Method to process variable binding
    def procVb(self):
        # print('procVb')
        if self.curr_token.type == Tokenizer.TokenType.ID:  # Check for identifier
            self.read()  # Move to the next token
            # print('Vb->id')
            # self.build_tree("id", 1)

        elif self.curr_token.val == '(':  # Check for opening parenthesis
            self.read()  # Move to the next token
            # print(self.curr_token.val)
            if self.curr_token.type == ')': # Check for closing parenthesis
                # print('Vb->( )')
                self.build_tree("()", 0)  # Build tree for empty parentheses
                self.read()  # Move to the next token
            else:
                self.procVL()  # Process variable list
                # print('Vb->( Vl )')
                if self.curr_token.val != ')':  # Check for closing parenthesis
                    print("Error: ) is expected")
                    return
            self.read()  # Move to the next token

            # self.build_tree("()", 1)

        else:
            print("Error: ID or ( is expected")
            return

    # Method to process variable list
    def procVL(self):
        # print("procVL")
        # print("559 "+str(self.curr_token.val))

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
                # print('VL->id , ?')

                trees_to_pop += 1  # Increment tree counter for popping
            # print('498')
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
                # print("AST flag is set")
                ast_flag = 1

            input_path = sys.argv[1]  # Get input file path from command-line arguments
        else:
            # print("Error: CSE machine not yet built . try -ast switch as second argument")
            # sys.exit(1)
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

    # sreen tokens
    screener = Screener(tokens)
    tokens = screener.screen()  # Screen the tokens

    parser = ASTParser()  # Initialize AST parser
    parser.tokens = tokens  # Set tokens for parsing
    parser.curr_token = tokens[0]  # Set current token to the first token
    parser.index = 0

    parser.procE()  # Process the expression
    # print(len(stack))
    root = stack[0]  # Get the root node of the AST
    # root.Tree()

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
        with open( "output_files/"+input_path.split("\\")[-1] + "__standardized_output", "w") as file:
            root.indentation = 0
            root.Tree_to_file(file)

        ctrlStructGen = controlStructure.ControlStructureGenerator()  # Initialize control structure generator
        ctr_structs = ctrlStructGen.generate_ctrlStructs(root)  # Generate control structures
        # ctrlStructGen.print_ctrl_structs()

        # Initialize CSE machine
        cseMachine = CSE_Machine(ctr_structs, input_path)
        # Execute the CSE machine
        result = cseMachine.execute()
        # print("\n")

