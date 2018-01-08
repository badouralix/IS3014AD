#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from anytree import RenderTree
from pprint import pprint


def print_ast(ast):
    print(RenderTree(ast))


def print_cfg(cfg):
    print("Nodes: " + str(list(cfg.nodes)))
    pprint(dict(cfg.nodes.data()))
    print("\nEdges:" + str(list(cfg.edges)))
    pprint(list(cfg.edges.data()))
