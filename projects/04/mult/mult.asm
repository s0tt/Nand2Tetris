// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// set result R2 to 0
@R2
M=0
// store the multiplier in loopcnt var
@R0
D=M
@loopcnt
M=D
// execute multiplication loop
(ADDLOOP)
@R2
D=M
@R1
D=D+M
@R2
M=D

//reduce loop cnt by 1
@loopcnt
M=M-1;
D=M
@ADDLOOP
D;JGT

//endless loop
(END)
@END
0;JMP