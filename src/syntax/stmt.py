#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Append parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from astree.aexp import *
from astree.stmt import *


# def p_stmt_sskip(p):
#     """
#     stmt :
#     """
#     p[0] = SSkip()

def p_stmt_sassign(p):
    """
    stmt : NUMBER ':' ID ASSIGN aexp ';'
    """
    p[0] = SAssign(AVariable(p[3]), p[5], label=p[1])

def p_stmt_ssequence(p):
    """
    stmt : stmt stmt
    """
    if isinstance(p[2], SSequence):
        p[0] = SSequence(p[1], *p[2].children)
    else:
        p[0] = SSequence(p[1], p[2])

def p_stmt_sif(p):
    """
    stmt : NUMBER ':' IF '(' bexp ')' '{' stmt '}'
         | NUMBER ':' IF '(' bexp ')' '{' stmt '}' ELSE '{' stmt '}'
    """
    if len(p) == 10:
        p[0] = SIf(p[5], p[8], SSkip(), label=p[1])
    elif len(p) == 14:
        p[0] = SIf(p[5], p[8], p[12], label=p[1])

def p_stmt_swhile(p):
    """
    stmt : NUMBER ':' WHILE '(' bexp ')' '{' stmt '}'
    """
    p[0] = SWhile(p[5], p[8], label=p[1])

def p_stmt_sprint(p):
    """
    stmt : NUMBER ':' PRINT '(' aexp ')' ';'
    """
    p[0] = SPrint(p[5], label=p[1])