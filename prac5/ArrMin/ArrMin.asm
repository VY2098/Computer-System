// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@1
A=M
D=M
@32767
D=A

@0
M=D

@2
D=M
@END
D-1;JLE

(LOOP)
@2
D=M
M=M-1
@END
D-1;JEQ

@1
AM=M+1
D=M

@0
D=D-M
@MIN
D;JLT

@LOOP
0;JMP


(MIN)
@1
A=M
D=M
@0
M=D

@LOOP
0;JMP

(END)
@END
0;JMP
