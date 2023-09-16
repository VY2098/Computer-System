// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@1
A=M
D=M
@0
M=D

(LOOP)
@2
MD=M-1
@END
D-1;JLE

@1
AM=M+1
D=M
@NEG1
D;JLT

@0
D=M
@NEG2
D;JLT

(COMPARE)
@1
A=M
D=M
@0
D=D-M
@SWAP
D;JLT

@LOOP
0;JMP


(SWAP)
@1
A=M
D=M
@0
M=D

@LOOP
0;JMP

(NEG1)
@0
D=M
@SWAP
D;JGE
@COMPARE
0;JMP

(NEG2)
@1
A=M
D=M
@LOOP
D;JGE
@COMPARE
0;JMP

(END)
@END
0;JMP
