# project part 2 electric boogaloo: syntax analyzer
from treelib import Tree # import to create a tree
from executor import execution # import from executor file to call this function at the end
nextTokenCounter = 0 # keep track of position in token/lexeme tuple array
nextToken = '' # initialize nextToken
treePlaceCounter = 0 # keep track of each node's ID by incrementing this once after 
                     # each node creation
treeParentCounter = 0  # keep track of each node's parent by setting this to the ID
                       # of a parent every time a parent node is reached
parentArray = [] # push parent nodes on to this stack to use, to keep track of the node's parent

def syntaxAnalyzer(tokenLexemePassed):
    global tokenLexeme
    global treePlaceCounter
    global parseTree
    global treeParentCounter
    tokenLexeme = tokenLexemePassed # initialize tokenLexeme with the passed value
    
    # Create our parse tree
    parseTree = Tree()
    parseTree.create_node("Start", str(treePlaceCounter)) # add Start as the root with ID='0'
    parentArray.append(treeParentCounter) # push the first parent on to the stack (root / ID='0')
    treePlaceCounter += 1 # increment ID variable

    print("Begin syntax analysis:\n")
    # get the token at the start of the program (lex() stores it in the global nextToken variable)
    # I believe calling this here is the same function as begin() / start() functions
    lex()

    # loop goes through the code line-by-line, restarting after each newline lexeme
    while nextTokenCounter < len(tokenLexeme): # go until the end of the array

        # This IF finds the next BNF statement to call based on the first token above 
        # / the first token that will be left in nextToken from either define() or statement()
        if nextToken == 'DEF_KEYWORD':
            define()
        else:
            statement()
            
    parseTree.create_node("EOF", str(treePlaceCounter), parent='0')

    # parsing is done, call our executor and pass it the parseTree
    execution(parseTree)

# get nextToken into global var using our prior lexical analyzer tuple array (token stored in position 0, lexeme in 1)
# I believe this function is AKA getNextToken()
def lex():
    
    # we have to re-define global variables in scope like this in Python, or it makes a new variable
    # this apparently also has to be done at the beginning of the method?
    global nextToken
    global nextTokenCounter 

    # give values to the 2 variables we're going to print 
    nextToken = tokenLexeme[nextTokenCounter][0]
    lexeme = tokenLexeme[nextTokenCounter][1]

    # increment the counter to go to the next position in the array, next time lex() is called
    nextTokenCounter += 1   
    
    print("Next token is: " + nextToken + ", Next lexeme is " + lexeme) 
    
    return nextToken
   
