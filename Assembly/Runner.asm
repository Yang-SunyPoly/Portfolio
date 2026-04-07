.const Test_Func                0x9000
.const Bot_Health               0x9001
.const Bot_Mode                 0x9002
.const Bot_Team                 0x9003
.const Bot_Pos_X                0x9004
.const Bot_Pos_Y                0x9005
.const Bot_Letter               0x9006
.const Bot_Damage               0x9007
.const Bot_Hurt                 0x9008
.const Team_Cnt                 0x9009
.const Enemy_Cnt                0x9010
.const Movement                 0x9011
.const RAND                     0x8010
.const Death                    0x9012
.const Stuck                    0x9013


    set rA, 100
    str [Bot_Health], rA
    set rA, 1
    str [Bot_Team], rA
    set rA, 1
    str [Bot_Mode], rA
    lod rB, [RAND]
    mod rB, 200
    set rA, 500
    sub rA, rB
    str [Bot_Pos_X], rA
    set rA, 200
    str [Bot_Pos_Y], rA

!main
    str [Movement], SP
    lod rA, [Death]
    cmp rA, 1
    je !Death
    lod rA, [Stuck]
    cmp rA, 1
    je !Death
    jmp !main

!Death
    lod rB, [RAND]
    mod rB, 1000
    str [Bot_Pos_X], rB
    lod rB, [RAND]
    mod rB, 1000
    str [Bot_Pos_Y], rB
    set rB, 100
    str [Bot_Health], rB
    jmp !main