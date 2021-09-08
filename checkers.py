#!/usr/bin/env python3
##
## PERSONAL PROJECT, 2021
## Chess
## File description:
## chess checking functions
##

from  copy import deepcopy as objdup
from enums import P

def isStalemate(b, mObj):
    if (mObj.held) : return False
    vb = objdup(b) # virtualboard like in getLeg funcs
    for x in range(8): # can their king move?
        for y in range(8):
            if (b[x][y].value == (0x15 if mObj.turn else 0x25)):
                vb[x][y] = P.E
                if (len(getLegMovesKing([b[x][y], (y, x)], vb, mObj.turn))) : return False
    for x in range(8): # can any of their pieces move?
        for y in range(8):
            if (b[x][y] != P.E and int(b[x][y].value / 0x20) != mObj.turn and
                ((b[x][y].value % 0x10 == 0 and len(getLegMovesPawn(  [b[x][y], (y, x)], vb, mObj.turn))) or
                 (b[x][y].value % 0x10 == 1 and len(getLegMovesKnight([b[x][y], (y, x)], vb, mObj.turn))) or
                 (b[x][y].value % 0x10 == 2 and len(getLegMovesBishop([b[x][y], (y, x)], vb, mObj.turn))) or
                 (b[x][y].value % 0x10 == 3 and len(getLegMovesRook(  [b[x][y], (y, x)], vb, mObj.turn))) or
                 (b[x][y].value % 0x10 == 4 and len(getLegMovesQueen( [b[x][y], (y, x)], vb, mObj.turn))))):
                return False
    return True
def isCheckingPieceEatable(b, turn, x, y):
    piece = str(chr(y + 97)) + str(chr(8 - x + 48))
    for x in range(8):
        for y in range(8):
            if (b[x][y] != P.E and int(b[x][y].value / 0x20) != turn and
                ((b[x][y].value % 0x10 == 0 and piece in getLegMovesPawn(  [b[x][y], (y, x)], b, turn)) or
                 (b[x][y].value % 0x10 == 1 and piece in getLegMovesKnight([b[x][y], (y, x)], b, turn)) or
                 (b[x][y].value % 0x10 == 2 and piece in getLegMovesBishop([b[x][y], (y, x)], b, turn)) or
                 (b[x][y].value % 0x10 == 3 and piece in getLegMovesRook(  [b[x][y], (y, x)], b, turn)) or
                 (b[x][y].value % 0x10 == 4 and piece in getLegMovesQueen( [b[x][y], (y, x)], b, turn)) or
                 (b[x][y].value % 0x10 == 5 and piece in getLegMovesKing(  [b[x][y], (y, x)], b, turn)))):
                 return True
    return False
def isMated(b, turn):
    vb = objdup(b) # virtualboard like in getLeg funcs
    for x in range(8): # can their king move?
        for y in range(8):
            if (b[x][y].value == (0x15 if turn else 0x25)):
                vb[x][y] = P.E
                if (len(getLegMovesKing([b[x][y], (y, x)], vb, turn))) : return False
    menace = False
    for x in range(8): # can the checking piece(s) be eaten?
        for y in range(8):
            if (b[x][y] != P.E and int(b[x][y].value / 0x20) == turn and
                ((b[x][y].value % 0x10 == 0 and hasEnemyKing(b, getAllMovesPawn(  [b[x][y], (y, x)], b), not turn)) or
                 (b[x][y].value % 0x10 == 1 and hasEnemyKing(b, getAllMovesKnight([b[x][y], (y, x)], b), not turn)) or
                 (b[x][y].value % 0x10 == 2 and hasEnemyKing(b, getAllMovesBishop([b[x][y], (y, x)], b), not turn)) or
                 (b[x][y].value % 0x10 == 3 and hasEnemyKing(b, getAllMovesRook(  [b[x][y], (y, x)], b), not turn)) or
                 (b[x][y].value % 0x10 == 4 and hasEnemyKing(b, getAllMovesQueen( [b[x][y], (y, x)], b), not turn)) or
                 (b[x][y].value % 0x10 == 5 and hasEnemyKing(b, getAllMovesKing(  [b[x][y], (y, x)], b), not turn)))):
                if (menace)                                : return True
                if (isCheckingPieceEatable(b, turn, x, y)) : menace = True
                else                                       : return True
    return False
def hasEnemyKing(b, possMoves, turn):
    for p in possMoves:
        if (b[8 - (ord(p[1]) - 48)][ord(p[0]) - 97].value == (0x15 if not turn else 0x25)):
            return True
    return False
def isChecked(b, turn):
    for x in range(8):
        for y in range(8):
            if (b[x][y] != P.E and int(b[x][y].value / 0x20) != turn and
                ((b[x][y].value % 0x10 == 0 and hasEnemyKing(b, getAllMovesPawn(  [b[x][y], (y, x)], b), turn)) or
                 (b[x][y].value % 0x10 == 1 and hasEnemyKing(b, getAllMovesKnight([b[x][y], (y, x)], b), turn)) or
                 (b[x][y].value % 0x10 == 2 and hasEnemyKing(b, getAllMovesBishop([b[x][y], (y, x)], b), turn)) or
                 (b[x][y].value % 0x10 == 3 and hasEnemyKing(b, getAllMovesRook(  [b[x][y], (y, x)], b), turn)) or
                 (b[x][y].value % 0x10 == 4 and hasEnemyKing(b, getAllMovesQueen( [b[x][y], (y, x)], b), turn)) or
                 (b[x][y].value % 0x10 == 5 and hasEnemyKing(b, getAllMovesKing(  [b[x][y], (y, x)], b), turn)))):
                return True
    return False

