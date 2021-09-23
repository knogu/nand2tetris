//begin func SimpleFunction.test
(SimpleFunction.test)
@2
D = A
@counter
M = D
(loop0)
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
@loop0
D;JGT
// finished func
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
M = !M
@SP
M = M+1
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
@1
D = A
@ARG
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
M = M - D
@SP
M = M+1
// begin return
@LCL
D = M
@FRAME1
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
@FRAME1
M = M-1
A = M
D = M
@THAT
M = D
@FRAME1
M = M-1
A = M
D = M
@THIS
M = D
@FRAME1
M = M-1
A = M
D = M
@ARG
M = D
@FRAME1
M = M-1
A = M
D = M
@LCL
M = D
@FRAME1
M = M-1
A = M
0;JMP
// finished return
