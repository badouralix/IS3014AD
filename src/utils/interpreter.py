#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Append parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from syntax.parser import parser


def interpreter(filename, init_state):
    with open(filename, 'r') as f:
        source_code = f.read()

    ast = parser.parse(source_code)

    result = ast.exec(init_state)
    print(result)


if __name__ == "__main__":
    interpreter(sys.argv[1], dict())