def getAllMovesKing(  held, b, canKC = [[False, False], [False, False]]):
    fcr  = (held[1][1], held[1][0]) # former position
    turn = not (int(held[0].value) / 0x20)
    possMoves = []

    if (fcr[1] - 1 >= 0): #   left
        if (fcr[0] - 1 >= 0 and int(b[fcr[0] - 1][fcr[1] - 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] - 1 + 97)) + str(8 - (fcr[0] - 1)))
        if (int(b[fcr[0]][fcr[1] - 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] - 1 + 97)) + str(8 - fcr[0]))
        if (fcr[0] + 1 <  8 and int(b[fcr[0] + 1][fcr[1] - 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] - 1 + 97)) + str(8 - (fcr[0] + 1)))
    if (fcr[0] - 1 >= 0 and #   up
        int(b[fcr[0] - 1][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
        possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] - 1)))
    if (fcr[0] + 1 <  8 and # down
        int(b[fcr[0] + 1][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
        possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] + 1)))
    if (fcr[1] + 1 <  8): #  right
        if (fcr[0] - 1 >= 0 and int(b[fcr[0] - 1][fcr[1] + 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 1 + 97)) + str(8 - (fcr[0] - 1)))
        if (int(b[fcr[0]][fcr[1] + 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 1 + 97)) + str(8 - fcr[0]))
        if (fcr[0] + 1 <  8 and int(b[fcr[0] + 1][fcr[1] + 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 1 + 97)) + str(8 - (fcr[0] + 1)))
    if (canKC[turn][0] and b[fcr[0]][fcr[1] + 1] == P.E and b[fcr[0]][fcr[1] + 2] == P.E and # small castling
        int(b[fcr[0]][fcr[1] + 2].value / 0x10) != int(held[0].value / 0x10)):
        possMoves.append(str(chr(fcr[1] + 2 + 97)) + str(8 - fcr[0]))
    if (canKC[turn][1] and b[fcr[0]][fcr[1] - 1] == P.E and b[fcr[0]][fcr[1] - 2] == P.E and #   big castling
        b[fcr[0]][fcr[1] - 3] == P.E and int(b[fcr[0]][fcr[1] - 2].value / 0x10) != int(held[0].value / 0x10)):
        possMoves.append(str(chr(fcr[1] - 2 + 97)) + str(8 - fcr[0]))
    return possMoves
def getAllMovesQueen( held, b):
    return (getAllMovesBishop(held, b) + getAllMovesRook(held, b))
