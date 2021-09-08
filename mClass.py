#!/usr/bin/env python3
##
## PERSONAL PROJECT, 2021
## Chess
## File description:
## chess moves class
##

from    enums import P
from     tool import txt
import pygame as pg

class MovesTable():
    moves = []
    mLast = []       # last 36 moves
    rLast = (-1, -1) # former position of last move
    prom  = P.Q      # promotion to Queen by default
    canKC = [[True, True], [True, True]] # can W/B king castle (small, king)
    canEP = None     # if enpassant possible: "e6"
    held  = None     # if held: [piece, oldcol, oldrow]
    turn  = False    # White's turn by default

    def dispPromotion(self, scr, font):
        pg.draw.rect(scr, [150, 0, 0], [ 876, 7, 65, 36])
        pg.draw.rect(scr, [150, 0, 0], [ 955, 7, 65, 36])
        pg.draw.rect(scr, [150, 0, 0], [1032, 7, 65, 36])
        pg.draw.rect(scr, [0, 200, 0], [1109, 7, 65, 36])
        scr.blit(txt(font[2], "N"),    [ 900, 5])
        scr.blit(txt(font[2], "B"),    [ 978, 5])
        scr.blit(txt(font[2], "R"),    [1053, 5])
        scr.blit(txt(font[2], "Q"),    [1131, 5])
        return
    def dispLastMove( self, scr, font):
        pg.draw.rect(scr, [64, 64, 64], [875,  50, 300,  32])
        if (not len(self.moves))     : return
        if (len(self.moves[-1]) < 2) : movePlayed = "White played " + self.moves[-1][0]
        else                         : movePlayed = "Black played " + self.moves[-1][1]
        scr.blit(txt(font[1], movePlayed,
                [255, 255, 255] if movePlayed[0] == 'W' else [0, 0, 0]), [1025 - 6.5 * len(movePlayed), 50])
    def dispAllMoves( self, scr, font):
        pg.draw.rect(scr, [64, 64, 64], [875, 100, 300, 750])
        self.mLast = self.moves[self.moves.__len__() - 36:] if self.moves.__len__() > 36 else self.moves
        nthMoves = self.moves.__len__() - 36
        nthMoves = 1 if nthMoves < 0 else nthMoves
        for x in range(len(self.mLast)):
            scr.blit(txt(font[0], (" " if nthMoves + x < 10 else "") +
                         str(nthMoves + x) + ". " + self.mLast[x][0],
                         [255, 255, 255]), [884, 110 + x * 20])
            if (len(self.mLast[x]) == 2):
                scr.blit(txt(font[0], self.mLast[x][1], [0, 0, 0]), [1049, 110 + x * 20])
    def dispResign(   self, scr, font):
        pg.draw.rect(scr, [99, 99, 99],  [ 875, 857, 100, 36])
        pg.draw.rect(scr, [99, 99, 99],  [ 990, 857, 185, 36])
        scr.blit(txt(font[1], "Revert"), [ 925 - len("Revert") * 6.5, 858])
        scr.blit(txt(font[1], "Resign"), [1082 - len("Resign") * 6.5, 858])
    def display(      self, scr, font):
        self.dispPromotion( scr, font)
        self.dispLastMove(  scr, font)
        self.dispAllMoves(  scr, font)
        self.dispResign(    scr, font)
