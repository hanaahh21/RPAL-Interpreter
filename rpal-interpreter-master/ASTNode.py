
class ASTNode:


    def standardize(self, root):
        # If the root is None, return None
        if root == None:
            return None

        # Recursively standardize the child and sibling nodes
        root.child = self.standardize(root.child)

        if root.sib != None:
            root.sib = self.standardize(root.sib)

        next_sib = root.sib

        
        # Using pattern matching to handle different node types
        match root.type:
            # Handle the "let" node type
            case "let":
                if root.child.type == "=":
                    equal = root.child
                    P = equal.sib
                    X = equal.child
                    E = X.sib
                    lambda_Node = ASTNode("lambda")
                    gamma_Node = ASTNode("gamma")
                    gamma_Node.child = lambda_Node
                    lambda_Node.sib = E
                    X.sib = P
                    lambda_Node.child = X

                    gamma_Node.sib = next_sib

                    return gamma_Node
                
                else:
                    root.sib = next_sib
                    return root
                
            # Handle the "rec" node type
            case "rec":
                eq = root.child
                X = eq.child
                E = X.sib

                new_root = ASTNode("=")
                new_root.child = X

                X_copy = X.createCopy()
                gamma = ASTNode("gamma")
                X.sib = gamma
                gamma.prev = X

                
                yStar = ASTNode("Y*")
                gamma.child = yStar
                lambda_ = ASTNode("lambda")
                yStar.sib = lambda_
                lambda_.prev = yStar

                lambda_.child = X_copy
                X_copy.sib = E
                E.prev = X_copy
                new_root.sib = next_sib


                return new_root
                
            # Handle the "function_form" node type
            case "function_form":
           
                P = root.child
                V = P.sib
                Vs = V.sib

                newRoot = ASTNode("=")
                newRoot.child = P

                lambda_Node = ASTNode("lambda")
                P.sib = lambda_Node
                lambda_Node.prev = P
                
                # Create a chain of lambda nodes for multiple arguments
                while Vs.sib != None:
                    lambda_Node.child = V
                    lambda_Node = ASTNode("lambda")
                    V.sib = lambda_Node
                    lambda_Node.prev = V
                    V = Vs
                    Vs = Vs.sib

                lambda_Node.child = V
                V.sib = Vs
                Vs.prev = V

                newRoot.sib = next_sib

                return newRoot

            
            # Handle the "within" node type
            case "within":
                if root.child.type =="=" and root.child.sib.type == "=":
                    eq1 = root.child
                    eq2 = eq1.sib
                    X1 = eq1.child
                    E1 = X1.sib
                    X2 = eq2.child
                    E2 = X2.sib

                    newRoot = ASTNode("=")
                    newRoot.child = X2
                    gamma = ASTNode("gamma")
                    lambda_Node = ASTNode("lambda")

                    X2.sib = gamma
                    gamma.prev = X2
                    gamma.child = lambda_Node
                    lambda_Node.sib = E1
                    E1.prev = lambda_Node
                    lambda_Node.child = X1
                    X1.sib = E2
                    E2.prev = X1
                    E1.sib = None
                    newRoot.sib = next_sib

                    return newRoot
                else :
                    root.sib = next_sib
                    return root
                
            # Handle the "where" node type
            case "where":
                if root.child.sib.type== "=":
                    P = root.child
                    equal = P.sib
                    X = equal.child
                    E = X.sib
                    lambda_Node = ASTNode("lambda")
                    gamma_Node = ASTNode("gamma")

                    gamma_Node.child = lambda_Node
                    lambda_Node.sib = E
                    lambda_Node.child = X

                    X.sib = P
                    P.sib = None

                    gamma_Node.sib = next_sib

                    return gamma_Node
                
                else:
                    root.sib = next_sib
                    return root
                
                    
            # Handle the "and" node type
            case "and":
                eq = root.child

                newRoot = ASTNode("=")
                comma = ASTNode(",")
                tau = ASTNode("tau")

                newRoot.child = comma
                comma.sib = tau
                tau.prev = comma

                X = eq.child
                E = X.sib

                comma.child = X
                tau.child = E

                eq = eq.sib
                while eq != None:
                    X.sib = eq.child
                    eq.child.prev = X
                    E.sib = eq.child.sib
                    eq = eq.sib
                    X = X.sib
                    E = E.sib

                X.sib = None
                E.sib = None
                newRoot.sib = next_sib


                return newRoot
            
            
            
            # Handle the "@" node type
            case "@":
                E1 = root.child
                N = E1.sib
                E2 = N.sib

                new_root = ASTNode("gamma")
                gamma_l = ASTNode("gamma")

                new_root.child = gamma_l
                gamma_l.sib = E2
                # E2.prev = gamma_l
                gamma_l.child = N
                N.sib = E1
                # E1.prev = N
                E1.sib = None
                new_root.sib=next_sib

                return new_root
            # For other node types, return the root as it is
            case _:
                return root

        return root

    def __init__(self, type):
        # Initialize the ASTNode with the given type
        self.type = type
        self.val = None
        self.source_LineNum = -1
        self.child = None
        self.sib = None      #sibling node
        self.prev = None     #previous node
        self.indentation = 0  # used for printing the tree structure

    def Tree(self):
        # Recursive function to print the tree
        if self.child:
            self.child.Tree()
        if self.sib:
            self.sib.Tree()

    def Tree_to_cmd(self):
        # Function to print the tree structure to the command line
        for i in range(self.indentation):
            print(".", end="")
        # Print the node type and value if available
        if self.val is not None:
            print("<"+str(self.type.split(".")[1]) +":" + str(self.val)+">")
        else:print(str(self.type))
        
        # Recursively print the child and sibling nodes with increased indentation
        if self.child:
            self.child.indentation = self.indentation + 1
            self.child.Tree_to_cmd()
        if self.sib:
            self.sib.indentation = self.indentation
            self.sib.Tree_to_cmd()

    
    # Function to output the tree structure to a file
    def Tree_to_file(self, file):

        for i in range(self.indentation):
            file.write(".")
        # Write the node type and value if available to the file
        if self.val is not None:
            file.write("<"+str(self.type.split(".")[1])+":"+str(self.val)+">" + "\n")
        else :
            file.write(str(self.type) + "\n")
            
        # Recursively write the child and sibling nodes to the file with increased indentation
        if self.child:
            self.child.indentation = self.indentation + 1
            self.child.Tree_to_file(file)
        if self.sib:
            self.sib.indentation = self.indentation
            self.sib.Tree_to_file(file)

    def createCopy (self):
        # Function to create a copy of the current node
        node = ASTNode(self.type)
        node.val = self.val
        node.source_LineNum = self.source_LineNum
        node.child = self.child
        node.sib = self.sib
        node.prev = self.prev
        return node