def getAllMovesRook(  held, b):
    fcr = (held[1][1], held[1][0]) # former position
    possMoves = []

    if (fcr[1] - 1 >= 0): #  left
        if (int(b[fcr[0]][fcr[1] - 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] - 1 + 97)) + str(8 - fcr[0]))
        if (fcr[1] - 2 >= 0):
            if (b[fcr[0]][fcr[1] - 1] == P.E and
                int(b[fcr[0]][fcr[1] - 2].value / 0x10) != int(held[0].value / 0x10)):
                possMoves.append(str(chr(fcr[1] - 2 + 97)) + str(8 - fcr[0]))
            if (fcr[1] - 3 >= 0):
                if (b[fcr[0]][fcr[1] - 1] == P.E and b[fcr[0]][fcr[1] - 2] == P.E and
                    int(b[fcr[0]][fcr[1] - 3].value / 0x10) != int(held[0].value / 0x10)):
                    possMoves.append(str(chr(fcr[1] - 3 + 97)) + str(8 - fcr[0]))
                if (fcr[1] - 4 >= 0):
                    if (b[fcr[0]][fcr[1] - 1] == P.E and b[fcr[0]][fcr[1] - 2] == P.E and b[fcr[0]][fcr[1] - 3] == P.E and
                        int(b[fcr[0]][fcr[1] - 4].value / 0x10) != int(held[0].value / 0x10)):
                        possMoves.append(str(chr(fcr[1] - 4 + 97)) + str(8 - fcr[0]))
                    if (fcr[1] - 5 >= 0):
                        if (b[fcr[0]][fcr[1] - 1] == P.E and b[fcr[0]][fcr[1] - 2] == P.E and b[fcr[0]][fcr[1] - 3] == P.E and
                            b[fcr[0]][fcr[1] - 4] == P.E and
                            int(b[fcr[0]][fcr[1] - 5].value / 0x10) != int(held[0].value / 0x10)):
                            possMoves.append(str(chr(fcr[1] - 5 + 97)) + str(8 - fcr[0]))
                        if (fcr[1] - 6 >= 0):
                            if (b[fcr[0]][fcr[1] - 1] == P.E and b[fcr[0]][fcr[1] - 2] == P.E and b[fcr[0]][fcr[1] - 3] == P.E and
                                b[fcr[0]][fcr[1] - 4] == P.E and b[fcr[0]][fcr[1] - 5] == P.E and
                                int(b[fcr[0]][fcr[1] - 6].value / 0x10) != int(held[0].value / 0x10)):
                                possMoves.append(str(chr(fcr[1] - 6 + 97)) + str(8 - fcr[0]))
                            if (fcr[1] - 7 >= 0):
                                if (b[fcr[0]][fcr[1] - 1] == P.E and b[fcr[0]][fcr[1] - 2] == P.E and b[fcr[0]][fcr[1] - 3] == P.E and
                                    b[fcr[0]][fcr[1] - 4] == P.E and b[fcr[0]][fcr[1] - 5] == P.E and b[fcr[0]][fcr[1] - 6] == P.E and
                                    int(b[fcr[0]][fcr[1] - 7].value / 0x10) != int(held[0].value / 0x10)):
                                    possMoves.append(str(chr(fcr[1] - 7 + 97)) + str(8 - fcr[0]))
    if (fcr[0] - 1 >= 0): #    up
        if (int(b[fcr[0] - 1][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] - 1)))
        if (fcr[0] - 2 >= 0):
            if (b[fcr[0] - 1][fcr[1]] == P.E and
                int(b[fcr[0] - 2][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] - 2)))
            if (fcr[0] - 3 >= 0):
                if (b[fcr[0] - 1][fcr[1]] == P.E and b[fcr[0] - 2][fcr[1]] == P.E and
                    int(b[fcr[0] - 3][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                    possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] - 3)))
                if (fcr[0] - 4 >= 0):
                    if (b[fcr[0] - 1][fcr[1]] == P.E and b[fcr[0] - 2][fcr[1]] == P.E and b[fcr[0] - 3][fcr[1]] == P.E and
                        int(b[fcr[0] - 4][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                        possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] - 4)))
                    if (fcr[0] - 5 >= 0):
                        if (b[fcr[0] - 1][fcr[1]] == P.E and b[fcr[0] - 2][fcr[1]] == P.E and b[fcr[0] - 3][fcr[1]] == P.E and
                            b[fcr[0] - 4][fcr[1]] == P.E and
                            int(b[fcr[0] - 5][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                            possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] - 5)))
                        if (fcr[0] - 6 >= 0):
                            if (b[fcr[0] - 1][fcr[1]] == P.E and b[fcr[0] - 2][fcr[1]] == P.E and b[fcr[0] - 3][fcr[1]] == P.E and
                                b[fcr[0] - 4][fcr[1]] == P.E and b[fcr[0] - 5][fcr[1]] == P.E and
                                int(b[fcr[0] - 6][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                                possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] - 6)))
                            if (fcr[0] - 7 >= 0):
                                if (b[fcr[0] - 1][fcr[1]] == P.E and b[fcr[0] - 2][fcr[1]] == P.E and b[fcr[0] - 3][fcr[1]] == P.E and
                                    b[fcr[0] - 4][fcr[1]] == P.E and b[fcr[0] - 5][fcr[1]] == P.E and b[fcr[0] - 6][fcr[1]] == P.E and
                                    int(b[fcr[0] - 7][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                                    possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] - 7)))
    if (fcr[0] + 1 <  8): #  down
        if (int(b[fcr[0] + 1][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] + 1)))
        if (fcr[0] + 2 < 8):
            if (b[fcr[0] + 1][fcr[1]] == P.E and
                int(b[fcr[0] + 2][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] + 2)))
            if (fcr[0] + 3 < 8):
                if (b[fcr[0] + 1][fcr[1]] == P.E and b[fcr[0] + 2][fcr[1]] == P.E and
                    int(b[fcr[0] + 3][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                    possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] + 3)))
                if (fcr[0] + 4 < 8):
                    if (b[fcr[0] + 1][fcr[1]] == P.E and b[fcr[0] + 2][fcr[1]] == P.E and b[fcr[0] + 3][fcr[1]] == P.E and
                        int(b[fcr[0] + 4][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                        possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] + 4)))
                    if (fcr[0] + 5 < 8):
                        if (b[fcr[0] + 1][fcr[1]] == P.E and b[fcr[0] + 2][fcr[1]] == P.E and b[fcr[0] + 3][fcr[1]] == P.E and
                            b[fcr[0] + 4][fcr[1]] == P.E and
                            int(b[fcr[0] + 5][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                            possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] + 5)))
                        if (fcr[0] + 6 < 8):
                            if (b[fcr[0] + 1][fcr[1]] == P.E and b[fcr[0] + 2][fcr[1]] == P.E and b[fcr[0] + 3][fcr[1]] == P.E and
                                b[fcr[0] + 4][fcr[1]] == P.E and b[fcr[0] + 5][fcr[1]] == P.E and
                                int(b[fcr[0] + 6][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                                possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] + 6)))
                            if (fcr[0] + 7 < 8):
                                if (b[fcr[0] + 1][fcr[1]] == P.E and b[fcr[0] + 2][fcr[1]] == P.E and b[fcr[0] + 3][fcr[1]] == P.E and
                                    b[fcr[0] + 4][fcr[1]] == P.E and b[fcr[0] + 5][fcr[1]] == P.E and b[fcr[0] + 6][fcr[1]] == P.E and
                                    int(b[fcr[0] + 7][fcr[1]].value / 0x10) != int(held[0].value / 0x10)):
                                    possMoves.append(str(chr(fcr[1] + 97)) + str(8 - (fcr[0] + 7)))
    if (fcr[1] + 1 <  8): # right
        if (int(b[fcr[0]][fcr[1] + 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 1 + 97)) + str(8 - fcr[0]))
        if (fcr[1] + 2 < 8):
            if (b[fcr[0]][fcr[1] + 1] == P.E and
                int(b[fcr[0]][fcr[1] + 2].value / 0x10) != int(held[0].value / 0x10)):
                possMoves.append(str(chr(fcr[1] + 2 + 97)) + str(8 - fcr[0]))
            if (fcr[1] + 3 < 8):
                if (b[fcr[0]][fcr[1] + 1] == P.E and b[fcr[0]][fcr[1] + 2] == P.E and
                    int(b[fcr[0]][fcr[1] + 3].value / 0x10) != int(held[0].value / 0x10)):
                    possMoves.append(str(chr(fcr[1] + 3 + 97)) + str(8 - fcr[0]))
                if (fcr[1] + 4 < 8):
                    if (b[fcr[0]][fcr[1] + 1] == P.E and b[fcr[0]][fcr[1] + 2] == P.E and b[fcr[0]][fcr[1] + 3] == P.E and
                        int(b[fcr[0]][fcr[1] + 4].value / 0x10) != int(held[0].value / 0x10)):
                        possMoves.append(str(chr(fcr[1] + 4 + 97)) + str(8 - fcr[0]))
                    if (fcr[1] + 5 < 8):
                        if (b[fcr[0]][fcr[1] + 1] == P.E and b[fcr[0]][fcr[1] + 2] == P.E and b[fcr[0]][fcr[1] + 3] == P.E and
                            b[fcr[0]][fcr[1] + 4] == P.E and
                            int(b[fcr[0]][fcr[1] + 5].value / 0x10) != int(held[0].value / 0x10)):
                            possMoves.append(str(chr(fcr[1] + 5 + 97)) + str(8 - fcr[0]))
                        if (fcr[1] + 6 < 8):
                            if (b[fcr[0]][fcr[1] + 1] == P.E and b[fcr[0]][fcr[1] + 2] == P.E and b[fcr[0]][fcr[1] + 3] == P.E and
                                b[fcr[0]][fcr[1] + 4] == P.E and b[fcr[0]][fcr[1] + 5] == P.E and
                                int(b[fcr[0]][fcr[1] + 6].value / 0x10) != int(held[0].value / 0x10)):
                                possMoves.append(str(chr(fcr[1] + 6 + 97)) + str(8 - fcr[0]))
                            if (fcr[1] + 7 < 8):
                                if (b[fcr[0]][fcr[1] + 1] == P.E and b[fcr[0]][fcr[1] + 2] == P.E and b[fcr[0]][fcr[1] + 3] == P.E and
                                    b[fcr[0]][fcr[1] + 4] == P.E and b[fcr[0]][fcr[1] + 5] == P.E and b[fcr[0]][fcr[1] + 6] == P.E and
                                    int(b[fcr[0]][fcr[1] + 7].value / 0x10) != int(held[0].value / 0x10)):
                                    possMoves.append(str(chr(fcr[1] + 7 + 97)) + str(8 - fcr[0]))
    return possMoves