# Parses strings in the language generated by the rule:
# <assign> --> <id> (= | += | -= | *= | /= | %= | //= | ^= | **= | <<= | >>=) <expr> \n 
def assign():
    print("Enter <assign>")
    
    global treePlaceCounter
    global treeParentCounter
    # create a node for our parse tree. Entering assign so name it <assign>, 
    # the node id is treePlaceCounter turned in to a string. Each node is just given
    # an id one higher: 0, 1, 2, 3, etc. The parent is the last node that was pushed
    # on to the parentArray (using as a stack)
    parseTree.create_node('<assign>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    # change the parent to this node, as it will be the parent of the next node
    treeParentCounter = treePlaceCounter
    # push the node on to the parentArray stack
    parentArray.append(treeParentCounter)
    # increment treePlaceCounter so the next node's ID is one higher
    treePlaceCounter += 1
    
    identifier()
    
    if nextToken == 'ASSIGN_OP' or nextToken == 'PLUS_EQ_OP' or nextToken == 'MINUS_EQ_OP' or nextToken == 'TIMES_EQUAL_OP' or nextToken == 'DIV_EQ_OP' or nextToken == 'MOD_EQ_OP' or nextToken == 'FLOOR_DIV_EQ_OP' or nextToken == 'XOR_EQ_OP' or nextToken == 'POWER_EQ_OP' or nextToken == 'LEFT_EQ_OP' or nextToken == 'RIGHT_EQ_OP':

        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out the OP

        expr()
        # if assign line doesn't end in a new line
        if nextToken != 'NEWLINE':
            print("Error: assignment line didn't end in a newline.")
            exit(1)
            
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out the newline
    else:
        print("Error: not assigned correctly.")
        exit(1)
    # pop this node's ID from the parentArray stack, as we're exiting the method, 
    # so it won't be the parent for the next node
    parentArray.pop()
    print("Exit <assign>")
    
# Parses strings in the language generated by the rule:
# <expr> -> <term> {or <term>} 
def expr():
    print("Enter <expr>") 
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<expr>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    term()
    
    # while the next token is "or", get the next token and parse the next term
    while nextToken == 'LOGICAL_OR_OP':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out OR
        term()
    parentArray.pop()
    print("Exit <expr>")

# Parses strings in the language generated by the rule:
# <term> --> <factor> {and <factor>} 
def term():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<term>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <term>") 
    factor()
    
    while nextToken == 'LOGICAL_AND_OP':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out AND
        factor()
    parentArray.pop()
    print("Exit <term>")

# Parses strings in the language generated by the rule:
# <factor> --> [not] <factor2>  
def factor():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor>") 
    if nextToken == 'NOT_OP':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
    factor2()
    parentArray.pop()
    print("Exit <factor>")

# Parses strings in the language generated by the rule:
# <factor2> --> <factor3> {(== | <= | >= | != | > | < | is | is not | in | not in) <factor3>} 
def factor2():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor2>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor2>") 
    factor3()
    while nextToken == 'IS_EQ_OP' or nextToken == 'LESS_THAN_EQ_OP' or nextToken == 'GREATER_THAN_EQ_OP' or nextToken == 'NOT_EQ_OP' or nextToken == 'LESS_THAN_OP' or nextToken == 'GREATER_THAN_OP' or nextToken == 'IDENT_OP' or nextToken == 'NOT_IDENT_OP' or nextToken == 'MEMBERSHIP_OP' or nextToken == 'NOT_MEMBERSHIP_OP':
       
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
        factor3()
    parentArray.pop()
    print("Exit <factor2>")
    
# Parses strings in the language generated by the rule:
# <factor3> --> <factor4> {| <factor4>} 
def factor3():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor3>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor3>") 
    factor4()
    while nextToken == 'BIT_OR_OP':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
        factor4()
    parentArray.pop()
    print("Exit <factor3>")
    
# Parses strings in the language generated by the rule:
# <factor4> --> <factor5> {^ <factor5>} 
def factor4():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor4>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor4>") 
    factor5()
    while nextToken == 'XOR_OP':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
        factor5()
    parentArray.pop()
    print("Exit <factor4>")

# Parses strings in the language generated by the rule:
# <factor5> --> <factor6> {& <factor6>} 
def factor5():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor5>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor5>") 
    factor6()
    while nextToken == 'BIT_AND_OP':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
        factor6()
    parentArray.pop()
    print("Exit <factor5>")

# Parses strings in the language generated by the rule:
# <factor6> --> <factor7> {(<< | >>) <factor7>}  
def factor6():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor6>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor6>") 
    factor7()
    while (nextToken == 'BIT_RIGHT_OP' or nextToken == 'BIT_LEFT_OP'):
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
        factor7()
    parentArray.pop()
    print("Exit <factor6>")

# Parses strings in the language generated by the rule:
# <factor7> --> <factor8> {(+ | -) <factor8>} 
def factor7():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor7>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor7>") 
    factor8()
    while nextToken == 'ADD_OP' or nextToken == 'SUB_OP':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
        factor8()
    parentArray.pop()
    print("Exit <factor7>")

# Parses strings in the language generated by the rule:
# <factor8> --> <factor9> {(* | / | // | %) <factor9>} 
def factor8():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor8>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor8>") 
    factor9()
    while nextToken == 'MULT_OP' or nextToken == 'DIV_OP' or nextToken == 'MODULO_OP' or nextToken == 'FLOOR_DIV_OP':
      
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1  
      
        lex()
        factor9()
    parentArray.pop()
    print("Exit <factor8>")

# Parses strings in the language generated by the rule:
# <factor9> --> <factor10> {(+x | -x | ~x) <factor10>} 
def factor9():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor9>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor9>") 
    factor10()
    while nextToken == 'UNARY_PLUS_OP' or nextToken == 'UNARY_MINUS_OP' or nextToken == 'BITWISE_NOT_OP':
       
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
        factor10()
        
    parentArray.pop()
    print("Exit <factor9>")

# Parses strings in the language generated by the rule:
# <factor10> --> <factor11> {** <factor11>} 
def factor10():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor10>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor10>") 
    factor11()
    while nextToken == 'EXPONENT_OP':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
        factor11()
    parentArray.pop()
    print("Exit <factor10>")

# Parses strings in the language generated by the rule:
# <factor11> --> ( <expr> ) | <parameter> 
def factor11():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<factor11>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <factor11>")
    if nextToken == 'LEFT_PAREN':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out of LEFT_PAREN
        expr()
        if (nextToken == 'RIGHT_PAREN'):
            
            parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
            treePlaceCounter += 1
            
            lex()
        else:
            print("Error: parentheses not closed.")
            exit(1)
    else:
        parameter()
    parentArray.pop()
    print("Exit <factor11>")

# Parses strings in the language generated by the rule:
# <parameter> --> <id> |  <INT_LITERAL> | <FLOAT> | <string_literal> | <boolean> 
def parameter():
    print("Enter <parameter>")
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<parameter>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    if nextToken == 'IDENTIFIER':
        identifier()
    elif nextToken == 'INT_LITERAL':
        int_literal()
    elif nextToken == 'FLOAT':
        float_function()
    elif nextToken == 'DOUBLE_QUOTE':
        string_literal()
    elif nextToken == 'BOOLEAN':
        boolean()
    else:
        print("Error: not a parameter or undeclared variable.")
        exit(1)
    parentArray.pop()
    print("Exit <parameter>")

# Parses strings in the language generated by the rule:
# <method> --> <method_id> ([<parameter> {, <parameter>}]) \n
def method():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<method>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <method>")
    method_id()
    if nextToken == 'LEFT_PAREN':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex our LEFT_PAREN
        if nextToken != 'RIGHT_PAREN':
            parameter()
            while nextToken == 'COMMA':
                
                parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
                treePlaceCounter += 1
                
                lex() # lex out COMMA
                parameter()
        if nextToken == 'RIGHT_PAREN':
            
            parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
            treePlaceCounter += 1
            
            lex() # lex our right parenthesis
            
            # if doesn't end in a new line
            if nextToken != 'NEWLINE':
                print("Error: method call line didn't end in a newline.")
                exit(1)
            
            parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
            treePlaceCounter += 1
            
            lex() # lex out NEWLINE
        else:
            print("Error: parentheses not closed or comma missing.")
            exit(1)
    else:
        print('Error: no left parenthesis following method name.')
        exit(1)
    parentArray.pop()
    print("Exit <method>")

# Parses strings in the language generated by the rule:
# <while> --> while <expr>: \n <statement> {<statement>} endwhile \n
def while_statement():
    print("Enter <while_statement>")
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<while_statement>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1
    
    lex() # lex out while
    expr()
    if (nextToken == 'COLON_OP'):
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out the colon
        
        # if doesn't end in a new line
        if nextToken != 'NEWLINE':
            print("Error: while statement line didn't end in a newline.")
            exit(1)
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
            
        lex()    # lex out the \n
        statement()
        while nextToken != 'END_WHILE':
            
            # check if EOF was reached before endwhile
            if nextToken == 'END_OF_FILE':
                print("Error: no endwhile detected in file.")
                exit(1)
                
            statement()
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out endwhile
        
        # if line doesn't end in a new line
        if nextToken != 'NEWLINE':
            print("Error: no newline after endwhile.")
            exit(1)
            
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out NEWLINE
    else:
        raise AssertionError("Error: expected nextToken to be 'COLON_OP', got '" + 
        nextToken + "' instead.")
    parentArray.pop()
    print("Exit <while>")

# Parses strings in the language generated by the rule:
# <statement> --> <assign> | <if_statement> | <method> | <while>    
def statement():
    print("Enter <statement>")
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<statement>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    # in our current BNF the only <id> = X definition is <assign>, so this is true
    if nextToken == 'IDENTIFIER':
        assign()
    elif nextToken == 'METHOD_IDENTIFIER':
        method()
    elif nextToken == 'WHILE_KEYWORD':
        while_statement()
    elif nextToken == 'IF_KEYWORD':
        if_statement()
    else:
        print("Error: not a statement.")
        exit(1)
    parentArray.pop()
    print("Exit <statement>")
        
# Parses strings in the language generated by the rule:
# <if_statement> --> if <expr>: \n <statement> {<statement>} {elif <expr>: \n <statement> {<statement>)} [else:\n <statement> {<statement>}] endif \n
def if_statement():
    print("Enter <if_statement>")
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<if_statement>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1

    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1
    
    lex() # lex out IF
    
    expr()
    if nextToken == 'COLON_OP':  # checks for the end of the if statement
    
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out colon
        
        # if line doesn't end in a new line
        if nextToken != 'NEWLINE':
            print("Error: no newline after if statement.")
            exit(1)
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out newline 
        statement()
        
        # while only in the IF, before hitting ELIF / ELSE / ENDIF
        while nextToken != 'ELIF_KEYWORD' and nextToken != 'ELSE_KEYWORD' and nextToken != 'END_IF': 
           
            # check if EOF was reached before endif (missing endif)
            if nextToken == 'END_OF_FILE':
                print("Error: no endif detected in file.")
                exit(1)
                
            statement()
            
        # while in an ELIF
        while nextToken == 'ELIF_KEYWORD':  # checks for anything other than an elif (like an else)
              
            parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
            treePlaceCounter += 1
            
            lex() # lex off elif
            expr()
            if nextToken == 'COLON_OP':  # checks for the end of the elif statement
                   
                parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
                treePlaceCounter += 1
            
                lex() # lex out the COLON
                
                # if line doesn't end in a new line
                if nextToken != 'NEWLINE':
                    print("Error: no newline after elif statement.")
                    exit(1)
                
                parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
                treePlaceCounter += 1
                    
                lex() # lex out the newline
                statement()
            else:
                print("Error: elif statement does not end in COLON_OP.")
                exit(1)
            
            # while still in the given ELIF (not hitting another ELIF, ELSE, or ENDIF)
            while nextToken != 'ELIF_KEYWORD' and nextToken != 'END_IF' and nextToken != 'ELSE_KEYWORD':  # repetition for elif
              
                # check if EOF was reached before endif    
                if nextToken == 'END_OF_FILE':
                    print("Error: no endif detected in file.")
                    exit(1)    
                    
                statement()
                
        if nextToken == 'ELSE_KEYWORD':  # checks for else
        
            parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
            treePlaceCounter += 1
            
            lex() # lex off ELSE
            if nextToken == 'COLON_OP':  # checks for end of the else statement
            
                parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
                treePlaceCounter += 1
                
                lex() # lex out the colon
                
                # if line doesn't end in a new line
                if nextToken != 'NEWLINE':
                    print("Error: no newline after 'else:'")
                    exit(1)
                
                parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
                treePlaceCounter += 1
                    
                lex() # lex out the newline
                statement()
            else:
                print("Error: no COLON_OP found after ELSE.")
                exit(1)
            while nextToken != 'END_IF':  # repetition for else
                
                # check if EOF was reached before endif    
                if nextToken == 'END_OF_FILE':
                    print("Error: no endif detected in file.")
                    exit(1)
                    
                statement()
                
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out endif
        
        # if line doesn't end in a new line
        if nextToken != 'NEWLINE':
            print("Error: no newline after endif.")
            exit(1)
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out NEWLINE
    else:
        print("Error: if statement does not end in COLON_OP.")
        exit(1)
    parentArray.pop()

    print("Exit <if_statement>")
    
# Parses string in the language generated by the rule:
# <define> --> def <method_id> ([<id> {, <id>}]): \n <statement> {<statement>} enddef \n
def define():
    print("Enter <define>")
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<define>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1
    
    lex() # lex off of def
    
    if nextToken == 'METHOD_IDENTIFIER': # method_id is required next
        method_id()
    else:
        print("Error: no method ID given.")
        exit(1)
        
    if nextToken == 'LEFT_PAREN': # left paren is required next
    
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
    else:
        print("Error: no left parenthesis after method ID.")
        exit(1)
        
    if nextToken != 'RIGHT_PAREN':
        if nextToken == 'IDENTIFIER':
            identifier()
        else:
            print("Error: invalid argument given.")
            exit(1)    
        while nextToken == 'COMMA':
            
            parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
            treePlaceCounter += 1
            
            lex()
            if nextToken == 'IDENTIFIER':
                identifier()
            else:
                print("Error: invalid argument given.")
                exit(1)   
    if nextToken == 'RIGHT_PAREN':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
    else:
        print("Error: no matching right parenthesis after method ID and arguments or missing comma.")
        exit(1)
    if nextToken == 'COLON_OP':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex() # lex out COLON_OP
        
        # if line doesn't end in a new line
        if nextToken != 'NEWLINE':
            print("Error: no newline after method declaration.")
            exit(1)
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
    else:
        print("Error: no colon following right parenthesis.")
        exit(1)
    statement()
    
    while nextToken != 'END_DEF':
        
        # check if EOF was reached before enddef    
        if nextToken == 'END_OF_FILE':
            print("Error: no enddef detected in file.")
            exit(1)
            
        statement()
    
    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1
    
    lex() # lex out END_DEF
    
    # if line doesn't end in a new line
    if nextToken != 'NEWLINE':
        print("Error: no newline after endwhile.")
        exit(1)
    
    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1

    lex() # lex out NEWLINE
    parentArray.pop()

    print("Exit <define>")

# Parses strings in the language generated by the rule:
# <id> --> IDENTIFIER 
def identifier():
        
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<id>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1

    print("Enter <id>")
    
    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1
    
    lex()
    parentArray.pop()
    print("Exit <id>")

# Parses strings in the language generated by the rule:
# <int_literal> --> INT_LITERAL 
def int_literal():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<int_literal>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <int_literal>")
    
    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1
    
    lex()
    parentArray.pop()
    print("Exit <int_literal>")

# Parses strings in the language generated by the rule:
# <FLOAT> --> FLOAT 
def float_function():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<float>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <float>")
    
    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1
    
    lex()
    parentArray.pop()
    print("Exit <float>")

# Parses strings in the language generated by the rule:
# <method_id> --> METHOD_IDENTIFIER 
def method_id():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<method_id>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <method_id>")

    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1
    
    lex()
    parentArray.pop()
    print("Exit <method_id>")

# Parses strings in the language generated by the rule:
# <string_literal> --> "{<STRING_LITERAL>}"
# ONLY DOUBLE QUOTES: "" ARE ALLOWED, no '', """, '''
def string_literal():
    print("Enter <string_literal>")
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<string_literal>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1

    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1
    
    lex() # lex out DOUBLE_QUOTE
    
    while nextToken == 'STRING_LITERAL':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
    if nextToken == 'DOUBLE_QUOTE':
        
        parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
        treePlaceCounter += 1
        
        lex()
    else:
        print("Error: quotations not closed.")
        exit(1)
    parentArray.pop()
    print("Exit <string_literal>")

# Parses strings in the language generated by the rule:
# <boolean> --> True | False 
def boolean():
    
    global treePlaceCounter
    global treeParentCounter
    parseTree.create_node('<boolean>', str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treeParentCounter = treePlaceCounter
    parentArray.append(treeParentCounter)
    treePlaceCounter += 1
    
    print("Enter <boolean>")
    
    parseTree.create_node(tokenLexeme[nextTokenCounter-1][1], str(treePlaceCounter), parent=str(parentArray[len(parentArray) - 1]))
    treePlaceCounter += 1
    
    lex()
    parentArray.pop()
    print("Exit <boolean>") 