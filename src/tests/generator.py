#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astree.aexp import *
from astree.bexp import *
from astree.com import *
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
        symbols[var].append( Int("_" + var + "_" + str(len(symbols[var]))) )

    # Generate constraints
    for i in range(len(path) - 1):
        edge = cfg.edges[path[i], path[i+1]]
        if edge["bexp"] == BConstant(True):
            add_stmt(s, symbols, edge["com"])
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


def add_aexp(s, symbols, aexp):
    pass


def add_bexp(s, symbols, bexp):
    pass


def add_stmt(s, symbols, stmt):
    pass