def getAllMovesBishop(held, b):
    fcr = (held[1][1], held[1][0]) # former position
    possMoves = []

    if (fcr[1] - 1 >= 0): # left
        if (fcr[0] - 1 >= 0 and int(b[fcr[0] - 1][fcr[1] - 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] - 1 + 97)) + str(8 - (fcr[0] - 1))) # up
        if (fcr[0] + 1 <  8 and int(b[fcr[0] + 1][fcr[1] - 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] - 1 + 97)) + str(8 - (fcr[0] + 1))) # down
        if (fcr[1] - 2 >= 0):
            if (fcr[0] - 2 >= 0 and b[fcr[0] - 1][fcr[1] - 1] == P.E and
                int(b[fcr[0] - 2][fcr[1] - 2].value / 0x10) != int(held[0].value / 0x10)):
                possMoves.append(str(chr(fcr[1] - 2 + 97)) + str(8 - (fcr[0] - 2))) # up
            if (fcr[0] + 2 <  8 and b[fcr[0] + 1][fcr[1] - 1] == P.E and
                int(b[fcr[0] + 2][fcr[1] - 2].value / 0x10) != int(held[0].value / 0x10)):
                possMoves.append(str(chr(fcr[1] - 2 + 97)) + str(8 - (fcr[0] + 2))) # down
            if (fcr[1] - 3 >= 0):
                if (fcr[0] - 3 >= 0 and b[fcr[0] - 1][fcr[1] - 1] == P.E and b[fcr[0] - 2][fcr[1] - 2] == P.E and
                    int(b[fcr[0] - 3][fcr[1] - 3].value / 0x10) != int(held[0].value / 0x10)):
                    possMoves.append(str(chr(fcr[1] - 3 + 97)) + str(8 - (fcr[0] - 3))) # up
                if (fcr[0] + 3 <  8 and b[fcr[0] + 1][fcr[1] - 1] == P.E and b[fcr[0] + 2][fcr[1] - 2] == P.E and
                    int(b[fcr[0] + 3][fcr[1] - 3].value / 0x10) != int(held[0].value / 0x10)):
                    possMoves.append(str(chr(fcr[1] - 3 + 97)) + str(8 - (fcr[0] + 3))) # down
                if (fcr[1] - 4 >= 0):
                    if (fcr[0] - 4 >= 0 and b[fcr[0] - 1][fcr[1] - 1] == P.E and b[fcr[0] - 2][fcr[1] - 2] == P.E and
                        b[fcr[0] - 3][fcr[1] - 3] == P.E and
                        int(b[fcr[0] - 4][fcr[1] - 4].value / 0x10) != int(held[0].value / 0x10)):
                        possMoves.append(str(chr(fcr[1] - 4 + 97)) + str(8 - (fcr[0] - 4))) # up
                    if (fcr[0] + 4 <  8 and b[fcr[0] + 1][fcr[1] - 1] == P.E and b[fcr[0] + 2][fcr[1] - 2] == P.E and
                        b[fcr[0] + 3][fcr[1] - 3] == P.E and
                        int(b[fcr[0] + 4][fcr[1] - 4].value / 0x10) != int(held[0].value / 0x10)):
                        possMoves.append(str(chr(fcr[1] - 4 + 97)) + str(8 - (fcr[0] + 4))) # down
                    if (fcr[1] - 5 >= 0):
                        if (fcr[0] - 5 >= 0 and b[fcr[0] - 1][fcr[1] - 1] == P.E and b[fcr[0] - 2][fcr[1] - 2] == P.E and
                            b[fcr[0] - 3][fcr[1] - 3] == P.E and b[fcr[0] - 4][fcr[1] - 4] == P.E and
                            int(b[fcr[0] - 5][fcr[1] - 5].value / 0x10) != int(held[0].value / 0x10)):
                            possMoves.append(str(chr(fcr[1] - 5 + 97)) + str(8 - (fcr[0] - 5))) # up
                        if (fcr[0] + 5 < 8 and b[fcr[0] + 1][fcr[1] - 1] == P.E and b[fcr[0] + 2][fcr[1] - 2] == P.E and
                            b[fcr[0] + 3][fcr[1] - 3] == P.E and b[fcr[0] + 4][fcr[1] - 4] == P.E and
                            int(b[fcr[0] + 5][fcr[1] - 5].value / 0x10) != int(held[0].value / 0x10)):
                            possMoves.append(str(chr(fcr[1] - 5 + 97)) + str(8 - (fcr[0] + 5))) # down
                        if (fcr[1] - 6 >= 0):
                            if (fcr[0] - 6 >= 0 and b[fcr[0] - 1][fcr[1] - 1] == P.E and b[fcr[0] - 2][fcr[1] - 2] == P.E and
                                b[fcr[0] - 3][fcr[1] - 3] == P.E and b[fcr[0] - 4][fcr[1] - 4] == P.E and b[fcr[0] - 5][fcr[1] - 5] == P.E and
                                int(b[fcr[0] - 6][fcr[1] - 6].value / 0x10) != int(held[0].value / 0x10)):
                                possMoves.append(str(chr(fcr[1] - 6 + 97)) + str(8 - (fcr[0] - 6))) # up
                            if (fcr[0] + 6 <  8 and b[fcr[0] + 1][fcr[1] - 1] == P.E and b[fcr[0] + 2][fcr[1] - 2] == P.E and
                                b[fcr[0] + 3][fcr[1] - 3] == P.E and b[fcr[0] + 4][fcr[1] - 4] == P.E and b[fcr[0] + 5][fcr[1] - 5] == P.E and
                                int(b[fcr[0] + 6][fcr[1] - 6].value / 0x10) != int(held[0].value / 0x10)):
                                possMoves.append(str(chr(fcr[1] - 6 + 97)) + str(8 - (fcr[0] + 6))) # down
                            if (fcr[1] - 7 >= 0):
                                if (fcr[0] - 7 >= 0 and b[fcr[0] - 1][fcr[1] - 1] == P.E and b[fcr[0] - 2][fcr[1] - 2] == P.E and
                                    b[fcr[0] - 3][fcr[1] - 3] == P.E and b[fcr[0] - 4][fcr[1] - 4] == P.E and
                                    b[fcr[0] - 5][fcr[1] - 5] == P.E and b[fcr[0] - 6][fcr[1] - 6] == P.E and
                                    int(b[fcr[0] - 7][fcr[1] - 7].value / 0x10) != int(held[0].value / 0x10)):
                                    possMoves.append(str(chr(fcr[1] - 7 + 97)) + str(8 - (fcr[0] - 7))) # up
                                if (fcr[0] + 7 <  8 and b[fcr[0] + 1][fcr[1] - 1] == P.E and b[fcr[0] + 2][fcr[1] - 2] == P.E and
                                    b[fcr[0] + 3][fcr[1] - 3] == P.E and b[fcr[0] + 4][fcr[1] - 4] == P.E and
                                    b[fcr[0] + 5][fcr[1] - 5] == P.E and b[fcr[0] + 6][fcr[1] - 6] == P.E and
                                    int(b[fcr[0] + 7][fcr[1] - 7].value / 0x10) != int(held[0].value / 0x10)):
                                    possMoves.append(str(chr(fcr[1] - 7 + 97)) + str(8 - (fcr[0] + 7))) # down
    if (fcr[1] + 1 <  8): # right
        if (fcr[0] - 1 >= 0 and int(b[fcr[0] - 1][fcr[1] + 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 1 + 97)) + str(8 - (fcr[0] - 1))) # up
        if (fcr[0] + 1 <  8 and int(b[fcr[0] + 1][fcr[1] + 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 1 + 97)) + str(8 - (fcr[0] + 1))) # down
        if (fcr[1] + 2 <  8):
            if (fcr[0] - 2 >= 0 and b[fcr[0] - 1][fcr[1] + 1] == P.E and
                int(b[fcr[0] - 2][fcr[1] + 2].value / 0x10) != int(held[0].value / 0x10)):
                possMoves.append(str(chr(fcr[1] + 2 + 97)) + str(8 - (fcr[0] - 2))) # up
            if (fcr[0] + 2 <  8 and b[fcr[0] + 1][fcr[1] + 1] == P.E and
                int(b[fcr[0] + 2][fcr[1] + 2].value / 0x10) != int(held[0].value / 0x10)):
                possMoves.append(str(chr(fcr[1] + 2 + 97)) + str(8 - (fcr[0] + 2))) # down
            if (fcr[1] + 3 <  8):
                if (fcr[0] - 3 >= 0 and b[fcr[0] - 1][fcr[1] + 1] == P.E and b[fcr[0] - 2][fcr[1] + 2] == P.E and
                    int(b[fcr[0] - 3][fcr[1] + 3].value / 0x10) != int(held[0].value / 0x10)):
                    possMoves.append(str(chr(fcr[1] + 3 + 97)) + str(8 - (fcr[0] - 3))) # up
                if (fcr[0] + 3 <  8 and b[fcr[0] + 1][fcr[1] + 1] == P.E and b[fcr[0] + 2][fcr[1] + 2] == P.E and
                    int(b[fcr[0] + 3][fcr[1] + 3].value / 0x10) != int(held[0].value / 0x10)):
                    possMoves.append(str(chr(fcr[1] + 3 + 97)) + str(8 - (fcr[0] + 3))) # down
                if (fcr[1] + 4 <  8):
                    if (fcr[0] - 4 >= 0 and b[fcr[0] - 1][fcr[1] + 1] == P.E and b[fcr[0] - 2][fcr[1] + 2] == P.E and
                        b[fcr[0] - 3][fcr[1] + 3] == P.E and
                        int(b[fcr[0] - 4][fcr[1] + 4].value / 0x10) != int(held[0].value / 0x10)):
                        possMoves.append(str(chr(fcr[1] + 4 + 97)) + str(8 - (fcr[0] - 4))) # up
                    if (fcr[0] + 4 <  8 and b[fcr[0] + 1][fcr[1] + 1] == P.E and b[fcr[0] + 2][fcr[1] + 2] == P.E and
                        b[fcr[0] + 3][fcr[1] + 3] == P.E and
                        int(b[fcr[0] + 4][fcr[1] + 4].value / 0x10) != int(held[0].value / 0x10)):
                        possMoves.append(str(chr(fcr[1] + 4 + 97)) + str(8 - (fcr[0] + 4))) # down
                    if (fcr[1] + 5 <  8):
                        if (fcr[0] - 5 >= 0 and b[fcr[0] - 1][fcr[1] + 1] == P.E and b[fcr[0] - 2][fcr[1] + 2] == P.E and
                            b[fcr[0] - 3][fcr[1] + 3] == P.E and b[fcr[0] - 4][fcr[1] + 4] == P.E and
                            int(b[fcr[0] - 5][fcr[1] + 5].value / 0x10) != int(held[0].value / 0x10)):
                            possMoves.append(str(chr(fcr[1] + 5 + 97)) + str(8 - (fcr[0] - 5))) # up
                        if (fcr[0] + 5 < 8 and b[fcr[0] + 1][fcr[1] + 1] == P.E and b[fcr[0] + 2][fcr[1] + 2] == P.E and
                            b[fcr[0] + 3][fcr[1] + 3] == P.E and b[fcr[0] + 4][fcr[1] + 4] == P.E and
                            int(b[fcr[0] + 5][fcr[1] + 5].value / 0x10) != int(held[0].value / 0x10)):
                            possMoves.append(str(chr(fcr[1] + 5 + 97)) + str(8 - (fcr[0] + 5))) # down
                        if (fcr[1] + 6 <  8):
                            if (fcr[0] - 6 >= 0 and b[fcr[0] - 1][fcr[1] + 1] == P.E and b[fcr[0] - 2][fcr[1] + 2] == P.E and
                                b[fcr[0] - 3][fcr[1] + 3] == P.E and b[fcr[0] - 4][fcr[1] + 4] == P.E and b[fcr[0] - 5][fcr[1] + 5] == P.E and
                                int(b[fcr[0] - 6][fcr[1] + 6].value / 0x10) != int(held[0].value / 0x10)):
                                possMoves.append(str(chr(fcr[1] + 6 + 97)) + str(8 - (fcr[0] - 6))) # up
                            if (fcr[0] + 6 <  8 and b[fcr[0] + 1][fcr[1] + 1] == P.E and b[fcr[0] + 2][fcr[1] + 2] == P.E and
                                b[fcr[0] + 3][fcr[1] + 3] == P.E and b[fcr[0] + 4][fcr[1] + 4] == P.E and b[fcr[0] + 5][fcr[1] + 5] == P.E and
                                int(b[fcr[0] + 6][fcr[1] + 6].value / 0x10) != int(held[0].value / 0x10)):
                                possMoves.append(str(chr(fcr[1] + 6 + 97)) + str(8 - (fcr[0] + 6))) # down
                            if (fcr[1] + 7 <  8):
                                if (fcr[0] - 7 >= 0 and b[fcr[0] - 1][fcr[1] + 1] == P.E and b[fcr[0] - 2][fcr[1] + 2] == P.E and
                                    b[fcr[0] - 3][fcr[1] + 3] == P.E and b[fcr[0] - 4][fcr[1] + 4] == P.E and
                                    b[fcr[0] - 5][fcr[1] + 5] == P.E and b[fcr[0] - 6][fcr[1] + 6] == P.E and
                                    int(b[fcr[0] - 7][fcr[1] + 7].value / 0x10) != int(held[0].value / 0x10)):
                                    possMoves.append(str(chr(fcr[1] + 7 + 97)) + str(8 - (fcr[0] - 7))) # up
                                if (fcr[0] + 7 <  8 and b[fcr[0] + 1][fcr[1] + 1] == P.E and b[fcr[0] + 2][fcr[1] + 2] == P.E and
                                    b[fcr[0] + 3][fcr[1] + 3] == P.E and b[fcr[0] + 4][fcr[1] + 4] == P.E and
                                    b[fcr[0] + 5][fcr[1] + 5] == P.E and b[fcr[0] + 6][fcr[1] + 6] == P.E and
                                    int(b[fcr[0] + 7][fcr[1] + 7].value / 0x10) != int(held[0].value / 0x10)):
                                    possMoves.append(str(chr(fcr[1] + 7 + 97)) + str(8 - (fcr[0] + 7))) # down
    return possMoves
