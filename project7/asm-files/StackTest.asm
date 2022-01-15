// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQTRUE1
D;JEQ
@SP
A=M-1
M=0
@ENDIF1
0;JMP
(EQTRUE1)
@SP
A=M-1
M=-1
(ENDIF1)
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQTRUE2
D;JEQ
@SP
A=M-1
M=0
@ENDIF2
0;JMP
(EQTRUE2)
@SP
A=M-1
M=-1
(ENDIF2)
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQTRUE3
D;JEQ
@SP
A=M-1
M=0
@ENDIF3
0;JMP
(EQTRUE3)
@SP
A=M-1
M=-1
(ENDIF3)
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LTTRUE4
D;JLT
@SP
A=M-1
M=0
@ENDIF4
0;JMP
(LTTRUE4)
@SP
A=M-1
M=-1
(ENDIF4)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LTTRUE5
D;JLT
@SP
A=M-1
M=0
@ENDIF5
0;JMP
(LTTRUE5)
@SP
A=M-1
M=-1
(ENDIF5)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LTTRUE6
D;JLT
@SP
A=M-1
M=0
@ENDIF6
0;JMP
(LTTRUE6)
@SP
A=M-1
M=-1
(ENDIF6)
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GTTRUE7
D;JGT
@SP
A=M-1
M=0
@ENDIF7
0;JMP
(GTTRUE7)
@SP
A=M-1
M=-1
(ENDIF7)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GTTRUE8
D;JGT
@SP
A=M-1
M=0
@ENDIF8
0;JMP
(GTTRUE8)
@SP
A=M-1
M=-1
(ENDIF8)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GTTRUE9
D;JGT
@SP
A=M-1
M=0
@ENDIF9
0;JMP
(GTTRUE9)
@SP
A=M-1
M=-1
(ENDIF9)
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
D=D+M
M=D
// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=D
// neg
@SP
A=M-1
M=-M
// and
@SP
AM=M-1
D=M
A=A-1
D=D&M
M=D
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
AM=M-1
D=M
A=A-1
D=D|M
M=D
// not
@SP
A=M-1
M=!M
