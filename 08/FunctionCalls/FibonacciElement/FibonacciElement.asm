@256
D = A
@SP
M = D
//begin func Sys.init
(Sys.init)
@4
D = A
@SP
A = M
M = D
@SP
M = M+1
// begin call Main.fibonacci
@label0
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@6
D = D - A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0;JMP
(label0)
//finished call Main.fibonacci
(WHILE)
@WHILE
0;JMP
//begin func Main.fibonacci
(Main.fibonacci)
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M+1
@2
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
D = M - D
@label0
D;JLT
@SP
A = M
M = 0
@label1
0;JMP
(label0)
@SP
A = M
M = -1
(label1)
@SP
M = M+1
@SP
M=M-1
A=M
D=M
@IF_TRUE
D;JNE
@IF_FALSE
0;JMP
(IF_TRUE)
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M+1
// begin return
@LCL
D = M
@FRAME2
M = D
@5
A = D - A
D = M
@R15
M = D
@SP
M = M - 1
A = M
D = M
@R13
M = D
@ARG
D = M
@R14
M = D
@R13
D = M
@R14
A = M
M = D
// finished pop
@ARG
D = M
@SP
M = D + 1
@FRAME2
M = M-1
A = M
D = M
@THAT
M = D
@FRAME2
M = M-1
A = M
D = M
@THIS
M = D
@FRAME2
M = M-1
A = M
D = M
@ARG
M = D
@FRAME2
M = M-1
A = M
D = M
@LCL
M = D
@R15
A = M
0;JMP
// finished return
(IF_FALSE)
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M+1
@2
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
M = M - D
@SP
M = M+1
// begin call Main.fibonacci
@label3
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@6
D = D - A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0;JMP
(label3)
//finished call Main.fibonacci
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M+1
@1
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
M = M - D
@SP
M = M+1
// begin call Main.fibonacci
@label4
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@6
D = D - A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0;JMP
(label4)
//finished call Main.fibonacci
@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
M = M + D
@SP
M = M+1
// begin return
@LCL
D = M
@FRAME5
M = D
@5
A = D - A
D = M
@R15
M = D
@SP
M = M - 1
A = M
D = M
@R13
M = D
@ARG
D = M
@R14
M = D
@R13
D = M
@R14
A = M
M = D
// finished pop
@ARG
D = M
@SP
M = D + 1
@FRAME5
M = M-1
A = M
D = M
@THAT
M = D
@FRAME5
M = M-1
A = M
D = M
@THIS
M = D
@FRAME5
M = M-1
A = M
D = M
@ARG
M = D
@FRAME5
M = M-1
A = M
D = M
@LCL
M = D
@R15
A = M
0;JMP
// finished return
