import Tokenizer
from Tokenizer import Screener
import controlStructure
from cseMachine import CSE_Machine
import os
from ASTNode import ASTNode

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

RESET = '\033[0m' # called to return to standard terminal text color

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems




class ASTParser:

    def __int__(self, tokens1):
        self.tokens = tokens1
        self.curr_token = None
        self.index = 0

    def read(self):

        if self.curr_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                       Tokenizer.TokenType.STRING] :

            terminal_nd = ASTNode( str(self.curr_token.type))
            terminal_nd.val= self.curr_token.val
            stack.append(terminal_nd)
            # #print stack
            # #print("stack content after reading")
            # for node in stack:
            #     #print(node.data)
        if self.curr_token.val in  ['true', 'false', 'nil', 'dummy']:
            # stack.append(ASTNode(self.curr_token.val))
            terminal_nd = ASTNode(str(self.curr_token.type))
            terminal_nd.val = self.curr_token.val
            stack.append(terminal_nd)

        #print("reading : " + str(self.curr_token.val))
        self.index += 1

        if (self.index < len(self.tokens)):
            self.curr_token = self.tokens[self.index]
        # elif self.index  >=len(self.tokens):



    def build_tree(self, token, ariness):
        global stack

        #print("stack content before ")
        # for node in stack:
        #     node.Tree_to_cmd()




        # #print("building tree")

        node = ASTNode(token)

        node.val = None
        node.source_LineNum = -1
        node.child = None
        node.sib = None
        node.prev = None

        while ariness > 0:
            # #print("error in while loop")
            child = stack[-1]
            stack.pop()
            # Assuming pop() is a function that returns an ASTNode
            if node.child is not None:
                child.sib = node.child
                node.child.prev = child
                # node.prev = child
            node.child = child

            node.source_LineNum = child.source_LineNum
            ariness -= 1
        # node.Tree()

        stack.append(node)  # Assuming push() is a function that pushes a node onto a stack
        # #print("stack content after")
        for node in stack:
            pass
            # #print(node.type)

    def procE(self):
        #print('procE')


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
                self.build_tree("let", 2)

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
                self.build_tree("lambda", n+1)

            case _:
                self.procEw()
                # #print('E->Ew')

    def procEw(self):
        #print('procEw')
        self.procT()
        # #print('Ew->T')
        if self.curr_token.val == 'where':
            self.read()
            self.procDr()
            # #print('Ew->T where Dr')
            self.build_tree("where", 2)

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

    def procTa(self):
        # print('procTa')
        self.procTc()
        # print('Ta->Tc')
        while self.curr_token.val == 'aug':
            self.read()
            self.procTc()
            # print('Ta->Tc aug Tc')

            self.build_tree("aug", 2)

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

    def procB(self):
        # print('procB')

        self.procBt()
        # print('B->Bt')
        while self.curr_token.val == 'or':
            self.read()
            self.procBt()
            # print('B->B or B')
            self.build_tree("or", 2)

    def procBt(self):
        # print('procBt')

        self.procBs()
        # print('Bt->Bs')
        while self.curr_token.val == '&':
            self.read()
            self.procBs()
            # print('Bt->Bs & Bs')
            self.build_tree("&", 2)

    def procBs(self):
        # print('procBs')

        if self.curr_token.val == 'not':
            self.read()
            self.procBp()
            # print('Bs->not Bp')
            self.build_tree("not", 1)
        else:
            self.procBp()
            # print('Bs->Bp')

    def procBp(self):
        # print('procBp')

        self.procA()
        # print('Bp->A')
        # print(self.curr_token.val+"######")

        ##  Bp -> A ( 'gr' | '>') A
        match self.curr_token.val:
            case '>':
                self.read()
                self.procA()
                # print('Bp->A gr A')
                self.build_tree("gr", 2)
            case 'gr':
                self.read()
                self.procA()
                # print('Bp->A gr A')
                self.build_tree("gr", 2)

            case 'ge':
                self.read()
                self.procA()
                # print('Bp->A ge A')
                self.build_tree("ge", 2)

            case '>=':
                self.read()
                self.procA()
                # print('Bp->A ge A')
                self.build_tree("ge", 2)



            case '<':
                self.read()
                self.procA()
                # print('Bp->A ls A')
                self.build_tree("ls", 2)

            case 'ls':
                self.read()
                self.procA()
                # print('Bp->A ls A')
                self.build_tree("ls", 2)

            case '<=':
                self.read()
                self.procA()
                # print('Bp->A le A')
                self.build_tree("le", 2)

            case 'le':
                self.read()
                self.procA()
                # print('Bp->A le A')
                self.build_tree("le", 2)

            case 'eq':
                self.read()
                self.procA()
                # print('Bp->A eq A')
                self.build_tree("eq", 2)

            case 'ne':
                self.read()
                self.procA()
                # print('Bp->A ne A')
                self.build_tree("ne", 2)

            case _:
                return

    def procA(self):
        # print('procA')

        if self.curr_token.val == '+':
            self.read()
            self.procAt()
            # print('A->+ At')
            # self.build_tree("+", 1)

        elif self.curr_token.val == '-':
            self.read()
            self.procAt()
            # print('A->- At')
            self.build_tree("neg", 1)


        else:
            self.procAt()
            # print('A->At')
        plus = '+'
        while self.curr_token.val == '+' or self.curr_token.val == '-':

            if self.curr_token.val=='-':
                plus='-'

            self.read()
            self.procAt()
            # print('A->A + / -At')
            # print(self.curr_token.val)
            self.build_tree(plus, 2)


    def procAt(self):
        # print('procAt')

        self.procAf()
        # print('At->Af')
        while self.curr_token.val == '*' or self.curr_token.val == '/':
            self.read()
            self.procAf()
            # print('At->Af * Af')
            # print("curr token val " + self.curr_token.val)
            self.build_tree("*", 2)

    def procAf(self):
        # print('procAf')

        self.procAp()
        # print('Af->Ap')
        while self.curr_token.val == '**':
            self.read()
            self.procAf()
            # print('Af->Ap ** Af')
            self.build_tree("**", 2)

    def procAp(self):
        # print('procAp')

        self.procR()
        # print('Ap->R')
        while self.curr_token.val == '@':
            self.read()
            self.procR()
            # print('Ap->R @ R')
            self.build_tree("@", 2)

    def procR(self):
        # print('procR')

        self.procRn()
        # print('R->Rn')
        # self.read()

        while (self.curr_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                           Tokenizer.TokenType.STRING] or self.curr_token.val in ['true', 'false',
                                                                                                        'nil', 'dummy',
                                                                                                        "("]):
            if self.index >= len(self.tokens):
                break
            self.procRn()
            # print('R->R Rn')
            self.build_tree("gamma", 2)

            # self.read()

    def procRn(self):
        # print("procRn")

        if self.curr_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                       Tokenizer.TokenType.STRING]:

            # print('Rn->' + str(self.curr_token.val))

            self.read()

            # self.read()
            # self.build_tree("id", 0)
        elif self.curr_token.val in ['true', 'false', 'nil', 'dummy']:
            # print('Rn->' + self.curr_token.val)
            self.read()
            # print("self.curr_token.val" , self.curr_token.val)
            # self.build_tree(self.curr_token.val, 0)
        elif self.curr_token.val == '(':
            self.read()
            self.procE()
            if self.curr_token.val != ')':
                # print("Error: ) is expected")
                return
            self.read()
            # print('Rn->( E )')
            # self.build_tree("()", 1)

    def procD(self):
        # print('procD')

        self.procDa()
        # print('D->Da')
        while self.curr_token.val == 'within':
            self.read()
            self.procD()
            # print('D->Da within D')
            self.build_tree("within", 2)

    def procDa(self):
        # print('procDa')

        self.procDr()
        # print('Da->Dr')
        n = 0
        while self.curr_token.val == 'and':
            n += 1
            self.read()
            self.procDa()
            # print('Da->and Dr')
        # if n == 0:
        #     print("Error")
        #     return
        if n > 0:
            self.build_tree("and", n + 1)

    def procDr(self):
        # print('procDr')

        if self.curr_token.val == 'rec':
            self.read()
            self.procDb()
            # print('Dr->rec Db')
            self.build_tree("rec", 1)

        self.procDb()
        # print('Dr->Db')

    def procDb(self):
        # print('procDb')

        if self.curr_token.val == '(':
            self.read()
            self.procD()
            if self.curr_token.val != ')':
                # print("Error: ) is expected")
                return
            self.read()
            # print('Db->( D )')
            self.build_tree("()", 1)

        elif self.curr_token.type == Tokenizer.TokenType.ID:
            self.read()

            if self.curr_token.type == Tokenizer.TokenType.COMMA:
                # Db -> Vl '=' E => '='
                self.read()
                self.procVb()

                if self.curr_token.val != '=':
                    print("Error: = is expected")
                    return
                self.build_tree(",", 2)
                self.read()
                self.procE()
                self.build_tree("=", 2)
            else :
                if self.curr_token.val == '=':
                    self.read()
                    self.procE()
                    # print('Db->id = E')
                    self.build_tree("=", 2)

                else :

                    n = 0
                    while self.curr_token.type == Tokenizer.TokenType.ID or self.curr_token.val == '(':
                        self.procVb()
                        n += 1

                    if n == 0:
                        print("Error: ID or ( is expected")
                        return

                    if self.curr_token.val != '=':
                        print("Error: = is expected")
                        return
                    self.read()
                    self.procE()
                    # print('Db->identifier Vb+ = E')
                    self.build_tree("function_form", n + 2)

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

    def procVb(self):
        # print('procVb')
        if self.curr_token.type == Tokenizer.TokenType.ID:
            self.read()
            # print('Vb->id')
            # self.build_tree("id", 1)

        elif self.curr_token.val == '(':
            self.read()
            # print(self.curr_token.val)
            if self.curr_token.type == ')':
                # print('Vb->( )')
                self.build_tree("()", 0)
                self.read()
            else:
                self.procVL()
                # print('Vb->( Vl )')
                if self.curr_token.val != ')':
                    print("Error: ) is expected")
                    return
            self.read()

            # self.build_tree("()", 1)

        else:
            print("Error: ID or ( is expected")
            return

    def procVL(self):
        # print("procVL")
        # print("559 "+str(self.curr_token.val))

        if self.curr_token.type != Tokenizer.TokenType.ID:
            pass
            # print("562 VL: Identifier expected")  # Replace with appropriate error handling
        else:
            pass
            # print('VL->' + self.curr_token.val)

            self.read()
            trees_to_pop = 0
            while self.curr_token.val == ',':
                # Vl -> '<IDENTIFIER>' list ',' => ','?;
                self.read()
                if self.curr_token.type != Tokenizer.TokenType.ID:
                    print(" 572 VL: Identifier expected")  # Replace with appropriate error handling
                self.read()
                # print('VL->id , ?')

                trees_to_pop += 1
            # print('498')
            if trees_to_pop > 0:
                self.build_tree(',', trees_to_pop +1)  # +1 for the child identifier





