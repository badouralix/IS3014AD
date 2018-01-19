#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Append parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from astree.bexp import *


def p_bexp_binop(p):
    """
    bexp   : aexp EQ aexp
           | aexp NE aexp
           | aexp LT aexp
           | aexp LE aexp
           | aexp GT aexp
           | aexp GE aexp
    bterm  : bterm AND bfactor
           | bterm OR bfactor
           | bterm XOR bfactor
    """
    p[0] = BBinOp(p[2], p[1], p[3])

def p_bexp_bterm(p):
    'bexp : bterm'
    p[0] = p[1]

def p_bterm_bfactor(p):
    'bterm : bfactor'
    p[0] = p[1]

def p_bfactor(p):
    """
    bfactor : '!' bfactor
            | '(' bexp ')'
    """
    if len(p) == 3:
        p[0] = BUnOp(p[1], p[2])
    elif len(p) == 4:
        p[0] = p[2]

def p_bfactor_bool(p):
    'bfactor : BOOL'
    p[0] = BConstant(p[1])

