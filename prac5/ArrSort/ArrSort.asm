// Sorts the array of length R2 whose first element is at RAM[R1] in ascending order in place. Sets R0 to True (-1) when complete.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@1
M=M-1

(OUTERLOOP)
@2
M=M-1
D=M
@END
D;JEQ
@7			// INNERLOOP counter
M=D+1
@1
M=M+1
D=M
@3			// min pointer
M=D
@4			// current pointer
AM=D
D=M
@5			// min value
M=D
@6
M=D			// current value

(INNERLOOP)
@7
M=M-1
D=M
@SWAP
D;JEQ
@4
AM=M+1
D=M
@6
M=D
@NEG1
D;JLT
@5
D=M
@NEG2
D;JLT

(COMPARE)
@6
D=M
@5
D=M-D
@INNERLOOP
D;JLE

(UPDATE)
@4
D=M
@3
AM=D
D=M
@5
M=D
@INNERLOOP
0;JMP

(NEG1)
@5
D=M
@COMPARE
D;JLT
@UPDATE
0;JMP

(NEG2)
@6
D=M
@COMPARE
D;JLT
@INNERLOOP
0;JMP

(SWAP)
@1
D=M
@3
D=M-D
@OUTERLOOP
D;JEQ
@1
A=M
D=M
@8
M=D			// temp
@3
A=M
M=D
@5
D=M
@1
A=M
M=D
@OUTERLOOP
0;JMP

(END)
@0
M=-1
@END
0;JMP
