#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from astree.aexp import *
from astree.bexp import *
from astree.stmt import *
from collections import defaultdict
from z3 import *


def generate_tests(cfg, paths):
    """
    Compute a set of tests such that the set of executions in the given cfg
    matches the given set of paths.

    Arguments:
        cfg    -- Control flow graph of the input program
        paths  -- Set of paths
        inputs -- Set of initial variable names
    """
    results = list()

    for path in paths:
        result = generate_test(cfg, path)
        if not result is None:
            results.append(result)

    return results


def generate_test(cfg, path):
    # Setup solver
    s = Solver()

    # On-the-fly generation of input varnames and symbols
    inputs = set()
    symbols = defaultdict(list)

    # Generate constraints
    for i in range(len(path) - 1):
        edge = cfg.edges[path[i], path[i+1]]
        if isinstance(edge["stmt"], SSkip):
            s.add( get_bexp_symbol(s, symbols, edge["bexp"]) )
        else:
            add_stmt(s, symbols, edge["stmt"], inputs)

    # Solve and send results
    s.check()
    try:
        result = dict()
        for var in inputs:
            result[var] = s.model()[symbols[var][0]]
        return result
    except:
        print("No test found for path {path}".format(path=path))
        return None


def new_symbol(name, symbols):
    symbol = Int("_" + name + "_" + str(len(symbols[name])))
    symbols[name].append(symbol)
    return symbol


def get_aexp_symbol(s, symbols, aexp):
    if isinstance(aexp, AConstant):
        return aexp.value

    elif isinstance(aexp, AVariable):
        return symbols[aexp.name][-1]

    elif isinstance(aexp, AUnOp):
        reg = new_symbol("_reg", symbols)
        child_symbol = get_aexp_symbol(s, symbols, aexp.child)
        if aexp.op == '-':
            s.add(reg + child_symbol == 0)
        elif aexp.op == '+':
            s.add(reg == child_symbol)
        else:
            raise ArithmeticError("Unsupported operator {}".format(aexp.op))
        return reg

    elif isinstance(aexp, ABinOp):
        reg = new_symbol("_reg", symbols)
        left_symbol = get_aexp_symbol(s, symbols, aexp.left)
        right_symbol = get_aexp_symbol(s, symbols, aexp.right)
        if aexp.op == '+':
            s.add(reg == left_symbol + right_symbol)
        elif aexp.op == '-':
            s.add(reg == left_symbol - right_symbol)
        elif aexp.op == '*':
            s.add(reg == left_symbol * right_symbol)
        elif aexp.op == '/':
            s.add(reg == left_symbol // right_symbol)
        elif aexp.op == '%':
            s.add(reg == left_symbol % right_symbol)
        elif aexp.op == '**':
            s.add(reg == left_symbol ** right_symbol)
        else:
            raise ArithmeticError("Unsupported operator {}".format(aexp.op))
        return reg

    else:
        return None


def get_bexp_symbol(s, symbols, bexp):
    if isinstance(bexp, BConstant):
        return bexp.value

    elif isinstance(bexp, BVariable):
        raise TypeError("Unsupported type BVariable")

    elif isinstance(bexp, BUnOp):
        child_symbol = get_bexp_symbol(s, symbols, bexp.child)
        if bexp.op == '!':
            return Not(child_symbol)
        else:
            raise TypeError("Unknown unary boolean operator {}".format(bexp.op))

    elif isinstance(bexp, BBinOp):
        if bexp.subtypes == "AEXP":
            left_symbol = get_aexp_symbol(s, symbols, bexp.left)
            right_symbol = get_aexp_symbol(s, symbols, bexp.right)
        elif bexp.subtypes == "BEXP":
            left_symbol = get_bexp_symbol(s, symbols, bexp.left)
            right_symbol = get_bexp_symbol(s, symbols, bexp.right)
        else:
            raise TypeError("Unknown binary boolean subtypes {}".format(bexp.subtypes))

        if bexp.op == '&&':
            return And(left_symbol, right_symbol)
        elif bexp.op == '||':
            return Or(left_symbol, right_symbol)
        elif bexp.op == '^':
            return Xor(left_symbol, right_symbol)
        elif bexp.op == '==':
            return left_symbol == right_symbol
        elif bexp.op == '!=':
            return left_symbol != right_symbol
        elif bexp.op == '<':
            return left_symbol < right_symbol
        elif bexp.op == '<=':
            return left_symbol <= right_symbol
        elif bexp.op == '>':
            return left_symbol > right_symbol
        elif bexp.op == '>=':
            return left_symbol >= right_symbol
        else:
            raise TypeError("Unknown binary boolean operator {}".format(bexp.op))


def add_stmt(s, symbols, stmt, inputs):
    if isinstance(stmt, SInput):
        varname = stmt.child.name
        inputs.add(varname)
        new_symbol(varname, symbols)

    elif isinstance(stmt, SAssign):
        # The order here is *very* important
        reg_symbol = get_aexp_symbol(s, symbols, stmt.aexp)
        var_symbol = new_symbol(stmt.var.name, symbols)

        s.add(var_symbol == reg_symbol)

    elif isinstance(stmt, SSkip) or isinstance(stmt, SPrint):
        pass

    else:
        raise TypeError("Unhandled statement {stmt}".format(stmt=stmt))


if __name__ == "__main__":
    from cfgraph.utils import gen_k_paths
    from syntax.parser import parser
    from utils.ast2cfg import ast2cfg
    from utils.printer import print_ast, print_cfg

    source_filename = "input/example.imp"
    with open(source_filename) as f:
        source_code = f.read()

    ast = parser.parse(source_code)
    print_ast(ast)

    print()

    cfg = ast2cfg(ast)
    print_cfg(cfg)

    print()

    paths = list()
    for path in gen_k_paths(cfg, 10):
        paths.append(path)
    path = paths[1]
    print(path)

    print()

    s = Solver()
    inputs = set()
    symbols = defaultdict(list)

    for i in range(len(path) - 1):
        edge = cfg.edges[path[i], path[i+1]]
        print(edge)
        if isinstance(edge["stmt"], SSkip):
            s.add( get_bexp_symbol(s, symbols, edge["bexp"]) )
        else:
            add_stmt(s, symbols, edge["stmt"], inputs)
        print(s)
        print(dict(symbols))
        print(inputs)
        print()

    check = s.check()
    print(check)
    try:
        result = dict()
        for var in inputs:
            result[var] = s.model()[symbols[var][0]]
        print(result)
    except:
        print("No test found for path {path}".format(path=path))
