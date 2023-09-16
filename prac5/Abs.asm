// Calculates the absolute value of R1 and stores the result in R0.
// (R0, R1 refer to RAM[0], and RAM[1], respectively.)

// Put your code here.
@1
D=M

@POS
D;JGE

@1
M=-M

(POS)
@1
D=M
@0
M=D