def getAllMovesKnight(held, b):
    fcr = (held[1][1], held[1][0]) # former position
    possMoves = []

    if (fcr[1] - 2 >= 0): # max left
        if (fcr[0] - 1 >= 0 and int(b[fcr[0] - 1][fcr[1] - 2].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] - 2 + 97)) + str(8 - (fcr[0] - 1))) # up
        if (fcr[0] + 1 <  8 and int(b[fcr[0] + 1][fcr[1] - 2].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] - 2 + 97)) + str(8 - (fcr[0] + 1))) # down
    if (fcr[1] - 1 >= 0): # min left
        if (fcr[0] - 2 >= 0 and int(b[fcr[0] - 2][fcr[1] - 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] - 1 + 97)) + str(8 - (fcr[0] - 2))) # up
        if (fcr[0] + 2 <  8 and int(b[fcr[0] + 2][fcr[1] - 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] - 1 + 97)) + str(8 - (fcr[0] + 2))) # down
    if (fcr[1] + 1 <  8): # min right
        if (fcr[0] - 2 >= 0 and int(b[fcr[0] - 2][fcr[1] + 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 1 + 97)) + str(8 - (fcr[0] - 2))) # up
        if (fcr[0] + 2 <  8 and int(b[fcr[0] + 2][fcr[1] + 1].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 1 + 97)) + str(8 - (fcr[0] + 2))) # down
    if (fcr[1] + 2 <  8): # max right
        if (fcr[0] - 1 >= 0 and int(b[fcr[0] - 1][fcr[1] + 2].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 2 + 97)) + str(8 - (fcr[0] - 1))) # up
        if (fcr[0] + 1 <  8 and int(b[fcr[0] + 1][fcr[1] + 2].value / 0x10) != int(held[0].value / 0x10)):
            possMoves.append(str(chr(fcr[1] + 2 + 97)) + str(8 - (fcr[0] + 1))) # down
    return possMoves
