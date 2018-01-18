#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ply.yacc as yacc

# Append parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# Get the token map from the lexer.  This is required.
from utils.lexer import tokens

from astree.aexp import *

def p_expression_plus(p):
    '''
    expression : expression PLUS term
               | expression MINUS term
    term       : term TIMES factor
               | term DIVIDE factor
               | term MODULO factor
               | term POWER factor
    '''
    p[0] = ABinOp(p[2], p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = AConstant(p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
# See https://stackoverflow.com/questions/28950925/ply-hide-output-file
parser = yacc.yacc(debug=False, write_tables=False)


if __name__ == "__main__":
    from utils.printer import print_ast
    print_ast(parser.parse('0 + (1 + 2) ** 3 * 4 / 5'))
