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
            address = 16
            return f'''
            @{address + offset}
            D=M
            @SP
            AM=M+1
            A=A-1
            M=D
            '''

        elif segment == "pointer":
            if offset == 0:
                pointer = "THIS"
            elif offset == 1:
                pointer = "THAT"
            return f'''
            @{pointer}
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
            address = 16
            return f'''
            @SP
            AM=M-1
            D=M
            @{address + offset}
            M=D
            '''

        elif segment == "pointer":
            if offset == 0:
                pointer = "THIS"
            elif offset == 1:
                pointer = "THAT"
            return f'''
            @SP
            AM=M-1
            D=M
            @{pointer}
            M=D
            '''
        
        elif segment in SEGMENT_MAP:
            pointer = SEGMENT_MAP[segment]
            return f'''
            @{offset}
            D=A
            @{pointer}
            D=M+D
            @R13
            M=D
            @SP
            AM=M-1
            D=M
            @R13
            A=M
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

    logic_counter = 0
    
    def vm_eq():
        '''Generate Hack Assembly code for a VM eq operation'''
        VMTranslator.logic_counter += 1
        return f'''
        @SP
        AM=M-1
        D=M
        @SP
        AM=M-1
        D=M-D
        @labelTrue_{VMTranslator.logic_counter}
        D;JEQ
        D=0
        @labelFalse_{VMTranslator.logic_counter}
        0;JMP
        (labelTrue_{VMTranslator.logic_counter})
        D=-1
        (labelFalse_{VMTranslator.logic_counter})
        @SP
        A=M
        M=D
        @SP
        M=M+1
        '''

    def vm_gt():
        '''Generate Hack Assembly code for a VM gt operation'''
        VMTranslator.logic_counter += 1
        return f'''
        @SP
        AM=M-1
        D=M
        @SP
        AM=M-1
        D=M-D
        @labelTrue_{VMTranslator.logic_counter}
        D;JGT
        D=0
        @labelFalse_{VMTranslator.logic_counter}
        0;JMP
        (labelTrue_{VMTranslator.logic_counter})
        D=-1
        (labelFalse_{VMTranslator.logic_counter})
        @SP
        A=M
        M=D
        @SP
        M=M+1
        '''

    def vm_lt():
        '''Generate Hack Assembly code for a VM lt operation'''
        VMTranslator.logic_counter += 1
        return f'''
        @SP
        AM=M-1
        D=M
        @SP
        AM=M-1
        D=M-D
        @labelTrue_{VMTranslator.logic_counter}
        D;JLT
        D=0
        @labelFalse_{VMTranslator.logic_counter}
        0;JMP
        (labelTrue_{VMTranslator.logic_counter})
        D=-1
        (labelFalse_{VMTranslator.logic_counter})
        @SP
        A=M
        M=D
        @SP
        M=M+1
        '''

    def vm_and():
        '''Generate Hack Assembly code for a VM and operation'''
        return '''
        @SP
        AM=M-1
        D=M
        A=A-1
        M=D&M
        '''

    def vm_or():
        '''Generate Hack Assembly code for a VM or operation'''
        return '''
        @SP
        AM=M-1
        D=M
        A=A-1
        M=D|M
        '''

    def vm_not():
        '''Generate Hack Assembly code for a VM not operation'''
        return '''
        @SP
        A=M-1
        M=!M
        '''

    def vm_label(label):
        '''Generate Hack Assembly code for a VM label operation'''
        return f'''
        ({label})
        '''

    def vm_goto(label):
        '''Generate Hack Assembly code for a VM goto operation'''
        return f'''
        @{label}
        0;JMP
        '''

    def vm_if(label):
        '''Generate Hack Assembly code for a VM if-goto operation'''
        return f'''
        @SP
        AM=M-1
        D=M
        @{label}
        D;JNE
        '''

    def vm_function(function_name, n_vars):
        '''Generate Hack Assembly code for a VM function operation'''
        init = "\n".join(["@SP\nAM=M+1\nA=A-1\nM=0\n" for _ in range(int(n_vars))])
        return f'''
        ({function_name})
        {init}
        '''

    call_counter = 0
    
    def vm_call(function_name, n_args):
        '''Generate Hack Assembly code for a VM call operation'''
        VMTranslator.call_counter += 1    
        return f'''
        @RETURN_ADDRESS_{VMTranslator.call_counter}
        D=A
        @SP
        AM=M+1
        A=A-1
        M=D
        
        @LCL
        D=M
        @SP
        AM=M+1
        A=A-1
        M=D

        @ARG
        D=M
        @SP
        AM=M+1
        A=A-1
        M=D

        @THIS
        D=M
        @SP
        AM=M+1
        A=A-1
        M=D

        @THAT
        D=M
        @SP
        AM=M+1
        A=A-1
        M=D

        @SP
        D=M
        @{5 + n_args}
        D=D-A
        @ARG
        M=D

        @SP
        D=M
        @LCL
        M=D

        @{function_name}
        0;JMP
        (RETURN_ADDRESS_{VMTranslator.call_counter})
        '''

    def vm_return():
        '''Generate Hack Assembly code for a VM return operation'''
        return '''
        @5
        D=A
        @LCL
        A=M-D
        D=M
        @R15
        M=D

        @SP
        AM=M-1
        D=M
        @ARG
        A=M
        M=D

        D=A+1
        @SP
        M=D

        @LCL
        AM=M-1
        D=M
        @THAT
        M=D

        @LCL
        AM=M-1
        D=M
        @THIS
        M=D

        @LCL
        AM=M-1
        D=M
        @ARG
        M=D

        @LCL
        AM=M-1
        D=M
        @LCL
        M=D

        @R15
        A=M
        0;JMP
        '''

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

        
