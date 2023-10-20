from ParseTree import *

class CompilerParser :

    def __init__(self,tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.tokens = tokens
        self.index = 0
    

    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """
        program_tree = ParseTree("class", "")
        program_tree.addChild(self.mustBe("keyword", "class"))
        program_tree.addChild(self.mustBe("identifier", self.current().getValue()))
        program_tree.addChild(self.mustBe("symbol", "{"))

        while not self.have("symbol", "}"):
            self.next() 
        program_tree.addChild(self.mustBe("symbol", "}"))

        return program_tree 
    
    
    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        class_tree = ParseTree("class", "")
        class_tree.addChild(self.mustBe("keyword", "class"))
        class_tree.addChild(self.mustBe("identifier", self.current().getValue()))
        class_tree.addChild(self.mustBe("symbol", "{"))
        
        while self.have("keyword", "static") or self.have("keyword", "field"):
            class_tree.addChild(self.compileClassVarDec())
        while self.have("keyword", "constructor") or self.have("keyword", "function") or self.have("keyword", "method"):
            class_tree.addChild(self.compileSubroutine())

        class_tree.addChild(self.mustBe("symbol", "}"))

        return class_tree 
    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        class_var_dec_tree = ParseTree("classVarDec", "")

        # check static/feild
        if not (self.have("keyword", "static") or self.have("keyword", "field")):
            raise ParseException("expected 'static' or 'field' for class variable declaration")

        class_var_dec_tree.addChild(self.mustBe("keyword", self.current().getValue()))
        
        if self.have("keyword", "int") or self.have("keyword", "char") or self.have("keyword", "boolean"):
                class_var_dec_tree.addChild(self.mustBe("keyword", self.current().getValue()))
        else:
                class_var_dec_tree.addChild(self.mustBe("identifier", self.current().getValue()))

        class_var_dec_tree.addChild(self.mustBe("identifier", self.current().getValue()))
    
        while self.have("symbol", ","):
            class_var_dec_tree.addChild(self.mustBe("symbol", ","))
            class_var_dec_tree.addChild(self.mustBe("identifier", self.current().getValue()))

        class_var_dec_tree.addChild(self.mustBe("symbol", ";"))

        return class_var_dec_tree 
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        sub_rout_tree = ParseTree("subroutine", "")
        
        sub_rout_tree.addChild(self.mustBe("keyword", self.current().getValue()))
        if self.have("keyword", "void") or self.have("keyword", "int") or self.have("keyword", "char") or self.have("keyword", "boolean"):
            sub_rout_tree.addChild(self.mustBe("keyword", self.current().getValue()))
        elif self.have("identifier", self.current().getValue()):
            sub_rout_tree.addChild(self.mustBe("identifier", self.current().getValue()))
        else:
            raise ParseException("expected keyword or identifier for class variable declaration")

        sub_rout_tree.addChild(self.mustBe("identifier", self.current().getValue()))
        sub_rout_tree.addChild(self.mustBe("symbol", "("))

        while not self.have("symbol", ")"):
            sub_rout_tree.addChild(self.compileParameterList())
        
        sub_rout_tree.addChild(self.mustBe("symbol", ")"))
        sub_rout_tree.addChild(self.compileSubroutineBody())

        return sub_rout_tree

    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        param_list_tree = ParseTree("parameterList", "")

        if self.have("keyword", "int") or self.have("keyword", "char") or self.have("keyword", "boolean"):
            param_list_tree.addChild(self.mustBe("keyword", self.current().getValue()))
        else:
            param_list_tree.addChild(self.mustBe("identifier", self.current().getValue()))

        param_list_tree.addChild(self.mustBe("identifier", self.current().getValue()))

        while self.have("symbol", ","):
            param_list_tree.addChild(self.mustBe("symbol", ","))

            if self.have("keyword", "int") or self.have("keyword", "char") or self.have("keyword", "boolean"):
                param_list_tree.addChild(self.mustBe("keyword", self.current().getValue()))
            else:
                param_list_tree.addChild(self.mustBe("identifier", self.current().getValue()))

            param_list_tree.addChild(self.mustBe("identifier", self.current().getValue()))
            
        return param_list_tree
    
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        sub_rout_body_tree = ParseTree("subroutineBody", "")

        sub_rout_body_tree.addChild(self.mustBe("symbol", "{"))

        while not self.have("symbol", "}"):
            if self.have("keyword", "var"):
                sub_rout_body_tree.addChild(self.compileVarDec())
            else:
                sub_rout_body_tree.addChild(self.compileStatements())
        
        sub_rout_body_tree.addChild(self.mustBe("symbol", "}"))

        return sub_rout_body_tree
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        var_dec_tree = ParseTree("varDec", "")

        var_dec_tree.addChild(self.mustBe("keyword", "var"))

        if self.have("keyword", "int") or self.have("keyword", "char") or self.have("keyword", "boolean"):
            var_dec_tree.addChild(self.mustBe("keyword", self.current().getValue()))
        else:
            var_dec_tree.addChild(self.mustBe("identifier", self.current().getValue()))

        var_dec_tree.addChild(self.mustBe("identifier", self.current().getValue()))

        while self.have("symbol", ","):
            var_dec_tree.addChild(self.mustBe("symbol", ","))
            var_dec_tree.addChild(self.mustBe("identifier", self.current().getValue()))

        var_dec_tree.addChild(self.mustBe("symbol", ";"))

        return var_dec_tree
    

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        """
        statements_tree = ParseTree("statements", "")

        while self.current() and self.current().getType() == "keyword" and self.current().getValue() in ["let", "if", "while", "do", "return"]:
            if self.current().getValue() == "let":
                statements_tree.addChild(self.compileLet())
            elif self.current().getValue() == "if":
                statements_tree.addChild(self.compileIf())
            elif self.current().getValue() == "while":
                statements_tree.addChild(self.compileWhile())
            elif self.current().getValue() == "do":
                statements_tree.addChild(self.compileDo())
            elif self.current().getValue() == "return":
                statements_tree.addChild(self.compileReturn())

        return statements_tree 
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        let_tree = ParseTree("letStatement", "")

        let_tree.addChild(self.mustBe("keyword", "let"))
        let_tree.addChild(self.mustBe("identifier", self.current().getValue()))

        if self.have("symbol", "["):
            let_tree.addChild(self.mustBe("symbol", "["))
            let_tree.addChild(self.compileExpression())
            let_tree.addChild(self.mustBe("symbol", "]"))

        let_tree.addChild(self.mustBe("symbol", "="))

        while not self.have("symbol", ";"):
            let_tree.addChild(self.compileExpression())

        let_tree.addChild(self.mustBe("symbol", ";"))

        return let_tree


    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        if_tree = ParseTree("ifStatement", "")

        if_tree.addChild(self.mustBe("keyword", "if"))
        if_tree.addChild(self.mustBe("symbol", "("))

        while not self.have("symbol", ")"):
            if_tree.addChild(self.compileExpression())
        
        if_tree.addChild(self.mustBe("symbol", ")"))
        if_tree.addChild(self.mustBe("symbol", "{"))

        while not self.have("symbol", "}"):
            if_tree.addChild(self.compileStatements())

        if_tree.addChild(self.mustBe("symbol", "}"))

        if self.have("keyword", "else"):
            if_tree.addChild(self.mustBe("keyword", "else"))
            if_tree.addChild(self.mustBe("symbol", "{"))
            while not self.have("symbol", "}"):
                if_tree.addChild(self.compileStatements())
            if_tree.addChild(self.mustBe("symbol", "}"))
        
        return if_tree

    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        while_tree = ParseTree("whileStatements", "")

        while_tree.addChild(self.mustBe("keyword", "while"))
        while_tree.addChild(self.mustBe("symbol", "("))

        while not self.have("symbol", ")"):
            while_tree.addChild(self.compileExpression())

        while_tree.addChild(self.mustBe("symbol", ")"))
        while_tree.addChild(self.mustBe("symbol", "{"))

        while not self.have("symbol", "}"):
            while_tree.addChild(self.compileStatements())

        while_tree.addChild(self.mustBe("symbol", "}"))

        return while_tree


    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        do_tree = ParseTree("doStatements", "")

        do_tree.addChild(self.mustBe("keyword", "do"))

        while not self.have("symbol", ";"):
            do_tree.addChild(self.compileExpression())

        do_tree.addChild(self.mustBe("symbol", ";"))

        return do_tree


    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        return_tree = ParseTree("returnStatements", "")

        return_tree.addChild(self.mustBe("keyword", "return"))

        while not self.have("symbol", ";"):
            return_tree.addChild(self.compileExpression())

        return_tree.addChild(self.mustBe("symbol", ";"))

        return return_tree 


    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        expression_tree = ParseTree("expression", "")
    
        expression_tree.addChild(self.mustBe("keyword", "skip"))

        return expression_tree 


    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """
        return None 


    def compileExpressionList(self):
        """
        Generates a parse tree for an expression list
        @return a ParseTree that represents the expression list
        """
        return None 


    def next(self):
        """
        Advance to the next token
        """
        if self.index < len(self.tokens):
            self.index += 1


    def current(self):
        """
        Return the current token
        @return the token
        """
        return self.tokens[self.index] if self.index < len(self.tokens) else None


    def have(self,expectedType,expectedValue=None):
        """
        Check if the current token matches the expected type and value.
        @return True if a match, False otherwise
        """
        token = self.current()
        return token is not None and token.getType() == expectedType and token.getValue() == expectedValue


    def mustBe(self,expectedType,expectedValue=None):
        """
        Check if the current token matches the expected type and value.
        If so, advance to the next token, returning the current token, otherwise throw/raise a ParseException.
        @return token that was current prior to advancing.
        """
        token = self.current()
        if not self.have(expectedType, expectedValue):
            raise ParseException(f"Expected {expectedType} '{expectedValue}', but found {token.getType()} '{token.getValue()}'")
        self.next()
        return token
    

if __name__ == "__main__":


    """ 
    Tokens for:
        class Main {
            static int a ;
        }
    """
    tokens = []
    tokens.append(Token("keyword","class"))
    tokens.append(Token("identifier","Main"))
    tokens.append(Token("symbol","{"))

    tokens.append(Token("keyword","static"))
    tokens.append(Token("keyword","int"))
    tokens.append(Token("identifier","a"))
    tokens.append(Token("symbol",","))
    tokens.append(Token("identifier","b"))
    tokens.append(Token("symbol",";"))

    tokens.append(Token("keyword","field"))
    tokens.append(Token("identifier","myV"))
    tokens.append(Token("identifier","c"))
    tokens.append(Token("symbol",";"))

    tokens.append(Token("keyword","function"))
    tokens.append(Token("keyword","void"))
    tokens.append(Token("identifier","myFunc"))

    tokens.append(Token("symbol","("))
    tokens.append(Token("keyword","int"))
    tokens.append(Token("identifier","a"))
    tokens.append(Token("symbol",")"))
    tokens.append(Token("symbol","{"))

    tokens.append(Token("keyword","var"))
    tokens.append(Token("keyword","char"))
    tokens.append(Token("identifier","a"))
    tokens.append(Token("symbol",";"))

    tokens.append(Token("keyword","var"))
    tokens.append(Token("keyword","int"))
    tokens.append(Token("identifier","b"))
    tokens.append(Token("symbol",";"))

    tokens.append(Token("keyword","let"))
    tokens.append(Token("identifier","a"))
    tokens.append(Token("symbol","="))
    tokens.append(Token("keyword","skip"))
    tokens.append(Token("symbol",";"))
    tokens.append(Token("symbol","}"))

    tokens.append(Token("keyword","method"))
    tokens.append(Token("keyword","int"))
    tokens.append(Token("identifier","myFunc2"))

    tokens.append(Token("symbol","("))
    tokens.append(Token("symbol",")"))
    tokens.append(Token("symbol","{"))

    tokens.append(Token("keyword","var"))
    tokens.append(Token("identifier","myV"))
    tokens.append(Token("identifier","a"))
    tokens.append(Token("symbol",";"))

    tokens.append(Token("keyword","do"))
    tokens.append(Token("keyword","skip"))
    tokens.append(Token("symbol",";"))

    tokens.append(Token("keyword","while"))
    tokens.append(Token("symbol","("))
    tokens.append(Token("keyword","skip"))
    tokens.append(Token("symbol",")"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("keyword","return"))
    tokens.append(Token("symbol",";"))
    tokens.append(Token("symbol","}"))

    tokens.append(Token("keyword","if"))
    tokens.append(Token("symbol","("))
    tokens.append(Token("keyword","skip"))
    tokens.append(Token("symbol",")"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))
    tokens.append(Token("keyword","else"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))

    tokens.append(Token("symbol","}"))
    tokens.append(Token("symbol","}"))

    parser = CompilerParser(tokens)
    try:
        result = parser.compileClass()
        print(result)
    except ParseException:
        print("Error Parsing!")
