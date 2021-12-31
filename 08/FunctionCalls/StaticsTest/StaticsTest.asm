@256
D = A
@SP
M = D
//begin func Sys.init
(Sys.init)
@6
D = A
@SP
A = M
M = D
@SP
M = M+1
@8
D = A
@SP
A = M
M = D
@SP
M = M+1
// begin call Class1.set
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
@7
D = D - A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Class1.set
0;JMP
(label0)
//finished call Class1.set
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
@23
D = A
@SP
A = M
M = D
@SP
M = M+1
@15
D = A
@SP
A = M
M = D
@SP
M = M+1
// begin call Class2.set
@label1
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
@7
D = D - A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Class2.set
0;JMP
(label1)
//finished call Class2.set
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
// begin call Class1.get
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
@5
D = D - A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Class1.get
0;JMP
(label2)
//finished call Class1.get
// begin call Class2.get
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
@5
D = D - A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Class2.get
0;JMP
(label3)
//finished call Class2.get
(WHILE)
@WHILE
0;JMP
//begin func Class2.set
(Class2.set)
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
M = M - 1
A = M
D = M
@Class2.0
M = D
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
@Class2.1
M = D
@0
D = A
@SP
A = M
M = D
@SP
M = M+1
// begin return
@LCL
D = M
@FRAME0
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
@FRAME0
M = M-1
A = M
D = M
@THAT
M = D
@FRAME0
M = M-1
A = M
D = M
@THIS
M = D
@FRAME0
M = M-1
A = M
D = M
@ARG
M = D
@FRAME0
M = M-1
A = M
D = M
@LCL
M = D
@R15
A = M
0;JMP
// finished return
//begin func Class2.get
(Class2.get)
@Class2.0
D = M
@SP
A = M
M = D
@SP
M = M+1
@Class2.1
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
@R15
A = M
0;JMP
// finished return
//begin func Class1.set
(Class1.set)
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
M = M - 1
A = M
D = M
@Class1.0
M = D
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
@Class1.1
M = D
@0
D = A
@SP
A = M
M = D
@SP
M = M+1
// begin return
@LCL
D = M
@FRAME0
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
@FRAME0
M = M-1
A = M
D = M
@THAT
M = D
@FRAME0
M = M-1
A = M
D = M
@THIS
M = D
@FRAME0
M = M-1
A = M
D = M
@ARG
M = D
@FRAME0
M = M-1
A = M
D = M
@LCL
M = D
@R15
A = M
0;JMP
// finished return
//begin func Class1.get
(Class1.get)
@Class1.0
D = M
@SP
A = M
M = D
@SP
M = M+1
@Class1.1
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
@R15
A = M
0;JMP
// finished return