def getAllMovesPawn(  held, b, canEP = None):
    fcr = (held[1][1], held[1][0]) # former position
    if (canEP) : ecr = (int(ord(canEP[0])) - 97, 8 - int(canEP[1])) # en passant possible here
    possMoves = []

    if (fcr[0]   + (1 if held[0].value == 0x10 else -1) in [0,1,2,3,4,5,6,7] and # +1
        b[fcr[0] + (1 if held[0].value == 0x10 else -1)][fcr[1]] == P.E):
        possMoves.append(str(chr(fcr[1] + 97)) +
                         str(chr(8 - fcr[0] + (1 if held[0].value == 0x20 else -1) + 48)))
    if (fcr[0]   + (2 if held[0].value == 0x10 else -2) in       [3,4]       and # +2
        fcr[0]  == (1 if held[0].value == 0x10 else  6) and
        b[fcr[0] + (1 if held[0].value == 0x10 else -1)][fcr[1]] == P.E and
        b[fcr[0] + (2 if held[0].value == 0x10 else -2)][fcr[1]] == P.E):
        possMoves.append(str(chr(fcr[1] + 97)) +
                         str(chr(8 - fcr[0] + (2 if held[0].value == 0x20 else -2) + 48)))
    if (fcr[1] - 1 >= 0 and fcr[0] not in [0, 7] and # x left
        b[fcr[0] + (1 if held[0].value == 0x10 else -1)][fcr[1] - 1] != P.E and
        int(b[fcr[0] + (1 if held[0].value == 0x10 else -1)][fcr[1] - 1].value / 0x10) != int(held[0].value / 0x10)):
        possMoves.append(str(chr(fcr[1] - 1 + 97)) +
                         str(chr(8 - fcr[0] + (1 if held[0].value == 0x20 else -1) + 48)))
    if (fcr[1] + 1 <  8 and fcr[0] not in [0, 7] and # x right
        b[fcr[0] + (1 if held[0].value == 0x10 else -1)][fcr[1] + 1] != P.E and
        int(b[fcr[0] + (1 if held[0].value == 0x10 else -1)][fcr[1] + 1].value / 0x10) != int(held[0].value / 0x10)):
        possMoves.append(str(chr(fcr[1] + 1 + 97)) +
                         str(chr(8 - fcr[0] + (1 if held[0].value == 0x20 else -1) + 48)))
    if (canEP and fcr[0] == (4 if held[0].value == 0x10 else 3)): # en passant
        if ((ecr[1] == 2 and fcr[0] == 3 and (fcr[1] == ecr[0] - 1 or fcr[1] == ecr[0] + 1)) or
            (ecr[1] == 5 and fcr[0] == 4 and (fcr[1] == ecr[0] - 1 or fcr[1] == ecr[0] + 1))):
            possMoves.append(canEP)
    # playMove() will decide if the pawn we're moving can be en passant--ed
    return possMoves

