#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter


def run_test(cfg, init_state):
    """
    Run an execution given initial values for variables.

    Arguments:
        cfg        -- control flow graph of the input program
        init_state -- a test

    Returns:
        path  -- path of the execution
        state -- state after execution
    """

    state = init_state.copy()
    current_node = "START"
    path = ["START"]

    while current_node != "END":
        for succ_node in cfg.successors(current_node):
            edge = cfg.edges[current_node, succ_node]
            if edge["bexp"].eval(state):
                edge["stmt"].exec(state, verbose=False)
                current_node = succ_node
                break

        path.append(current_node)

    return path, state


def run_test_set(cfg, valuations):
    """
    Run executions for all given tests.

    Arguments:
        cfg        -- control flow graph of the input program
        valuations -- a list of tests

    Returns:
        paths -- list of paths of executions
    """

    paths = list()

    for valuation in valuations:
        path, _ = run_test(cfg, valuation)
        paths.append(path)

    return paths
