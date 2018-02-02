#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astree.aexp import *
from astree.bexp import *
from astree.stmt import *
from collections import defaultdict
from z3 import *


def generate_tests(cfg, paths, inputs):
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
        result = generate_test(cfg, path, inputs)
        if not result is None:
            results.append(result)

    return results


def generate_test(cfg, path, inputs):
    # Setup solver
    s = Solver()

    # Initialize symboles with known unknowns
    symbols = defaultdict(list)
    for var in inputs:
        new_symbol(var, symbols)

    # Generate constraints
    for i in range(len(path) - 1):
        edge = cfg.edges[path[i], path[i+1]]
        if edge["bexp"] == BConstant(True):
            add_stmt(s, symbols, edge["stmt"])
        else:
            add_bexp(s, symbols, edge["bexp"])

    # Solve and send results
    check = s.check()
    if check == "sat":
        result = dict()
        for var in inputs:
            result[var] = s.model()[symbols[var][0]]
        return result
    else:
        return None


def new_symbol(name, symbols):
    symbol = "_" + name + "_" + str(len(symbols[name]))
    symbols[name].append(symbol)
    return symbol


def add_aexp(s, symbols, aexp):
    if isinstance(aexp, AConstant):
        return aexp.value

    elif isinstance(aexp, AVariable):
        return symbols[aexp.name][-1]

    elif isinstance(aexp, AUnOp):
        reg = new_symbol("_reg", symbols)
        symbol = add_aexp(s, symbols, aexp.child)
        if aexp.op == '-':
            s.add(reg + symbol == 0)
        elif aexp.op == '+':
            s.add(reg == symbols)
        else:
            raise ArithmeticError("Unsupported operator {}".format(aexp.op))
        return reg

    elif isinstance(aexp, ABinOp):
        reg = new_symbol("_reg", symbols)
        left_symbol = add_aexp(s, symbols, aexp.left)
        right_symbol = add_aexp(s, symbol, aexp.right)
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


def add_bexp(s, symbols, bexp):
    pass


def add_stmt(s, symbols, stmt):
    pass

