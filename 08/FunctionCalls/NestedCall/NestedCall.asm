//begin func Sys.init
(Sys.init)
@4000
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M - 1
A = M
D = M
@R13
M = D
@3
D = A
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@5000
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M - 1
A = M
D = M
@R13
M = D
@4
D = A
@R14
M = D
@R13
D = M
@R14
A = M
M = D
// begin call Sys.main
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
@5
D = D - A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Sys.main
0;JMP
(label0)
//finished call Sys.main
@SP
M = M - 1
A = M
D = M
@R13
M = D
@6
D = A
@R14
M = D
@R13
D = M
@R14
A = M
M = D
(LOOP)
@LOOP
0;JMP
//begin func Sys.main
(Sys.main)
@5
D = A
@counter
M = D
(loop1)
@0
D = A
@SP
A = M
M = D
@SP
M = M+1
@counter
M = M - 1
D = M
@loop1
D;JGT
// finished func
@4001
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M - 1
A = M
D = M
@R13
M = D
@3
D = A
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@5001
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M - 1
A = M
D = M
@R13
M = D
@4
D = A
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@200
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M - 1
A = M
D = M
@R13
M = D
@1
D = A
@LCL
D = M + D
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@40
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M - 1
A = M
D = M
@R13
M = D
@2
D = A
@LCL
D = M + D
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@6
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M - 1
A = M
D = M
@R13
M = D
@3
D = A
@LCL
D = M + D
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@123
D = A
@SP
A = M
M = D
@SP
M = M+1
// begin call Sys.add12
@label2
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
@Sys.add12
0;JMP
(label2)
//finished call Sys.add12
@SP
M = M - 1
A = M
D = M
@R13
M = D
@5
D = A
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M+1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M+1
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M+1
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M+1
@4
D = A
@LCL
A = M + D
D = M
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
M = M + D
@SP
M = M+1
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
@FRAME3
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
@FRAME3
M = M-1
A = M
D = M
@THAT
M = D
@FRAME3
M = M-1
A = M
D = M
@THIS
M = D
@FRAME3
M = M-1
A = M
D = M
@ARG
M = D
@FRAME3
M = M-1
A = M
D = M
@LCL
M = D
@R15
A = M
0;JMP
// finished return
//begin func Sys.add12
(Sys.add12)
@4002
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M - 1
A = M
D = M
@R13
M = D
@3
D = A
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@5002
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M - 1
A = M
D = M
@R13
M = D
@4
D = A
@R14
M = D
@R13
D = M
@R14
A = M
M = D
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
@12
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
M = M + D
@SP
M = M+1
// begin return
@LCL
D = M
@FRAME4
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
@FRAME4
M = M-1
A = M
D = M
@THAT
M = D
@FRAME4
M = M-1
A = M
D = M
@THIS
M = D
@FRAME4
M = M-1
A = M
D = M
@ARG
M = D
@FRAME4
M = M-1
A = M
D = M
@LCL
M = D
@R15
A = M
0;JMP
// finished return
