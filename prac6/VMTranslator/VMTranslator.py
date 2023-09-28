class VMTranslator:

    def vm_push(segment, offset):
        '''Generate Hack Assembly code for a VM push operation'''
        
        SEGMENT_MAP = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
        
        if segment == "constant":
            return f'''
            @{offset}
            D=A
            @SP
            AM=M+1
            A=A-1
            M=D
            '''

        elif segment == "temp":
            address = 5
            return f'''
            @{address + offset}
            D=M
            @SP
            AM=M+1
            A=A-1
            M=D
            '''
        
        elif segment == "static":
            file_name = "Filename"
            return f'''
            @{file_name}.{offset}
            D=M
            @SP
            AM=M+1
            A=A-1
            M=D
            '''

        elif segment in SEGMENT_MAP:
            pointer = SEGMENT_MAP[segment]
            return f'''
            @{offset}
            D=A
            @{pointer}
            A=M+D
            D=M
            @SP
            AM=M+1
            A=A-1
            M=D
            '''

    def vm_pop(segment, offset):
        '''Generate Hack Assembly code for a VM pop operation'''
        
        SEGMENT_MAP = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
        
        if segment == "temp":
            address = 5
            return f'''
            @SP
            AM=M-1
            D=M
            @{address + offset}
            M=D
            '''
        
        elif segment == "static":
            file_name = "Filename"
            return f'''
            @SP
            AM=M-1
            D=M
            @{file_name}.{offset}
            M=D
            '''

        elif segment in SEGMENT_MAP:
            pointer = SEGMENT_MAP[segment]
            return f'''
            @SP
            AM=M-1
            D=M
            @{offset}
            D=A+D
            @{pointer}
            A=M+D
            M=D
            '''

    def vm_add():
        '''Generate Hack Assembly code for a VM add operation'''
        return '''
        @SP
        AM=M-1
        D=M
        A=A-1
        M=D+M
        '''

    def vm_sub():
        '''Generate Hack Assembly code for a VM sub operation'''
        return '''
        @SP
        AM=M-1
        D=M
        A=A-1
        M=M-D
        '''

    def vm_neg():
        '''Generate Hack Assembly code for a VM neg operation'''
        return '''
        @SP
        A=M-1
        M=-M
        '''

    def vm_eq():
        '''Generate Hack Assembly code for a VM eq operation'''
        return ""

    def vm_gt():
        '''Generate Hack Assembly code for a VM gt operation'''
        return ""

    def vm_lt():
        '''Generate Hack Assembly code for a VM lt operation'''
        return ""

    def vm_and():
        '''Generate Hack Assembly code for a VM and operation'''
        return ""

    def vm_or():
        '''Generate Hack Assembly code for a VM or operation'''
        return ""

    def vm_not():
        '''Generate Hack Assembly code for a VM not operation'''
        return ""

    def vm_label(label):
        '''Generate Hack Assembly code for a VM label operation'''
        return ""

    def vm_goto(label):
        '''Generate Hack Assembly code for a VM goto operation'''
        return ""

    def vm_if(label):
        '''Generate Hack Assembly code for a VM if-goto operation'''
        return ""

    def vm_function(function_name, n_vars):
        '''Generate Hack Assembly code for a VM function operation'''
        return ""

    def vm_call(function_name, n_args):
        '''Generate Hack Assembly code for a VM call operation'''
        return ""

    def vm_return():
        '''Generate Hack Assembly code for a VM return operation'''
        return ""

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))

        
