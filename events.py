#!/usr/bin/env python3
##
## PERSONAL PROJECT, 2021
## Chess
## File description:
## chess events handling
##

from    enums import P
from   cClass import Game
from checkers import pieceCanMove as pCanMove, isMoveLegal
from     tool import deduceMove
import pygame as pg

def revert():
    return

def resign():
    return

def setPromotion():
    return

def evtManager(event, g):
    for evt in event:
        if (evt.type == pg.QUIT or (evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE)) : return False
        if (evt.type == pg.MOUSEBUTTONUP):
            pos = pg.mouse.get_pos()
            if (g.mObj.held):
                if (pos[0] > 50 and pos[0] < 850 and pos[1] > 50 and pos[1] < 850):
                    moveToPlay = deduceMove(g.mObj.held, pos, g.board)
                else:
                    moveToPlay = None
                if (isMoveLegal(moveToPlay, g.mObj, g.board)):
                    m = g.playMove(moveToPlay)
                    print (m, end = "\t|\t" if g.mObj.turn else "\n") # logging played move in terminal
                else:
                    g.board[g.mObj.held[1][1]][g.mObj.held[1][0]] = g.mObj.held[0]
                g.mObj.held = None
        elif (evt.type == pg.MOUSEBUTTONDOWN):
            pos = pg.mouse.get_pos()
            if (pCanMove(pos, g.board, g.mObj.turn)):
                col = int((pos[0] - 50) / 100)
                row = int((pos[1] - 50) / 100)
                g.mObj.held = [g.board[row][col], (col, row)]
                g.board[row][col] = P.E
    return True