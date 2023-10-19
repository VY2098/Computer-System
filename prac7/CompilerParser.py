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

        if not self.have("keyword", "class"):
            raise ParseException("the program doesn't begin with a class")

        class_keyword = Token("keyword", "class")
        program_tree.addChild(class_keyword)

        if not self.have("identifier", None):
            raise ParseException("expected class name after 'class' keyword")
        class_name_token = Token("identifier", self.current().value)
        program_tree.addChild(class_name_token)
        self.next() 

        if not self.have("symbol", "{"):
            raise ParseException("Expected '{' after class name")
        left_brace = Token("symbol", "{")
        program_tree.addChild(left_brace)
        self.next()

        while not self.have("symbol", "}"):
            self.next() 
        right_brace = Token("symbol", "}")
        program_tree.addChild(right_brace)

        return program_tree 
    
    
    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        class_tree = ParseTree("class", "")

        self.mustBe("keyword", "class")
        class_keyword = Token("keyword", "class")
        class_tree.addChild(class_keyword)

        class_name_token = self.mustBe("identifier", self.current().value)
        class_tree.addChild(class_name_token)

        left_brace = self.mustBe("symbol", "{")
        class_tree.addChild(left_brace)

        while not self.have("symbol", "}"):
            if self.have("keyword", "static") or self.have("keyword", "field"):
                class_var_dec_tree = self.compileClassVarDec()
                class_tree.addChild(class_var_dec_tree)
            else:
                self.next()

        right_brace = self.mustBe("symbol", "}")
        class_tree.addChild(right_brace)

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

        visibility = Token("keyword", self.current().value)
        class_var_dec_tree.addChild(visibility)
        self.next()

        if not self.have("keyword", None) and not self.have("identifier", None):
            raise ParseException("Expected type after 'static' or 'field'")
        type_token = Token(self.current().type, self.current().value)
        class_var_dec_tree.addChild(type_token)
        self.next()

        if not self.have("identifier", None):
            raise ParseException("Expected variable name after type")
        var_name_token = Token("identifier", self.current().value)
        class_var_dec_tree.addChild(var_name_token)
        self.next()

        while self.have("symbol", ","):
            comma = Token("symbol", ",")
            class_var_dec_tree.addChild(comma)
            self.next()

            if not self.have("identifier", None):
                raise ParseException("Expected another variable name after ','")
            var_name_token = Token("identifier", self.current().value)
            class_var_dec_tree.addChild(var_name_token)
            self.next()

        if not self.have("symbol", ";"):
            raise ParseException("Expected ';' at the end of class variable declaration")
        semicolon = Token("symbol", ";")
        class_var_dec_tree.addChild(semicolon)

        return class_var_dec_tree 
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        return None 
    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        param_list_tree = ParseTree("parameterList", "")

        if self.have("symbol", ")"):
            return param_list_tree

        param_type_token = self.mustBe(["keyword", "identifier"], self.current().value)
        param_list_tree.addChild(param_type_token)

        param_name_token = self.mustBe("identifier", self.current().value)
        param_list_tree.addChild(param_name_token)

        while self.have("symbol", ","):
            comma_token = self.mustBe("symbol", ",")
            param_list_tree.addChild(comma_token)

            param_type_token = self.mustBe(["keyword", "identifier"], self.current().value)
            param_list_tree.addChild(param_type_token)

            param_name_token = self.mustBe("identifier", self.current().value)
            param_list_tree.addChild(param_name_token)

        return param_list_tree 
    
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        return None 
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        return None 
    

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
        return None 


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


    def have(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        @return True if a match, False otherwise
        """
        token = self.current()
        return token is not None and token.getType() == expectedType and token.getValue() == expectedValue


    def mustBe(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        If so, advance to the next token, returning the current token, otherwise throw/raise a ParseException.
        @return token that was current prior to advancing.
        """
        token = self.current()
        if not self.have(expectedType, expectedValue):
            raise ParseException(f"Expected {expectedType} '{expectedValue}', but found {token.getType()} '{token.getvalue()}'")
        self.next()
        return token
    

if __name__ == "__main__":


    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    tokens = []
    tokens.append(Token("keyword","class"))
    tokens.append(Token("identifier","MyClass"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))

    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException:
        print("Error Parsing!")
