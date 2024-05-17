
import ASTNode

#This class is used to represent the tau node in the control structures
class Tau:
    def __init__(self, n):
        self.n = n
        
        
#This class is used to represent the beta node in the control structures.
class Beta:
    def __init__(self):
        pass
    
    
#This class is used to represent the control structures generated from the AST.
class CtrlStruct:
    def __init__(self, idx, delta):
        self.idx = idx
        self.delta = delta
        
        
#This class is used to represent the lambda expression in the control structures.
class LambdaExpression:
    def __init__(self, envIdx, lambdaIdx, tok):
        self.envIdx = envIdx
        self.lambdaIdx = lambdaIdx
        self.item = tok

    # function to print lambda expression
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
        
        
#This function is used to print the control structures generated from the AST.
    def print_ctrlStructs(self):
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
                elif isinstance(obj, list):
                    
                    for item in obj:
                        if isinstance(item, ASTNode):
                            pass
                            # print("Token item: " + item.type)
                        else:
                            pass
                            # print("item: " + str(item))
                else:
                    print("Neither Token nor LambdaExpression, val: " + str(obj))
            
#This function is used to generate the control structures from the AST. It uses pre-order traversal to generate the control structures.
    def generate_ctrlStructs(self, root):
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


#This function is used to traverse the AST in pre-order fashion and generate the control structures.
    def preorder_traversal(self, root ,delta):
        
        match root.type :
            case "lambda":
                
                self.curIdxDelta += 1
                # currently all environment Indices of each lambda are set to 0, they will be set to proper vals when the lambda gets moved to stack.
                lambda_exp = None
                
                # Check if the root's child type is a comma, indicating multiple parameters (rule 11)
                if root.child.type ==',':
                    # rule 11
                    tau_list = []
                    child = root.child.child
                    # Traverse through all sibling nodes and collect parameters
                    while child is not None:
                        tau_list.append(child)
                        child = child.sib
                    # Create a LambdaExpression with the collected parameters
                    lambda_exp = LambdaExpression(0, self.curIdxDelta, tau_list)
                else:
                    # Create a LambdaExpression with a single parameter
                    lambda_exp = LambdaExpression(0, self.curIdxDelta, root.child)

                # Add the created lambda expression to the current delta list
                self.curr_delta.append(lambda_exp)
                delta_lambda = []

                # Queue the next node for processing, along with the current index delta and the lambda list
                self.queue.append((self.curIdxDelta, root.child.sib, delta_lambda))
                return
            
            
            
            case "gamma":
                self.curr_delta.append(root)
                self.preorder_traversal(root.child, delta)   # Perform a preorder traversal on the child node of the root
                if root.child.sib is not None:          # If the child node has a sibling, perform a preorder traversal on it as well
                    self.preorder_traversal(root.child.sib, delta)
                return

            case "tau":
                init_len=len(self.curr_delta)
                node = root.child           # Initialize the node and next_node for traversal
                next_node = node.sib
                
                # List to hold delta values for tau nodes
                deltas_tau = []
                counter = 0
                
                # Traverse through all child nodes
                while node is not None:
                    # Detach the sibling reference of the current node
                    node.sib = None
                    self.preorder_traversal(node, deltas_tau)
                    node = next_node
                    if node is not None:
                        next_node = node.sib
                    counter += 1

                tau = Tau(counter)
                temp=[]    # to hold nodes being popped from the current delta
                final_len=len(self.curr_delta)
                
                # Determine the number of nodes to be processed
                counter=final_len-init_len
                
                # Pop nodes from the current delta list into the temporary list
                for i in range(counter):
                    temp.append(self.curr_delta.pop())

                self.curr_delta.append(tau)
                
                # Push nodes back from the temporary list into the current delta list
                for i in range(counter):
                    self.curr_delta.append(temp.pop())

                # if root has siblings, preorder traverse it
                if root.sib is not None:
                    self.preorder_traversal(root.sib, delta)
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
                
                delta3 = []
                self.queue.append((savedcurIdxDelta3, node3, delta3))
                
                # Add control structures to curr_delta
                self.curr_delta.append( CtrlStruct ( savedcurIdxDelta2 , delta2))
                self.curr_delta.append(CtrlStruct ( savedcurIdxDelta3 , delta3))
                
                # Add Beta node to curr_delta
                beta = Beta()
                self.curr_delta.append(beta)  

                root.child.sib = None
                self.preorder_traversal(root.child, delta)

                return
            

            case _ :
                self.curr_delta.append(root);
                # If the root node has a child, perform a preorder traversal on it
                if (root.child is not None):
                    self.preorder_traversal(root.child, delta);
                    # If the child node has a sibling, perform a preorder traversal on it
                    if (root.child.sib is not None):
                        self.preorder_traversal(root.child.sib, delta);
                # print("default " + root.type)
                return
            