def getLegMovesKing(  held, b, turn, canKC = [[False, False], [False, False]]):
    allMoves = getAllMovesKing(held, b, canKC)
    legMoves = []

    for p in allMoves:
        virtualBoard = objdup(b)
        virtualBoard[8 - int(p[1])][int(ord(p[0])) - 97] = held[0]
        if (not isChecked(virtualBoard, not turn)) : legMoves.append(p)
    return legMoves
def getLegMovesQueen( held, b, turn):
    allMoves = getAllMovesQueen(held, b)
    legMoves = []

    for p in allMoves:
        virtualBoard = objdup(b)
        virtualBoard[8 - int(p[1])][int(ord(p[0])) - 97] = held[0]
        if (not isChecked(virtualBoard, not turn)) : legMoves.append(p)
    return legMoves
def getLegMovesRook(  held, b, turn):
    allMoves = getAllMovesRook(held, b)
    legMoves = []

    for p in allMoves:
        virtualBoard = objdup(b)
        virtualBoard[8 - int(p[1])][int(ord(p[0])) - 97] = held[0]
        if (not isChecked(virtualBoard, not turn)) : legMoves.append(p)
    return legMoves
def getLegMovesBishop(held, b, turn):
    allMoves = getAllMovesBishop(held, b)
    legMoves = []

    for p in allMoves:
        virtualBoard = objdup(b)
        virtualBoard[8 - int(p[1])][int(ord(p[0])) - 97] = held[0]
        if (not isChecked(virtualBoard, not turn)) : legMoves.append(p)
    return legMoves
