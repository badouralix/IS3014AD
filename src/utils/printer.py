#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from anytree import RenderTree
from networkx import nx
import os
import pygraphviz


def print_ast(ast):
    print(RenderTree(ast))


def print_cfg(cfg):
    print(nx.drawing.nx_pydot.to_pydot(cfg))

def write_cfg(cfg, filename, layout="dot"):
    path = "output/" + os.path.splitext(filename)[0] + f".{layout}.png"
    graph = nx.drawing.nx_agraph.to_agraph(cfg)
    graph.layout(layout)
    graph.draw(path)
