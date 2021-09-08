#!/usr/bin/env python3
##
## PERSONAL PROJECT, 2021
## Chess
## File description:
## main chess
##

from      sys import argv as av
from     time import sleep as lsleep
from   cClass import Game
from    enums import S, lng
from   events import evtManager
from     tool import getInt
import pygame as pg

from enums import W,B,P

def main(args):
    pg.init()
    scr = pg.display.set_mode([1200, 900])
    pg.display.set_caption("Chess")
    pg.display.set_icon(pg.image.load('assets/piecesB/bk.png'))
    font = [pg.font.Font('assets/txtL.ttf', 26),
            pg.font.Font('assets/txtB.ttf', 26),
            pg.font.Font('assets/txtB.ttf', 36)]
    noEsc = True
    game  = Game(args[0], args[1], args[2])

    while (noEsc and game.state == S.ONGOING):
        noEsc = evtManager(pg.event.get(), game)
        if (game.checkForceGameOver() != S.ONGOING) : noEsc = False
        scr.fill([50, 50, 50])
        game.display(     scr, font)
        game.mObj.display(scr, font)
        pg.display.update()
    print ("Game has ended:", game.state)
    if (game.state != S.ONGOING) : lsleep(1)

def checkIncorrectArgs(n, t, h):
    class HasNoIncrement(SyntaxError) : pass
    class InvalidTimelim(SyntaxError) : pass
    class InvalidIncrTim(SyntaxError) : pass
    class InvalidRemoves( ValueError) : pass
    class InvalidAddPiec( ValueError) : pass

    def checkHa(a):
        if (len(a) % 3) : return True
        for x in range(len(a)):
            if   (x % 3 == 0):
                if (a[x] in "PNBRQK")   : continue
                else : return True
            elif (x % 3 == 1):
                if (a[x] in "abcdefgh") : continue
                else : return True
            if     (a[x] in "12345678") : continue
            else     : return True
        return False
    def checkRemoves(r, a1, a2):
        if (r and len(r) % 2) : return True
        for x in range(len(r)):
            if   (not x % 2 and r[x] not in "abcdefgh") : return True
            elif (x % 2     and r[x] not in "12345678") : return True
        if (("e1" in r and "K" not in a1) or ("e8" in r and "K" not in a2) or
            ("e1" not in r and "K" in a1) or ("e8" not in r and "K" in a2)) : return True
        return False
    if (n and n[0] and len(n[0]) > 30) : n[0] = n[0][:29] + "." # simplify nameW
    if (n and n[1] and len(n[1]) > 30) : n[1] = n[1][:29] + "." # simplify nameB
    if (t and '+' not in t)                     : raise HasNoIncrement(t)
    if (t and getInt(t) < 1)                    : raise InvalidTimelim(t)
    if (t and getInt(t[t.find('+') + 1:]) < 0)  : raise InvalidIncrTim(t)
    if (h and checkRemoves(h[0], h[1], h[2]))   : raise InvalidRemoves(h[0])
    if (h and (checkHa(h[1]) or checkHa(h[2]))) : raise InvalidAddPiec(h[1], h[2])

def getArgs(av):
    names   = ["Magnus Carlsen", "Ian Nepomniatchi"] # white, black
    timemod = "15+10" # time+increment
    hndcp   = ["", "", ""] # ["rmv", "addW", "addB"]

    for x in range(len(hndcp)) : hndcp[x] = hndcp[x].lower()
    checkIncorrectArgs(None, None, None)
    return [names, timemod, hndcp]

if (__name__ == "__main__"):
    if ("-h" in av or "--help" in av):
        print ("")
        exit(0)
    main(getArgs(av))
