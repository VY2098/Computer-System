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

        while not self.have("symbol", "}"):
            if self.have("keyword", "static") or self.have("keyword", "field"):
                class_tree.addChild(self.compileClassVarDec())
            elif self.have("keyword", "constructor") or self.have("keyword", "function") or self.have("keyword", "method"):
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

        class_var_dec_tree.addChild(self.mustBe("keyword", self.current().getValue()))

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

        if not (self.have("keyword", "constructor") or self.have("keyword", "function") or self.have("keyword", "method")):
            raise ParseException("expected 'constructor' or 'function' or 'method' for subroutine")
        
        sub_rout_tree.addChild(self.mustBe("keyword", self.current().getValue()))
        sub_rout_tree.addChild(self.mustBe("keyword", self.current().getValue()))
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

        if self.have("symbol", ")"):
            return param_list_tree

        param_list_tree.addChild(self.mustBe("keyword", self.current().getValue()))
        param_list_tree.addChild(self.mustBe("identifier", self.current().getValue()))

        while self.have("symbol", ","):
            param_list_tree.addChild(self.mustBe("symbol", ","))
            param_list_tree.addChild(self.mustBe("keyword", self.current().getValue()))
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
        
        sub_rout_body_tree.addChild(self.mustBe("symbol", "}"))

        return sub_rout_body_tree
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        var_dec_tree = ParseTree("varDec", "")

        var_dec_tree.addChild(self.mustBe("keyword", "var"))

        var_dec_tree.addChild(self.mustBe("keyword", self.current().getValue()))

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
        return None 
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        return None 

    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        return None 


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
    tokens.append(Token("keyword","function"))
    tokens.append(Token("keyword","void"))
    tokens.append(Token("identifier","myFunc"))
    tokens.append(Token("symbol","("))
    tokens.append(Token("keyword","int"))
    tokens.append(Token("identifier","a"))
    tokens.append(Token("symbol",")"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("keyword","var"))
    tokens.append(Token("keyword","int"))
    tokens.append(Token("identifier","a"))
    tokens.append(Token("symbol",";"))
    tokens.append(Token("symbol","}"))

    parser = CompilerParser(tokens)
    try:
        result = parser.compileSubroutine()
        print(result)
    except ParseException:
        print("Error Parsing!")
