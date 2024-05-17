
class ASTNode:


    def standardize(self, root):

        if root == None:
            return None


        root.child = self.standardize(root.child)

        if root.sib != None:
            root.sib = self.standardize(root.sib)

        next_sib = root.sib

        # prev_sib = root.prev
        # next_sib = root.sib

        match root.type:
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

                    # P.prev = X
                    gamma_Node.sib = next_sib


                    return gamma_Node
                else:
                    root.sib = next_sib

                    return root

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
                    # P.prev = gamma_Node
                    P.sib = None

                    gamma_Node.sib = next_sib


                    return gamma_Node
                else:
                    root.sib = next_sib

                    return root

            case "function_form":
                P = root.child
                V = P.sib
                Vs = V.sib

                newRoot = ASTNode("=")
                newRoot.child = P

                lambda_Node = ASTNode("lambda")
                P.sib = lambda_Node
                lambda_Node.prev = P

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

            case _:
                return root

        return root

    def __init__(self, type):
        self.type = type
        self.val = None
        self.source_LineNum = -1
        self.child = None
        self.sib = None      #sibling
        self.prev = None     #previous
        self.indentation = 0

    def Tree(self):

        if self.child:
            self.child.Tree()
        if self.sib:
            self.sib.Tree()

    def Tree_to_cmd(self):

        for i in range(self.indentation):
            print(".", end="")
        if self.val is not None:
            print("<"+str(self.type.split(".")[1]) +":" + str(self.val)+">")
        else:print(str(self.type))
        

        if self.child:
            self.child.indentation = self.indentation + 1
            self.child.Tree_to_cmd()
        if self.sib:
            self.sib.indentation = self.indentation
            self.sib.Tree_to_cmd()

    # output to the file
    def Tree_to_file(self, file):

        for i in range(self.indentation):
            file.write(".")
        # if(self.type ==)
        if self.val is not None:

            file.write("<"+str(self.type.split(".")[1])+":"+str(self.val)+">" + "\n")
        else :
            file.write(str(self.type) + "\n")

        if self.child:

            self.child.indentation = self.indentation + 1
            self.child.Tree_to_file(file)
        if self.sib:
            self.sib.indentation = self.indentation
            self.sib.Tree_to_file(file)

    def createCopy (self):
        node = ASTNode(self.type)
        node.val = self.val
        node.source_LineNum = self.source_LineNum
        node.child = self.child
        node.sib = self.sib
        node.prev = self.prev
        return node

