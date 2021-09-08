#!/usr/bin/env python3
##
## PERSONAL PROJECT, 2021
## Chess
## File description:
## chess tool functions
##

from enums import *

def pickPromotion(prom, turn):
    if   (prom == P.N) : return B.N if turn else W.N
    elif (prom == P.B) : return B.B if turn else W.B
    elif (prom == P.R) : return B.R if turn else W.R
    elif (prom == P.Q) : return B.Q if turn else W.Q
    return P.E

def deduceMove(held, pos, board):
    mov = ""
    if   (held[0].value % 0x10 == 1)    : mov += 'N'
    elif (held[0].value % 0x10 == 2)    : mov += 'B'
    elif (held[0].value % 0x10 == 3)    : mov += 'R'
    elif (held[0].value % 0x10 == 4)    : mov += 'Q'
    elif (held[0].value % 0x10 == 5)    : mov += 'K'
    nPos = (int((pos[0] - 50) / 100), 7 - int((pos[1] - 50) / 100))
    if (board[7 - nPos[1]][nPos[0]] != P.E):
        if (not held[0].value % 0x10) : mov += str(chr(held[1][0] + 97))
        mov += 'x'
    mov += str(chr(nPos[0] + 97)) + str(chr(nPos[1] + 49))
    return mov

def reorder(s):
    p = [0,0,0,0,0]
    for x in s:
        if   (x == 'P') : p[0] += 1
        elif (x == 'N') : p[1] += 1
        elif (x == 'B') : p[2] += 1
        elif (x == 'R') : p[3] += 1
        elif (x == 'Q') : p[4] += 1
    return 'Q' * p[4] + 'R' * p[3] + 'B' * p[2] + 'N' * p[1] + 'P' * p[0]

def pieceEaten(board, move):
    piece = board[8 - int(move[-1])][ord(move[-2]) - 97]
    p     = piece.value % 0x10
    return ("P" if p == 0 else "N" if p == 1 else "B" if p == 2 else "R" if p == 3 else "Q")

def getFormattedTime(t):
    if   (t <= 0):
        return "00.00"
    elif (t < 10): # < 10s, displays hundreds
        return '0' + str(int(t)) + '.' +\
                ('0' if int(t * 100 % 100) < 10 else "") + str(int(t * 100 % 100))
    else:
        return ('0' if int(t) < 600 else "") + str(int(t / 60))  + ':' +\
                ('0' if t % 60 < 10 else "") + str(int(t % 60))

def getTimeIncr(t):
    if (not len(t))   : return (0, 0)
    if ('+' not in t) : return (int(t), 0)
    return [int(t[:t.find("+")]) * 60] * 2, int(t[t.find("+"):])

def genBoard(handicap = ""):
    return [[B.R, B.N, B.B, B.Q, B.K, B.B, B.N, B.R],
            [B.P, B.P, B.P, B.P, B.P, B.P, B.P, B.P],
            [P.E, P.E, P.E, P.E, P.E, P.E, P.E, P.E],
            [P.E, P.E, P.E, P.E, P.E, P.E, P.E, P.E],
            [P.E, P.E, P.E, P.E, P.E, P.E, P.E, P.E],
            [P.E, P.E, P.E, P.E, P.E, P.E, P.E, P.E],
            [W.P, W.P, W.P, W.P, W.P, W.P, W.P, W.P],
            [W.R, W.N, W.B, W.Q, W.K, W.B, W.N, W.R]]

def txt(font, msg, color = [255, 255, 255]):
    return font.render(msg, True, color)

def getInt(s):
    if (not len(s)) : return 0
    if (s[0] != '-' and (s[0] < '0' or s[0] > '9')) : return -1
    if (s[0] == '-' and (s[1] < '0' or s[1] > '9')) : return -1
    nb = s[0 if s[0] != '-' else 1 : s.find('+')]
    for x in range(len(nb)):
        if (nb[x] < '0' or nb[x] > '9') : return -1
    return ((1 if s[0] != '-' else -1) * int(nb))