#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Append parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from astree.aexp import *
from astree.com import *


# def p_stmt_cskip(p):
#     """
#     stmt :
#     """
#     p[0] = CSkip()

def p_stmt_cassign(p):
    """
    stmt : ID ASSIGN aexp ';'
    """
    p[0] = CAssign(AVariable(p[1]), p[3])

def p_stmt_csequence(p):
    """
    stmt : stmt stmt
    """
    if isinstance(p[2], CSequence):
        p[0] = CSequence(p[1], *p[2].children)
    else:
        p[0] = CSequence(p[1], p[2])

def p_stmt_cif(p):
    """
    stmt : IF '(' bexp ')' '{' stmt '}'
         | IF '(' bexp ')' '{' stmt '}' ELSE '{' stmt '}'
    """
    if len(p) == 8:
        p[0] = CIf(p[3], p[6], CSkip())
    elif len(p) == 12:
        p[0] = CIf(p[3], p[6], p[10])

def p_stmt_cwhile(p):
    """
    stmt : WHILE '(' bexp ')' '{' stmt '}'
    """
    p[0] = CWhile(p[3], p[6])
