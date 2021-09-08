#!/usr/bin/env python3
##
## PERSONAL PROJECT, 2021
## Chess
## File description:
## chess game class
##

from   mClass import MovesTable
from    enums import *
from checkers import *
from     tool import genBoard, txt, getTimeIncr, pieceEaten, getFormattedTime as getFmtTime, reorder, pickPromotion
from     time import time as now
import pygame as pg

class Game:
    iBoard =   pg.image.load('assets/img/board.png')
    iPrior =   pg.image.load('assets/img/prior.png')
    iPossM =   pg.image.load('assets/img/possible.png')
    pieceB = [[pg.image.load('assets/piecesB/wp.png'),pg.image.load('assets/piecesB/wn.png'),pg.image.load('assets/piecesB/wb.png'),\
               pg.image.load('assets/piecesB/wr.png'),pg.image.load('assets/piecesB/wq.png'),pg.image.load('assets/piecesB/wk.png')],
              [pg.image.load('assets/piecesB/bp.png'),pg.image.load('assets/piecesB/bn.png'),pg.image.load('assets/piecesB/bb.png'),\
               pg.image.load('assets/piecesB/br.png'),pg.image.load('assets/piecesB/bq.png'),pg.image.load('assets/piecesB/bk.png')]]
    pieceL = [[pg.image.load('assets/piecesL/wp.png'),pg.image.load('assets/piecesL/wn.png'),pg.image.load('assets/piecesL/wb.png'),\
               pg.image.load('assets/piecesL/wr.png'),pg.image.load('assets/piecesL/wq.png'),pg.image.load('assets/piecesL/wk.png')],
              [pg.image.load('assets/piecesL/bp.png'),pg.image.load('assets/piecesL/bn.png'),pg.image.load('assets/piecesL/bb.png'),\
               pg.image.load('assets/piecesL/br.png'),pg.image.load('assets/piecesL/bq.png'),pg.image.load('assets/piecesL/bk.png')]]
    board, taken, checked = genBoard(), ["", ""], [False, False]
    clocks, incr, lastTimeClick = [0, 0], 0, now()
    mObj   = MovesTable()
    names  = []
    lang   = lng.FR
    state  = S.ONGOING

    def playMove(self, movePlayed):
        fcr = (self.mObj.held[1][1],          self.mObj.held[1][0])    # former position
        tcr = (int(ord(movePlayed[-2])) - 97, 8 - int(movePlayed[-1])) # target position
        self.board[tcr[1]][tcr[0]] = self.mObj.held[0] # place the held piece where it's played
        if (movePlayed.find('x') > 0):                 # capture repercussions
            self.taken[self.mObj.turn] += pieceEaten(self.board, movePlayed) # add to captured pieces
            self.taken[self.mObj.turn]  = reorder(self.taken[self.mObj.turn != False])
        if (movePlayed[0] == 'R' and fcr[1] in [0,7]): # castling abillity lost
            self.mObj.canKC[self.mObj.turn][1 if fcr[1] == 0 else 0] = False
        if (movePlayed[0] == 'K'):                     # castling
            if   (tcr[0] == fcr[1] + 2):
                self.board[tcr[1]][tcr[0] - 1] = B.R if self.mObj.turn else W.R
                self.board[7 if tcr[0] == 0 else 0][7] = P.E
            elif (tcr[0] == fcr[1] - 2):
                self.board[tcr[1]][tcr[0] + 1] = B.R if self.mObj.turn else W.R
                self.board[7 if tcr[0] == 0 else 0][0] = P.E
            movePlayed = "0-0" if (tcr[0] == fcr[1] + 2) else "0-0-0" if (tcr[0] == fcr[1] - 2) else movePlayed
            self.mObj.canKC[self.mObj.turn] = [False, False]
        if (movePlayed[0] >= 'a' and movePlayed[0] <= 'h' and # en passant
            movePlayed.find('x') < 0 and tcr[0] != fcr[1]):
            self.board[tcr[1] - (1 if self.mObj.turn else -1)][tcr[0]] = P.E
            self.taken[self.mObj.turn] += "P"
            movePlayed = str(chr(fcr[1] + 97)) + "x" + movePlayed + " EP"
            self.mObj.canEP = None
        if (movePlayed[0] >= 'a' and movePlayed[0] <= 'h' and # set enpassant as possible
            fcr[0] == (1 if self.mObj.held[0].value == 0x10 else 6) and
            tcr[1] == fcr[0] + (2 if self.mObj.held[0].value == 0x10 else -2)):
            self.mObj.canEP = str(movePlayed[-2]) + str(int(movePlayed[-1]) + (1 if self.mObj.held[0].value == 0x10 else -1))
        if (movePlayed[0] >= 'a' and movePlayed[0] <= 'h' and # promotion
            movePlayed[-1] == ('1' if self.mObj.turn else '8')):
            movePlayed += "=" + chr(self.mObj.prom.value)
            self.board[tcr[1]][tcr[0]] = pickPromotion(self.mObj.prom, self.mObj.turn)
        if (isChecked(self.board, self.mObj.turn)): # check and checkmate
            if (isMated(self.board, not self.mObj.turn)):
                movePlayed += "#"
                self.state = S.CKMATEW if not self.mObj.turn else S.CKMATEB
            else:
                movePlayed += "+"
            self.checked[self.mObj.turn] = True
        else:
            self.checked[self.mObj.turn] = False
        self.clocks[self.mObj.turn] += self.lastTimeClick - now() + self.incr
        self.lastTimeClick = now()
        if (self.mObj.turn) : self.mObj.moves[-1].append(movePlayed)
        else                : self.mObj.moves.append(   [movePlayed])
        self.mObj.rLast = fcr
        self.mObj.turn  = not self.mObj.turn
        return movePlayed

    def checkForceGameOver(self):
        if (self.clocks[0] == 0)                : self.state = S.OUTTIMW
        if (self.clocks[1] == 0)                : self.state = S.OUTTIMB
        if (isStalemate(self.board, self.mObj)) : self.state = S.STLMATE
        return self.state

    def displayPieces(   self, scr):
        if (self.mObj.rLast[0] >= 0) : scr.blit(self.iPrior, [50 + self.mObj.rLast[1] * 100, 50 + self.mObj.rLast[0] * 100])
        for y in range(8):
            for x in range(8):
                if (self.board[y][x] == P.E) : continue
                scr.blit(self.pieceB[self.board[y][x].value < 0x20][self.board[y][x].value % 0x10],\
                         [50 + x * 100, 50 + y * 100])
        possMoves = []                                                                             if (self.mObj.held == None)              else \
                    getLegMovesPawn(  self.mObj.held, self.board, self.mObj.turn, self.mObj.canEP) if (self.mObj.held[0].value % 0x10 == 0) else \
                    getLegMovesKnight(self.mObj.held, self.board, self.mObj.turn)                  if (self.mObj.held[0].value % 0x10 == 1) else \
                    getLegMovesBishop(self.mObj.held, self.board, self.mObj.turn)                  if (self.mObj.held[0].value % 0x10 == 2) else \
                    getLegMovesRook(  self.mObj.held, self.board, self.mObj.turn)                  if (self.mObj.held[0].value % 0x10 == 3) else \
                    getLegMovesQueen( self.mObj.held, self.board, self.mObj.turn)                  if (self.mObj.held[0].value % 0x10 == 4) else \
                    getLegMovesKing(  self.mObj.held, self.board, self.mObj.turn, self.mObj.canKC)
        for p in possMoves:
            scr.blit(self.iPossM, [50 + (int(ord(p[0])) - 97) * 100, 50 + (8 - int(p[1])) * 100])
        if (self.mObj.held): # held piece follows the cursor
            pos = pg.mouse.get_pos()
            scr.blit(self.pieceB[self.mObj.held[0].value < 0x20][self.mObj.held[0].value % 0x10], [pos[0] - 50, pos[1] - 50])
    def displayNames(    self, scr, font):
        pg.draw.rect(scr, [  0,   0,   0], [50,   7, 12 + 13 * len(self.names[1]), 36])
        pg.draw.rect(scr, [255, 255, 255], [50, 857, 12 + 13 * len(self.names[0]), 36])
        scr.blit(txt(font[1], self.names[1], [255, 255, 255]), [56,   9])
        scr.blit(txt(font[1], self.names[0], [  0,   0,   0]), [56, 859])
    def displayClocks(   self, scr, font):
        vals = [self.clocks[0], self.clocks[1]]
        vals[self.mObj.turn] += self.lastTimeClick - now()
        dispB, dispW = getFmtTime(vals[1]), getFmtTime(vals[0])
        pg.draw.rect(scr, [  0,   0,   0], [750,   7, 100, 36])
        pg.draw.rect(scr, [255, 255, 255], [750, 857, 100, 36])
        scr.blit(txt(font[2], dispB, [255, 255, 255]), [755,   5])
        scr.blit(txt(font[2], dispW, [  0,   0,   0]), [755, 855])
        if (dispW == "00.00") : self.clocks[0] = 0
        if (dispB == "00.00") : self.clocks[1] = 0
    def displayAdvantage(self, scr, font):
        for x in range(len(self.taken[0])):
            scr.blit(self.pieceL[1]["PNBRQK".find(self.taken[0][x])], [64 + len(self.names[0] * 13) + 15 * x, 858])
        for x in range(len(self.taken[1])):
            scr.blit(self.pieceL[0]["PNBRQK".find(self.taken[1][x])], [64 + len(self.names[1] * 13) + 15 * x,   8])
        adv = 0
        for x in self.taken[0] : adv += (1 if x == 'P' else 3 if x in "NB" else 5 if x == 'R' else 9)
        for x in self.taken[1] : adv -= (1 if x == 'P' else 3 if x in "NB" else 5 if x == 'R' else 9)
        if   (adv > 0) : scr.blit(txt(font[2], "+" + str(adv),     ), [80 + len(self.names[0]) * 13 + len(self.taken[0]) * 15, 855])
        elif (adv < 0) : scr.blit(txt(font[2], "+" + str(adv * -1),), [80 + len(self.names[1]) * 13 + len(self.taken[1]) * 15,   5])
    def display(         self, scr, font):
        scr.blit(self.iBoard, [50, 50])
        if (self.checked != [False, False]) : scr.blit(txt(font[2], "!", [255,0,0]), [32, 6 if self.mObj.turn else 856])
        self.displayPieces(   scr)
        self.displayNames(    scr, font)
        self.displayClocks(   scr, font)
        self.displayAdvantage(scr, font)

    def setHandicap(self, h):
        if (len(h[0])): # removing pieces
            for x in range(0, len(h[0])):
                if (not x % 2):
                    stk = h[0][x]
                    continue
                self.board[8 - int(h[0][x])][ord(stk) - 97] = P.E
        if (len(h[1])):
            0 # make white adds happen
        if (len(h[2])):
            0 # make black adds happen

    def __init__(self, names = ["White", "Black"], time = "15+10", handicap = ["","",""]):
        self.names = [names[0], names[1]]
        self.setHandicap(handicap)
        self.clocks, self.incr = getTimeIncr(time)
        print ("Time mode:     ", int(self.clocks[0] / 60), "+", self.incr)
