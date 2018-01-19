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
from syntax.stmt import *
from utils.printer import print_ast


start = 'stmt'

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
# See https://stackoverflow.com/questions/28950925/ply-hide-output-file
parser = yacc.yacc(debug=False, write_tables=False)


if __name__ == "__main__":
    from utils.printer import print_ast
    print_ast(parser.parse("if (x == 1) {x := 0; y:=2; z := 3;} else {x := 1;}"))
    print_ast(parser.parse("x:= 5; while (x > 0) {x := x - 1;}"))
