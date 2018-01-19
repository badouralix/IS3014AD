#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ply.lex as lex


# List of token names. This is always required
va = (
    'BOOL',
    'VALUE',
    'VARIABLE',
)
aop = (
    'POWER',
)
bop = (
    'AND',
    'OR',
    'XOR',

    'EQ',
    'NE',
    'LT',
    'LE',
    'GT',
    'GE',
)
tokens = va + aop + bop
literals = [ '+', '-', '*', '/', '!', '(', ')' ]

# Regular expression rules for simple tokens
t_VARIABLE  = r'\w+'

t_POWER = r'\*\*'

t_AND   = r'&&'
t_OR    = r'\|\|'
t_XOR   = r'\^'

t_EQ    = r'=='
t_NE    = r'!='
t_LT    = r'<'
t_LE    = r'<='
t_GT    = r'>'
t_GE    = r'>='

t_ignore_COMMENT = r'//.*'

# A regular expression rule with some action code
def t_lparen(t):
    r'\('
    t.type = '('
    return t

def t_rparen(t):
    r'\)'
    t.type = ')'
    return t

def t_BOOL(t):
    r'(true|false)'
    t.value = True if t.value == "true" else False
    return t

def t_VALUE(t):
    r'\d+'
    t.value = int(t.value)
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
    source_code = """0 + (1 + 2) ** 3 * 4 / 4
    // comment
    true && false"""
    lexer.input(source_code)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
