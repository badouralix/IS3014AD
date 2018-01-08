#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter


def run_test(cfg, init_state):
    """[summary]

    Arguments:
        cfg        -- control flow graph of the input program
        init_state -- a test

    Returns:
        path  -- path of the execution
        state -- state after execution
    """

    state = init_state.copy()   # TODO: use another data struct than a dict
    current_node = "START"
    path = ["START"]

    while current_node != "END":
        for succ_node in cfg.successors(current_node):
            edge = cfg.edges[current_node, succ_node]
            if edge['bexp'].eval(state):
                edge['com'].exec(state)
                current_node = succ_node
                break

        path.append(current_node)

    return path, state


def reachable_nodes(path):
    """[summary]

    Arguments:
        path -- [description]

    Returns:
        [type] -- [description]
    """

    return Counter(path)
