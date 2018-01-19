#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ply.lex as lex


# List of token names. This is always required
va = (
    'VALUE',
    'VARIABLE',
)
ops = (
    'POWER',
)
tokens = va + ops
literals = [ '+', '-', '*', '/', '(', ')' ]

# Regular expression rules for simple tokens
t_VARIABLE  = r'\w+'
t_POWER     = r'\*\*'

# A regular expression rule with some action code
def t_VALUE(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_lparen(t):
    r'\('
    t.type = '('
    return t

def t_rparen(t):
    r'\)'
    t.type = ')'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '{char}'".format(char=t.value[0]))
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


if __name__ == "__main__":
    # Test it out
    source_code = '0 + (1 + 2) ** 3 * 4 / 4'
    lexer.input(source_code)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
