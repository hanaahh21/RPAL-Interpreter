import math
import sys

import ASTNode

from Environment import Environment
from controlStructure import LambdaExpression, Beta, Tau


class CSE_Machine :
    ress = []  # Class variable to store results
    def __init__(self , ctrlStructs ,file):
         # Initialize variables
        self.mapEnv={}
        self.curEnvIdx=0
        self.maxEnvIdx=0

        self.curEnvStack=[]
        self.file=file

        # Create initial environment and add it to environment map and stack
        env=Environment(self.curEnvIdx)
        self.mapEnv[self.curEnvIdx]=env
        self.curEnvStack.append(env)


         # Initialize control structures
        self.ctrlStructs = ctrlStructs
        self.stack = []
        self.ctrl = []
        self.stack.append(env)
        self.ctrl.append(env)
        self.ctrl.extend(ctrlStructs[0])


    def binOp(self ,op, rand1,rand2):

        # Perform binary operations
        # Extract operation type and operand values
        binop_type=op.type
        if isinstance(rand2 , ASTNode.ASTNode) and isinstance(rand1 ,ASTNode.ASTNode):
            type1=rand1.type
            type2=rand2.type
            val1=rand1.val
            val2=rand2.val

        # Perform different binary operations based on operation type
        if binop_type == "+":
            # Addition operation
            res = ASTNode.ASTNode("TokenType.INT")
            res.val = str(int(val1) + int(val2))
            return res

        elif binop_type == "-":
            # Subtraction operation
            res=ASTNode.ASTNode( "TokenType.INT")
            res.val=str(int(val1) -int(val2))
            return res

        elif binop_type == "*":
            # Multiplication operation
            res= ASTNode.ASTNode(  "TokenType.INT" )
            res.val=str(int(val1 )* int(val2))
            return res
        
        elif binop_type == "/":
            # division operation
            res=ASTNode.ASTNode("TokenType.INT")
            res.val=str(val1 // val2)
            return res
        
        elif binop_type == "**":
            # Exponential operation
            res = ASTNode.ASTNode("TokenType.INT")
            res.val = str( math.pow(int(val2) ,int(val1)))
            return res

        elif binop_type == "&":
            # AND operation
            res=""
            if val1 == "true" and val2 == "true":
                res = ASTNode.ASTNode("true")
                res.val = "true"
            else:
                res = ASTNode.ASTNode("false")
                res.val = "false"
            return res

        elif binop_type == "or":
            # OR operation
            res=""
            if val1 == "true" and val2 == "true":
                res = ASTNode.ASTNode("true")
                res.val = "true"
            elif  val1 == "false" and val2 == "true":
                res = ASTNode.ASTNode("true")
                res.val = "true"

            elif  val1 == "true" and val2 == "false":
                res = ASTNode.ASTNode("true")
                res.val = "true"



            else:
                
                res = ASTNode.ASTNode("false")
                res.val = "false"
            
            return res


        elif binop_type == "aug":
            

            if isinstance(rand1, list):
                if isinstance(rand2, list):
                    # add all elements of rand2 to rand1
                    temp1 = rand1
                    temp2 = rand2
                    temp2Size = len(temp2)
                    for i in range(temp2Size):
                        temp1.append(temp2[i])
                    return temp1
                else:
                    if isinstance(rand2, ASTNode.ASTNode):
                        # add rand2 to a new tuple and return the new tuple
                        temp1 = rand1
                        temp1.append(rand2)
                        return temp1
                    else:
                        exit(-1)
            elif rand1.val == "nil":
                if isinstance(rand2, list):
                    return rand2
                else:
                    if isinstance(rand2, ASTNode.ASTNode):
                        # add rand2 to a new tuple and return the new tuple
                        t = []
                        t.append(rand2)
                        return t
                    else:
                        exit(-1)
            else:
                # error condition
                exit(-1)
                
                
        elif binop_type == "gr" or  binop_type == ">" : # greater than

            if float(val1)>float(val2):
                res = ASTNode.ASTNode("true")

                res.val = "true"
            else :
                res = ASTNode.ASTNode("false")

                res.val = "false"
            return  res

        elif binop_type == "ge" or  binop_type == ">=":  # greater than or equal

            if int(val1) >= int(val2):
                res = ASTNode.ASTNode("true")

                res.val = "true"
            else:
                res = ASTNode.ASTNode("false")

                res.val = "false"
            return  res

        elif binop_type == "ls" or  binop_type == "<":  # less than

            if int(val1) < int(val2):
                res = ASTNode.ASTNode("true")

                res.val = "true"
            else:
                res = ASTNode.ASTNode("false")

                res.val = "false"
            return  res

        elif binop_type == "le" or  binop_type == "<=": # less than or equal

            if int(val1) <= int(val2):
                res = ASTNode.ASTNode("true")

                res.val = "true"
            else:
                res = ASTNode.ASTNode("false")

                res.val = "false"
            return  res


        elif binop_type == "ne":    # not equal

            res = None
            if rand1.type == "TokenType.STRING" and rand2.type == "TokenType.STRING":
                if val1 != val2:
                    res = ASTNode.ASTNode("true")
                    res.val = "true"

                else:
                    res = ASTNode.ASTNode("false")
                    res.val = "false"

                return res

            else:
                if (int(val1) != int(val2)):
                    res = ASTNode.ASTNode("true")
                    res.val = "true"

                else:
                    res = ASTNode.ASTNode("false")
                    res.val = "false"

            return res

        elif binop_type == "eq":    # equal
            
            res=None
            if rand1.type == "TokenType.STRING" and rand2.type == "TokenType.STRING":
                if val1 == val2:
                    res = ASTNode.ASTNode("true")
                    res.val = "true"
                else:
                    res = ASTNode.ASTNode("false")
                    res.val = "false"
                return res
            else :

                if  (float(val1) == float(val2)):

                    res=ASTNode.ASTNode("true")
                    res.val="true"
                else:
                    res=ASTNode.ASTNode("false")
                    res.val="false"

            return res

        else:
            print("Not found: ", binop_type)

        print("Code not reachable!")
        return None

    def unaryOp(self, op, rand):
        # Perform unary operations
        # Extract operation type and operand value
        unop_type=op.type
        type1=rand.type
        val1=rand.val
        # Perform different unary operations based on operation type
        if unop_type == "not":
            # Logical negation operation
            if type1 != "true" and type1 != "false":
                print("Wrong type: true/false expected for operand: type1:", type1)
                exit(-1)
            if val1 == "true":
                res=ASTNode.ASTNode("false")
                res.val="false"

                return res
            else:
                res = ASTNode.ASTNode("true")
                res.val = "true"

                return res
            
            
        if unop_type == "neg":
            # Numerical negation operation
            if type1 != "TokenType.INT":
                print("Wrong type: INT expected for operand: type1:", type1)
                exit(-1)

            res=ASTNode.ASTNode("TokenType.INT")
            res.val= str(-int(val1))
            return res

        print("Not found :", unop_type)
        return None


    def Print(self ,obj):
        # Method to print an object

        if isinstance( obj , ASTNode.ASTNode):
            # If the object is an instance of ASTNode
            string = obj.val
            if isinstance(obj.val,str):
                # If the value is a string, replace escape characters
                if "\\n" in string:
                    string=string.replace("\\n","\n")
                if "\\t" in string:
                    string=string.replace("\\t","\t")


            # Print the string value
            print(string ,end="")

        if isinstance(obj ,list):
            # If the object is a list
            print("(",end="")
            for index ,i in enumerate(obj) :
                # Print each item in the list
                self.Print(i)
                if index < len(obj)-1:
                    print(",",end=" " )

            print(")",end="\n")


    def execute(self):
        # Method to execute the CSE Machine
        count = 0;
        # Iterate while control stack is not empty
        while len(self.ctrl)>0:
            ctrlTop=self.ctrl[-1]
            stackTop=self.stack[-1]



            # If control is LambdaExpression
            if isinstance(ctrlTop, LambdaExpression):
                lamda=self.ctrl.pop(-1)
                lamda.envIdx=self.curEnvIdx
                self.stack.append(lamda)

            elif isinstance(ctrlTop, ASTNode.ASTNode):
                node=ctrlTop
            
                # gamma node
                if node.type=="gamma":
                    if isinstance(stackTop, LambdaExpression):
                        # APply gamma reduction
                        self.ctrl.pop()  # remove gamma
                        self.stack.pop()  # remove lambda

                        
                        rand = self.stack[-1] # get rand from stack
                        self.stack.pop()  # remove rand from stack

                        lambdaStack = stackTop
                        k = lambdaStack.lambdaIdx
                        envIdLambda = lambdaStack.envIdx
                        tokStack_Lambda_List = None
                        tokStack_Lambda = None




                        if isinstance(lambdaStack.item, ASTNode.ASTNode):
                            tokStack_Lambda = lambdaStack.item  # the variable of lambda of stack
                        else:
                            # a list of Tokens
                            # rule 11
                            if isinstance(lambdaStack.item, list):
                                tokStack_Lambda_List = lambdaStack.item
                            else:
                                print("tokStack_Lambda_List is not a list")

                        
                        # update environment index
                        self.maxEnvIdx += 1
                        self.curEnvIdx = self.maxEnvIdx
                        env = Environment(self.curEnvIdx)

                        
                        if tokStack_Lambda_List is None:
                            env.set_env_parameters(self.mapEnv.get(envIdLambda), tokStack_Lambda.val, rand)
                        else:

                            cnt = 0
                            for item in tokStack_Lambda_List:
                                env.set_env_parameters(self.mapEnv.get(envIdLambda), item.val,rand[cnt])
                                
                                cnt += 1

                        self.ctrl.append(env)
                        self.ctrl.extend(self.ctrlStructs[k]) # k is from stack
                        self.stack.append(env)
                        # maintain environment variables
                        self.curEnvStack.append(env)
                        self.mapEnv[self.curEnvIdx] = env
                    
                    elif isinstance(stackTop, Eta):
                        # rule 13
                        self.ctrl.append(ASTNode.ASTNode("gamma"))
                        eta = stackTop
                        lambdaStack = LambdaExpression(eta.envId, eta.id, eta.tok)
                        self.stack.append(lambdaStack)
                        
                        
                    elif isinstance( stackTop, ASTNode.ASTNode):
                       
                        if stackTop.type == "Y*":
                          # rule for Y*

                            self.ctrl.pop(-1)
                            self.stack.pop(-1)
                            lambdaY=self.stack[-1]
                           
                            self.stack.pop(-1)
                            self.stack.append(Eta(lambdaY.envIdx,lambdaY.lambdaIdx,lambdaY.item))
                        
                        elif stackTop.val == "Print": # rule for print
                            self.ctrl.pop(-1)
                            self.stack.pop(-1)
                            rand =self.stack.pop(-1)
                            self.Print(rand)
                            self.stack.append(ASTNode.ASTNode("dummy"))

                        elif stackTop.val == "Conc":  
                            self.stack.pop(-1)
                            stackTop =self.stack[-1]
                            str1 = stackTop.val
                            self.stack.pop(-1)
                           
                            str2 = self.stack[-1].val
                            self.stack.pop(-1)  # remove str2
                            
                            str_res =  str2 +str1
                            res=ASTNode.ASTNode("TokenType.STRING")
                            res.val= str_res
                            self.stack.append(res)  # push res into stack

                            self.ctrl.pop(-1)  # remove gamma from control
                            
                            self.ctrl.pop(-1)  # remove gamma from control
                            

                        elif stackTop.val=="Stem":
                            self.ctrl.pop(-1)
                            self.stack.pop(-1)
                            str1=self.stack.pop(-1)
                            if len(str1.val) == 0:
                                sys.exit(0)
                            
                            else:
                                val = str1.val[0]
                            res = ASTNode.ASTNode("TokenType.STRING")
                            res.val = val
                            self.stack.append(res)
                            

                        elif stackTop.val=="Stern":
                           
                            self.ctrl.pop(-1)
                            self.stack.pop(-1)
                            str1=self.stack.pop(-1)
                            if len(str1.val) == 0:
                                sys.exit(0)
                            if len(str1.val)==1:
                                val=''
                                
                            else:

                                val=str1.val[1:]
                            res = ASTNode.ASTNode("TokenType.STRING")
                            res.val = val
                            self.stack.append(res)
                            # self.stack.append(val)

                        elif stackTop.val== "Null":
                            self.ctrl.pop(-1)
                            self.stack.pop(-1)
                            stackTop=self.stack[-1]
                            self.stack.pop(-1)


                            if isinstance(stackTop , ASTNode.ASTNode):
                                if stackTop.type== 'nil':
                                    res=ASTNode("true")
                                    res.val="true"
                                    self.stack.append(res)

                            elif isinstance(stackTop ,list):
                                if len(stackTop) == 0 :
                                    res = ASTNode.ASTNode("true")
                                    res.val = "true"
                                    self.stack.append(res)
                                else:
                                    res = ASTNode.ASTNode("false")
                                    res.val = "false"
                                    self.stack.append(res)

                        elif stackTop.val =="ItoS":
                            self.ctrl.pop(-1)
                            self.stack.pop(-1)

                            stackTop= self.stack.pop(-1)
                            res=ASTNode.ASTNode("TokenType.STRING")
                            res.val=str(stackTop.val)
                            # print("ItoS")
                            print(res.val)
                            self.stack.append(res)

                        elif stackTop.val == "Isinteger":
                            self.ctrl.pop(-1)
                            self.stack.pop(-1)
                            stackTop = self.stack.pop(-1)

                            if isinstance(stackTop , ASTNode.ASTNode):
                                if stackTop.type=="TokenType.INT":
                                    res=ASTNode.ASTNode("true")
                                    res.val="true"
                                    self.stack.append(res)
                                else:
                                    res = ASTNode.ASTNode("false")
                                    res.val = "false"
                                    self.stack.append(res)
                            else :
                                sys.exit(0)


                        elif stackTop.val == "Istruthval":

                            self.ctrl.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)

                            if isinstance(stackTop, ASTNode.ASTNode):

                                if stackTop.type == "true" or stackTop.type=="false":

                                    res = ASTNode.ASTNode("true")

                                    res.val = "true"

                                    self.stack.append(res)

                            else:
                                res = ASTNode.ASTNode("false")

                                res.val = "false"

                                self.stack.append(res)

                        elif stackTop.val== "Isstring" :
                            self.ctrl.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)

                            if isinstance(stackTop, ASTNode.ASTNode):
                                if stackTop.type == "TokenType.STRING":
                                    res = ASTNode.ASTNode("true")
                                    res.val = "true"
                                    self.stack.append(res)
                                else:
                                    res = ASTNode.ASTNode("false")
                                    res.val = "false"
                                    self.stack.append(res)
                            else:
                                sys.exit(0)

                        elif stackTop.val=="Istuple":
                            self.ctrl.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)
                            if isinstance(stackTop,list):
                                res = ASTNode.ASTNode("true")
                                res.val = "true"
                                self.stack.append(res)

                            else:
                                res = ASTNode.ASTNode("false")
                                res.val = "false"
                                self.stack.append(res)


                        elif stackTop.val=="Isdummy":
                            self.ctrl.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)
                            if stackTop.val=="dummy":
                                res = ASTNode.ASTNode("true")
                                res.val = "true"
                                self.stack.append(res)
                            else:
                                res = ASTNode.ASTNode("false")
                                res.val = "false"
                                self.stack.append(res)


                        elif stackTop.val =="Order":
                            self.ctrl.pop(-1)
                            self.stack.pop(-1)
                            rand=self.stack.pop(-1)
                            if isinstance(rand,ASTNode.ASTNode):
                                node = ASTNode.ASTNode("TokenType.INT")
                                node.val="0"

                                self.stack.append(node)
                            elif isinstance(rand, list):
                                node=ASTNode.ASTNode("TokenType.INT")
                                node.val=(len(rand))
                                self.stack.append(node)
                            else:
                                #print("Order: rand is not a tuple or nil!!")
                                exit(-1)

                        elif stackTop.type=="TokenType.INT":
                            self.ctrl.pop(-1)

                        elif stackTop.type=="TokenType.STRING":
                            self.ctrl.pop(-1)

                    elif isinstance(stackTop, list):
                        self.ctrl.pop(-1)
                        self.stack.pop(-1)
                        # print("738 ",stackTop[-1].type)
                        index=int(self.stack[-1].val)
                        #print(index ,"index")
                        self.stack.pop(-1)

                        self.stack.append(stackTop[index-1])


                    elif isinstance(stackTop,Eta):
                        # logger.info("applying rule 13")
                        self.ctrl.append(ASTNode.ASTNode( "gamma"))
                        eta = stackTop
                        # Token tempLambdaToken = Token(eta.token.type, eta.token.name)
                        lambdaStack = LambdaExpression(eta.envId, eta.id, eta.tok)
                        self.stack.append(lambdaStack)




                elif node.type in ["-", "+" , "*", "/","or","&","**" ,"aug" ,"gr",">=","ge",">","ls","<","<=","eq","ne","le" ]:
                    #print("Control is - ")
                    op=self.ctrl.pop(-1)
                    rand=self.stack.pop(-1)
                    ran2=self.stack.pop(-1)
                    val=self.binOp(op,rand,ran2 )
                    self.stack.append(val)






                elif node.type=="neg":
                    op = self.ctrl.pop(-1)
                    rand = self.stack.pop(-1)
                    val = self.unaryOp(op, rand)
                    self.stack.append(val)

                elif node.type=="not":
                    op = self.ctrl.pop(-1)
                    rand = self.stack.pop(-1)
                    val = self.unaryOp(op, rand)
                    self.stack.append(val)





                elif node.type=="Y*":
                
                    Ystar=self.ctrl.pop(-1)
                    self.stack.append(Ystar)
                   

                elif node.type=="TokenType.INT":
                   

                    Ystar = self.ctrl.pop(-1)
                    self.stack.append(Ystar)
                    


                else :
                    # rule 1 : lookup in curr or parent environments, and put the val on stack
                    # logger.info("applying rule 1")
                    self.ctrl.pop()
                    curEnv = self.curEnvStack[-1]
                    type_ = ctrlTop.type
                    ctrl_val=ctrlTop.val
                    

                    # first lookup in the environment tree
                    if ctrlTop.type == "TokenType.ID":
                        # do a lookup
                        
                        stackVal = curEnv.get_val(ctrlTop.val)
                        

                        if stackVal is None:
                            curEnv = curEnv.parent
                            
                            while curEnv is not None:
                                
                                stackVal = curEnv.get_val(ctrlTop.val)
                                if stackVal is not None:
                                    break
                                curEnv = curEnv.parent

                               

                        if stackVal is not None:
                           
                            self.stack.append(stackVal)
                            if isinstance(stackVal, ASTNode.ASTNode):
                                pass
                                

                        if stackVal is None:
                            # if not found in the env tree, check if it was a special function
                            # it may be a special function name which was not redefined
                            if ctrl_val in ["Print", "Conc", "Stern", "Stem", "Order", "Isinteger", "Istruthval",
                                         "Isstring", "Isinteger",
                                         "Istuple", "Isfunction", "Isdummy", "ItoS", "Null"]:
                                # just stack the Print, Stern, Stem, ItoS, Order, conc, may be: aug too
                                
                                self.stack.append(ctrlTop)
                            else:
                                
                                sys.exit(-1)
                    else:
                        # just put into stack from control
                        # logger.info("putting ctrlTop: {} | {} on stack".format(ctrlTop, ctrlTop.name))
                        self.stack.append(ctrlTop)



            elif isinstance(ctrlTop , Tau):
                n = self.ctrl[-1].n

                self.ctrl.pop()
                tuple = []
                

                while n > 0:
                    
                    tuple.append(self.stack.pop())
                    stackTop = self.stack[-1] if self.stack else None
                    n -= 1
                self.stack.append(tuple)
            elif isinstance(ctrlTop, Beta):
                if stackTop.type == "true":
                    self.ctrl.pop(-1)  # remove beta
                    self.ctrl.pop(-1)  # remove else
                    self.ctrl.extend(self.ctrlStructs[self.ctrl.pop(-1).idx])
                    self.stack.pop(-1)
                elif stackTop.type == "false":
                    self.ctrl.pop(-1)
                    ctrlTop = self.ctrl[-1]
                    self.ctrl.pop(-1)  # remove else
                    self.ctrl.pop(-1)  # remove then
                    self.ctrl.extend( self.ctrlStructs[ctrlTop.idx])  # insert else back
                    self.stack.pop(-1)
            elif isinstance(ctrlTop, Environment):
                
                self.ctrl.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.append(stackTop)
                
                self.curEnvStack.pop()
                



            count+=1
            if (count>500):
                break







class Eta :
    # Class to represent Eta nodes
    def __init__ (self, envId,id ,tok):
        self.envId=envId
        self.id=id
        self.tok=tok



