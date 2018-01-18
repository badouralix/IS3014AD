#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Append parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from astree.aexp import *


def p_aexp_binop(p):
    '''
    aexp   : aexp PLUS aterm
           | aexp MINUS aterm
    aterm  : aterm TIMES afactor
           | aterm DIVIDE afactor
           | aterm MODULO afactor
           | aterm POWER afactor
    '''
    p[0] = ABinOp(p[2], p[1], p[3])

def p_aexp_aterm(p):
    'aexp : aterm'
    p[0] = p[1]

def p_aterm_afactor(p):
    'aterm : afactor'
    p[0] = p[1]

def p_afactor_anum(p):
    'afactor : NUMBER'
    p[0] = AConstant(p[1])

def p_afactor_aexpr(p):
    'afactor : LPAREN aexp RPAREN'
    p[0] = p[2]