def getLegMovesKnight(held, b, turn):
    allMoves = getAllMovesKnight(held, b)
    legMoves = []

    for p in allMoves:
        virtualBoard = objdup(b)
        virtualBoard[8 - int(p[1])][int(ord(p[0])) - 97] = held[0]
        if (not isChecked(virtualBoard, not turn)) : legMoves.append(p)
    return legMoves
def getLegMovesPawn(  held, b, turn, canEP = None):
    allMoves = getAllMovesPawn(held, b, canEP)
    legMoves = []

    for p in allMoves:
        virtualBoard = objdup(b)
        virtualBoard[8 - int(p[1])][int(ord(p[0])) - 97] = held[0]
        if (not isChecked(virtualBoard, not turn)) : legMoves.append(p)
    return legMoves

def isMoveLegal(move, mObj, board):
    if   (move == None) : return False
    if   (move[0] >= 'a' and move[0] <= 'h') : possMoves = getLegMovesPawn(  mObj.held, board, mObj.turn, mObj.canEP)
    elif (move[0] == 'N')                    : possMoves = getLegMovesKnight(mObj.held, board, mObj.turn)
    elif (move[0] == 'B')                    : possMoves = getLegMovesBishop(mObj.held, board, mObj.turn)
    elif (move[0] == 'R')                    : possMoves = getLegMovesRook(  mObj.held, board, mObj.turn)
    elif (move[0] == 'Q')                    : possMoves = getLegMovesQueen( mObj.held, board, mObj.turn)
    elif (move[0] == 'K')                    : possMoves = getLegMovesKing(  mObj.held, board, mObj.turn, mObj.canKC)
    else                                     : print (move, "is illegal!")
    return move[-2:] in possMoves

def pieceCanMove(pos, board, turn):
    if (pos[0] < 50 or pos[0] > 850 or pos[1] < 50 or pos[1] > 850) : return False
    col = int((pos[0] - 50) / 100)
    row = int((pos[1] - 50) / 100)
    return (board[row][col] != P.E and
            ((board[row][col].value >= 0x20 and not turn) or
             (board[row][col].value <  0x20 and turn)))
