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

//pseudocode
// (LOOP)
// while(1)
// {
//     if(keyReg == pressed){
//         GOTO Black
//     } else{
//         GOTO White
//     }
// }
// (Black)
// for(i=0; i<screenX;i++){
//     for(j=0;j<screenY;j++){
        
//     }
// }


//code
//********Check keyboard********
(LOOP)
@24576
D=M;
@BLACK
D;JGT
@WHITE
0;JMP


//********Make screen black********
(BLACK)
@black_cnt
M=0;

(BLACKLOOP1)
@black_cnt
D=M;
@SCREEN
D=A+D;
A=D
M=-1;

//increment counter
@black_cnt
M=M+1;

@8191
D=A;
@black_cnt
D=M-D;
@LOOP
D;JGT
@BLACKLOOP1
0;JMP

//********Make screen white********
(WHITE)
@white_cnt
M=0;

(WHITELOOP1)
@white_cnt
D=M;
@SCREEN
A=A+D;
M=0;

//Increment counter
@white_cnt
M=M+1;

@8191
D=A;
@white_cnt
D=M-D;
@LOOP
D;JGT
@WHITELOOP1
0;JMP