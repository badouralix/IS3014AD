#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ply.yacc as yacc

# Append parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# Get the token map from the lexer.  This is required.
from syntax.lexer import tokens
from syntax.aexp import *
from syntax.bexp import *


start = 'bexp'

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
# See https://stackoverflow.com/questions/28950925/ply-hide-output-file
parser = yacc.yacc(debug=False, write_tables=False)


if __name__ == "__main__":
    from utils.printer import print_ast
    # print_ast(parser.parse('-x0 * yx0 + -(1 +- 2) ** -3 * 4 / 5'))
    # print_ast(parser.parse('(true ^ false) ^ !true && (false || true)'))
    print(parser.parse('X > 0').eval({'X': 1}))
