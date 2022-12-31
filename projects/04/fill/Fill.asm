// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Assign keyboard array to keyaddress
@KBD
D=A
@keyaddress
M=D

// Check for key press
(PRESS)
    @KBD
    D=M
    @PRESS
    D;JEQ


// Assign screen array to screenaddress
@SCREEN
D=A
@screenaddress
M=D

// Loop through entirety of screen array - darken all pixels
(PRESSED)
    @keyaddress
    D=M
    @screenaddress
    D=D-M
    @RELEASE
    D;JEQ
    // Set the current screen register to all 1's
    @screenaddress
    A=M
    M=-1
    // Move to next screen address
    @screenaddress
    M=M+1
    @PRESSED
    0;JEQ


// Check for key release
(RELEASE)
    @KBD
    D=M
    @RELEASE
    D;JNE

// Assign screen array to screenaddress
@SCREEN
D=A
@screenaddress
M=D

// Loop through entirety of screen array - lighten all pixels
(LIGHTEN)
    @keyaddress
    D=M
    @screenaddress
    D=D-M
    @PRESS
    D;JEQ

    // Set the current screen register to all 1's
    @screenaddress
    A=M
    M=0

    // Move to next screen address
    @screenaddress
    M=M+1

    @LIGHTEN
    0;JEQ



