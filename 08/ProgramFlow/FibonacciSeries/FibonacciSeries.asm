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
@0
D = A
@THAT
D = M + D
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@1
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
@THAT
D = M + D
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
@SP
M = M - 1
A = M
D = M
@R13
M = D
@0
D = A
@ARG
D = M + D
@R14
M = D
@R13
D = M
@R14
A = M
M = D
(MAIN_LOOP_START)
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
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JNE
@END_PROGRAM
0;JMP
(COMPUTE_ELEMENT)
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M+1
@1
D = A
@THAT
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
M = M - 1
A = M
D = M
@R13
M = D
@2
D = A
@THAT
D = M + D
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@4
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
M = M + D
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
@SP
M = M - 1
A = M
D = M
@R13
M = D
@0
D = A
@ARG
D = M + D
@R14
M = D
@R13
D = M
@R14
A = M
M = D
@MAIN_LOOP_START
0;JMP
(END_PROGRAM)
