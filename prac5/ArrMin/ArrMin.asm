// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@1
D=M
@0
M=D

@2
D=M
@END
D;JEQ

@1
D=A+1
@1
M=D

(LOOP)
@1
D=M

@0
D=D-M
@MIN
D;JLT

@1
M=M+1

@2
M=M-1
D=M
@LOOP
D;JGT

@END
0;JMP

(MIN)
@1
D=M
@0
M=D
@1
M=M+1
@2
M=M-1
D=M
@LOOP
D;JGT

(END)