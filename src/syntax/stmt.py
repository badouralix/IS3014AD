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
    stmt : NUMBER ':' ID ASSIGN aexp ';'
    """
    p[0] = CAssign(AVariable(p[3]), p[5], label=p[1])

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
    stmt : NUMBER ':' IF '(' bexp ')' '{' stmt '}'
         | NUMBER ':' IF '(' bexp ')' '{' stmt '}' ELSE '{' stmt '}'
    """
    if len(p) == 10:
        p[0] = CIf(p[5], p[8], CSkip(), label=p[1])
    elif len(p) == 14:
        p[0] = CIf(p[5], p[8], p[12], label=p[1])

def p_stmt_cwhile(p):
    """
    stmt : NUMBER ':' WHILE '(' bexp ')' '{' stmt '}'
    """
    p[0] = CWhile(p[5], p[8], label=p[1])

def p_stmt_cprint(p):
    """
    stmt : NUMBER ':' PRINT '(' aexp ')' ';'
    """
    p[0] = CPrint(p[5], label=p[1])