if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        argv_idx = 1  # Index of file name in argv
        ast_flag = 0  # Flag to check if AST or ST is to be printed

        if len(sys.argv) == 3:  # Check if AST or ST flag is present
            argv_idx = 2
            if sys.argv[2] == "-ast":  # Check if AST flag is present
                # print("AST flag is set")
                ast_flag = 1

            input_path = sys.argv[1]
        else:
            # print("Error: CSE machine not yet built . try -ast switch as second argument")
            # sys.exit(1)
            input_path = sys.argv[1]

    with open(input_path) as file:
        program = file.read();

    stack = []
    tokens = []

    # tokenize input
    Tokenize = Tokenizer.Tokenize(program)
    token = Tokenize.getNextToken()
    while token.type != Tokenizer.TokenType.EOF:
        tokens.append(token)
        token = Tokenize.getNextToken()

    # sreen tokens
    screener = Screener(tokens)
    tokens = screener.screen()

    parser = ASTParser()
    parser.tokens = tokens
    parser.curr_token = tokens[0]
    parser.index = 0

    parser.procE()
    # print(len(stack))
    root = stack[0]
    # root.Tree()

    with open("output_files/" + input_path.split("\\")[-1], "w") as file:
        root.indentation = 0
        root.Tree_to_file(file)
        if ast_flag == 1: root.Tree_to_cmd()

    if ast_flag == 0:
        ASTStandardizer = ASTNode("ASTStandardizer")
        root = ASTStandardizer.standardize(root)

        with open( "output_files/"+input_path.split("\\")[-1] + "__standardized_output", "w") as file:
            root.indentation = 0
            root.Tree_to_file(file)

        ctrlStructGen = controlStructure.ControlStructureGenerator()
        ctr_structs = ctrlStructGen.generate_ctrlStructs(root)
        # ctrlStructGen.print_ctrl_structs()

        cseMachine = CSE_Machine(ctr_structs, input_path)
        result = cseMachine.execute()
        # print("\n")

