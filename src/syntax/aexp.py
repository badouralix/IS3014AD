#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Append parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from astree.aexp import *


def p_aexp_binop(p):
    """
    aexp   : aexp '+' aterm
           | aexp '-' aterm
    aterm  : aterm '*' afactor
           | aterm '/' afactor
           | aterm '%' afactor
           | aterm POWER afactor
    """
    p[0] = ABinOp(p[2], p[1], p[3])

def p_aexp_aterm(p):
    'aexp : aterm'
    p[0] = p[1]

def p_aterm_afactor(p):
    'aterm : afactor'
    p[0] = p[1]

def p_afactor(p):
    """
    afactor : '-' afactor
            | '(' aexp ')'
    """
    if len(p) == 3:
        p[0] = AUnOp(p[1], p[2])
    elif len(p) == 4:
        p[0] = p[2]

def p_afactor_number(p):
    'afactor : VALUE'
    p[0] = AConstant(p[1])

def p_afactor_variable(p):
    'afactor : VARIABLE'
    p[0] = AVariable(p[1])
