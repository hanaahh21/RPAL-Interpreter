
import ASTNode


class Tau:
    ''' This class is used to represent the tau node in the control structures.'''
    def __init__(self, n):
        self.n = n
class Beta:
    ''' This class is used to represent the beta node in the control structures.'''
    def __init__(self):
        pass

class CtrlStruct:
    ''' This class is used to represent the control structures generated from the AST.'''
    def __init__(self, idx, delta):
        self.idx = idx
        self.delta = delta
class LambdaExpression:
    ''' This class is used to represent the lambda expression in the control structures.'''
    def __init__(self, envIdx, lambdaIdx, tok):
        self.envIdx = envIdx
        self.lambdaIdx = lambdaIdx
        self.item = tok

    def print_lambdaExp(self):
        if isinstance(self.item, ASTNode.ASTNode):
            pass

            
        elif isinstance(self.item, list):
            
            lam_vars = ""
            for it in self.item:
                lam_vars += it.name + ','
            

class ControlStructureGenerator:
    def __init__(self):
        self.curIdxDelta = 0
        self.queue = []
        self.map_ctrl_structs = {}
        self.curr_delta=[]

    def print_ctrlStructs(self):
        ''' This function is used to print the control structures generated from the AST.'''
        for key, ctrl_struct in self.map_ctrl_structs.items():
            print("key: " + str(key))
            for obj in ctrl_struct:
                if isinstance(obj, ASTNode.ASTNode):
                    if obj.val is not None:
                        print("val: " +  obj.type + str(obj.val))
                    else:
                        print("val: " +  obj.type )

                elif isinstance(obj, LambdaExpression):
                    pass
                    #print("val: ", " envIdx: ", obj.envIdx, " lambdaIdx: ", obj.lambdaIdx)
                elif isinstance(obj, list):
                    #print("a list")
                    for item in obj:
                        if isinstance(item, ASTNode):
                            pass
                            # print("Token item: " + item.type)
                        else:
                            pass
                            # print("item: " + str(item))
                else:
                    print("Neither Token nor LambdaExpression, val: " + str(obj))
            #print("next obj\n\n")

    def generate_ctrlStructs(self, root):
        ''' This function is used to generate the control structures from the AST. It uses pre-order traversal to generate the control structures.'''
        delta = []
        self.curr_delta = []
        self.preorder_traversal(root, delta)
        
        ctrl_delta = CtrlStruct(self.curIdxDelta, delta)
        self.map_ctrl_structs[0] = self.curr_delta.copy()


        while len(self.queue)>0:
            
            self.curr_delta = []


            idx, node, delta_queue = self.queue[0]
            self.preorder_traversal(node, delta_queue)
            
            ctrl_delta = CtrlStruct(idx, delta_queue)
            self.map_ctrl_structs[idx] = self.curr_delta.copy()

            # #print(self.map_ctrl_structs)
            self.queue.pop(0)
            
        return self.map_ctrl_structs



    def preorder_traversal(self, root ,delta):
        ''' This function is used to traverse the AST in pre-order fashion and generate the control structures.'''


        match root.type :
            case "lambda":
                
                self.curIdxDelta += 1
                # currly all environment Indices of each lambda are set to 0, they will be
                # set to proper vals when the lambda gets moved to stack.
                lambda_exp = None
                if root.child.type ==',':
                    # rule 11
                    #print("rule 11")
                    tau_list = []
                    child = root.child.child
                    while child is not None:
                        tau_list.append(child)
                        child = child.sib
                    lambda_exp = LambdaExpression(0, self.curIdxDelta, tau_list)
                else:
                    lambda_exp = LambdaExpression(0, self.curIdxDelta, root.child)

                self.curr_delta.append(lambda_exp)
                delta_lambda = []

                self.queue.append((self.curIdxDelta, root.child.sib, delta_lambda))

                return
            case "->":
                delta2 = []
                # savedcurIdxDelta = curIdxDelta
                savedcurIdxDelta2 = self.curIdxDelta + 1
                savedcurIdxDelta3 = self.curIdxDelta + 2
                self.curIdxDelta += 2

                node2 = root.child.sib
                

                node3 = root.child.sib.sib

                node2.sib = None  # to avoid re-traversal

                self.queue.append((savedcurIdxDelta2, node2, delta2))

                # node3.sib = None

                delta3 = []

                self.queue.append((savedcurIdxDelta3, node3, delta3))
                self.curr_delta.append( CtrlStruct ( savedcurIdxDelta2 , delta2))
                self.curr_delta.append(CtrlStruct ( savedcurIdxDelta3 , delta3))
                beta = Beta()
                self.curr_delta.append(beta)  # TODO: may create a problem: be careful!!!!!!!!!!!!!!!!

                root.child.sib = None
                self.preorder_traversal(root.child, delta)

                return
            case "gamma":
                # print("adding gamma")
                self.curr_delta.append(root)
                self.preorder_traversal(root.child, delta)
                if root.child.sib is not None:
                    self.preorder_traversal(root.child.sib, delta)
                return

            case "tau":
                init_len=len(self.curr_delta)
                node = root.child
                next_node = node.sib
                deltas_tau = []
                counter = 0
                while node is not None:
                    node.sib = None
                    self.preorder_traversal(node, deltas_tau)
                    node = next_node
                    if node is not None:
                        next_node = node.sib
                    counter += 1

                tau = Tau(counter)
                temp=[]
                final_len=len(self.curr_delta)
                # print("adding tau" )
                counter=final_len-init_len
                for i in range(counter):
                    temp.append(self.curr_delta.pop())

                self.curr_delta.append(tau)
                for i in range(counter):
                    self.curr_delta.append(temp.pop())
                # delta.extend(deltas_tau)

                if root.sib is not None:
                    self.preorder_traversal(root.sib, delta)
                return


            case _ :
                self.curr_delta.append(root);
                if (root.child is not None):
                    self.preorder_traversal(root.child, delta);
                    if (root.child.sib is not None):
                        self.preorder_traversal(root.child.sib, delta);
                # print("default " + root.type)
                return
            








