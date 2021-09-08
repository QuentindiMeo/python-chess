#!/usr/bin/env python3
##
## PERSONAL PROJECT, 2021
## Chess
## File description:
## chess enums
##

from enum import Enum

class S(Enum): # State of the game
    ONGOING = 0
    STLMATE = 1
    CKMATEW = 2
    CKMATEB = 3
    OUTTIMW = 4
    OUTTIMB = 5
    RESIGNW = 6
    RESIGNB = 7

class lng(Enum):
    FR = 0
    EN = 1

class B(Enum): # Black's pieces
    P = 0x10 # pawn
    N = 0x11 # knight
    B = 0x12 # bishop
    R = 0x13 # rook
    Q = 0x14 # queen
    K = 0x15 # king

class W(Enum): # White's pieces
    P = 0x20 # pawn
    N = 0x21 # knight
    B = 0x22 # bishop
    R = 0x23 # rook
    Q = 0x24 # queen
    K = 0x25 # king

class P(Enum):
    E = 0x00 # empty square
    N = ord('N') # promotion knight
    B = ord('B') # promotion bishop
    R = ord('R') # promotion rook
    Q = ord('Q') # promotion queen
