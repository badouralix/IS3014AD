#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Add parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queue import Queue
from astree.bexp import BConstant
from astree.com import CAssign


def get_assignments(cfg):
    """
    Returns the set of all the labels of assignment instructions.

    Arguments:
        cfg -- control flow graph of the input program

    Returns:
        result -- set of labels
    """

    result = set()

    for src, dest in cfg.edges:
        edge = cfg.edges[src, dest]
        if isinstance(edge['com'], CAssign):
            result.add(src)

    return result


def get_decisions(cfg):
    """
    Returns the set of labels whose instructions are in a conditional branch
    (if statement or while statement).

    TODO: currently, only the node following the branching is added to the
          result set. Adding all the nodes in the branch may be "sounder".

    Arguments:
        cfg -- control flow graph of the input program

    Returns:
        result -- set of labels
    """

    result = set()

    for src, dest in cfg.edges:
        edge = cfg.edges[src, dest]
        if not isinstance(edge['bexp'], BConstant):
            result.add(dest)

    return result

# def get_k(cfg):
#     reached_nodes = Queue()
#     reached_nodes.put("START")

#     result = set()

#     while not reached_nodes.empty():
#         node = reached_nodes.get(block=False)

