// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// Assign RAM[0] to multiplicand variable
@R0
D=M
@multiplicand
M=D

// Assign RAM[1] to multiplier variable
@R1
D=M
@multiplier
M=D

// Initialize result variable
@result
M=0

// Core multiplication loop
(LOOP)
    // Check if multiplier is 0, if so calculation is complete
    @multiplier
    D=M
    @END
    D;JEQ
    // Decrement the multiplier
    @multiplier
    M=M-1
    // Add multiplicand to result
    @result
    D=M
    @multiplicand
    D=D+M
    @result
    M=D
    // Jump to start of core multiplication loop
    @LOOP
    0;JMP

// Store results in RAM[2], and infinite loop
(END)
    @result
    D=M
    @R2
    M=D
    @END
    0;JMP