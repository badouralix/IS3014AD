#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import networkx as nx

# Add parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from astree.aexp import *
from astree.bexp import BConstant
from astree.com import CAssign, CSkip


def ast2cfg(ast):
    ast = copy.deepcopy(ast)
    cfg = nx.DiGraph()

    add_start_node(cfg)

    cfg, next_nodes = rec_ast2cfg(ast, cfg, {"START": (BConstant(True), CSkip())})

    add_end_node(cfg)
    for node, data in next_nodes.items():
        bexp, com = data
        cfg.add_edge(node, "END", bexp=bexp, com=com)

    return cfg


def add_start_node(cfg):
    cfg.add_node("START")
    return cfg


def rec_ast2cfg(ast, cfg, previous_nodes):
    next_nodes = {}

    if isinstance(ast, CAssign):
        cfg.add_node(ast.label)
        for node, data in previous_nodes.items():
            bexp, com = data
            cfg.add_edge(node, ast.label, bexp=bexp, com=com)
        next_nodes = {ast.label: (BConstant(True), CAssign(*ast.children))}

    return cfg, next_nodes


def add_end_node(cfg):
    cfg.add_node("END")
    return cfg


if __name__ == "__main__":
    from printer import print_ast, print_cfg
    ast = CAssign(AVariable('X'), AConstant(1), label=1)
    print_ast(ast)
    cfg = ast2cfg(ast)
    print_cfg(cfg)
    print_ast(ast)
