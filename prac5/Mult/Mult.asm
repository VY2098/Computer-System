// This file is based on part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: Mult.asm

// Multiplies R1 and R2 and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@2
D=M
@NEG
D;JLT

@0
M=0

(LOOP)
@2
D=M
@END
D;JEQ

@1
D=M
@0
M=D+M

@2
M=M-1

@LOOP
0;JMP

(NEG)
@1
M=-M
@2
M=-M
@0
0;JMP

(END)